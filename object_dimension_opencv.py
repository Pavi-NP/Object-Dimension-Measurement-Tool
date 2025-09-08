# object-dimension-measurement/object_dimension_opencv.py
# import necessary libraries
import cv2
import numpy as np
import random
import base64
import io
from PIL import Image
import os


def process_image_from_data(image_data, threshold=100, blur_amount=3, pixel_ratio=0.2645833):
    """
    Process image from base64 data and return results
    """
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert PIL image to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Process the image
        result = process_opencv_image(opencv_image, threshold, blur_amount, pixel_ratio)
        
        return result
        
    except Exception as e:
        return {"error": str(e)}


def process_opencv_image(img, threshold=100, blur_amount=3, pixel_ratio=0.2645833):
    """
    Process OpenCV image and return measurements
    """
    # Convert image to gray colored and blur it
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.blur(img_gray, (blur_amount, blur_amount))

    # create canny image to detect edges
    imgThresh = cv2.Canny(img_gray, threshold, threshold * 2)

    # draw contours
    contours, extra = cv2.findContours(imgThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return {
            "error": "No contours found",
            "diameter_mm": 0,
            "category": "None",
            "radius_pixels": 0,
            "processed_image": None
        }

    # initialize arrays to store contour details
    contours_poly = [0] * len(contours)
    centers = [0] * len(contours)
    radius = [0] * len(contours)

    for i, c in enumerate(contours):
        # store contour details
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])

    drawing = np.zeros((imgThresh.shape[0], imgThresh.shape[1], 3), dtype=np.uint8)

    # now we need to check maximum radius from all contours
    max_rad = 0
    for i in range(len(contours)):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.drawContours(drawing, contours_poly, i, color, 1)

        if int(radius[i]) > int(radius[max_rad]):
            max_rad = i

    # draw circle with maximum radius
    if len(centers) > max_rad and radius[max_rad] > 0:
        cv2.circle(drawing, (int(centers[max_rad][0]),
                             int(centers[max_rad][1])),
                   int(radius[max_rad]), (0, 255, 0), 2)
        
        # Draw center point
        cv2.circle(drawing, (int(centers[max_rad][0]),
                             int(centers[max_rad][1])), 3, (0, 0, 255), -1)

        # convert pixel value to millimeters
        diameter_mm = round(int(radius[max_rad]) * pixel_ratio * 2)
        radius_pixels = int(radius[max_rad])

        # call classifier function
        category = classifier(diameter_mm)

        # put details on output image
        txt = "[{cat}] {mm}mm".format(cat=category, mm=diameter_mm)
        cv2.putText(drawing, txt, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Convert processed image to base64
        _, buffer = cv2.imencode('.png', drawing)
        processed_image_b64 = base64.b64encode(buffer).decode('utf-8')

        return {
            "diameter_mm": diameter_mm,
            "category": category,
            "radius_pixels": radius_pixels,
            "processed_image": f"data:image/png;base64,{processed_image_b64}",
            "center_x": int(centers[max_rad][0]),
            "center_y": int(centers[max_rad][1])
        }
    else:
        return {
            "error": "No valid circles found",
            "diameter_mm": 0,
            "category": "None",
            "radius_pixels": 0,
            "processed_image": None
        }


def classifier(diam):
    if diam < 47:
        return "Small"
    elif diam > 64:
        return "Large"
    else:
        return "Medium"


def process_file_image(file_path, threshold=100, blur_amount=3, pixel_ratio=0.2645833):
    """
    Process image from file path
    """
    try:
        img = cv2.imread(file_path)
        if img is None:
            return {"error": "Could not load image"}
        
        return process_opencv_image(img, threshold, blur_amount, pixel_ratio)
    except Exception as e:
        return {"error": str(e)}


# Keep the original main function for standalone usage
def main():
    cam = cv2.VideoCapture(0)
    img_name = ""
    cont = False

    while True:
        ret, frame = cam.read()

        # if there is an issue to open the webcam
        if not ret:
            print("failed to grab frame")
            break

        cv2.imshow("test", frame)
        k = cv2.waitKey(1)

        # press ESC button to cancel process
        if k % 256 == 27:
            print("Escape hit, closing...")
            break

        # press SPACE button to capture image
        elif k % 256 == 32:
            img_name = "input.jpg"
            cv2.imwrite(img_name, frame)
            cont = True
            break

    cam.release()
    cv2.destroyAllWindows()

    if cont:
        result = process_file_image(img_name)
        print("Diameter : " + str(result.get('diameter_mm', 0)) + " mm")
        print("Category : " + result.get('category', 'Unknown'))


if __name__ == "__main__":
    main()
    