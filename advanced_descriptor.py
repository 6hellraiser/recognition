import cv2
import math
from sklearn import svm
import numpy as np

color = 255
horizontal_center = 0
vertical_center = 0
box_width = 0
box_height = 0
on_pixels = 0

def roundd(number):
    return '%.1f' % round(number, 1)

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
    return roundd(count/(box_width*box_height))

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
            if matrix[row, col] == color:
                mean_horizontal += x
                count += 1
            x += 1
        y += 1
    sixth_feature = mean_horizontal/(count * box_width)
    return roundd(sixth_feature)

def seventh(matrix):
    #7. The mean vertical position of all "on" pixels relative to the center of the box and divided
    #by the height of the box.
    rows_count = matrix.shape[0]
    columns_count = matrix.shape[1]
    mean_vertical = 0
    x = 0 - box_width/2
    y = 0 - box_height/2
    count = 0
    for row in rows_count:
        for col in columns_count:
            if matrix[row, col] == color:
                mean_vertical += y
                count += 1
            x += 1
        y += 1
    seventh_feature = mean_vertical/(count * box_height)
    return roundd(seventh_feature)

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
    return roundd(eighth_feature)

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
    return roundd(nineth_feature)

def tenth(matrix):
    #10. The mean product of the horizontal and vertical distances for each "on" pixel as measured
    #in 6 and 7 above. This attribute has a positive value for diagonal lines that run
    #from bottom left to top right and a negative value for diagonal lines from top left to
    #bottom right.
    rows_count = matrix.shape[0]
    columns_count = matrix.shape[1]
    sum = 0
    x = 0 - box_width/2
    y = 0 - box_height/2
    for row in rows_count:
        for col in columns_count:
            if matrix[row, col] == color:
                sum += x*y
            x += 1
        y += 1
    return roundd(sum/(on_pixels*box_width*box_height))

def eleventh_twelfth(matrix):
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
    x = 0 - box_width/2
    y = 0 - box_height/2
    for row in rows_count:
        for col in columns_count:
            if matrix[row, col] == color:
                sum_gor += ((x/box_width)**2)*y
                sum_vert += ((y/box_height)**2)*x
            x += 1
        y += 1
    eleventh_feature = roundd(sum_gor/(on_pixels*box_height))
    twelfth_feature = roundd(sum_vert/(on_pixels*box_width))
    features = [eleventh_feature, twelfth_feature]
    return features

def thirteen_fourteen(matrix):
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
    for row in rows_count:
        for col in columns_count:
            if matrix[row, col] == color:
                if (col-1) < 0 or matrix[row, col - 1] != color:
                    count_edges += 1
                    vert_sum += y
        y += 1
    thirteen_feature = roundd(count_edges/(box_height*box_width))
    fourteen_feature = roundd(vert_sum/box_height) #??????????????????????
    features = [thirteen_feature, fourteen_feature]
    return features

def fifteen_sixteen(matrix):
    #15. The mean number of edges (an "on" pixel immediately above either an "off" pixel
    #or the image boundary) encountered when making systematic scans of the image from
    #bottom to top over all horizontal positions within the box.
    #16. The sum of horizontal positions of edges encountered as measured in 15 above.
    rows_count = matrix.shape[0]
    columns_count = matrix.shape[1]
    count_edges = 0
    x = 0
    hor_sum = 0
    for row in rows_count:
        for col in columns_count:
            if matrix[row, col] == color:
                if (row + 1) == rows_count or matrix[row + 1, col] != color:
                    count_edges += 1
                    hor_sum += x
            x += 1
    fifteen_feature = roundd(count_edges/(box_width*box_height))
    sixteen_feature = roundd(hor_sum/box_width) #???????????????????????
    features = [fifteen_feature, sixteen_feature]
    return features

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