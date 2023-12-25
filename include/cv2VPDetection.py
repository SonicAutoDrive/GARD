import cv2
import math
import numpy as np

class cv2VPDetection():
    '''
    OpenCV版本的灭点检测
    - REJECT_DEGREE_TH: Threshold by which lines will be rejected wrt the horizontal
    '''
    def __init__(self, REJECT_DEGREE_TH = 4.0):
        self.REJECT_DEGREE_TH = REJECT_DEGREE_TH

    def FilterLines(self, Lines):
        '''
        将检测出的直线，从xyxy形式，计算斜率m和偏置c和线段长度l，返回[x,y,x,y,m,c,l]

        v = mu + c
        '''
        FinalLines = []

        for Line in Lines:
            [[x1, y1, x2, y2]] = Line
            ##img = np.zeros((512,512,3), np.uint8)
            
            # Calculating equation of the line: y = mx + c
            if x1 != x2:
                m = (y2 - y1) / (x2 - x1)
                ##cv2.line(img, (x1,y1),(x2,y2),(0,0,255),5)
                #print('1点', x1,y1)
                #print('2点' ,x2,y2)
                
            else:
                m = 100000000
            c = y2 - m*x2
            # theta will contain values between -90 -> +90. 
            theta = math.degrees(math.atan(m))

            # Rejecting lines of slope near to 0 degree or 90 degree and storing others
            if self.REJECT_DEGREE_TH <= abs(theta) <= (90 - self.REJECT_DEGREE_TH):
                l = math.sqrt( (y2 - y1)**2 + (x2 - x1)**2 )    # length of the line
                FinalLines.append([x1, y1, x2, y2, m, c, l])


        # Removing extra lines 
        # (we might get many lines, so we are going to take only longest 15 lines 
        # for further computation because more than this number of lines will only 
        # contribute towards slowing down of our algo.)
        #cv2.imshow('image', img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        if len(FinalLines) > 15:
            FinalLines = sorted(FinalLines, key=lambda x: x[-1], reverse=True)
            FinalLines = FinalLines[:15]

        return FinalLines



    def GetLines(self, Image):
        # Converting to grayscale
        GrayImage = cv2.cvtColor(Image, cv2.COLOR_RGB2GRAY)
        # Blurring image to reduce noise.
        BlurGrayImage = cv2.GaussianBlur(GrayImage, (5, 5), 1)
        # Generating Edge image
        EdgeImage = cv2.Canny(BlurGrayImage, 40, 255)

        # Finding Lines in the image
        Lines = cv2.HoughLinesP(EdgeImage, 1, np.pi / 180, 30, 10, 15)

        # Check if lines found and exit if not.
        if Lines is None:
            print("Not enough lines found in the image for Vanishing Point detection.")
            return []

        # Filtering Lines wrt angle
        FilteredLines = self.FilterLines(Lines)

        return FilteredLines



    def GetVanishingPoint(self, Lines):
        # We will apply RANSAC inspired algorithm for this. We will take combination 
        # of 2 lines one by one, find their intersection point, and calculate the 
        # total error(loss) of that point. Error of the point means root of sum of 
        # squares of distance of that point from each line.
        VanishingPoint = None
        MinError = 100000000000

        for i in range(len(Lines)):
            for j in range(i+1, len(Lines)):
                m1, c1 = Lines[i][4], Lines[i][5]
                m2, c2 = Lines[j][4], Lines[j][5]

                if m1 != m2:
                    x0 = (c1 - c2) / (m2 - m1)
                    y0 = m1 * x0 + c1

                    err = 0
                    for k in range(len(Lines)):
                        m, c = Lines[k][4], Lines[k][5]
                        m_ = (-1 / m)
                        c_ = y0 - m_ * x0

                        x_ = (c - c_) / (m_ - m)
                        y_ = m_ * x_ + c_

                        l = math.sqrt((y_ - y0)**2 + (x_ - x0)**2)

                        err += l**2

                    err = math.sqrt(err)

                    if MinError > err:
                        MinError = err
                        VanishingPoint = [x0, y0]

        return VanishingPoint, MinError
