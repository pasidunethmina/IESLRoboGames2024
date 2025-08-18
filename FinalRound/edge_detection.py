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


cap = cv2.VideoCapture(0)

def is_wall(color):
    ret, frame = cap.read()

    if color == "red":
        mask = cv2.inRange(frame, lower_red, upper_red)

    elif color == "green":
        mask = cv2.inRange(frame, lower_green, upper_green)

    elif color == "blue":
        mask = cv2.inRange(frame, lower_blue, upper_blue)
    
    elif color == "yellow":
        mask = cv2.inRange(frame, lower_yellow, upper_yellow)


    # Find contours in the red mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the bounding box that includes all red areas
        x_min, y_min, x_max, y_max = float('inf'), float('inf'), 0, 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            x_min, y_min = min(x_min, x), min(y_min, y)
            x_max, y_max = max(x_max, x + w), max(y_max, y + h)

        bound_value = 5
        x_min = abs(x_min - bound_value)
        x_max = x_max + bound_value
        y_min = abs(y_min - bound_value)
        y_max = bound_value + y_max
        # Extract the entire red region
        roi = frame[y_min:y_max, x_min:x_max]

        # Convert ROI to grayscale for edge detection
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Apply edge detection
        edges = cv2.Canny(gray_roi, 50, 150)

        # Compute edge density
        edge_pixels = cv2.countNonZero(edges)
        total_pixels = (x_max - x_min) * (y_max - y_min) if (x_max - x_min) * (y_max - y_min) > 0 else 1
        edge_density = edge_pixels / total_pixels
        print(edge_density)

        # Classify based on edge density
        label = "Box" if edge_density > 0.03 else "Wall"

                # Draw bounding box and label on the original frame
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Show detected edges inside the red region
        frame[y_min:y_max, x_min:x_max] = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Keep detected red pixels red
        if color == "red":
            frame[np.where(mask > 0)] = [0, 0, 255]

        elif color == "green":
            frame[np.where(mask > 0)] = [0, 255, 0]
        
        elif color == "blue":
            frame[np.where(mask > 0)] = [255, 0, 0]

        elif color == "yellow":
            frame[np.where(mask > 0)] = [0, 255, 255]

        cv2.imshow("Highlighted & Processed", frame)

        if edge_density > 0.02:
            return True
    
        else:
            return False


while True:
    is_wall("blue")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
