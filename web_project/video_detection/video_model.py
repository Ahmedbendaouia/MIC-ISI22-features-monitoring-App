import base64
import cv2 as cv
import numpy as np
import time
import math


#this class handles the video streaming using openCv and a video feed path as un argument for it's constractor
class video_feed(object):

    def __init__(self, pathVideo):
        start = time.process_time()
        # Parameters for Shi-Tomasi corner detection
        self.feature_params = dict(maxCorners=0,
                                   qualityLevel=0.2,
                                   minDistance=10,
                                   blockSize=7)
        # Parameters for Lucas-Kanade optical flow
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv.TERM_CRITERIA_EPS
                                        | cv.TERM_CRITERIA_COUNT, 10, 0.03))
        # The video feed is read in as a VideoCapture object
        self.cap = cv.VideoCapture(pathVideo)
        if not self.cap.isOpened():
            print("Cannot open the file !")
        # Variable for color to draw optical flow track
        self.color = (0, 255, 0)
        # pixel to mm
        self.pixels_to_mm = 1
        # get the FPS of the video
        self.fps = int(self.cap.get(cv.CAP_PROP_FPS))
        # set the step for taking frames based on the FPS
        ### step = int((1/fps) * 1000) # msec in this case the programme will be slower
        self.step = 150  # this is the best value
        # set the counter of frames
        self.count = 0
        # ret = a boolean return value from getting the frame, first_frame = the first frame in the entire video sequence
        ret, self.first_frame = self.cap.read()
        # crop the frame
        self.first_frame = self.crop_image(self.first_frame, 200, 300)
        # Converts frame to grayscale because we only need the luminance channel for detecting edges - less computationally expensive
        self.prev_gray = cv.cvtColor(self.first_frame, cv.COLOR_BGR2GRAY)
        # Otsu's thresholding
        ret2, self.prev_gray = cv.threshold(self.prev_gray, 0, 255,
                                            cv.THRESH_BINARY + cv.THRESH_OTSU)
        # Finds the strongest corners in the first frame by Shi-Tomasi method - we will track the optical flow for these corners
        # https://docs.opencv.org/3.0-beta/modules/imgproc/doc/feature_detection.html#goodfeaturestotrack
        self.prev = cv.goodFeaturesToTrack(self.prev_gray,
                                           mask=None,
                                           **self.feature_params)
        # Creates an image filled with zero intensities with the same dimensions as the frame - for later drawing purposes
        self.mask = np.zeros_like(self.first_frame)

    def __del__(self):
        self.cap.release()

    def get_frames(self):
        # set the counter of frames
        self.count = self.count + 1
        # set the position to take the frame
        self.cap.set(cv.CAP_PROP_POS_MSEC, (self.count * self.step))
        # ret = a boolean return value from getting the frame, frame = the current frame being projected in the video
        ret, self.frame = self.cap.read()
        # crop the frame
        self.frame = self.crop_image(self.frame, 200, 300)
        # Converts each frame to grayscale - we previously only converted the first frame to grayscale
        self.gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        # Otsu's thresholding
        ret2, self.gray = cv.threshold(self.gray, 0, 255,
                                       cv.THRESH_BINARY + cv.THRESH_OTSU)
        # Calculates sparse optical flow by Lucas-Kanade method
        # https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowpyrlk

        self.prev = cv.goodFeaturesToTrack(self.prev_gray,
                                           mask=None,
                                           **self.feature_params)
        next, status, error = cv.calcOpticalFlowPyrLK(self.prev_gray,
                                                      self.gray, self.prev,
                                                      None, **self.lk_params)

        #self.prev = cv.goodFeaturesToTrack(self.prev_gray, mask = None, **self.feature_params)
        #next, status, error = cv.calcOpticalFlowPyrLK(self.prev_gray, self.gray, self.prev, None, **self.lk_params)
        # Selects good feature points for previous position
        good_old = self.prev[status == 1].astype(int)
        # Selects good feature points for next position
        good_new = next[status == 1].astype(int)
        # Creates an image filled with zero intensities with the same dimensions as the frame - for later drawing purposes
        self.mask = np.zeros_like(self.first_frame)
        # Draws the optical flow tracks
        vx_list = []
        vy_list = []
        dt = self.step / 1000  # dt in second fixed for all frames
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            # Returns a contiguous flattened array as (x, y) coordinates for new point
            x_new, y_new = new.ravel()
            # Returns a contiguous flattened array as (x, y) coordinates for old point
            x_old, y_old = old.ravel()
            # calculate the speed in x and y axis
            vx = abs((x_new - x_old) * self.pixels_to_mm / dt)
            vy = abs((y_new - y_old) * self.pixels_to_mm / dt)
            vx_list.append(vx)
            vy_list.append(vy)
            # Draws line between new and old position with green color and 2 thickness
            self.mask = cv.line(self.mask, (x_new, y_new), (x_old, y_old),
                                self.color, 2)
            # Draws filled circle (thickness of -1) at new position with green color and radius of 3
            self.frame = cv.circle(self.frame, (x_new, y_new), 3, (0, 0, 255),
                                   -1)
        # calculate the average speed in x and y axis
        average_vx = sum(vx_list) / len(vx_list)
        average_vy = sum(vy_list) / len(vy_list)
        avrage_v = math.sqrt(pow(average_vx, 2) + pow(average_vy, 2))
        # Overlays the optical flow tracks on the original frame
        self.output = cv.add(self.frame, self.mask)
        # Updates previous frame
        prev_gray = self.gray.copy()
        # resize the image
        ####scale_percent = 50 # percent of original size
        ####width = int(output.shape[1] * scale_percent / 100)
        ####height = int(output.shape[0] * scale_percent / 100)
        ####dim = (width, height)
        ####output = cv.resize(output, dim, interpolation = cv.INTER_AREA)
        ####frame = cv.resize(frame, dim, interpolation = cv.INTER_AREA)
        ####gray = cv.resize(gray, dim, interpolation = cv.INTER_AREA)
        # image to display speed measures
        speed = np.zeros((250, 600), dtype=np.uint8)
        # whritw the speed result in the video
        text_vx = "vx = " + str(average_vx)
        text_vy = "vy = " + str(average_vy)
        text_v = "v = " + str(
            math.sqrt(pow(average_vx, 2) + pow(average_vy, 2)))
        font = cv.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        cv.putText(speed, text_vx, (50, 50), font, fontScale, (255, 0, 0), 3)
        cv.putText(speed, text_vx, (50, 50), font, fontScale, (255, 0, 0), 3)
        cv.putText(speed, text_vy, (50, 100), font, fontScale, (255, 0, 0), 3)
        cv.putText(speed, text_vy, (50, 100), font, fontScale, (255, 0, 0), 3)
        cv.putText(speed, text_v, (50, 150), font, fontScale, (255, 0, 0), 3)

        _, frame = cv.imencode('.jpg', self.frame)
        _, gray = cv.imencode('.jpg', self.gray)
        _, output = cv.imencode('.jpg', self.output)

        #encode the binary data of the image as a Base64 string
        #this you can send it inside JSON object in a channel
        flotation_froth = base64.b64encode(frame.tobytes()).decode()
        Otsu_thresholding = base64.b64encode(gray.tobytes()).decode()
        Sparse_optical_flow = base64.b64encode(output.tobytes()).decode()

        #in this dic we gather all of the elements of our video streameing from the 3 frames to the speeds
        streaming_dic = {
            "vx": average_vx,
            "vy": average_vy,
            "v": avrage_v,
            "flotation_vid": flotation_froth,
            "otsu_vid": Otsu_thresholding,
            "sparse_vid": Sparse_optical_flow
        }

        return streaming_dic

    def crop_image(self, Image, offsetHauteur, offsetLargeur):
        hauteur = Image.shape[0]
        largeur = Image.shape[1]
        croped_image = Image[(hauteur // 2 - offsetHauteur):(hauteur // 2 +
                                                             offsetHauteur),
                             (largeur // 2 - offsetLargeur):(largeur // 2 +
                                                             offsetLargeur)]
        return croped_image


#method to return speed and frames as a list of avarage_vx ,vy , v , spare frame ,otsu frame and floation frame
def gen_speed(video_feed):
    while True:
        streaming_dic = video_feed.get_frames()
        yield streaming_dic
