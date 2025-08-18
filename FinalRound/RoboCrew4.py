import cv2
import numpy as np
from kobukidriver import Kobuki  # Ensure you have the correct Kobuki class

# Define color thresholds in BGR order (OpenCV uses BGR)
lower_red = np.array([0, 0, 140])
upper_red = np.array([100, 100, 255])

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

    # Create masks for Red color
    mask_red = cv2.inRange(roi_frame, lower_red, upper_red)

    # Calculate total number of pixels
    total_pixels = roi_frame.size // 3  # Since it's a color image, divide by 3 (BGR channels)

    # Calculate the number of red pixels
    red_pixels = np.sum(mask_red > 0)

    # Calculate the percentage of red pixels
    red_percentage = (red_pixels / total_pixels) * 100

    # Find contours of the red region to get the center of the red color
    contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Get the largest contour (the one with the biggest area)
        largest_contour = max(contours, key=cv2.contourArea)

        # Calculate the center of the largest red contour
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            center_x = int(moments["m10"] / moments["m00"])
            center_y = int(moments["m01"] / moments["m00"])

            # Draw a circle at the center of the red region
            cv2.circle(frame, (center_x, center_y), 10, (0, 255, 255), -1)

            # Control logic to move towards the red region
            # Calculate the error between the center of the red region and the center of the frame
            error_x = center_x - (roi_left + roi_right) // 2  # Error in X-axis (horizontal direction)

            # Adjust robot speed based on the error
            # If the error is positive, the robot is to the right of the red center, so move left
            # If the error is negative, the robot is to the left of the red center, so move right
            if abs(error_x) > 20:  # Dead zone to avoid unnecessary small movements
                if error_x > 0:
                    kobuki.move(100, -100, 0)  # Move left
                    print("Moving Left")
                else:
                    kobuki.move(-100, 100, 0)  # Move right
                    print("Moving Right")
            else:
                # If the robot is close to the red center, move forward
                kobuki.move(200, 200, 0)  # Move forward
                print("Moving Forward")

    # Show the frame with the detected red area
    cv2.imshow("Color Detection", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
