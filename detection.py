import cv2
import numpy as np
import time
import pygame

'''
1. Store First Image
2. Grey Scale
[Done] 3. Start initialization process - 5 secs
[Done] 4. Take video input
[Done] 5. Detect edges - Canny
[Done] 6. Find contours
[Done] 7. Find max radius
[Done] 8. Find center of max radius
[Done] 9. Store max radius and center
[Done] 10. Divide max diameter by 7 - each a note
[Done] 11. End initialization process
12. Find change inside circle compared to previous frame
13. Find note where change is
14. print note
'''

pygame.init()
pygame.mixer.init()

radius_max = 0
center_max = tuple()
width = int()
height = int()
cell_width = int()
cell_array = list()
previous_gray = np.array([])
previous_top_cell = 0


def initializationProcess():
    global radius_max, center_max, width, height, cell_width, previous_gray
    cap = cv2.VideoCapture('video3.mp4')
    t_end = time.time() + 1
    img = cap.read()[1]
    previous_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    temp_previous_img = img
    box_array = list()
    for i in range(500):
        edges = cv2.Canny(img, 100, 200)
        if edges is not None:
            contours, _ = cv2.findContours(
                edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                box_array.append(box)
                cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
        print(box_array[1][1][0] - box_array[0][0][0])
        print(box_array)
        width = box_array[1][1][0] - box_array[0][0][0]
        height = width
        cell_width = width//7
        center_max = box_array[0][0][0] + width//2
        radius_max = width//2

        # cv2.drawContours(img, center_max, radius_max, (0, 255, 0), 2)
        cv2.imshow('img', img)
        cv2.waitKey(0)
        temp_previous_img = img
        img = cap.read()[1]
        if img is None or time.time() > t_end:
            break
    fillCellArray(cell_width, center_max)
    cv2.waitKey(0)
    cap.release()


def fillCellArray(cell_width, center_max):
    global cell_array, previous_gray
    for i in range(7):
        cell_array.append((center_max - radius_max + cell_width*i,
                          center_max - radius_max + cell_width*(i+1)))
    # plot all cells
    for i in range(7):
        cv2.rectangle(previous_gray, (cell_array[i][0], 0),
                      (cell_array[i][1], height), (255, 255, 255), 2)
    cv2.imshow("contours_cell", previous_gray)
    cv2.waitKey(0)
    print(cell_array)


def normalProcedure():
    global previous_gray, previous_top_cell
    cap = cv2.VideoCapture('video3.mp4')
    img = cap.read()[1]
    while (True):
        current_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        delta = cv2.absdiff(previous_gray, current_gray)
        threshold_image = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        previous_gray = current_gray
        cv2.imshow("contours", threshold_image)
        cv2.waitKey(0)
        img = cap.read()[1]

        # store motion level for each cell
        cells = np.array([0, 0, 0, 0, 0, 0, 0])
        cells[0] = cv2.countNonZero(
            threshold_image[0:height, cell_array[0][0]:cell_array[0][1]])
        cells[1] = cv2.countNonZero(
            threshold_image[0:height, cell_array[1][0]:cell_array[1][1]])
        cells[2] = cv2.countNonZero(
            threshold_image[0:height, cell_array[2][0]:cell_array[2][1]])
        cells[3] = cv2.countNonZero(
            threshold_image[0:height, cell_array[3][0]:cell_array[3][1]])
        cells[4] = cv2.countNonZero(
            threshold_image[0:height, cell_array[4][0]:cell_array[4][1]])
        cells[5] = cv2.countNonZero(
            threshold_image[0:height, cell_array[5][0]:cell_array[5][1]])
        cells[6] = cv2.countNonZero(
            threshold_image[0:height, cell_array[6][0]:cell_array[6][1]])

        # obtain the most active cell
        top_cell = np.argmax(cells)

        # return the most active cell, if threshold met
        if (cells[top_cell] >= 2000):
            pygame.mixer.Sound(str(top_cell)+'.wav').play()
            previous_top_cell = top_cell
        if img is None:
            break


initializationProcess()
# print("Initialization Complete")
normalProcedure()
