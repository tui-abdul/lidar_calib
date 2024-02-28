import numpy as np
import cv2

def t_cam(rvec, tvec):
    R_lidar_to_camera, _ = cv2.Rodrigues(rvec)

    # Compose transformation matrix T (LIDAR to camera)
    T_lidar_to_camera = np.eye(4)
    T_lidar_to_camera[:3, :3] = R_lidar_to_camera
    
    T_lidar_to_camera[:3, 3] = tvec.flatten()
    #print('T_lidar_to_camera',T_lidar_to_camera)
    # Invert T to get camera to LIDAR transformation
    T_camera_to_lidar = np.linalg.inv(T_lidar_to_camera)

    # Projection matrix from camera to LIDAR
    # Projection matrix from camera to LIDAR
    #P_camera_to_lidar = np.vstack((T_camera_to_lidar[:3], [0, 0, 0, 1]))

    print("Projection Matrix (LIDAR to Camera):\n", T_lidar_to_camera)

    return T_lidar_to_camera