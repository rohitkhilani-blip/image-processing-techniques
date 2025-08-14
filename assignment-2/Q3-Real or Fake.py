import cv2
import numpy as np

def solution(audio_path):
    ############################
    ############################

    def check_maxima(lower_counts, lower_indices):
        if lower_counts == 9:
            sliced_indices = [int(column / 5) for column in lower_indices]

            increasing_order = all(sliced_indices[i] < sliced_indices[i + 1] for i in range(8))

            if increasing_order:
                return "real"
            else:
                return "fake"
        else:
            return "fake"

    def find_lower_bounds(image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h, w = img.shape

        non_white_indices = [next((row for row in range(h) if img[row][col] != 255), h) for col in range(w)]
        indices_sliced = non_white_indices[::5]

        lower_bound_counts = sum(1 for col in range(1, (int)(w / 5) - 1)if indices_sliced[col] > indices_sliced[col - 1] and indices_sliced[col] > indices_sliced[col + 1])
        lower_indices = [col * 5 for col in range(1, (int)(w / 5) - 1)if indices_sliced[col] > indices_sliced[col - 1] and indices_sliced[col] > indices_sliced[col + 1]]

        return check_maxima(lower_bound_counts, lower_indices)

    def detect_object_boundaries(image_path):
        input_image = cv2.imread(image_path)
        gray_scaled_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

        _, binary_image = cv2.threshold(gray_scaled_image, 245, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_area = 0
        largest_contour = None
        for cnt in contours:
            contour_area = cv2.contourArea(cnt)
            if contour_area > largest_area:
                largest_area = contour_area
                largest_contour = cnt

        boundary_mask = np.ones_like(input_image)*255
        cv2.drawContours(boundary_mask, [largest_contour], -1, (0, 0, 0), 5)

        return find_lower_bounds(boundary_mask)

    ############################
    ############################
    ## comment the line below before submitting else your code wont be executed##
    # pass
    # class_name = 'fake'
    return detect_object_boundaries(audio_path)
