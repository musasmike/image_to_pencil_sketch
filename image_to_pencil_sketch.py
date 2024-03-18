# Import packages
import cv2
import base64

# Image Transformation
image = "images/car.png"
image_base64 = base64.b64encode(open(image, 'rb').read()).decode('ascii')


# Function that transforms the image to pencil drawing
def update_output_pencil(my_image):
    image_read = cv2.imread(my_image)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
    # Invert the image
    inverted_image = 255 - gray_image
    # Blurring the image
    blurred_image = cv2.GaussianBlur(inverted_image, ksize=(151, 151), sigmaX=0, sigmaY=0)
    # Inverting the blurred image
    inv_blur = 255 - blurred_image
    # Sketch the image
    sketched_image = cv2.divide(gray_image, inv_blur, scale=285.0)

    return cv2.imwrite("images/car_sketch.png", sketched_image)


# Transforms the image to a pencil sketch image
new_image = update_output_pencil(image)
new_image_ = "images/car_sketch.png"

# Read the pencil sketch image
pencil_sketch_image = cv2.imread(new_image_)
# Display the image
cv2.imshow('RGB', pencil_sketch_image)
cv2.waitKey(0)


