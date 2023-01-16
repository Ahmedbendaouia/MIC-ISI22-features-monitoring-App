import numpy as np
import cv2
import skimage.morphology as skm
from skimage import measure, color


def image_segmentation(path_img, size_img, display_results=True):
    #================================================================
    # Read the image and convert it to gray scale

    img = cv2.imread(path_img)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #================================================================
    # Preprocessing of the image

    # sharpen operation
    kernel_pre1 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    #kernel_pre1 = np.array([[-1, -1, -1, -1, -1],[-1, -1, -1, -1, -1],[-1, -1, 27, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]])
    #kernel_pre = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img_sharpen = cv2.filter2D(gray_img, -1, kernel_pre1)

    # gaussien blur operation
    kernel_pre2 = np.array([[1, 4, 6, 4, 1], [4, 16, 24, 16, 4],
                            [6, 24, 36, 24, 6], [4, 16, 24, 16, 4],
                            [1, 4, 6, 4, 1]]) / 256
    img_blur = cv2.filter2D(img_sharpen, -1, kernel_pre2)
    #img_smooth = cv2.medianBlur(img_sharpen,3)

    #================================================================
    # edges extraction based on the adaptive treshold

    img_AT_1 = cv2.adaptiveThreshold(img_blur, 255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 9, 3)
    closing1 = skm.area_closing(img_AT_1, area_threshold=15, connectivity=1)

    #================================================================
    # Extraction of sure forground using distance transform, treshold and opening algorithms

    # distance transform allow more controle than erosion
    dist_transform = cv2.distanceTransform(closing1, cv2.DIST_L2, 3)
    ret1, sure_fg1 = cv2.threshold(dist_transform, 0.1 * dist_transform.max(),
                                   255, cv2.THRESH_BINARY)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(sure_fg1, cv2.MORPH_OPEN, kernel, iterations=1)
    sure_fg2 = opening.astype(np.uint8)

    #================================================================
    # Creating background image (white image all value == 255)
    # we don't need to use dilation because in our case we dont have a background

    sure_bg = np.full(size_img, 255, np.uint8)
    #kernel = np.ones((3,3),np.uint8)
    #sure_bg = cv2.dilate(sure_fg2, kernel, iterations = 100)

    #================================================================
    # Finding unknown region

    unknown1 = cv2.subtract(sure_bg, sure_fg2)

    #================================================================
    # preparing markers

    # Marker labelling
    ret1, markers1 = cv2.connectedComponents(sure_fg2)
    # Add one to all labels so that sure background is not 0, but 1
    markers1 = markers1 + 1
    # Now, mark the region of unknown with zero
    markers1[unknown1 == 255] = 0

    #================================================================
    # apply watershed algorithm

    markers1 = cv2.watershed(img, markers1)
    markers1_img = markers1.astype(np.uint8)
    markers1b = color.label2rgb(markers1, bg_label=0)

    #================================================================
    # display images

    if display_results == True:
        img1 = np.copy(img)
        img1[markers1 == -1] = [0, 0, 255]
        ##cv2.imshow("img1",img1)
        #cv2.imshow("gray_img",gray_img)
        #cv2.imshow("img_sharpen",img_sharpen)
        #cv2.imshow("img_blur",img_blur)
        #cv2.imshow("img_AT_1",img_AT_1)
        ##cv2.imshow("closin1",closing1)
        #cv2.imshow("sure_fg1",sure_fg1)
        #cv2.imshow("opening",opening)
        #cv2.imshow("sure_fg2",sure_fg2)
        #cv2.imshow("sure_bg",sure_bg)
        ##cv2.imshow("markers1_img",markers1_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return markers1, gray_img, img1, opening, markers1_img


def bubble_size_measurements(markers, gray_img, list_max_group_perimeters,
                             list_max_group_areas, pixels_to_mm):
    ### this function arrange perimeters and areas into groups and returns :
    # the total number of bubbles in an image
    # a list of percentage of number of items in each group
    # a average perimeter and the average area in each group

    regions = measure.regionprops(markers, intensity_image=gray_img)
    pixels_to_mm = 1  # Determine how many pixels are in each mm
    perimeters_list = []
    areas_list = []

    for region in regions:
        perimeters_list.append(region['perimeter'] * pixels_to_mm)
        areas_list.append(region['area'] * pixels_to_mm**2)

    # Calculate the total number of bubbles
    total_number = len(regions)

    # Creat groupes of perimeters and areas
    list_groups_perimeters = []
    list_groups_areas = []
    for i in range(len(list_max_group_perimeters) + 1):
        list_groups_perimeters.append([])
        list_groups_areas.append([])

    # Arrange perimeters and areas into groups
    for (perimeter, area) in zip(perimeters_list, areas_list):
        i = 0  # the index of a groupe of perimeters in list_groups_perimeters (same with areas)
        perimeter_appended = False
        area_appended = False
        for (max_group_perimeters,
             max_group_areas) in zip(list_max_group_perimeters,
                                     list_max_group_areas):
            if perimeter <= max_group_perimeters and perimeter_appended == False:
                list_groups_perimeters[i].append(perimeter)
                perimeter_appended = True

            if area <= max_group_areas and area_appended == False:
                list_groups_areas[i].append(area)
                area_appended = True

            i = i + 1  # we pass to the next groupe of perimeters or areas

        # for the last groupe
        if perimeter > list_max_group_perimeters[
                i - 1] and perimeter_appended == False:
            list_groups_perimeters[i].append(perimeter)
            perimeter_appended = True

        if area > list_max_group_areas[i - 1] and area_appended == False:
            list_groups_areas[i].append(area)
            area_appended = True

    # Calculate the percentage and the average for each group
    list_percentages = []
    list_averages = []
    for (group_p, group_a) in zip(list_groups_perimeters, list_groups_areas):

        ####################################################################
        # Calculate the percentage of number of items in each group
        ####################################################################
        percentage = {}

        ### for the group of perimeters
        if group_p:  # if the list group_p is not empty
            p = len(group_p) / total_number
            p = p * 100
            percentage["perimeters"] = p
        else:
            percentage["perimeters"] = 0

        ### for the group of areas
        if group_a:  # if the list group_p is not empty
            p = len(group_a) / total_number
            p = p * 100
            percentage["areas"] = p
        else:
            percentage["areas"] = 0

        list_percentages.append(percentage)

        ####################################################################
        # Calculate the average perimeter and the average area in each group
        ####################################################################
        average = {}

        ### for the group perimeters
        if group_p:  # if the list group_p is not empty
            a = sum(group_p) / len(group_p)
            average["perimeter"] = a
        else:
            average["perimeter"] = -1

        ### for the group areas
        if group_a:  # if the list group_p is not empty
            a = sum(group_a) / len(group_a)
            average["area"] = a
        else:
            average["area"] = -1

        list_averages.append(average)

    return total_number, list_percentages, list_averages


def bubble_size_distribution(path_img,
                             size_img,
                             list_max_group_perimeters,
                             list_max_group_areas,
                             pixels_to_mm,
                             display_results=True):
    # segment the image
    markers, gray_img, img1, opening, markers1_img = image_segmentation(
        path_img, size_img, display_results)
    # extract bubble size measurements
    total_number, list_percentages, list_averages = bubble_size_measurements(
        markers, gray_img, list_max_group_perimeters, list_max_group_areas,
        pixels_to_mm)

    segmented_froth_img = r'static\app_resources\images\output\segmented_froth_img.png'
    Otsu_thresholding_img = r'static\app_resources\images\output\Otsu_thresholding_img.png'
    shadow_img = r'static\app_resources\images\output\shadow_img.png'

    #save the result images in the static folder
    cv2.imwrite(segmented_froth_img, img1)
    cv2.imwrite(Otsu_thresholding_img, opening)
    cv2.imwrite(shadow_img, markers1_img)

    #The reason behind saving the imgs  in the django statics folder (root_folder) is that when DEBUG = False the statics in the static folder should be also in the django statics
    #Which means any change should be on both sides and that's also a problem that should be fixed
    segmented_froth_img2 = r'Django_statics\app_resources\images\output\segmented_froth_img.png'
    Otsu_thresholding_img2 = r'Django_statics\app_resources\images\output\Otsu_thresholding_img.png'
    shadow_img2 = r'Django_statics\app_resources\images\output\shadow_img.png'

    cv2.imwrite(segmented_froth_img2, img1)
    cv2.imwrite(Otsu_thresholding_img2, opening)
    cv2.imwrite(shadow_img2, markers1_img)

    return total_number, list_percentages, list_averages


def image_processus(path_img):
    size_img = (500, 500)
    list_max_group_perimeters = [100, 300, 500]
    list_max_group_areas = [500, 1000, 2000]
    pixels_to_mm = 1

    total_number, list_percentages, list_averages = bubble_size_distribution(
        path_img,
        size_img,
        list_max_group_perimeters,
        list_max_group_areas,
        pixels_to_mm,
        display_results=True)
    # if display_results == True the function will display the images results in each step of segmentation

    return total_number, list_percentages, list_averages


def extractImages(pathIn):    
    pathOut = r'static/app_resources/images/inputs'
    count = 0
    try:
        vidcap = cv2.VideoCapture(pathIn)
        if not vidcap.isOpened():
            print("Cannot open the file !")
    except Exception as e:
        print(e)
    vid = pathIn.split("/")[-1].split(".")[0]
    #vid= pathIn.split(".")[0]
    print(vid)
    success, image = vidcap.read()
    success = True
    while success:
        # added this line
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
        success, image = vidcap.read()
        if (success != False):            
            image = crop(image, 250, 250)            
            output_images_path = pathOut + "/" + vid + "-%d.jpg" % count
            # save frame as JPEG file
            cv2.imwrite(output_images_path, image)
            print("frame " + vid + "-%d.jpg" % count, success)
        count = count + 1
        yield output_images_path


def crop(Image, offsetHauteur, offsetLargeur):
    hauteur = Image.shape[0]
    largeur = Image.shape[1]
    croped_image = Image[(hauteur // 2 - offsetHauteur):(hauteur // 2 +
                                                         offsetHauteur),
                         (largeur // 2 - offsetLargeur):(largeur // 2 +
                                                         offsetLargeur)]
    return croped_image
