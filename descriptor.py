import numpy as np
import cv2
import math
import normalization

class Descriptor:

    color = 255
    black = 0
    horizontal_center = 0
    vertical_center = 0
    box_width = -1
    box_height = -1
    on_pixels = 1
    l_edge = 0
    r_edge = 0
    t_edge = 0
    b_edge = 0

    def __init__(self):
        return

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
        Descriptor.l_edge = left_edge
        Descriptor.r_edge = right_edge
        Descriptor.horizontal_center = first_feature
        Descriptor.box_width = third_feature
        features = [first_feature, third_feature]
        #print "first ",first_feature
        #print "third ",third_feature
        return features

    def second_fourth(self, matrix):
        #2. The vertical position, counting pixels from the bottom, of the above box.
        #4. The height, in pixels, of the box.
        #print matrix
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        bottom_edge = -1
        top_edge = -1
        ok = 0
        for row in range(rows_count):
            for col in range(columns_count):
                if matrix[row, col] == Descriptor.black:
                    top_edge = row
                    ok = 1
                if ok == 1:
                    break
            if ok == 1:
                break
        ok = 0
        for row in reversed(range(rows_count)):
            for col in reversed(range(columns_count)):
                if matrix[row, col] == Descriptor.black:
                    bottom_edge = row
                    ok = 1
                if ok == 1:
                    break
            if ok == 1:
                break
        second_feature = ((bottom_edge + 1) - top_edge)/2
        fourth_feature = (bottom_edge + 1) - top_edge
        Descriptor.t_edge = top_edge
        Descriptor.b_edge = bottom_edge
        Descriptor.vertical_center = second_feature
        Descriptor.box_height = fourth_feature
        features = [second_feature, fourth_feature]
       # print "second ",second_feature
       # print "fourth ",fourth_feature
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
       # return self.roundd(float(count)/(Descriptor.box_width*Descriptor.box_height))
       # print "fifth", count
        print "norm fifth", normalization.normalize(count,Descriptor.box_width*Descriptor.box_height,0)
        #return count
        return normalization.normalize(count,Descriptor.box_width*Descriptor.box_height,0)

    def sixth(self, matrix): ######################################################################333debug
        #6. The mean horizontal position of all "on" pixels relative to the center of the box and
        #divided by the width of the box. This feature has a negative value if the image is "leftheavy"
        #as would be the case for the letter L.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        hor_distances = np.zeros((rows_count, columns_count))
        mean_horizontal = 0
        x = 0 - Descriptor.box_width/2
        #y = 0 - Descriptor.box_height/2
        for col in range(Descriptor.l_edge, columns_count):
            for row in range(Descriptor.t_edge, rows_count):
                if matrix[row, col] == Descriptor.black:
                    mean_horizontal += x
                    hor_distances[row, col] = x
                #y += 1
            #y = 0 - Descriptor.box_height/2
            x += 1
       # sixth_feature = float(mean_horizontal)/(Descriptor.on_pixels * Descriptor.box_width)
       # return self.roundd(sixth_feature) #very little number!
        #print hor_distances

        #print "sixth", float(mean_horizontal)/(Descriptor.on_pixels * Descriptor.box_width)
        sixth_feature = float(mean_horizontal)/(Descriptor.on_pixels * Descriptor.box_width)
        print "norm sixth", normalization.normalize(sixth_feature, 0.5, -0.5)
        #return sixth_feature
        return normalization.normalize(sixth_feature, 0.5, -0.5)

    def seventh(self, matrix):
        #7. The mean vertical position of all "on" pixels relative to the center of the box and divided
        #by the height of the box.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        mean_vertical = 0
        x = 0 - Descriptor.box_width/2
        y = 0 - Descriptor.box_height/2
        for col in range(Descriptor.l_edge, columns_count):
            for row in range(Descriptor.t_edge, rows_count):
                if matrix[row, col] == Descriptor.black:
                    mean_vertical += y
                y += 1
            y = 0 - Descriptor.box_height/2
            x += 1
        seventh_feature = float(mean_vertical)/(Descriptor.on_pixels * Descriptor.box_height)
        #return self.roundd(seventh_feature)
        print "norm seventh", normalization.normalize(seventh_feature,0.5,-0.5)
        #return seventh_feature
        return normalization.normalize(seventh_feature,0.5,-0.5)

    def eighth(self, matrix):
        #8. The mean squared value of the horizontal pixel distances as measured in 6 above. This
        #attribute will have a higher value for images whose pixels are more widely separated
        #in the horizontal direction as would be the case for the letters W or M.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        quadr_sum = 0
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.black:
                    quadr_sum += (float(Descriptor.horizontal_center - col)/Descriptor.box_width)**2
        eighth_feature = math.sqrt(float(quadr_sum)/Descriptor.on_pixels)
        #return self.roundd(eighth_feature)
        print "norm eighth", normalization.normalize(eighth_feature,0.5,0)
        #return eighth_feature
        return normalization.normalize(eighth_feature,0.5,0)

    def nineth(self, matrix):
        # 9. The mean squared value of the vertical pixel distances as measured in 7 above.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        quadr_sum = 0
        for col in range(columns_count):
            for row in range(rows_count):
                if matrix[row, col] == Descriptor.black:
                    quadr_sum += (float(Descriptor.vertical_center - row)/Descriptor.box_height)**2
        nineth_feature = math.sqrt(float(quadr_sum)/Descriptor.on_pixels)
        #return self.roundd(nineth_feature)
        print 'norm nineth', normalization.normalize(nineth_feature,0.5,0)
        #return nineth_feature
        return normalization.normalize(nineth_feature,0.5,0)

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
        for col in range(Descriptor.l_edge, columns_count):
            for row in range(Descriptor.t_edge, rows_count):
                if matrix[row, col] == Descriptor.black:
                    sum += x*y
                y += 1
            y = 0 - Descriptor.box_height/2
            x += 1
        #return self.roundd(float(sum)/Descriptor.on_pixels)
        tenth_feature = float(sum)/Descriptor.on_pixels/Descriptor.box_width/Descriptor.box_height
        print 'norm tenth', normalization.normalize(tenth_feature,0.25,-0.25)
        #return tenth_feature
        return normalization.normalize(tenth_feature,0.25,-0.25)

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
        for col in range(Descriptor.l_edge, columns_count):
            for row in range(Descriptor.t_edge, rows_count):
                if matrix[row, col] == Descriptor.black:
                    sum_gor += ((float(x)/Descriptor.box_width)**2)*y
                    sum_vert += ((float(y)/Descriptor.box_height)**2)*x
                y += 1
            y = 0 - Descriptor.box_height/2
            x += 1
        #eleventh_feature = self.roundd(float(sum_gor)/(Descriptor.on_pixels * Descriptor.box_height))
        #twelfth_feature = self.roundd(float(sum_vert)/(Descriptor.on_pixels*Descriptor.box_width))
        eleventh_feature = float(sum_gor)/(Descriptor.on_pixels * Descriptor.box_height)
        twelfth_feature = float(sum_vert)/(Descriptor.on_pixels*Descriptor.box_width)
        print 'norm 11', normalization.normalize(eleventh_feature,0.125,-0.125)
        print 'norm 12', normalization.normalize(twelfth_feature,0.125,-0.125)
        #features = [eleventh_feature, twelfth_feature]
        features = [normalization.normalize(eleventh_feature,0.125,-0.125), normalization.normalize(twelfth_feature,0.125,-0.125)]
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
        y = 0 - Descriptor.box_height/2
        vert_sum = 0
        for col in range(Descriptor.l_edge, columns_count):
            for row in range(Descriptor.t_edge, rows_count):
                if matrix[row, col] == Descriptor.black:
                    if (col-1) < 0 or matrix[row, col - 1] != Descriptor.black:
                        count_edges += 1
                        vert_sum += y
                y += 1
            y = 0 - Descriptor.box_height/2
        #thirteen_feature = self.roundd(float(count_edges)/Descriptor.on_pixels)
        #fourteen_feature = self.roundd(float(vert_sum)/Descriptor.box_height)
        thirteen_feature = float(count_edges)/Descriptor.box_height
        fourteen_feature = float(vert_sum)/Descriptor.on_pixels
        print 'NONnorm 13', round(thirteen_feature,3)
        print "NONnorm 14", round(fourteen_feature,3)
        features = [round(thirteen_feature,3), round(fourteen_feature,3)]
        return features

    def fifteen_sixteen(self, matrix):
        #15. The mean number of edges (an "on" pixel immediately above either an "off" pixel
        #or the image boundary) encountered when making systematic scans of the image from
        #bottom to top over all horizontal positions within the box.
        #16. The sum of horizontal positions of edges encountered as measured in 15 above.
        rows_count = matrix.shape[0]
        columns_count = matrix.shape[1]
        count_edges = 0
        x = 0 - Descriptor.box_width/2
        hor_sum = 0
        for col in range(Descriptor.l_edge, columns_count):
            for row in range(Descriptor.t_edge, rows_count):
                if matrix[row, col] == Descriptor.black:
                    if (row + 1) == rows_count or matrix[row + 1, col] != Descriptor.black:
                        count_edges += 1
                        hor_sum += x
            x += 1
        #fifteen_feature = self.roundd(float(count_edges)/Descriptor.on_pixels)
        #sixteen_feature = self.roundd(float(hor_sum)/Descriptor.box_width) #???????????????????????
        fifteen_feature = float(count_edges)/Descriptor.box_width
        sixteen_feature = float(hor_sum)/Descriptor.on_pixels
        print 'NONnorm 15', round(fifteen_feature,3)
        print 'NONnorm 16', round(sixteen_feature,3)
        features = [round(fifteen_feature,3), round(sixteen_feature,3)]
        return features

    def descriptor(self, matrix0):
        # 16 features 18 30
        sized = cv2.resize(matrix0, (18, 30))
        matrix = cv2.threshold(sized, 127, Descriptor.color, cv2.THRESH_BINARY)[1]
        cv2.imshow('digit', matrix)
        cv2.waitKey(0)
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
       # print vector
        return vector