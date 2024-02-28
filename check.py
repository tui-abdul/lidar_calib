from checkerboard import detect_checkerboard
import cv2
import numpy as np
#pixels per cm (ppc)
ppc = 4000

box_cm = 95.0 / 10.0


# Load an image from file
image = cv2.imread('/home/abd1340m/Dokumente/pointcloud/frame0000.jpg')
#image =  cv2.resize(image, (0,0), fx=0.5, fy=0.5)
if image is not None:
    # Display the image
    cv2.imshow('Image', image)
    cv2.waitKey(0)  # Wait for any key to be pressed
    cv2.destroyAllWindows()  # Close all OpenCV windows
else:
    print("Image not found or unable to load.")

 
#size = (8, 6) # size of checkerboard
#image = "frame0000.jpg" # obtain checkerboard
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


pattern_size = (5, 7)  # Change this according to your checkerboard

# Find the corners of the checkerboard
ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
if ret:
    # Draw the corners on the image
    cv2.drawChessboardCorners(image, pattern_size, corners, ret)

    # Display the image with detected corners
    cv2.imshow('Checkerboard', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Checkerboard pattern not found.")

corners = np.reshape(corners, (35, 2))

print(corners.shape)

# Accessing top-left corner
top_left_corner = corners[0,:]

# Accessing top-right corner
top_right_corner = corners[4,:]

# Accessing bottom-left corner
bottom_left_corner = corners[30,:] 

# Accessing bottom-right corner
bottom_right_corner = corners[34,:] 


def cm_to_pixel(cm):
    # 196 is th value of pixel from left vertix to right vertix
    x = top_left_corner[0] - top_right_corner[0]
    y = (abs(x) / 4.0) / box_cm
    return y*cm

print(top_left_corner[0] )

top_left_corner_u = [[] ,[]] 
top_right_corner_u = [[] ,[]] 
bottom_left_corner_u = [[] ,[]] 
bottom_right_corner_u = [[] ,[]] 

top_left_corner_u[0] = top_left_corner[0] - cm_to_pixel(11.5)
top_left_corner_u[1] = top_left_corner[1] - cm_to_pixel(14)


top_right_corner_u[0] = top_right_corner[0] + cm_to_pixel(11.5)
top_right_corner_u[1] = top_right_corner[1] - cm_to_pixel(14)

bottom_left_corner_u[0] = bottom_left_corner[0] - cm_to_pixel(11.5)
bottom_left_corner_u[1] = bottom_left_corner[1] + cm_to_pixel(14.5)

bottom_right_corner_u[0] = bottom_right_corner[0] + cm_to_pixel(11)
bottom_right_corner_u[1] = bottom_right_corner[1] + cm_to_pixel(15)


print("top_left_corner",top_left_corner_u)
print("top_right_corner",top_right_corner_u)
print("bottom_left_corner",bottom_left_corner_u)
print("bottom_right_corner",bottom_right_corner_u)




#corners, score = detect_checkerboard(image, size)

#print(corners)
#print(score)
