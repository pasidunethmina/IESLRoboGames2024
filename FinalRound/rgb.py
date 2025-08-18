import cv2
import numpy as np

def get_middle_area_rgb(frame, area_fraction=0.02):
    height, width, _ = frame.shape
    x_start = int(width * (0.5 - area_fraction / 2))
    x_end = int(width * (0.5 + area_fraction / 2))
    y_start = int(height * (0.5 - area_fraction / 2))
    y_end = int(height * (0.5 + area_fraction / 2))
    
    middle_area = frame[y_start:y_end, x_start:x_end]
    avg_rgb = np.mean(middle_area, axis=(0, 1))  # Calculate average RGB
    return tuple(map(int, avg_rgb[::-1])), (x_start, y_start, x_end, y_end)  # Return RGB and box coordinates

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    avg_rgb, (x_start, y_start, x_end, y_end) = get_middle_area_rgb(frame)
    print("Average RGB (Middle Area):", avg_rgb)
    
    cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
    cv2.imshow("Video Feed", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
