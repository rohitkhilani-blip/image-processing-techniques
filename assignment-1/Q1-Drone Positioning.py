import cv2
import numpy as np

# Usage
def solution(image_path):
    image= cv2.imread(image_path)
    ######################################################################
    ######################################################################
    #####  WRITE YOUR CODE BELOW THIS LINE ###############################

    frame = cv2.resize(image, (600, 600))

    def flag_orientation_color(flag_image):
        top_left_colour = flag_image[50, 50]
        top_right_colour = flag_image[50, -50]
        saffron_thresh = (51, 153, 255)
        green_thresh = (0, 128, 0)

        if np.all(np.abs(top_left_colour - saffron_thresh) < 20) and np.all(np.abs(top_right_colour - saffron_thresh) < 20):
            flag_orientation = 1
            start_color = 1
        elif np.all(np.abs(top_left_colour - green_thresh) < 20) and np.all(np.abs(top_right_colour - green_thresh) < 20):
            flag_orientation = 1
            start_color = 0
        else:
            flag_orientation = 0
            if (np.all(np.abs(top_left_colour - green_thresh) < 20)):
                start_color = 0
            else:
                start_color = 1

        return flag_orientation, start_color

    def create_indian_flag(hr, saff):
        flag = np.ones((600, 600, 3), dtype=np.uint8) * 255
        saffron = [51, 153, 255]
        green = [0, 128, 0]
        white = [255, 255, 255]

        if (hr):
            if (saff):
                flag[:200, :] = saffron
                flag[200:400, :] = white
                flag[400:, :] = green
            else:
                flag[:200, :] = green
                flag[200:400, :] = white
                flag[400:, :] = saffron
        else:
            if (saff):
                flag[:, :200] = saffron
                flag[:, 200:400] = white
                flag[:, 400:] = green
            else:
                flag[:, :200] = green
                flag[:, 200:400] = white
                flag[:, 400:] = saffron

        centre = (300, 300)
        radius = 100
        circle_width = 2
        spoke_width = 1
        cv2.circle(flag, centre, radius, (255, 0, 0), circle_width)
        for angle in range(0, 360, 15):
            x1 = int(centre[0] + (radius - circle_width) * np.cos(np.radians(angle)))
            y1 = int(centre[1] + (radius - circle_width) * np.sin(np.radians(angle)))
            cv2.line(flag, (x1, y1), (300, 300), (255, 0, 0), spoke_width)

        return flag

    def cropping(image):
        h, w, _ = image.shape
        crop_amt = 0.05  # 5% crop
        top_c = int(h * crop_amt)
        bottom_c = int(h * crop_amt)
        left_c = int(w * crop_amt)
        right_c = int(w * crop_amt)
        cropped_image = image[top_c:h - bottom_c, left_c:w - right_c]
        return cropped_image

    def vertices(input_image):
        gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #determining the shape/edges of the flag based on the largest quadrilateral found in the gray scale image
        max_area = 0
        largest_quadrilateral = None

        for contour in contours:
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx_shape = cv2.approxPolyDP(contour, epsilon, True) #approximating the contour as a polygon but we consider only the polygons with 4 sides (a quadrilateral)

            if len(approx_shape) == 4:
                area_of_quad = cv2.contourArea(approx_shape)
                if area_of_quad > max_area:
                    max_area = area_of_quad
                    largest_quadrilateral = approx_shape

        vertices_of_quad = largest_quadrilateral.reshape(-1, 2)

        return vertices_of_quad

    vertices_of_the_flag = vertices(frame) #getting the vertices of the flag in the original input image

    min_x = min(vertices_of_the_flag[0][0], vertices_of_the_flag[1][0], vertices_of_the_flag[2][0], vertices_of_the_flag[3][0])
    max_x = max(vertices_of_the_flag[0][0], vertices_of_the_flag[1][0], vertices_of_the_flag[2][0], vertices_of_the_flag[3][0])
    min_y = min(vertices_of_the_flag[0][1], vertices_of_the_flag[1][1], vertices_of_the_flag[2][1], vertices_of_the_flag[3][1])
    max_y = max(vertices_of_the_flag[0][1], vertices_of_the_flag[1][1], vertices_of_the_flag[2][1], vertices_of_the_flag[3][1])

    frame = frame[min_y:600 - max_y, min_x:600 - max_x] #cropping the image so that max no. of the vertices of the flag can be on the image boundary for increased accuracy
    frame = cv2.resize(image, (600, 600))

    vertices_of_the_flag = vertices(frame) #finding the vertices of the flag again in the resized and cropped image

    tl = None
    tr = None
    bl = None
    br = None
    centre = (300, 300)

    #assigning the closes corner to each vertex to fix the perspective of the input flag
    for vertex in vertices_of_the_flag:

        distance_tl = np.linalg.norm(np.array(vertex) - np.array((0, 0)))
        distance_tr = np.linalg.norm(np.array(vertex) - np.array((600, 0)))
        distance_bl = np.linalg.norm(np.array(vertex) - np.array((0, 600)))
        distance_br = np.linalg.norm(np.array(vertex) - np.array((600, 600)))

        closest_distance = min(distance_tl, distance_tr, distance_bl, distance_br)

        # Assign the vertex to the corresponding corner
        if closest_distance == distance_tl and tl == None:
            tl = vertex
        elif closest_distance == distance_tr and tr == None:
            tr = vertex
        elif closest_distance == distance_bl and bl == None:
            bl = vertex
        else:
            br = vertex

    vertices_coordinates = np.float32([tl, bl, tr, br])
    image_corners = np.float32([(0, 0), (0, 600), (600, 0), (600, 600)])

    #geometrical transformation (transforming the coordinates of the pixels to get the idea of the orientation of the flag)
    perspective_matrix = cv2.getPerspectiveTransform(vertices_coordinates, image_corners)
    transformed_input_image = cv2.warpPerspective(frame, perspective_matrix, (600, 600))
    transformed_input_image = cropping(transformed_input_image) #cropping the image a little so that there are no rough edges with black pixels in the image

    #checking the correct orientation of the flag- (Horizontal, Upright), (Horizontal, Flipped), (Vertical, 90degree), (Vertical, -90degree)
    hr, saff = flag_orientation_color(transformed_input_image)

    #generating the output image based on the image of the flag obtained from the input image
    image = create_indian_flag(hr, saff)

    ######################################################################

    return image