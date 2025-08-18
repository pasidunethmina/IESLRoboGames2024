import cv2
import numpy as np

# Open webcam
cap = cv2.VideoCapture(0)

def detect_walls():
    ret, frame = cap.read()

    # Get frame dimensions
    height, width, _ = frame.shape

    # Define middle region
    startY = height // 3  # Start from 1/3 of the height
    endY = 2 * (height // 3)  # End at 2/3 of the height
    startX = width // 4  # Start from 1/4 of the width
    endX = 3 * (width // 4)  # End at 3/4 of the width

    # Draw rectangle around middle region
    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Crop middle region
    middle_region = frame[startY:endY, startX:endX]

    # Convert to grayscale & apply edge detection
    gray = cv2.cvtColor(middle_region, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # Compute edge density (total edges / total area)
    total_pixels = (endX - startX) * (endY - startY)
    edge_density = np.count_nonzero(edges) / total_pixels

    # Classify the entire middle region
    if edge_density < 0.04:
        label = "Wall"
        print("wall")

    else:
        label = "Object"
        print("Object")

    # Draw label on the full image
    label_position = (startX + 10, startY - 10)
    cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display results
    cv2.imshow('Full Image with Middle Region', frame)
    cv2.imshow('Edge Detection (Middle Region)', edges)

    # Classify the entire middle region
    if edge_density < 0.04:
        return True

    else:
        return False

while True:
    detect_walls()

# Cleanup
cap.release()
cv2.destroyAllWindows()
