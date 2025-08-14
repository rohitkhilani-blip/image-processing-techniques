import cv2
import numpy as np

def solution(image_path):
    ############################
    ############################

    ############################
    ############################
    ## comment the line below before submitting else your code wont be executed##
    # pass
    # image = cv2.imread(image_path)

    def cropping(image):
        h, w, _ = image.shape
        crop_amt = 0.20
        top_c = int(h * crop_amt)
        bottom_c = int(h * crop_amt)
        left_c = int(w * crop_amt)
        right_c = int(w * crop_amt)
        cropped_image = image[top_c:h - bottom_c, left_c:w - right_c]
        return cropped_image

    def realign_text(input_image_path):
        input_image = cv2.imread(input_image_path)
        gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        gauss_blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0) #applying gaussian blur to reduce noise and improve edge detection

        edges = cv2.Canny(gauss_blurred_image, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

        if lines is not None and len(lines) > 0:
            x1, y1, x2, y2 = lines[0][0]
            angle = np.arctan2(y2 - y1, x2 - x1)
            angle_in_degrees = np.degrees(angle)
        else:
            angle_in_degrees = 0

        #creating a new canvas so that there are no black spaces after rotation
        new_width = int(input_image.shape[1] * 2)
        new_height = int(input_image.shape[0] * 2)
        white_background = np.ones((new_height, new_width, 3), dtype=np.uint8) * 255
        x_offset = (new_width - input_image.shape[1]) // 2
        y_offset = (new_height - input_image.shape[0]) // 2

        white_background[y_offset:y_offset + input_image.shape[0], x_offset:x_offset + input_image.shape[1]] = input_image

        centre = tuple(np.array(white_background.shape[1::-1]) / 2)

        if angle_in_degrees >= 0:
            rot_mat = cv2.getRotationMatrix2D(centre, angle_in_degrees, 1.0)
        else:
            rot_mat = cv2.getRotationMatrix2D(centre, 360 + angle_in_degrees, -1.0)

        white_background = cv2.warpAffine(white_background, rot_mat, white_background.shape[1::-1], flags=cv2.INTER_LINEAR)
        return cropping(white_background)

    final = realign_text(image_path)

    return final
