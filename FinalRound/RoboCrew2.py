import cv2
import numpy as np
import time
from kobukidriver import Kobuki  # Assuming the provided class is saved in kobuki_control.py

# Define color thresholds in BGR order (OpenCV uses BGR)
lower_red = np.array([0, 0, 140])   # Low values for Red
upper_red = np.array([100, 100, 255])  # High values for Red

lower_green = np.array([0, 120, 0])  # Low values for Green
upper_green = np.array([120, 255, 120])  # High values for Green

lower_blue = np.array([170, 0, 0])  # Low values for Blue
upper_blue = np.array([255, 250, 180])  # High values for Blue

# Open webcam
cap = cv2.VideoCapture(0)

def cam():
    
    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Define the middle region (ROI)
    roi_top = height // 7
    roi_bottom = 6 * height // 7
    roi_left = 3*width // 7
    roi_right = 4* width // 7

    # Crop the frame to the middle region
    roi_frame = frame[roi_top:roi_bottom, roi_left:roi_right]

    # Create masks for Red, Green, and Blue in BGR space
    mask_red = cv2.inRange(roi_frame, lower_red, upper_red)
    mask_green = cv2.inRange(roi_frame, lower_green, upper_green)
    mask_blue = cv2.inRange(roi_frame, lower_blue, upper_blue)

    # Highlight detected colors on the original frame
    roi_frame[mask_red > 0] = [0, 0, 255]   # Mark Red regions as Red
    roi_frame[mask_green > 0] = [0, 255, 0] # Mark Green regions as Green
    roi_frame[mask_blue > 0] = [255, 0, 0]  # Mark Blue regions as Blue


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
    print("-" * 30)  # Divider for readability

    # Show the cropped region (optional)
    #cv2.imshow("Middle Area Color Percentage Detection", roi_frame)
    # Highlight the ROI frame by drawing a green rectangle around it
    cv2.rectangle(frame, (roi_left, roi_top), (roi_right, roi_bottom), (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Color Detection", frame)

def main():
    # Initialize Kobuki
    kobuki = Kobuki()

    try:
        print("Starting Kobuki control...")

        # Move forward at 0.2 m/s for 2 seconds
        print("Moving forward...")
        kobuki.move(200, 200, 0)  # Left and right wheels at 200 mm/s
        time.sleep(3)

        # Stop for 1 second
        print("Stopping...")
        kobuki.move(0, 0, 0)
        time.sleep(1)

        # Move backward at 0.2 m/s for 2 seconds
        print("Moving backward...")
        kobuki.move(-200, -200, 0)  # Left and right wheels at -200 mm/s
        time.sleep(3)

        # Stop for 1 second
        print("Stopping...")
        kobuki.move(0, 0, 0)
        time.sleep(1)

        # Rotate left (counter-clockwise) at 0.5 rad/s for 1 second
        print("Rotating left...")
        kobuki.move(-200, 400, 1)  # Left wheel backward, right wheel forward
        time.sleep(6)

        # Stop for 1 second
        print("Stopping...")
        kobuki.move(0, 0, 0)
        time.sleep(1)

        # Rotate right (clockwise) at 0.5 rad/s for 1 second
        print("Rotating right...")
        kobuki.move(400, -200, 1)  # Left wheel forward, right wheel backward
        time.sleep(6)

        # Stop for 1 second
        print("Stopping...")
        kobuki.move(0, 0, 0)
        time.sleep(1)
        
        # Move backward at 0.2 m/s for 2 seconds
        print("Moving backward...")
        #kobuki.move(-200, -200, 0)  # Left and right wheels at -200 mm/s
        time.sleep(5)

        print("Finished control sequence.")

    except KeyboardInterrupt:
        print("Stopping Kobuki...")
    finally:
        # Ensure the robot stops
        kobuki.move(0, 0, 0)
        print("Kobuki stopped.")

#def forward():


if __name__ == "__main__":
    # Initialize Kobuki
    kobuki = Kobuki()
    kobuki.move(100, 100, 0)  # Left and right wheels at 200 mm/s
    
    while True :
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = cap.read()
        if not ret:
            break
        cam()
        if blue_percentage > 4 :
            kobuki.move(0, 0, 0)
            break
        
    
    
# Release resources
cap.release()
cv2.destroyAllWindows()
