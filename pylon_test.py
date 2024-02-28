'''
A simple Program for grabing video from basler camera and converting it to opencv img.
Tested on Basler acA1300-200uc (USB3, linux 64bit , python 3.5)

'''
from pypylon import pylon
import cv2
import numpy as np
from read_txt import format_lidar_data
from read_camera_calib import camera_calib
from convert_t_cam import t_cam
from translate_image import proj_image, process_lidar_data
def access_camera():


    # conecting to the first available camera
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
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            pattern_size = (5, 7)  # Change this according to your checkerboard

            # Find the corners of the checkerboard
            ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
            cv2.drawChessboardCorners(gray, pattern_size, corners, ret)
            cv2.namedWindow('title', cv2.WINDOW_NORMAL)

            cv2.imshow('title', gray)
            # Accessing top-left corner
            top_left_corner = corners[0,:]

            # Accessing top-right corner
            top_right_corner = corners[4,:]

            # Accessing bottom-left corner
            bottom_left_corner = corners[30,:] 

            # Accessing bottom-right corner
            bottom_right_corner = corners[34,:] 
            k = cv2.waitKey(1)
            if k == 27:
                break
        grabResult.Release()
    #print("top_left_corner",top_left_corner)
    #print("top_right_corner",top_right_corner)
    #print("bottom_left_corner",bottom_left_corner)
    #print("bottom_right_corner",bottom_right_corner)
    # Releasing the resource    
    camera.StopGrabbing()

    cv2.destroyAllWindows()

    return corners

def calculate_ext_param(objectPoints,imagePoints,mat_intrinsic,dist_coeffs):

    success, rvec, tvec, inliers, = cv2.solvePnPRansac(objectPoints,imagePoints,mat_intrinsic,dist_coeffs)

    return success, rvec, tvec, inliers

if __name__ == "__main__":
    corners = access_camera()
    corners = np.reshape(corners, (35, 2))
    #print(corners.shape)
    mat_intrinsic,dist_coeffs = camera_calib('ost.yaml')
   
    #mat_intrinsic = np.array( [ [1537.394467, 0.000000, 1183.173109],[0.000000, 1529.572552, 592.352286],[0.000000, 0.000000, 1.00000]]  )
    #dist_coeffs = np.array([0.003822, -0.014384, 0.001954, 0.025222, 0.000000], dtype=np.float32) # the image is already rectified
    
    #objectPoints = np.array([[1.21,1.43,0.18],[1.58,0.49,-0.22],[1.72,0.37,-0.15],[2.0,0.0,0.24],[1.34,-0.71,-0.21],[1.29,-0.87,-0.17]],dtype="float32")
    #objectPoints = np.array([[1.3748879432678223, -0.20816142857074738,  0.016405373811721802],[1.2905548810958862,0.11999906599521637, 0.3645657002925873],[1.2909877300262451 , 0.0757225900888443 , 0.26947978138923645],[ 1.3125885725021362 , 0.028771057724952698 , 0.18996796011924744],[ 1.3149960041046143  , -0.01846848428249359 , 0.11061904579401016],[1.3323179483413696 ,-0.07065974175930023 , 0.031791482120752335],[ 1.273952603340149 , 0.20255233347415924 ,0.3154390752315521],[ 1.2662569284439087 , 0.1481959968805313 , 0.23378601670265198],[ 1.2851654291152954  , 0.10655136406421661  , 0.14330372214317322],[ 1.2951453924179077  , 0.05655963718891144  , 0.06427953392267227],[1.3748879432678223, -0.20816142857074738,  0.016405373811721802],[1.2905548810958862,0.11999906599521637, 0.3645657002925873],[1.2909877300262451 , 0.0757225900888443 , 0.26947978138923645],[ 1.3125885725021362 , 0.028771057724952698 , 0.18996796011924744],[ 1.3149960041046143  , -0.01846848428249359 , 0.11061904579401016],[1.3323179483413696 ,-0.07065974175930023 , 0.031791482120752335],[ 1.273952603340149 , 0.20255233347415924 ,0.3154390752315521],[ 1.2662569284439087 , 0.1481959968805313 , 0.23378601670265198],[ 1.2851654291152954  , 0.10655136406421661  , 0.14330372214317322],[ 1.2951453924179077  , 0.05655963718891144  , 0.06427953392267227],[1.3748879432678223, -0.20816142857074738,  0.016405373811721802],[1.2905548810958862,0.11999906599521637, 0.3645657002925873],[1.2909877300262451 , 0.0757225900888443 , 0.26947978138923645],[ 1.3125885725021362 , 0.028771057724952698 , 0.18996796011924744],[ 1.3149960041046143  , -0.01846848428249359 , 0.11061904579401016],[1.3323179483413696 ,-0.07065974175930023 , 0.031791482120752335],[ 1.273952603340149 , 0.20255233347415924 ,0.3154390752315521],[ 1.2662569284439087 , 0.1481959968805313 , 0.23378601670265198],[ 1.2851654291152954  , 0.10655136406421661  , 0.14330372214317322],[ 1.2951453924179077  , 0.05655963718891144  , 0.06427953392267227],[1.3748879432678223, -0.20816142857074738,  0.016405373811721802],[1.2905548810958862,0.11999906599521637, 0.3645657002925873],[1.2909877300262451 , 0.0757225900888443 , 0.26947978138923645],[ 1.3125885725021362 , 0.028771057724952698 , 0.18996796011924744],[ 1.3149960041046143  , -0.01846848428249359 , 0.11061904579401016]])
    objectPoints = format_lidar_data('data.txt')
    #print("objectPoints",objectPoints.shape)
    imagePoints = np.array(corners)
    #print(imagePoints.shape)


    success, rvec, tvec, inliers = calculate_ext_param(objectPoints,imagePoints,mat_intrinsic,dist_coeffs)
    print(success, rvec.shape, tvec.shape, inliers.shape)
    p_cam_to_lidar = t_cam(rvec, tvec)
    points_2d = process_lidar_data(objectPoints, rvec, tvec, mat_intrinsic, dist_coeffs)
    proj_image(points_2d)
    
    