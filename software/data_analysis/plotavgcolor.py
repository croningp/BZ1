from generate_dataset import GridClickData
from generate_dataset import bz_average_color

import matplotlib.pyplot as plt
from collections import deque
import numpy as np
import cv2

def plot_average_color(video):

    vc = cv2.VideoCapture(video)
    click_grid = GridClickData()

    frame_colors = []
    pixel_colors = []
    window_color = []
    deque_color = deque(maxlen=200)

    while(True):

        ret,frame = vc.read()

        if ret is False:
            break

        if click_grid.finished is False:
            click_grid.get_platform_corners(frame, "avg_color_calculator")

        avg_c = bz_average_color(frame, click_grid.points)

        deque_color.append(avg_c)
        window_c = np.average(deque_color, axis=0).astype('float32')
        window_color.append(window_c)

        frame_colors.append(avg_c)
        pixel_colors.append(frame[430,430])

frame_colors = np.array(frame_colors)
pixel_colors = np.array(pixel_colors)
window_colors = np.array(window_color)

plt.plot(frame_colors[:,0], "b-")
plt.plot(frame_colors[:,1], "g-")
plt.plot(frame_colors[:,2], "r-")
plt.ylabel('RGB intensity')
plt.xlabel('Time')

plt.plot(window_colors[:,0], "b-")
plt.plot(window_colors[:,1], "g-")
plt.plot(window_colors[:,2], "r-")
plt.ylabel('RGB intensity')
plt.xlabel('Time')

rectified = frame_colors - window_colors

plt.plot(frame_colors[:,0], "b-")
plt.plot(rectified[:,0], "b-")

plt.plot(frame_colors[:,2], "r-")
plt.plot(rectified[:,2], "r-")
