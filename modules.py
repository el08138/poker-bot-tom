"""
Created on Wed Jun  3 19:45:13 2020
Supporting modules
@author: Stamatis
"""

""" import libraries """
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

class ImageEditor:
    def __init__(self):
        pass
    
    def merge_images(self, imga, imgb):
        """
        Merges 2 color image ndarrays side-by-side.
        """
        ha, wa = imga.shape[:2]
        hb, wb = imgb.shape[:2]
        max_height = np.max([ha, hb])
        total_width = wa + wb
        new_img = np.zeros(shape=(max_height, total_width, 3))
        new_img[:max_height, :wa] = imga
        new_img[:max_height, wa:wa+wb] = imgb
        return new_img
    
    def merge_n_images(self, image_list):
        """
        Merges n color images from a list of images.
        """
        output = None
        for i, img_path in enumerate(image_list):
            img = mpimg.imread(img_path)[:,:,:3]
            if i==0:
                output = img
            else:
                output = self.merge_images(output, img)
        return output
    
    def print_image(self, img):
        fig = plt.figure()
        plt.imshow(img.astype('uint8'))
        plt.axis('off')
        plt.show()