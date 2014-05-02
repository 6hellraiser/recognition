import cv2
import math
from sklearn import svm
import numpy as np

color = 255
horizontal_center = 0
vertical_center = 0
box_width = 0
box_height = 0
on_pixels = 0;

def first_third(matrix):
    #return integer
    #1. The horizontal position, counting pixels from the left edge of the image, of the center
    #of the smallest rectangular box that can be drawn with all "on" pixels inside the box.
    #3. The width, in pixels, of the box.
    rows_count = matrix.shape[0]
    columns_count = matrix.shape[1]
    left_edge = -1
    right_edge = -1
    for col in columns_count:
        for row in rows_count:
            if matrix[row, col] == color:
                left_edge = col
                break
            break
    for col in reversed(range(columns_count)):
        for row in reversed(range(rows_count)):
            if matrix[row, col] == color:
                right_edge = col
                break
            break
    first_feature = (right_edge - left_edge)/2
    third_feature = right_edge - left_edge
    #it is for sixth feature
    horizontal_center = first_feature
    box_width = third_feature
    features = [first_feature, third_feature]
    return features

def second_fourth(matrix):
    #2. The vertical position, counting pixels from the bottom, of the above box.
    #4. The height, in pixels, of the box.
    rows_count = matrix.shape[0]
    columns_count = matrix.shape[1]
    bottom_edge = -1
    top_edge = -1
    for row in rows_count:
        for col in columns_count:
            if matrix[row, col] == color:
                top_edge = row
                break
            break
    for row in reversed(range(rows_count)):
        for col in reversed(range(columns_count)):
            if matrix[row, col] == color:
                bottom_edge = row
                break
            break
    second_feature = (bottom_edge - top_edge)/2
    fourth_feature = bottom_edge - top_edge
    vertical_center = second_feature
    box_height = fourth_feature
    features = [second_feature, fourth_feature]
    return features

def fifth(matrix):
    #5. The total number of "on" pixels in the character image.
    rows_count = matrix.shape[0]
    columns_count = matrix.shape[1]
    count = 0
    for row in rows_count:
        for col in columns_count:
            if matrix[row, col] == color:
                count += 1
    on_pixels = count
    return count

def sixth(matrix):
    #6. The mean horizontal position of all "on" pixels relative to the center of the box and
    #divided by the width of the box. This feature has a negative value if the image is "leftheavy"
    #as would be the case for the letter L.
    rows_count = matrix.shape[0]
    columns_count = matrix.shape[1]
    mean_horizontal = 0
    x = 0 - box_width/2
    y = 0 - box_height/2
    count = 0
    for row in rows_count:
        for col in columns_count:
            if matrix[x, y] == color:
                mean_horizontal += y ####################################################################3???
                count += 1
            y += 1
        x += 1
    sixth_feature = mean_horizontal/(count * box_width)
    return sixth_feature

def seventh(matrix):
    #7. The mean vertical position of all "on" pixels relative to the center of the box and divided
    #by the height of the box.
    rows_count = matrix.shape[0]
    columns_count = matrix.shape[1]
    mean_vertical = 0
    x = 0 - box_width/2
    y = 0 - box_height/2
    count = 0
    for row in rows_count: #################################################################################????
        for col in columns_count:
            if matrix[x, y] == color:
                mean_vertical += x
                count += 1
            y += 1
        x += 1
    seventh_feature = mean_vertical/(count * box_height)
    return seventh_feature

def eighth(matrix):
    #8. The mean squared value of the horizontal pixel distances as measured in 6 above. This
    #attribute will have a higher value for images whose pixels are more widely separated
    #in the horizontal direction as would be the case for the letters W or M.
    rows_count = matrix.shape[0]
    columns_count = matrix.shape[1]
    quadr_sum = 0
    for row in rows_count:
        for col in columns_count:
            if matrix[row, col] == color:
                quadr_sum += ((horizontal_center - col)/box_width)**2
    eighth_feature = math.sqrt(quadr_sum/on_pixels)
    return eighth_feature

def nineth(matrix):
    # 9. The mean squared value of the vertical pixel distances as measured in 7 above.
    rows_count = matrix.shape[0]
    columns_count = matrix.shape[1]
    quadr_sum = 0
    for row in rows_count:
        for col in columns_count:
            if matrix[row, col] == color:
                quadr_sum += ((vertical_center - row)/box_height)**2
    nineth_feature = math.sqrt(quadr_sum/on_pixels)
    return nineth_feature

def descriptor(matrix):
    # 16 features

    return

def main():

    thresh = 127
    vectors = []
    images = [cv2.imread('new_learn/0_1.png',0), cv2.imread('new_learn/0_2.png',0), cv2.imread('new_learn/0_3.png',0), cv2.imread('new_learn/0_4.png',0),
              cv2.imread('new_learn/0_5.png',0), cv2.imread('new_learn/0_6.png',0),cv2.imread('new_learn/0_7.png',0), cv2.imread('new_learn/0_8.png',0),
              cv2.imread('new_learn/4_1.png',0),cv2.imread('new_learn/4_2.png',0),cv2.imread('new_learn/4_3.png',0),cv2.imread('new_learn/4_4.png',0),
              cv2.imread('new_learn/4_5.png',0),cv2.imread('new_learn/4_6.png',0), cv2.imread('new_learn/4_7.png',0),cv2.imread('new_learn/4_8.png',0),
              cv2.imread('new_learn/5_1.png',0),cv2.imread('new_learn/5_2.png',0),cv2.imread('new_learn/5_3.png',0),cv2.imread('new_learn/5_4.png',0),
              cv2.imread('new_learn/5_6.png',0),cv2.imread('new_learn/5_7.png',0),cv2.imread('new_learn/5_8.png',0)]
    for el in images:
        binary_matrix = cv2.threshold(el, thresh, color, cv2.THRESH_BINARY)[1]
       # cv2.imshow('digit', im_bw)
        #cv2.waitKey(0)
        linear_vector = descriptor(binary_matrix)
        vectors.append(linear_vector)

if __name__ == '__main__':
    main()