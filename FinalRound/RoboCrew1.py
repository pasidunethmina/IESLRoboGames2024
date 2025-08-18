import time
from kobukidriver import Kobuki  # Assuming the provided class is saved in kobuki_control.py

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

if __name__ == "__main__":
    main()
