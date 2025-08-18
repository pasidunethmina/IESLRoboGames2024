import cv2
import numpy as np


# Define color thresholds in BGR order (OpenCV uses BGR)
lower_red = np.array([40, 20, 185])   # Low values for Red
upper_red = np.array([150, 120, 255])  # High values for Red

lower_green = np.array([0, 120, 0])  # Low values for Green
upper_green = np.array([120, 255, 120])  # High values for Green

lower_blue = np.array([180, 0, 0])  # Low values for Blue
upper_blue = np.array([255, 180, 110])  # High values for Blue

lower_yellow = np.array([0, 170, 170])  # Low values for Blue
upper_yellow = np.array([140, 255, 255])  # High values for Blue

# Open webcam
cap = cv2.VideoCapture(0)


def camera(color):
    
    ret, frame = cap.read()
    # Get the dimensions of the frame
    height, width, _ = frame.shape
    print(height, width)

    # Define the middle region (ROI)
    roi_top = 0
    roi_bottom = 9*height//10
    roi_left = 3*width // 7
    roi_right = 4* width // 7

    # Crop the frame to the middle region
    roi_frame = frame[roi_top:roi_bottom, roi_left:roi_right]

    # Calculate total number of pixels
    total_pixels = roi_frame.size // 3  # Since it's a color image, divide by 3 (BGR channels)

    if color == "red":
        # Create masks for Red, Green, and Blue in BGR space
        mask = cv2.inRange(roi_frame, lower_red, upper_red)
        # Highlight detected colors on the original frame
        roi_frame[mask > 0] = [0, 0, 255]   # Mark Red regions as Red
        red_pixels = np.sum(mask > 0)
        color_percentage = (red_pixels / total_pixels) * 100
   
    elif color == "green":
        # Create masks for Red, Green, and Blue in BGR space
        mask = cv2.inRange(roi_frame, lower_green, upper_green)
        roi_frame[mask > 0] = [0, 255, 0] # Mark Green regions as Green
        green_pixels = np.sum(mask > 0)
        color_percentage = (green_pixels / total_pixels) * 100

    elif color == "blue":
        # Create masks for Red, Green, and Blue in BGR space
        mask = cv2.inRange(roi_frame, lower_blue, upper_blue)
        roi_frame[mask > 0] = [255, 0, 0]  # Mark Blue regions as
        blue_pixels = np.sum(mask > 0) 
        color_percentage = (blue_pixels / total_pixels) * 100

    elif color == "yellow":
        # Create masks for Red, Green, and Blue in BGR space
        mask = cv2.inRange(roi_frame, lower_yellow, upper_yellow)
        roi_frame[mask > 0] = [0, 255, 255]  # Mark Blue regions as Blue
        yellow_pixels = np.sum(mask > 0)
        color_percentage = (yellow_pixels / total_pixels) * 100

    # Print the percentages in the terminal
    print(f"{color}: {color_percentage:.1f}%")
    print("-" * 30)  # Divider for readability

    # Highlight the ROI frame by drawing a green rectangle around it
    cv2.rectangle(frame, (roi_left, roi_top), (roi_right, roi_bottom), (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Color Detection", frame)

    return color_percentage

while True:
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        camera("blue")


# Release resources
cap.release()
cv2.destroyAllWindows()