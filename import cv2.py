import cv2
 
#Load the image
image = cv2.imread("C:/Users/KlodiShpetimi/Pictures/cat.jpg")

#Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #cvt means convert

#Resize the window to a specific size without resizing the image
cv2.namedWindow('Loaded Image', cv2.WINDOW_NORMAL) #Create resizable window
cv2.resizeWindow('Loaded Image', 800, 500) #Set the window size (width*height)

#Display the image in the resized window
cv2.imshow('Loaded Image', gray_image)
cv2.waitKey(0) #Wait for a key to press #Zero means it will wait for any milisecond
cv2.destroyAllWindows() #Close the window

#Print image properties
print(f"Image Dimentions: {image.shape}") #height, Width, Channels 
#you can add variable with f string
