import cv2
import numpy as np
import math
import random
import time

angle = random.uniform(0, 2 * math.pi)

# Window
window_name = 'Moving Circle'
cv2.namedWindow(window_name)
window_size = (1000, 1000)
window_size_x, window_size_y = window_size
background = np.zeros((window_size_x, window_size_y, 3), dtype=np.uint8)

class EyeTrackingDot: 
    def __init__(self, radius, speed, angle_range) -> None:

        # Properties
        self.radius = radius
        self.color = (255, 255, 255)

        # Position
        self.x = window_size_x // 2
        self.y = window_size_y // 2

        # Direction
        self.direction = random.uniform(0, 2 * math.pi)
        self.angle_range = angle_range/2

        # Speed
        self.speed = speed 
        self.padding = 10 + self.radius
        self.pause_flag = False

    def reset(self) -> None:
        self.x = window_size_x// 2
        self.y = window_size_y // 2
        self.angle = random.uniform(0, 2 * math.pi)

    def update_position(self) -> None:

        if self.pause_flag:
            return

        # New Position
        new_direction = self.direction + math.radians(random.uniform(-self.angle_range, self.angle_range))
        x_step = self.speed * math.cos(new_direction)
        y_step = self.speed * math.sin(new_direction)
        x_step, y_step = self.valid_position(x_step, y_step)

        # Update direction
        self.direction =  math.atan2(y_step, x_step)

        # Update position
        self.x += int(x_step)
        self.y += int(y_step)
        # self.log()
    
    def valid_position(self, x_step, y_step) -> None:

        # Left
        if self.x <= self.padding:
            x_step += self.speed *(self.padding-self.x)

        # Right
        elif self.x >= window_size[0] - self.padding:
            x_step -= self.speed

        # Top
        if self.y <= self.padding:
            y_step += self.speed
            
        # Bottom
        elif self.y >= window_size[1] - self.padding:
            y_step -= self.speed
        
        return x_step, y_step
    
    def log(self) -> None:
        print(f"Direction: {self.direction}")
        print(f"Step: {self.x}, {self.y}")

    def pause(self) -> None:
        self.pause_flag = not self.pause_flag


def eye_tracking_animation():
    slow_mode = False
    circle = EyeTrackingDot(10, 5, 30)

    while True:

        # Clear screen
        background.fill(0)

        # Draw circle 
        circle.update_position()
        cv2.circle(background, (circle.x, circle.y), circle.radius, circle.color, -1)

        # Draw image
        cv2.imshow(window_name, background)

        time.sleep(0.2*slow_mode)
            
        # Button Interrupts
        key = cv2.waitKey(30)

        # 'q': Exit
        if key == ord('q'):  
            break

        # Press 'q' to exit
        if key == ord('w'): 
            slow_mode = not slow_mode 
        
        # 'Enter': Reset
        elif key == 13:  
            circle.reset()

        # 'Space': Pause
        if key == 32: 
            circle.pause()


    # Release resources and close the window
    cv2.destroyAllWindows()

eye_tracking_animation()
