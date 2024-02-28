import numpy as np
import cv2
from pypylon import pylon

def process_lidar_data(objectPoints, rvec, tvec, mat_intrinsic, dist_coeffs):
    points_2D, _ = cv2.projectPoints(objectPoints,rvec,tvec,mat_intrinsic , dist_coeffs)
    return points_2D

def proj_image(points_2D):

    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray()
            #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #gray = img
            #projection_matrix = projection_matrix[:3, :3].astype(np.float32)
            #image_translated = cv2.warpPerspective(gray, projection_matrix, (gray.shape[1], gray.shape[0]))
            for k in range(len(points_2D)):
                x,y = points_2D[k][0][0].astype(int),points_2D[k][0][1].astype(int)
                if 0<x<len(img[0]) and 0<y<len(img[1]):
                    cv2.circle(img, (x,y), 6,  (255, 0, 0), -1)
            #cv2.imshow("Calibration", img)
            cv2.waitKey(1)
            cv2.namedWindow('title', cv2.WINDOW_NORMAL)
            cv2.imshow("title", img)
            k = cv2.waitKey(1)
            if k == 27:
                break
        grabResult.Release()
    
    camera.StopGrabbing()

    cv2.destroyAllWindows()