import cv2
import math
from sklearn import svm
import matplotlib.pyplot as plt
import numpy as np
import descriptor

thresh = 127

def predict_number(clf, array):
    d = descriptor.Descriptor()
    descr = d.descriptor(array)
    label = clf.predict(descr)
    print label

def recognize_number(number, clf):
    height = number.shape[0]
    number = cv2.resize(number, (2000,height))
    splitted = np.hsplit(number, 10)
    for array in splitted:
        bin_array = cv2.threshold(array, 127, descriptor.Descriptor.color, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        predict_number(clf, bin_array)
    return

def main():
    images = [cv2.imread('new_learn/0_1.png',0), cv2.imread('new_learn/0_2.png',0), cv2.imread('new_learn/0_3.png',0), cv2.imread('new_learn/0_4.png',0),
              cv2.imread('new_learn/0_5.png',0), cv2.imread('new_learn/0_6.png',0),cv2.imread('new_learn/0_7.png',0), cv2.imread('new_learn/0_8.png',0),
              cv2.imread('new_learn/4_1.png',0),cv2.imread('new_learn/4_2.png',0),cv2.imread('new_learn/4_3.png',0),cv2.imread('new_learn/4_4.png',0),
              cv2.imread('new_learn/4_5.png',0),cv2.imread('new_learn/4_6.png',0), cv2.imread('new_learn/4_7.png',0),cv2.imread('new_learn/4_8.png',0),
              cv2.imread('new_learn/5_1.png',0),cv2.imread('new_learn/5_2.png',0),cv2.imread('new_learn/5_3.png',0),cv2.imread('new_learn/5_4.png',0),
              cv2.imread('new_learn/5_6.png',0),cv2.imread('new_learn/5_7.png',0),cv2.imread('new_learn/5_8.png',0),
              cv2.imread('new_learn/3_0.png',0),cv2.imread('new_learn/3_1.png',0),cv2.imread('new_learn/3_2.png',0),cv2.imread('new_learn/3_3.png',0),
              cv2.imread('new_learn/3_4.png',0),
              cv2.imread('real_learn/0_1.png',0),cv2.imread('real_learn/0_2.png',0),cv2.imread('real_learn/0_3.png',0),
              cv2.imread('real_learn/3_1.png',0),cv2.imread('real_learn/3_2.png',0),cv2.imread('real_learn/3_3.png',0),
              cv2.imread('real_learn/5_1.png',0),cv2.imread('real_learn/5_2.png',0),cv2.imread('real_learn/5_3.png',0),#cv2.imread('real_learn/5_4.png',0),
              cv2.imread('real_learn/6_1.png',0),cv2.imread('real_learn/6_2.png',0),cv2.imread('real_learn/6_3.png',0), cv2.imread('real_learn/6_4.png',0),
              cv2.imread('real_learn/6_5.png',0),cv2.imread('real_learn/6_6.png',0),
              cv2.imread('real_learn/9_1.png',0),cv2.imread('real_learn/9_2.png',0),cv2.imread('real_learn/9_3.png',0),
              cv2.imread('real_learn/c_1.png',0),cv2.imread('real_learn/c_2.png',0),cv2.imread('real_learn/c_3.png',0), cv2.imread('real_learn/c_4.png',0),
              cv2.imread('real_learn/h_1.png',0),cv2.imread('real_learn/h_2.png',0),cv2.imread('real_learn/h_3.png',0),
              cv2.imread('real_learn/y_1.png',0),cv2.imread('real_learn/y_2.png',0),
              cv2.imread('real_learn/m_1.png',0),cv2.imread('real_learn/m_2.png',0),cv2.imread('real_learn/m_4.jpg',0),cv2.imread('real_learn/m_5.jpg',0),
              cv2.imread('real_learn/k_1.png',0),cv2.imread('real_learn/k_2.png',0),cv2.imread('real_learn/k_4.jpg',0),
              cv2.imread('real_learn/k_5.jpg',0),cv2.imread('real_learn/k_6.png',0),]

    vectors = []
    for el in images:
        binary_matrix = cv2.threshold(el, thresh, descriptor.Descriptor.color, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        #cv2.imshow('digit', binary_matrix)
        #cv2.waitKey(0)
        d = descriptor.Descriptor()
        linear_vector = d.descriptor(binary_matrix)
        vectors.append(linear_vector)

    #1 = C
    #2 = H
    #7 = Y
    #8 = M
    #10 = K

    y = [0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,3,3,3,3,3,0,0,0,3,3,3,5,5,5,6,6,6,6,6,6,9,9,9,1,1,1,1,2,2,2,7,7,8,8,8,8,10,10,10,10,10]
    clf = svm.LinearSVC()
    clf.fit(vectors, y)

    number = cv2.imread('numbers/1.jpeg',0)
    recognize_number(number, clf)

if __name__ == '__main__':
    main()
