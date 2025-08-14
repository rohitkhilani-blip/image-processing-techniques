import cv2
import numpy as np

def solution(image_path_a, image_path_b):
    ############################
    ############################
    ## image_path_a is path to the non-flash high ISO image
    ## image_path_b is path to the flash low ISO image
    ############################
    ############################
    ## comment the line below before submitting else your code wont be executed##
    # pass
    # image = cv2.imread(image_path_b)

    def cross_bilateral_filter(flash_image, no_flash_image, spatial_sigma, range_sigma):
        rows, cols, channels = flash_image.shape
        final_image = np.zeros_like(flash_image)

        for i in range(rows):
            i_begin, i_end = max(0, i - 2 * spatial_sigma), min(rows, i + 2 * spatial_sigma + 1)

            for j in range(cols):
                j_begin, j_end = max(0, j - 2 * spatial_sigma), min(cols, j + 2 * spatial_sigma + 1)

                i_diff = np.arange(i_begin, i_end)[:, np.newaxis] - i
                j_diff = np.arange(j_begin, j_end) - j

                spatial_weights = np.exp(-(i_diff ** 2 + j_diff ** 2) / (2 * spatial_sigma ** 2))

                for k in range(channels):
                    intensity_diff = no_flash_image[i_begin:i_end, j_begin:j_end, k] - no_flash_image[i, j, k]
                    range_weights = np.exp(-(intensity_diff ** 2) / (2 * range_sigma ** 2))

                    normalized_weights = spatial_weights * range_weights
                    normalized_weights /= np.sum(normalized_weights)

                    final_image[i, j, k] = np.sum(normalized_weights * flash_image[i_begin:i_end, j_begin:j_end, k])

        return final_image

    def bilateral_filter(image, spatial_sigma, range_sigma):
        rows, cols, channels = image.shape
        final_image = np.zeros_like(image)

        for i in range(rows):
            i_begin, i_end = max(0, i - 2 * spatial_sigma), min(rows, i + 2 * spatial_sigma + 1)

            for j in range(cols):
                j_begin, j_end = max(0, j - 2 * spatial_sigma), min(cols, j + 2 * spatial_sigma + 1)

                i_diff = np.arange(i_begin, i_end)[:, np.newaxis] - i
                j_diff = np.arange(j_begin, j_end) - j

                spatial_weights = np.exp(-(i_diff ** 2 + j_diff ** 2) / (2 * spatial_sigma ** 2))

                for k in range(channels):
                    intensity_diff = image[i_begin:i_end, j_begin:j_end, k] - image[i, j, k]
                    range_weights = np.exp(-(intensity_diff ** 2) / (2 * range_sigma ** 2))

                    normalized_weights = spatial_weights * range_weights
                    normalized_weights /= np.sum(normalized_weights)

                    final_image[i, j, k] = np.sum(normalized_weights * image[i_begin:i_end, j_begin:j_end, k])

        return final_image

    def enhance_light(flash_image_path, no_flash_image_path):
        flash_image = cv2.imread(flash_image_path)
        no_flash_image = cv2.imread(no_flash_image_path)

        # flash_image_filtered = bilateral_filter(flash_image, 2,2)
        # flash_image_filtered = cv2.bilateralFilter(flash_image, d=5, sigmaColor=20, sigmaSpace=20)
        # no_flash_image_filtered=cv2.bilateralFilter(no_flash_image, d=5, sigmaColor=20, sigmaSpace=20)
        # no_flash_image_filtered = bilateral_filter(no_flash_image, 2,2)

        spatial_sigma = 3
        range_sigma = 3

        flash_image_filtered = cross_bilateral_filter(flash_image, no_flash_image, spatial_sigma, range_sigma)
        no_flash_image_filtered = cross_bilateral_filter(no_flash_image, flash_image, spatial_sigma, range_sigma)

        shadow_mask = detect_image_shadows(flash_image_filtered, no_flash_image_filtered)
        enhanced_light_image = transfer_details(flash_image_filtered, no_flash_image_filtered, shadow_mask)

        return enhanced_light_image

    def detect_image_shadows(flash_image, no_flash_image):
        flash_gray = cv2.cvtColor(flash_image, cv2.COLOR_BGR2GRAY)
        no_flash_gray = cv2.cvtColor(no_flash_image, cv2.COLOR_BGR2GRAY)

        diff_image = cv2.absdiff(flash_gray, no_flash_gray)
        threshold = 30
        shadow_mask = (diff_image > threshold).astype(np.uint8) * 255

        return shadow_mask

    def transfer_details(flash_image, no_flash_image, shadow_mask):
        final_enhanced_image = cv2.addWeighted(no_flash_image, 0.8, flash_image, 0.2, 0.0)

        return final_enhanced_image

    return enhance_light(image_path_b,image_path_a)
