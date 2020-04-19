import mmcv
import cv2
import os
import numpy as np
import os.path as osp
from skimage.measure import label
from scipy.ndimage import filters
from skimage.filters import scharr
from skimage.segmentation import flood, flood_fill
from cv2 import Canny

NO_FIGURE_PIXEL_NUM_THRESHOLD = 1000
GRADIENT_LINE_LENGTH_FOR_VIS = 50



INPUT_PATH = '/yuanProject/CAMIOT/fingure_data'
OUTPUT_PATH = '/yuanProject/CAMIOT/fingure_data_results'


mmcv.mkdir_or_exist(OUTPUT_PATH)

for item in os.listdir(INPUT_PATH):
    if '.jpg' in item:
        image = cv2.imread(osp.join(INPUT_PATH, item))
        imageYCrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)

        # skin detection
        min_YCrCb = np.array([0, 133, 77], np.uint8)
        max_YCrCb = np.array([255, 173, 127], np.uint8)
        skinRegionYCrCb = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)

        # preprocessing
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        skinRegionYCrCb = cv2.erode(skinRegionYCrCb, kernel, iterations=2)
        skinRegionYCrCb = cv2.dilate(skinRegionYCrCb, kernel, iterations=2)
        skinRegionYCrCb = cv2.GaussianBlur(skinRegionYCrCb, (3, 3), 0)

        # largest island
        skinRegionYCrCb = label(skinRegionYCrCb)
        skinRegionYCrCb = skinRegionYCrCb == np.argmax(np.bincount(skinRegionYCrCb.flat)[1:]) + 1

        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_debug_mask.jpg'.format(item.split('.')[0], 'skin')), cv2.bitwise_and(image, image, mask=np.uint8(skinRegionYCrCb)))

        # get a starting point
        points_x, points_y = np.where(skinRegionYCrCb == 1)
        if len(points_x) == 0 or len(points_y) == 0:
            print('no finger detected.')
            continue
        # selected_x = points_x[np.argmax(points_x)]
        # selected_y = points_y[np.argmax(points_x)]
        img_certer = (image.shape[0]//2, image.shape[0]//2)
        selected_x = -1
        selected_y = -1
        cur_min = 999999
        for per_points_x, per_points_y in zip(points_x, points_y):
            if (per_points_x-img_certer[0])*(per_points_x-img_certer[0]) + (per_points_y-img_certer[1])*(per_points_y-img_certer[1]) < cur_min:
                cur_min = (per_points_x-img_certer[0])*(per_points_x-img_certer[0]) + (per_points_y-img_certer[1])*(per_points_y-img_certer[1])
                selected_x = per_points_x
                selected_y = per_points_y
        #
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_debug_selected_point.jpg'.format(item.split('.')[0], 'skin')),
        #             cv2.circle(cv2.bitwise_and(image, image, mask=np.uint8(skinRegionYCrCb)), (selected_y, selected_x), 8, 255, 2))

        # flooding
        image = image.astype('int32')
        image_sobel_x = filters.sobel(image, axis=0).astype(np.float32)
        image_sobel_y = filters.sobel(image, axis=1).astype(np.float32)
        image_sobel = image_sobel_x * image_sobel_x + image_sobel_y * image_sobel_y
        image_sobel *= 255.0 / np.max(image_sobel)
        image_sobel = (image_sobel[:, :, 0] + image_sobel[:, :, 1] + image_sobel[:, :, 2]) / 3.0
        image_sobel = flood(image_sobel, (selected_x, selected_y), tolerance=0.2)
        if np.count_nonzero(image_sobel) <= NO_FIGURE_PIXEL_NUM_THRESHOLD:
            print('no finger detected.')
            continue

        # another filter
        image = image.astype('uint8')
        image_canny_filter = Canny(image=image, threshold1=12, threshold2=24)
        image_canny_filter = (image_canny_filter < 100).astype(np.int32)
        image_canny_filter_left = np.roll(image_canny_filter, 1, axis=0)
        image_canny_filter_right = np.roll(image_canny_filter, -1, axis=0)
        image_canny_filter_up = np.roll(image_canny_filter, 1, axis=1)
        image_canny_filter_down = np.roll(image_canny_filter, -1, axis=1)
        image_sobel = image_sobel * image_canny_filter * image_canny_filter_left * image_canny_filter_right * image_canny_filter_up * image_canny_filter_down

        # largest island
        image_sobel = label(image_sobel)
        image_sobel = image_sobel == np.argmax(np.bincount(image_sobel.flat)[1:]) + 1

        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_canny_as_filter.jpg'.format(item.split('.')[0], 'skin')), image_canny_filter)

        # postprocessing
        image_sobel = image_sobel.astype(np.uint8)
        # kernel = np.ones((2,2),np.uint8)
        # image_sobel = cv2.erode(image_sobel, kernel, iterations=3)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
        image_sobel = cv2.dilate(image_sobel, kernel, iterations=2)
        image_sobel = cv2.GaussianBlur(image_sobel, (3, 3), 0)
        image_sobel = image_sobel.astype(np.int32)
        # image_sobel = cv2.circle(image_sobel, (selected_y, selected_x), 8, 255, 2)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_flood_mask_new.jpg'.format(item.split('.')[0], 'skin')), image_sobel * 255)

        # laplace
        # image = image.astype('uint8')
        # image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # image_laplace = cv2.Laplacian(image_gray, cv2.CV_64F)
        # image_laplace = image_laplace.astype(np.float32)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_lap_mask.jpg'.format(item.split('.')[0], 'skin')), image_laplace)
        # image_laplace = 255.0 * (image_laplace - np.min(image_laplace)) / (np.max(image_laplace) - np.min(image_laplace))
        # image_laplace = flood(image_laplace, (selected_x, selected_y), tolerance=3.5)
        # image_laplace = image_laplace.astype(np.int32)
        # image_laplace = image_laplace * 255
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_lap_flood_mask.jpg'.format(item.split('.')[0], 'skin')), image_laplace)

        # scharr
        # image = image.astype(np.uint8)
        # image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # image_scharr = scharr(image_gray).astype(np.float32)
        # image_scharr = 255.0 * image_scharr / np.max(image_scharr)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_scharr_mask.jpg'.format(item.split('.')[0], 'skin')), image_scharr)
        # image_scharr = flood(image_scharr, (selected_x, selected_y), tolerance=2.5)
        # image_scharr = image_scharr.astype(np.int32)
        # image_scharr = image_scharr * 255
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_flood_scharr_mask.jpg'.format(item.split('.')[0], 'skin')), image_scharr)

        # image_laplace = filters.laplace(image).astype(np.float32)
        # image_laplace *= 255.0 / np.max(image_laplace)



        # canny
        # image_canny_1 = Canny(image=image, threshold1=100, threshold2=200)
        # image_canny_2 = Canny(image=image, threshold1=50, threshold2=100)
        # image_canny_3 = Canny(image=image, threshold1=25, threshold2=50)
        # image_canny_4 = Canny(image=image, threshold1=12, threshold2=24)
        # image_canny_5 = Canny(image=image, threshold1=6, threshold2=12)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_canny_1.jpg'.format(item.split('.')[0], 'skin')), image_canny_1)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_canny_2.jpg'.format(item.split('.')[0], 'skin')), image_canny_2)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_canny_3.jpg'.format(item.split('.')[0], 'skin')), image_canny_3)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_canny_4.jpg'.format(item.split('.')[0], 'skin')), image_canny_4)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_canny_5.jpg'.format(item.split('.')[0], 'skin')), image_canny_5)


        # skinYCrCb = cv2.bitwise_and(image, image, mask=np.uint8(cat_nose))
        #
        #
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_new.jpg'.format(item.split('.')[0], 'skin')), skinYCrCb)

        # lower = np.array([0, 48, 80], dtype="uint8")
        # upper = np.array([20, 255, 255], dtype="uint8")
        # converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # skinMask = cv2.inRange(converted, lower, upper)
        # skin = cv2.bitwise_and(image, image, mask=skinMask)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}.jpg'.format(item.split('.')[0], 'newskin')), skin)

        # image = image.astype('int32')
        # cat_sobel_x = filters.sobel(image, axis=0)
        # cat_sobel_y = filters.sobel(image, axis=1)
        # mag = np.hypot(cat_sobel_x, cat_sobel_y)
        # mag *= 255.0 / np.max(mag)
        # cat_sobel = cat_sobel_x^2 + cat_sobel_y^2
        # print(cat_sobel.shape)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}.jpg'.format(item.split('.')[0], 'sobel')), cat_sobel)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}.jpg'.format(item.split('.')[0], 'sobel0')), cat_sobel[:, :, 0])
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}.jpg'.format(item.split('.')[0], 'sobel1')), cat_sobel[:, :, 1])
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}.jpg'.format(item.split('.')[0], 'sobel2')), cat_sobel[:, :, 2])
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}.jpg'.format(item.split('.')[0], 'sobelall')), (cat_sobel[:, :, 0]+cat_sobel[:, :, 1]+cat_sobel[:, :, 2])/3.0)

        # get directions
        # get mid points
        image_sobel_copy = np.zeros_like(image_sobel)
        points_x, points_y = np.where(image_sobel == 1)
        top_line_index = np.max(points_x)
        bot_line_index = np.min(points_x)
        mid_line_index = (top_line_index + bot_line_index) // 2
        line_length = top_line_index - bot_line_index + 1 - 6
        top_line_index = mid_line_index - line_length // 2
        bot_line_index = mid_line_index + line_length // 2
        mid_points = []
        for i in range(top_line_index, bot_line_index+1):
            y_coordinates = np.where(image_sobel[i, :] == 1)
            mid_points.append((i, np.mean(y_coordinates).astype(np.int32)))
        #     cv2.circle(image_sobel_copy, (np.mean(y_coordinates).astype(np.int32), i), 8, 255, 2)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_mid_points.jpg'.format(item.split('.')[0], 'skin')), image_sobel_copy)
        # cv2.circle(image_sobel, (int(np.mean([item[1] for item in mid_points])), int(np.mean([item[0] for item in mid_points]))), 8, 2, 2)
        # cv2.imwrite(osp.join(OUTPUT_PATH, '{}_{}_average_mid_points.jpg'.format(item.split('.')[0], 'skin')), image_sobel * 100)

        mid_gradients = []
        # get gradient
        for i in range(0, line_length // 2):
            mid_gradients.append(
                np.arcsin(
                    (mid_points[i+line_length//2+1][1] - mid_points[i][1]).astype(np.float32)
                    /
                    np.math.sqrt(np.math.pow((mid_points[i+line_length//2+1][1]-mid_points[i][1]+1).astype(np.float32), 2.0)+np.math.pow(line_length//2+2, 2.0))
                ) / np.pi * 180.0
            )
        if len(mid_gradients) == 0:
            print('no finger detected.')
            continue
        average_mid_gradient = np.mean(mid_gradients)
        start_point = (int(np.mean([item[1] for item in mid_points])), int(np.mean([item[0] for item in mid_points])))
        end_point = (int(start_point[0]+GRADIENT_LINE_LENGTH_FOR_VIS * np.sin(average_mid_gradient * np.pi / 180.0)), int(start_point[1]+GRADIENT_LINE_LENGTH_FOR_VIS * np.cos(average_mid_gradient * np.pi / 180.0)))
        cv2.line(image_sobel, start_point, end_point, 2, 2)
        cv2.imwrite(osp.join(OUTPUT_PATH, '{}_seg_and_gradient.jpg'.format(item.split('.')[0])), image_sobel * 100)
















