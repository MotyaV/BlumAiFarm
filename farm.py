import pyautogui
from ultralytics import YOLO
import cv2
import time
import numpy as np
import mouse
import win32gui
import win32con
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model = YOLO("best.pt").to(device)

screen_width, screen_height = pyautogui.size()
center_x, center_y = screen_width // 2, screen_height // 2
region_width, region_height = 380, 650
region_left = center_x - region_width // 2
region_top = center_y - region_height // 2

def get_center(x1, y1, x2, y2):
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return center_x, center_y

def click_on_object(results):
    click_position = None
    for result in results:
        if len(result.boxes) > 3:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                confidence = box.conf.item()
                label = box.cls.item()
                print(f"Label: {label}, Confidence: {confidence}")
            
                if label == 1: 
                    click_position = get_center(x1, y1, x2, y2)
            
                if label == 2:
                    center_x, center_y = get_center(x1, y1, x2, y2)
                    click_position = (center_x, center_y - 10)

            if click_position:
                x = region_left + click_position[0]
                y = region_top + click_position[1]
                mouse.move(x, y, absolute=True)
                mouse.click(button=mouse.LEFT)
                click_position = None

cv2.namedWindow("Put blumapp here", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Put blumapp here", region_width, region_height)
print("Put blum app in the window. Don't move the window. Then press any key to start")
hwnd = win32gui.FindWindow(None, "Put blumapp here")
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, 0, int(255 * 0.5), win32con.LWA_ALPHA)
cv2.imshow("Put blumapp here", np.zeros((region_height, region_width, 3), dtype=np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()
print("Started. Wait for YOLO model to load")

#main loop
while True:
    screenshot = pyautogui.screenshot(region=(region_left, region_top, region_width, region_height))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    results = model(screenshot, stream=True, conf=0.8)
    click_on_object(results)
    cv2.waitKey(1)
    time.sleep(0.005)

cv2.destroyAllWindows()
