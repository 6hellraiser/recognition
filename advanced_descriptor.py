import cv2
import math
from sklearn import svm
import matplotlib.pyplot as plt
import numpy as np

class Descriptor:

    color = 255
    black = 0
    horizontal_center = 0
    vertical_center = 0
    box_width = -1
    box_height = -1
    on_pixels = 1

    def __init__(self):
        return

    def roundd(self, number):
        return '%.1f' % round(number, 1)

    def first_third(self, matrix):
        #1. The horizontal position, counting pixels from the left edge of the image, of the center
        #of the smallest rectangular box that can be drawn with all "on" pixels inside the box.
        #3. The width, in pixels, of the box.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        left_edge = -1
        right_edge = -1
        ok = 0
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.black:
                    left_edge = col
                    ok = 1
                if ok == 1:
                    break
            if ok == 1:
                break
        ok = 0

        for col in reversed(range(columns_count)):
            for row in reversed(range(rows_count)):
                if matrix[row, col] == Descriptor.black:
                    right_edge = col
                    ok = 1
                if ok == 1:
                    break
            if ok == 1:
                break
        first_feature = ((right_edge + 1) - left_edge)/2
        third_feature = (right_edge + 1) - left_edge
        #it is for sixth feature
        Descriptor.horizontal_center = first_feature
        Descriptor.box_width = third_feature
        features = [first_feature, third_feature]
        return features

    def second_fourth(self, matrix):
        #2. The vertical position, counting pixels from the bottom, of the above box.
        #4. The height, in pixels, of the box.
        print matrix
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        bottom_edge = -1
        top_edge = -1
        ok = 0
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.color:
                    top_edge = row
                    ok = 1
                if ok == 1:
                    break
            if ok == 1:
                break
        ok = 0
        for col in reversed(range(columns_count)):
            for row in reversed(range(rows_count)):
                if matrix[row, col] == Descriptor.color:
                    bottom_edge = row
                    ok = 1
                if ok == 1:
                    break
            if ok == 1:
                break
        second_feature = (bottom_edge - top_edge)/2
        fourth_feature = bottom_edge - top_edge
        Descriptor.vertical_center = second_feature
        Descriptor.box_height = fourth_feature
        features = [second_feature, fourth_feature]
        return features

    def fifth(self, matrix):
        #5. The total number of "on" pixels in the character image.
      #  print matrix
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        count = 0
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.black:
                    count += 1
        Descriptor.on_pixels = count
        return self.roundd(float(count)/(Descriptor.box_width*Descriptor.box_height))

    def sixth(self, matrix):
        #6. The mean horizontal position of all "on" pixels relative to the center of the box and
        #divided by the width of the box. This feature has a negative value if the image is "leftheavy"
        #as would be the case for the letter L.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        mean_horizontal = 0
        x = 0 - Descriptor.box_width/2
        y = 0 - Descriptor.box_height/2
      #  count = 0
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.color:
                    mean_horizontal += x
                    #count += 1
                x += 1
            y += 1
        sixth_feature = mean_horizontal/(Descriptor.on_pixels * Descriptor.box_width)
        return self.roundd(sixth_feature)

    def seventh(self, matrix):
        #7. The mean vertical position of all "on" pixels relative to the center of the box and divided
        #by the height of the box.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        mean_vertical = 0
        x = 0 - Descriptor.box_width/2
        y = 0 - Descriptor.box_height/2
        #count = 0
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.color:
                    mean_vertical += y
                   # count += 1
                x += 1
            y += 1
        seventh_feature = mean_vertical/(Descriptor.on_pixels * Descriptor.box_height)
        return self.roundd(seventh_feature)

    def eighth(self, matrix):
        #8. The mean squared value of the horizontal pixel distances as measured in 6 above. This
        #attribute will have a higher value for images whose pixels are more widely separated
        #in the horizontal direction as would be the case for the letters W or M.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        quadr_sum = 0
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.color:
                    quadr_sum += ((Descriptor.horizontal_center - col)/Descriptor.box_width)**2
        eighth_feature = math.sqrt(quadr_sum/Descriptor.on_pixels)
        return self.roundd(eighth_feature)

    def nineth(self, matrix):
        # 9. The mean squared value of the vertical pixel distances as measured in 7 above.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        quadr_sum = 0
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.color:
                    quadr_sum += ((Descriptor.vertical_center - row)/Descriptor.box_height)**2
        nineth_feature = math.sqrt(quadr_sum/Descriptor.on_pixels)
        return self.roundd(nineth_feature)

    def tenth(self, matrix):
        #10. The mean product of the horizontal and vertical distances for each "on" pixel as measured
        #in 6 and 7 above. This attribute has a positive value for diagonal lines that run
        #from bottom left to top right and a negative value for diagonal lines from top left to
        #bottom right.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        sum = 0
        x = 0 - Descriptor.box_width/2
        y = 0 - Descriptor.box_height/2
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.color:
                    sum += x*y
                x += 1
            y += 1
        return self.roundd(sum/(Descriptor.on_pixels*Descriptor.box_width*Descriptor.box_height))

    def eleventh_twelfth(self, matrix):
        #11. The mean value of the squared horizontal distance times the vertical distance for each
        #"on" pixel. This measures the correlation of the horizontal variance with the vertical
        #position.
        #12. The mean value of the squared vertical distance times the horizontal distance for each
        #"on" pixel. This measures the correlation of the vertical variance with the horizontal
        #position.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        sum_gor = 0
        sum_vert = 0
        x = 0 - Descriptor.box_width/2
        y = 0 - Descriptor.box_height/2
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.color:
                    sum_gor += ((x/Descriptor.box_width)**2)*y
                    sum_vert += ((y/Descriptor.box_height)**2)*x
                x += 1
            y += 1
        eleventh_feature = self.roundd(sum_gor/(Descriptor.on_pixels*Descriptor.box_height))
        twelfth_feature = self.roundd(sum_vert/(Descriptor.on_pixels*Descriptor.box_width))
        features = [eleventh_feature, twelfth_feature]
        return features

    def thirteen_fourteen(self, matrix):
        #13. The mean number of edges (an "on" pixel immediately to the right of either an "off"
        #pixel or the image boundary) encountered when making systematic scans from left
        #to right at all vertical positions within the box. This measure distinguishes between
        #letters like "W" or "M" and letters like "I" or "L." #divide by height

        #14. The sum of the vertical positions of edges encountered as measured in 13 above. This
        #feature will give a higher value if there are more edges at the top of the box, as in
        #the letter "Y." #divide by height
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        count_edges = 0
        y = 0
        vert_sum = 0
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.color:
                    if (col-1) < 0 or matrix[row, col - 1] != Descriptor.color:
                        count_edges += 1
                        vert_sum += y
            y += 1
        thirteen_feature = self.roundd(count_edges/(Descriptor.box_height*Descriptor.box_width))
        fourteen_feature = self.roundd(vert_sum/Descriptor.box_height) #??????????????????????
        features = [thirteen_feature, fourteen_feature]
        return features

    def fifteen_sixteen(self, matrix):
        #15. The mean number of edges (an "on" pixel immediately above either an "off" pixel
        #or the image boundary) encountered when making systematic scans of the image from
        #bottom to top over all horizontal positions within the box.
        #16. The sum of horizontal positions of edges encountered as measured in 15 above.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        count_edges = 0
        x = 0
        hor_sum = 0
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.color:
                    if (row + 1) == rows_count or matrix[row + 1, col] != Descriptor.color:
                        count_edges += 1
                        hor_sum += x
                x += 1
        fifteen_feature = self.roundd(count_edges/(Descriptor.box_width*Descriptor.box_height))
        sixteen_feature = self.roundd(hor_sum/Descriptor.box_width) #???????????????????????
        features = [fifteen_feature, sixteen_feature]
        return features

    def descriptor(self, matrix):
        # 16 features
        vector = []
        first = self.first_third(matrix)
        for el in first:
            vector.append(el)
        second = self.second_fourth(matrix)
        for el in second:
            vector.append(el)
        vector.append(self.fifth(matrix))
        vector.append(self.sixth(matrix))
        vector.append(self.seventh(matrix))
        vector.append(self.eighth(matrix))
        vector.append(self.nineth(matrix))
        vector.append(self.tenth(matrix))
        eleventh = self.eleventh_twelfth(matrix)
        for el in eleventh:
            vector.append(el)
        thirteen = self.thirteen_fourteen(matrix)
        for el in thirteen:
            vector.append(el)
        fifteen = self.fifteen_sixteen(matrix)
        for el in fifteen:
            vector.append(el)
        return vector

def predict(path, clf, input):
    test_image = cv2.imread(path,0)

    bin_matrix = cv2.threshold(test_image, 127, Descriptor.color, cv2.THRESH_BINARY)[1]
    #cv2.imshow('digit', im_bw)
    #cv2.waitKey(0)
    #print type(im_bw)
   # print im_bw.shape
    d = Descriptor()
    descr = d.descriptor(bin_matrix)
    label = clf.predict(descr)
    print label
   # plot_vector(descr, label, input)
    return



def main():

    thresh = 127
    vectors = []
    """
    images = [cv2.imread('new_learn/0_1.png',0), cv2.imread('new_learn/0_2.png',0), cv2.imread('new_learn/0_3.png',0), cv2.imread('new_learn/0_4.png',0),
              cv2.imread('new_learn/0_5.png',0), cv2.imread('new_learn/0_6.png',0),cv2.imread('new_learn/0_7.png',0), cv2.imread('new_learn/0_8.png',0),
              cv2.imread('new_learn/4_1.png',0),cv2.imread('new_learn/4_2.png',0),cv2.imread('new_learn/4_3.png',0),cv2.imread('new_learn/4_4.png',0),
              cv2.imread('new_learn/4_5.png',0),cv2.imread('new_learn/4_6.png',0), cv2.imread('new_learn/4_7.png',0),cv2.imread('new_learn/4_8.png',0),
              cv2.imread('new_learn/5_1.png',0),cv2.imread('new_learn/5_2.png',0),cv2.imread('new_learn/5_3.png',0),cv2.imread('new_learn/5_4.png',0),
              cv2.imread('new_learn/5_6.png',0),cv2.imread('new_learn/5_7.png',0),cv2.imread('new_learn/5_8.png',0)]
    """
    images = [cv2.imread('new_learn/0_1.png',0)]
    for el in images:
        binary_matrix = cv2.threshold(el, thresh, Descriptor.color, cv2.THRESH_BINARY)[1]
        #cv2.imshow('digit', binary_matrix)
        #cv2.waitKey(0)
       # linear_vector = descriptor(binary_matrix)
        d = Descriptor()
        linear_vector = d.descriptor(cv2.threshold(cv2.resize(binary_matrix,(8,10)),thresh,Descriptor.color,cv2.THRESH_BINARY)[1]) #test! comment this and uncommend previous string!!
        vectors.append(linear_vector)

   # y = [0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5]
   # y = [0]
   # clf = svm.SVC()
   # clf.fit(vectors, y)

    """
    print 'expect 0, get: '
    predict('new_ask/0_t1.png',clf,'0')
    print 'expect 0, get: '
    predict('new_ask/0_t2.png',clf,'0')
    print 'expect 0, get: '
    predict('new_ask/0_t3.png',clf,'0')
    print 'expect 4, get: '
    predict('new_ask/4_t1.png',clf,'4')
    print 'expect 4, get: '
    predict('new_ask/4_t2.png',clf,'4')
    print 'expect 4, get: '
    predict('new_ask/4_t3.png',clf,'4')
    print 'expect 5, get: '
    predict('new_ask/5_t1.png',clf,'5')
    print 'expect 5, get: '
    predict('new_ask/5_t2.png',clf,'5')
    print 'expect 5, get: '
    predict('new_ask/5_t3.png',clf,'5')

    print
    print 'output with noise-----------'
    print

    print 'expect 0, get: '
    predict('error_ask/0_t1.png',clf,'0')
    print 'expect 0, get: '
    predict('error_ask/0_t2.png',clf,'0')
    print 'expect 0, get: '
    predict('error_ask/0_t3.png',clf,'0')
    print 'expect 4, get: '
    predict('error_ask/4_t1.png',clf,'4')
    print 'expect 4, get: '
    predict('error_ask/4_t2.png',clf,'4')
    print 'expect 4, get: '
    predict('error_ask/4_t3.png',clf,'4')
    print 'expect 5, get: '
    predict('error_ask/5_t1.png',clf,'5')
    """

if __name__ == '__main__':
    main()