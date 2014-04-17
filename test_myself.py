import cv2
from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt

dimensons = (12,9)

def descriptor(image):
    return cv2.resize(image,dimensons).reshape((-1))

def invert_binary(vector):
    output = []
    for el in vector:
        output.append(1-el)
    return output

def predict(path, clf, input):
    test_image = cv2.imread(path,0)

    im_bw = cv2.threshold(test_image, 127, 1, cv2.THRESH_BINARY)[1]
    #print type(im_bw)
    print im_bw.shape
    im_desc = descriptor(im_bw)
    im_inverted = invert_binary(im_desc)
    label = clf.predict(im_inverted)
    print label
    #plot_vector(im_inverted, label, input)
    return



def plot_vector(vector, name,input):
    data = list(vector)
    std = []
    for i in range(dimensons[0]*dimensons[1]):
        std.append(3)
    n_groups = dimensons[0]*dimensons[1]
    index = np.arange(n_groups)
    bar_width = 1
    opacity = 1
    error_config = {'ecolor': '0.3'}

    rects1 = plt.bar(index, data, bar_width,
                    alpha=opacity,
                    color='b',
                    error_kw=error_config,
                    label='expect: '+ input +'; predict: ' + str(name))
    plt.legend()
    plt.tight_layout()
    plt.show()
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
        im_bw = cv2.threshold(el, thresh, 1, cv2.THRESH_BINARY)[1]
        im_desc = descriptor(im_bw)
        im_inverted = invert_binary(im_desc)
        vectors.append(im_inverted)

    y = [0,0,0,0,0,0,0,0,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5]
    clf = svm.SVC()
    clf.fit(vectors,y)

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

if __name__ == '__main__':
    main()
