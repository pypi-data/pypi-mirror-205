"""Main module."""
import os
import cv2
import numpy as np


class SahFilters:
    def __init__(self, image_path=None):
        self._image_path = None
        self.set_image_path(image_path)

    def set_image_path(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            if not os.path.exists(image_path):
                print("Image file not found")
            else:
                print("Invalid image format")
        else:
            self._image_path = image_path

    def get_image_path(self):
        return self._image_path

    def light_sketch(self):
        if self._image_path is None:
            print("No image loaded")
            return

        
        image = cv2.imread(self._image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 30, 300)
        edged = 255 - edged

        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        edged = cv2.filter2D(edged, -1, kernel)
        
        precision = 0.6
        recall = 0.6
        
        threshold = precision * recall * 255 / (precision + recall)
        (T, edged) = cv2.threshold(edged, threshold, 255, cv2.THRESH_BINARY)

        return edged
    

    def dark_sketch(self):
        if self._image_path is None:
            print("No image loaded")
            return

        image = cv2.imread(self._image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        precision = 0.7
        recall = 0.7
        
        threshold = precision * recall * 255 / (precision + recall)
        (T, bw) = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

        return bw
    

    def oil_paint(self):
        if self._image_path is None:
            print("No image loaded")
            return

        image = cv2.imread(self._image_path)
        oil = cv2.xphoto.oilPainting(image, 7, 1)
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        oil = cv2.filter2D(oil, -1, kernel)
        oil = cv2.GaussianBlur(oil, (3, 3), 0)

        return oil
    

    def noise_reduction(self):
        if self._image_path is None:
            print("No image loaded")
            return
        image = cv2.imread(self._image_path)
        noise = cv2.fastN1MeansDenoisingColored(image, None, 10, 10, 7, 21)

        return noise
    

    def grain_effect(self):
        if self._image_path is None:
            print("No image loaded")
            return

        image = cv2.imread(self._image_path)
        grain = cv2.xphoto.oilPainting(image, 7, 1)

        kernal = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        grain = cv2.filter2D(grain, -1, kernal)

        return grain
    


    def pixelize(self):
        if self._image_path is None:
            print("No image loaded")
            return

        image = cv2.imread(self._image_path)
        pixel = cv2.resize(image, (32, 32), interpolation=cv2.INTER_LINEAR)
        pixel = cv2.resize(pixel, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)

        return pixel
    

    def light_glow(self):
        if self._image_path is None:
            print("No image loaded")
            return
        
        image = cv2.imread(self._image_path)
        glow = cv2.GaussianBlur(image, (0, 0), 10)
        glow = cv2.addWeighted(image, 0.7, glow, 0.6, 0.5)

        return glow
    

    def contrast(self):
        if self._image_path is None:
            print("No image loaded")
            return

        image = cv2.imread(self._image_path)
        contrast = cv2.addWeighted(image, 1.5, np.zeros(image.shape, image.dtype), 0, 0)

        return contrast
    


    def cartoonize(self):
        if self._image_path is None:
            print("No image loaded")
            return

        image = cv2.imread(self._image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        
        gray = cv2.medianBlur(gray, 5)

        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

        
        def color_quantization(img, k):
            data = np.float32(img).reshape((-1, 3))
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
            ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            center = np.uint8(center)
            result = center[label.flatten()]
            result = result.reshape(img.shape)
            return result

        
        color = color_quantization(image, 3)
        bilateral = cv2.bilateralFilter(color, 9, 400, 400) # 

    
        cartoon = cv2.bitwise_and(bilateral, bilateral, mask=edges)

        return cartoon
    


    def sharpen_image(self):
        if self._image_path is None:
            print("No image loaded")
            return

        image = cv2.imread(self._image_path)
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpen = cv2.filter2D(image, -1, kernel)

        return sharpen
    

    def blur_image(self, percent=20):
        if self._image_path is None:
            print("No image loaded")
            return
        
        
        image = cv2.imread(self._image_path)
        blur = cv2.GaussianBlur(image, (0, 0), percent)

        return blur
    


    def color_channels(self):
        if self._image_path is None:
            print("No image loaded")
            return

        image   = cv2.imread(self._image_path)
        b, g, r = cv2.split(image)

        return b, g, r


    






