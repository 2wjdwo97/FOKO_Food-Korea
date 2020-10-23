from PIL import Image, ImageEnhance
import cv2
import numpy as np
import pytesseract
from matplotlib import pyplot as plt
from ocr.tet import runCRAFT


def crop(img_to_crop, arr):
    # assume coord is a list with 8 float values, the points of the rectangle area should
    # have be clockwise
    x1, y1, x2, y2, x3, y3, x4, y4 = arr
    cnt = [[[int(x1), int(y1)], [int(x2), int(y2)], [int(x3), int(y3)], [int(x4), int(y4)]]]
    # cv2.drawContours(img, [cnt], 0, (128, 255, 0), 3)
    # find the rotated rectangle enclosing the contour
    # rect has 3 elements, the first is rectangle center, the second is
    # width and height of the rectangle and the third is the rotation angle
    minX = img_to_crop.shape[1]
    maxX = -1
    minY = img_to_crop.shape[0]
    maxY = -1
    for point in cnt[0]:
        x = point[0]
        y = point[1]
        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y

    # Go over the points in the image if thay are out side of the emclosing rectangle put zero
    # if not check if thay are inside the polygon or not
    cropedImage = np.zeros_like(img_to_crop)
    for y in range(0, img_to_crop.shape[0]):
        for x in range(0, img_to_crop.shape[1]):

            if x < minX or x > maxX or y < minY or y > maxY:
                continue

            if cv2.pointPolygonTest(np.asarray(cnt), (x, y), False) >= 0:
                cropedImage[y, x] = img_to_crop[y, x]
                cropedImage[y, x] = img_to_crop[y, x]
                cropedImage[y, x] = img_to_crop[y, x]

    # Now we can crop again just the envloping rectangle
    im_crop = cropedImage[minY:maxY, minX:maxX]

    # Now strectch the polygon to a rectangle. We take the points that
    polygonStrecth = np.float32(
        [[0, 0], [im_crop.shape[1], 0], [im_crop.shape[1], im_crop.shape[0]], [0, im_crop.shape[0]]])

    # Convert the polygon corrdanite to the new rectnagle
    polygonForTransform = np.zeros_like(polygonStrecth)

    index = 0
    for point in cnt[0]:
        x = point[0]
        y = point[1]

        newX = x - minX
        newY = y - minY

        polygonForTransform[index] = [newX, newY]
        index += 1

    # Find affine transform
    M = cv2.getPerspectiveTransform(np.asarray(polygonForTransform).astype(np.float32),
                                    np.asarray(polygonStrecth).astype(np.float32))

    # Warp one image to the other
    warpedImage = cv2.warpPerspective(im_crop, M, (im_crop.shape[1], im_crop.shape[0]))

    # cv2.imshow('crop', im_crop)
    # cv2.waitKey(0)
    # cv2.imshow('warped', warpedImage)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return warpedImage

def runOCR(orig_img):
    menu_list = list()
    # orig_img = Image.open('C:/Users/LG/Desktop/testImages/legend.PNG')

    # run CRAFT
    text_region = runCRAFT(orig_img)
    arr_text_region = text_region.splitlines()
    for i in range(len(arr_text_region)):
        arr_text_region[i] = arr_text_region[i].split(',')

    # print(arr_text_region)
    img = np.asarray(orig_img.convert('L'))  # Image to cv2

    # Crop image and run Tesseract
    for i in range(len(arr_text_region)):
        crop_img = crop(img, arr_text_region[i])
#        ret3, th1 = cv2.threshold(crop_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # reverse RGB if characters are white
#        if int(th1[0, 0]) == 0:
#            th1 = cv2.bitwise_not(th1)

        # cv2.imshow('crop', crop_img)
        # cv2.waitKey(0)
        # cv2.imshow('th1', th1)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        custom_oem_psm_config = r'--oem 3 --psm 7'
        result = pytesseract.image_to_string(crop_img, lang='kor', config=custom_oem_psm_config)
        menu_list.append(result.replace('\n', '').replace('\x0c', ''))

    return menu_list

#    for i in range(len(menu_list)):
#        print(f"{arr_text_region[i]}")
#        print(f"{menu_list[i]}")
#        print()

    # imgfile = Image.open('C:/Users/LG/Desktop/testImages/test4_carft2.jpg')
    # imgfile = image_smoothening(imgfile)
    # img1 = cv2.imread('C:/Users/LG/Desktop/testImages/test4_carft2.jpg', 0)
    # ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
