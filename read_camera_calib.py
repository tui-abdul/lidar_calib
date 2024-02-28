import yaml
import numpy as np

def camera_calib(file):
    with open(file, 'r') as file:
        calib = yaml.safe_load(file)
    #print(calib['camera_matrix']['data'])
    #print(calib['distortion_coefficients']['data']  )
    mat_intrinsic =  np.array(calib['camera_matrix']['data']).reshape(3,3)
    #print(mat_intrinsic.shape)
    dist_coeffs = np.array(calib['distortion_coefficients']['data'])

    return mat_intrinsic , dist_coeffs

#camera_calib('ost.yaml')