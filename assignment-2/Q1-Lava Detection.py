import cv2
import numpy as np

# Usage
def solution(image_path):
    image= cv2.imread(image_path)
    ######################################################################
    ######################################################################
    '''
    The pixel values of output should be 0 and 255 and not 0 and 1
    '''
    #####  WRITE YOUR CODE BELOW THIS LINE ###############################

    lower_bound = np.array([0, 10, 130], dtype=np.uint8)
    upper_bound = np.array([85, 255, 255], dtype=np.uint8)

    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    color_mask = cv2.inRange(image, lower_bound, upper_bound)

    combined_mask = cv2.bitwise_and(grayscale_image, color_mask)

    kernel = np.ones((5, 5), np.uint8)
    closed_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lava_mask = np.zeros_like(image)
    largest_contour = max(contours, key=cv2.contourArea)

    cv2.drawContours(lava_mask, [largest_contour], -1, (255, 255, 255), thickness=cv2.FILLED)

    ######################################################################
    return lava_mask