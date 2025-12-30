import cv2
import numpy as np

def apply_color_filter(image, filter_type):
    filtered_image = image.copy()
    
    if filter_type == 'red_tint':
        filtered_image[:, :, 1] = filtered_image[:, :, 0] = 0
    
    elif filter_type == 'green_tint':
        filtered_image[:, :, 0] = filtered_image[:, :, 2] = 0
        
    elif filter_type == 'blue_tint':
        filtered_image[:, :, 1] = filtered_image[:, :, 2] = 0
        
    elif filter_type == 'sobel':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobelX = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3) #1 is x 0 is y
        sobelY = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3) #all float numbers up to 64 bits
        bit = cv2.bitwise_or(sobelX.astype("uint8"), sobelY.astype("uint8")) #uint8 converts integers up to 8 bits
        filtered_image = cv2.cvtColor(bit, cv2.COLOR_GRAY2BGR)
       
    elif filter_type == 'canny':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny_edges = cv2.Canny(gray, 100, 200)
        filtered_image = cv2.cvtColor(canny_edges, cv2.COLOR_GRAY2BGR)
        
    elif filter_type == 'cartoon':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(image, 9, 300, 300)
        bit = cv2.bitwise_and(color, color, mask=edges)
        filtered_image = bit
        
    elif filter_type == 'original':
        filtered_image = image.copy()
        
    return filtered_image

def main():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open video.")
        return
    filter_type = 'original'
    print("r = red_tint")
    print("b = blue_tint")
    print("g = green_tint")
    print("s = sobel")
    print("c = canny")
    print("t = cartoon")
    print("q = quit")
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        filtered_frame = apply_color_filter(frame, filter_type)
        cv2.imshow('Video Filter', filtered_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            filter_type = 'red_tint'
        elif key == ord('g'):
            filter_type = 'green_tint'
        elif key == ord('b'):
            filter_type = 'blue_tint'
        elif key == ord('s'):
            filter_type = 'sobel'
        elif key == ord('c'):
            filter_type = 'canny'
        elif key == ord('t'):
            filter_type = 'cartoon'
        elif key == ord('q'):
            break
        
    video_capture.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()