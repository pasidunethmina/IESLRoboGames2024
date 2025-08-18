import cv2
import numpy as np
from kobukidriver import Kobuki  # Ensure you have the correct Kobuki class

# Define color thresholds in BGR order (OpenCV uses BGR)
lower_red = np.array([0, 0, 140])
upper_red = np.array([100, 100, 255])

lower_green = np.array([0, 120, 0])
upper_green = np.array([120, 255, 120])

lower_blue = np.array([140, 0, 0])
upper_blue = np.array([255, 150, 150])

# Open webcam
cap = cv2.VideoCapture(0)

# Initialize Kobuki
kobuki = Kobuki()

# Start rotating continuously
kobuki.move(400, -200, 0)  # Left wheel forward, right wheel backward for continuous rotation

while True:
    kobuki.move(400, -200, 0)  # Left wheel forward, right wheel backward for continuous rotation
    ret, frame = cap.read()
    if not ret:
        break

    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Define the middle region (ROI)
    roi_top = height // 7
    roi_bottom = 6 * height // 7
    roi_left = 3 * width // 7
    roi_right = 4 * width // 7

    # Crop the frame to the middle region
    roi_frame = frame[roi_top:roi_bottom, roi_left:roi_right]

    # Create masks for Red, Green, and Blue
    mask_red = cv2.inRange(roi_frame, lower_red, upper_red)
    mask_green = cv2.inRange(roi_frame, lower_green, upper_green)
    mask_blue = cv2.inRange(roi_frame, lower_blue, upper_blue)

    # Calculate total number of pixels
    total_pixels = roi_frame.size // 3  # Since it's a color image, divide by 3 (BGR channels)

    # Calculate the number of pixels for each color
    red_pixels = np.sum(mask_red > 0)
    green_pixels = np.sum(mask_green > 0)
    blue_pixels = np.sum(mask_blue > 0)

    # Calculate percentage for each color
    red_percentage = (red_pixels / total_pixels) * 100
    green_percentage = (green_pixels / total_pixels) * 100
    blue_percentage = (blue_pixels / total_pixels) * 100

    # Print the percentages in the terminal
    print(f"Red: {red_percentage:.2f}%")
    print(f"Green: {green_percentage:.2f}%")
    print(f"Blue: {blue_percentage:.2f}%")
    print("-" * 30)

    # Stop the robot when red is detected

    # Highlight the region with detected colors
    roi_frame[mask_red > 0] = [0, 0, 255]   # Mark Red regions as Red
    roi_frame[mask_green > 0] = [0, 255, 0] # Mark Green regions as Green
    roi_frame[mask_blue > 0] = [255, 0, 0]  # Mark Blue regions as Blue

    # Draw the ROI rectangle on the original frame
    cv2.rectangle(frame, (roi_left, roi_top), (roi_right, roi_bottom), (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Color Detection", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

