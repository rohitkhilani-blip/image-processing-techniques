# image-processing-techniques

# Algorithms Used :
## Drone Positioning
1. Read the image and resize it to appropriate size (here, 600 x 600).
2. Get the vertices of the object (here, flag) in the original image using the 'vertices' function.
3. The function converts the image into gray-scale, starts finding the contours and returns the vertices with the largest possible quadrilateral area.
4. Then we arrange the vertices to the 4 corners of the flag and crop the image accordingly to remove any extra spaces from around it.
5. We then again get the vertices of the flag in this cropped image.
6. The top_left, top_right, bottom_left and bottom_right corners are selected based on the linear distance of the four vertices of the quadrilateral found.
7. Based on these, the correct orientation of the flag is found using the colours of the flag.
8. We can then generate a flag with the correct orientation based on this information.

## Audio Classification
1. The audio path is given as an input to the function.
2. The wave_form and samp_rate is found out using the librosa library.
3. I then used the mel-spectrogram technique to get the power of the audio.
4. This is then converted to decibles.
5. The spectrogram image is saved and then read to generate the edges in the image.
6. Based on a threshold, it is decided if the audio is 'metal' or 'cardboard'.

## Text Alignment
1. The image path is given as an input to the function.
2. The image is then converted to gray-scale and I applied gaussian blur to it so that only the most intense edges are detected.
3. The Canny technique is used to detect the edges in the image and then HoughLines algorithm is applied to get straight lines in the image from the detected edges.
4. Based on these straight lines and the angle they make with the horizontal (0 degrees), the alignment of the text is known and then the text is rotated in the opposite direction by the same angle to straighten it.
5. If the angle (say, theta) is negative (clockwise), then it is rotated in the opposite direction and by an angle of (360+theta).

## Region Detection
1. The main objective here is to separate the image into two (or more) regions.
2. With prior information about the image, we can set various threshold ranges based on the colours, contrast, sharpness or other features to extract the required regions.
3. Here, I've used the colour contrast to separate the lava region from the image.
4. Based on the lower and upper bound of the colours present in the image, I've created a colour-mask of the image.
5. This colour mask is then combined with the gray-scale image to create a combined mask of the image.
6. Then using kernels of size (5, 5), I've created another mask using Morphology, which is then used to detect the contours of the lava region.

## Flash No-flash Images
1. We use flash to light up and area, and capture the surroundings better. But while the flash improves the lighting of the image, it reduces the details because of the reflections.
2. In this algorithm, I've used the bilateral filter to combine the flash and no-flash formats of the same image to improve the overall quality of the image.
3. I've used various different functions in this algorithm- Cross-bilateral Filter, Bilateral Filter, Enhancing the Light and Detecting the shadows.
4. Firstly, I created the filtered versions of both the images using the cross-bilateral filter.
5. Then I created a shadow-mask using the filtered images using thresholding.
6. Finally, combining the two images with different weights to each, we get the final image.
7. *Note - Here I've created my own functions. Although, we can also use the functions available in different libraries.*

## Real OR Fake
1. This algorithm deals with the detection of the originality of a specific object or person based on the image inputs.
2. We can do this using various approaches based on the information we have about the image. Here I've used the object boundaries and the number of *heads* Ravana has in any specific image.
3. The basic function is to detect the boundaries of the figure using binary thresholding and contour detection.
4. I've detected the various possible contours possible in the image and then kept the shape with the maximum area as the contour of the figure.
5. Then I've checked the lower bounds of the contour of the figure and detected the number of *heads* on each side of the face, which reveals if the image is real or fake.