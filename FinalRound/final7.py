import cv2
import numpy as np
import time
# from kobukidriver import Kobuki 


# Define color thresholds in BGR order (OpenCV uses BGR)
lower_red = np.array([40, 20, 185])   # Low values for Red
upper_red = np.array([150, 120, 255])  # High values for Red

lower_green = np.array([0, 150, 0])  # Low values for Green
upper_green = np.array([120, 255, 120])  # High values for Green

lower_blue = np.array([180, 0, 0])  # Low values for Blue
upper_blue = np.array([255, 180, 110])  # High values for Blue

lower_yellow = np.array([0, 170, 170])  # Low values for Blue
upper_yellow = np.array([140, 255, 255])  # High values for Blue

# Open webcam
cap = cv2.VideoCapture(0)

#Initialize Kobuki
# kobuki = Kobuki()


# def turn_right():
#     kobuki.move(160, -80, 0)

# def move_right():
#     kobuki.move(100, 50, 0)

# def turn_left():
#     kobuki.move(-80, 160, 0)

# def move_left():
#     kobuki.move(50, 100, 0)

# def forward():
#     kobuki.move(80, 80, 0)

# def backward():
#     kobuki.move(-80, -80, 0)

# def stop():
#     kobuki.move(0, 0, 0)


def camera(color):
    
    ret, frame = cap.read()
    # Get the dimensions of the frame
    height, width, _ = frame.shape
    print(height, width)

    # Define the middle region (ROI)
    roi_top = 0
    roi_bottom = 7*height//10
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


def find_color(color):

    if  camera(color) < 1:
        return False
    
    else:
        print("stop")
        # stop()
        return True
    

def color_percentages(color):

    ret, frame = cap.read()
    # Get the dimensions of the frame
    height, width, _ = frame.shape
    
    # Define the left region (ROI)
    roi_top1 = 0
    roi_bottom1 = 8*height//10
    roi_left1 = 0
    roi_right1 = width // 2

    roi_top2 = 0
    roi_bottom2 = 8*height//10
    roi_left2 = width // 2
    roi_right2 = width
    
    # Crop the frameof the left region
    roi_frame_left = frame[roi_top1:roi_bottom1, roi_left1:roi_right1]

    # Crop the frame of the right region
    roi_frame_right = frame[roi_top2:roi_bottom2, roi_left2:roi_right2]

    # Calculate total number of pixels
    total_pixels = roi_frame_left.size // 3  # Since it's a color image, divide by 3 (BGR channels)
    
    if color == "red" :
        mask_red1 = cv2.inRange(roi_frame_left, lower_red, upper_red)
        roi_frame_left[mask_red1 > 0] = [0, 0, 255]   # Mark Red regions as Red
        mask_red2 = cv2.inRange(roi_frame_right, lower_red, upper_red)
        roi_frame_right[mask_red2 > 0] = [0, 0, 255]   # Mark Red regions as Red
        red_pixels_left = np.sum(mask_red1 > 0)
        red_pixels_right = np.sum(mask_red2 > 0)
        color_percentage_left = (red_pixels_left / total_pixels) * 100
        color_percentage_right = (red_pixels_right / total_pixels) * 100

    elif color == "green" :
        mask_green1 = cv2.inRange(roi_frame_left, lower_green, upper_green)
        roi_frame_left[mask_green1 > 0] = [0, 255, 0] # Mark Green regions as Green
        mask_green2 = cv2.inRange(roi_frame_right, lower_green, upper_green)
        roi_frame_right[mask_green2 > 0] = [0, 255, 0] # Mark Green regions as Green
        green_pixels_left = np.sum(mask_green1 > 0)
        green_pixels_right = np.sum(mask_green2 > 0)
        color_percentage_left = (green_pixels_left / total_pixels) * 100
        color_percentage_right = (green_pixels_right / total_pixels) * 100

    elif color == "blue" :
        mask_blue1 = cv2.inRange(roi_frame_left, lower_blue, upper_blue)
        roi_frame_left[mask_blue1 > 0] = [255, 0, 0]  # Mark Blue regions as 
        mask_blue2 = cv2.inRange(roi_frame_right, lower_blue, upper_blue)
        roi_frame_right[mask_blue2 > 0] = [255, 0, 0]  # Mark Blue regions as 
        blue_pixels_left = np.sum(mask_blue1 > 0)
        blue_pixels_right = np.sum(mask_blue2 > 0)
        color_percentage_left = (blue_pixels_left / total_pixels) * 100
        color_percentage_right = (blue_pixels_right / total_pixels) * 100
	
    elif color == "yellow" :
        mask_yellow1 = cv2.inRange(roi_frame_left, lower_yellow, upper_yellow)
        roi_frame_left[mask_yellow1 > 0] = [0, 255, 255]  # Mark Blue regions as Blue
        mask_yellow2 = cv2.inRange(roi_frame_right, lower_yellow, upper_yellow)
        roi_frame_right[mask_yellow2 > 0] = [0, 255, 255]  # Mark Blue regions as Blue
        yellow_pixels_left = np.sum(mask_yellow1 > 0)
        yellow_pixels_right = np.sum(mask_yellow2 > 0)
        color_percentage_left = (yellow_pixels_left / total_pixels) * 100
        color_percentage_right = (yellow_pixels_right / total_pixels) * 100

    print(f"{color}_left: {color_percentage_left:.1f}%")
    print(f"{color}_right: {color_percentage_right:.1f}%")

    # Highlight the ROI line by drawing a green rectangle around it
    cv2.line(frame, (width//2, 0), (width//2, 7*height//10), (0, 255, 0), 2)
    cv2.line(frame, (width//7, 7 * height // 10), (6*width//7, 7*height//10), (0, 255, 0), 2)
    cv2.line(frame, (width//7, 8* height // 10), (6*width//7, 8*height//10), (0, 255, 0), 2)
    # Show the frame
    cv2.imshow("Color Detection", frame)
    return color_percentage_left, color_percentage_right


def reach_color(color):

    left, right = color_percentages(color)
    error = round((left - right), 1)
    print(error)

    if abs(error) > 0.3:

        if error > 0:
            print("move left")
            # move_left()

        else:
            print("move right")
            # move_right()

    else:
        print("move forward")
        # forward()

def color_reached(color):
    ret, frame = cap.read()
    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Define the stop region (ROI)
    roi_top = 7 * height // 10
    roi_bottom = 8*height//10
    roi_left = width // 7
    roi_right = 6 * width // 7

    # Crop the frame to the bottom middle region
    roi_frame = frame[roi_top:roi_bottom, roi_left:roi_right]

    # Calculate total number of pixels in the region
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


    if color_percentage > 2:
        time.sleep(2)
        # stop()
        print("stop")
        return True
    else:
        return False


if __name__ == "__main__":

    # forward()
    # time.sleep(2)
    # stop()
    # time.sleep(1)

    # backward()
    # time.sleep(2)
    # stop()
    # time.sleep(1)

    # turn_right()
    # time.sleep(2)
    # stop()
    # time.sleep(1)

    # turn_left()
    # time.sleep(2)
    # stop()
    # time.sleep(1)

    # move_right()
    # time.sleep(2)
    # stop()
    # time.sleep(1)

    # move_left()
    # time.sleep(2)
    # stop()
    # time.sleep(1)

    while not find_color("yellow"):
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("rotate counter clockwise")
        # turn_right()

    while not color_reached("yellow") :
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        reach_color("yellow") 
    
    while not find_color("yellow"):
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("rotate clockwise")
        # turn_right()
        
    while not color_reached("yellow") :
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        reach_color("yellow")

    # backward()
    time.sleep(3) 

# --------------------------------
    while not find_color("green"):
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("rotate clockwise")
        # turn_right()

    while not color_reached("green") :
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        reach_color("green") 
    
    while not find_color("green"):
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("rotate clockwise")
        # turn_right()
        
    while not color_reached("green") :
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        reach_color("green")

    # backward()
    time.sleep(3)


    # --------------------------------
    while not find_color("green"):
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("rotate clockwise")
        # turn_right()

    while not color_reached("green") :
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        reach_color("green") 
    
    while not find_color("green"):
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("rotate clockwise")
        # turn_right()
        
    while not color_reached("green") :
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        reach_color("green")

    # backward()
    time.sleep(3)


    # --------------------------------
    while not find_color("yellow"):
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("rotate clockwise")
        # turn_right()

    while not color_reached("yellow") :
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        reach_color("yellow") 
    
    while not find_color("yellow"):
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("rotate clockwise")
        # turn_right()
        
    while not color_reached("yellow") :
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        reach_color("yellow")

    # backward()
    time.sleep(3)

        
# Release resources
cap.release()
cv2.destroyAllWindows()

