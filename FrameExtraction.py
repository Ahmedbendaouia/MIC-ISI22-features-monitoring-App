def extractImages(pathIn, pathOut):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)
    print(pathIn)
    vid= pathIn.split("/")[2].split(".")[0]
    #vid= pathIn.split(".")[0]
    #print(vid)
    success,image = vidcap.read()
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*500))    # added this line
        success,image = vidcap.read()
        if(success != False):
            #print(vid+"-%d.jpg" % count)

            image = crop(image,200,200)

            #print(image)
            cv2.imwrite(pathOut + "/" + vid+"-%d.jpg" % count, image)     # save frame as JPEG file
            print("frame "+vid+"-%d.jpg" % count,success)
        count = count + 1