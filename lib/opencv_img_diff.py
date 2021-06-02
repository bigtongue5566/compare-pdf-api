# import the necessary packages
# from skimage.metrics import structural_similarity
# from skimage import img_as_float
import imutils
import cv2
import numpy as np

def compare(file_path_1, file_path_2):
    # load the two input images
    imageA = cv2.imread(file_path_1)
    imageB = cv2.imread(file_path_2)
    # convert the images to grayscale
    # grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    # grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    # diff = cv2.subtract(imageA, imageB)
    diff = np.bitwise_xor(imageA, imageB)
    diff = np.bitwise_or.reduce(diff, axis=2)
    diff[diff != 0] = 255
    #diff = (diff * 255).astype("uint8")
    # diff = (diff * 255).astype("uint8")
    # (score, diff) = structural_similarity(imageA, imageB,multichannel =True, full=True)
    # diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  
    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    ret, mask = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # x,y,w,h
    return list(map(lambda c: cv2.boundingRect(c), cnts))
