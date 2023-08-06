"""
Filename: fancy_bbox.py
Author: Prashant Verma
Email: Prashant27050@gmail.com
Version: 0.0.12
Release Date: 
"""

import cv2
import numpy as np

class FancyBox:
    def __init__(self, x, y, w, h, border_thickness=2, line_type=cv2.LINE_AA, border_color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.border_thickness = border_thickness
        self.line_type = line_type
        self.border_color = border_color


    def adjust_opacity(self, image, opacity, opacity_color):
        # Define the fill color with 50% opacity (alpha = 0.5)
        
        tuple_value = (opacity_color, opacity)
        fill_color = tuple_value[0] + (tuple_value[1],)
        # Create a numpy array with the same shape as the image
        mask = np.zeros_like(image)
        # Draw the bounding box on the mask
        cv2.rectangle(mask, [self.x, self.y, self.w, self.h], fill_color, cv2.FILLED)
        image = cv2.addWeighted(image, 1, mask, 0.2, 0)
        return image

    
    def draw(self, image, opacity = None):
        """_summary_

        Args:
            image (_type_): _description_

        Returns:
            _type_: _description_
        """
        if opacity:
            image = self.adjust_opacity(image, opacity[0], opacity[1])
        # Define the corner points of the rectangle
        pt1 = (self.x, self.y)
        pt2 = (self.x + self.w, self.y)
        pt3 = (self.x + self.w, self.y + self.h)
        pt4 = (self.x, self.y + self.h)

        # Define the corner points of the border
        bpt1 = (self.x - self.border_thickness, self.y - self.border_thickness)
        bpt2 = (self.x + self.w + self.border_thickness, self.y - self.border_thickness)
        bpt3 = (self.x + self.w + self.border_thickness, self.y + self.h + self.border_thickness)
        bpt4 = (self.x - self.border_thickness, self.y + self.h + self.border_thickness)

        # Draw the border lines
        cv2.line(image, bpt1, pt1, self.border_color, self.border_thickness, self.line_type)
        cv2.line(image, bpt1, bpt4, self.border_color, self.border_thickness, self.line_type)
        cv2.line(image, bpt4, pt4, self.border_color, self.border_thickness, self.line_type)
        cv2.line(image, bpt2, pt2, self.border_color, self.border_thickness, self.line_type)
        cv2.line(image, bpt2, bpt3, self.border_color, self.border_thickness, self.line_type)
        cv2.line(image, bpt3, pt3, self.border_color, self.border_thickness, self.line_type)

        return image

    def draw_dashed_border(self, image, dash_length=10, opacity = None):
        """_summary_

        Args:
            image (_type_): _description_
            dash_length (int, optional): _description_. Defaults to 10.

        Returns:
            _type_: _description_
        """
        if opacity:
            image = self.adjust_opacity(image, opacity[0], opacity[1])
        # Define the corner points of the rectangle
        pt1 = (self.x, self.y)
        pt2 = (self.x + self.w, self.y)
        pt3 = (self.x + self.w, self.y + self.h)
        pt4 = (self.x, self.y + self.h)

        # Define the corner points of the border
        bpt1 = (self.x - self.border_thickness, self.y - self.border_thickness)
        bpt2 = (self.x + self.w + self.border_thickness, self.y - self.border_thickness)
        bpt3 = (self.x + self.w + self.border_thickness, self.y + self.h + self.border_thickness)
        bpt4 = (self.x - self.border_thickness, self.y + self.h + self.border_thickness)

        # Draw the dashed border lines
        for i in range(0, self.w, dash_length*2):
            cv2.line(image, (self.x+i, self.y), (self.x+i+dash_length, self.y), self.border_color, self.border_thickness, self.line_type)
            cv2.line(image, (self.x+i, self.y+self.h), (self.x+i+dash_length, self.y+self.h), self.border_color, self.border_thickness, self.line_type)
        for i in range(0, self.h, dash_length*2):
            cv2.line(image, (self.x, self.y+i), (self.x, self.y+i+dash_length), self.border_color, self.border_thickness, self.line_type)
            cv2.line(image, (self.x+self.w, self.y+i), (self.x+self.w, self.y+i+dash_length), self.border_color, self.border_thickness, self.line_type)

        return image

    def draw_rounded_corners(self, image, radius=10, opacity= None):
        """_summary_

        Args:
            image (_type_): _description_
            radius (int, optional): _description_. Defaults to 10.

        Returns:
            _type_: _description_
        """
        # Define the corner points of the rectangle
        # Define the corner points of the rectangle
        if opacity:
            image = self.adjust_opacity(image, opacity[0], opacity[1])
        pt1 = (self.x, self.y)
        pt2 = (self.x + self.w, self.y)
        pt3 = (self.x + self.w, self.y + self.h)
        pt4 = (self.x, self.y + self.h)
        
        # Define the corner points of the border
        bpt1 = (self.x - self.border_thickness, self.y - self.border_thickness)
        bpt2 = (self.x + self.w + self.border_thickness, self.y - self.border_thickness)
        bpt3 = (self.x + self.w + self.border_thickness, self.y + self.h + self.border_thickness)
        bpt4 = (self.x - self.border_thickness, self.y + self.h + self.border_thickness)

        # Draw the rounded corners
        cv2.line(image, (self.x+radius, self.y), (self.x+self.w-radius, self.y), self.border_color, self.border_thickness, self.line_type)
        cv2.line(image, (self.x+self.w, self.y+radius), (self.x+self.w, self.y+self.h-radius), self.border_color, self.border_thickness, self.line_type)
        cv2.line(image, (self.x+radius, self.y+self.h), (self.x+self.w-radius, self.y+self.h), self.border_color, self.border_thickness, self.line_type)
        cv2.line(image, (self.x, self.y+radius), (self.x, self.y+self.h-radius), self.border_color, self.border_thickness, self.line_type)

        cv2.ellipse(image, (self.x+radius, self.y+radius), (radius, radius), 180, 0, 90, self.border_color, self.border_thickness, self.line_type)
        cv2.ellipse(image, (self.x+self.w-radius, self.y+radius), (radius, radius), 270, 0, 90, self.border_color, self.border_thickness, self.line_type)
        cv2.ellipse(image, (self.x+radius, self.y+self.h-radius), (radius, radius), 90, 0, 90, self.border_color, self.border_thickness, self.line_type)
        cv2.ellipse(image, (self.x+self.w-radius, self.y+self.h-radius), (radius, radius), 0, 0, 90, self.border_color, self.border_thickness, self.line_type)

        return image

    def target_rect_bbox(self, image, l=30, t =5, rt =1, opacity = None):
        """_summary_

        Args:
            image (_type_): _description_
            l (int, optional): _description_. Defaults to 30.
            t (int, optional): _description_. Defaults to 5.
            rt (int, optional): _description_. Defaults to 1.

        Returns:
            image: returning output image
        """
        x1, y1  = self.x + self.w, self.y + self.w
        if opacity:
            image = self.adjust_opacity(image, opacity[0], opacity[1])
        cv2.rectangle(image, [self.x, self.y, self.w, self.h], self.border_color, rt)
        # Top Left
        cv2.line(image, (self.x, self.y), (self.x+ l, self.y), self.border_color, t)
        cv2.line(image, (self.x, self.y), (self.x, self.y + l), self.border_color, t)
        # Top Right
        cv2.line(image, (x1, self.y), (x1 - l, self.y), self.border_color, t)
        cv2.line(image, (x1, self.y), (x1, self.y + l), self.border_color, t)
        # Bottom Left
        cv2.line(image, (self.x, y1), (self.x+ l, y1), self.border_color, t)
        cv2.line(image, (self.x, y1), (self.x, y1 - l), self.border_color, t)
        # Bottom Right
        cv2.line(image, (x1, y1), (x1 - l, y1), self.border_color, t)
        cv2.line(image, (x1, y1), (x1, y1 - l), self.border_color, t)

        return image

    def target_angle_bbox(self, image, l= 30, t = 5, opacity=None):
        """target_angle_bbox: return's fancy angle shape corners bbox
        Args:
            image (_type_): _description_
            l (int, optional): length of line - Defaults to 30.
            t (int, optional): width of line - Defaults to 5.

        Returns:
            image: returning output image
        """
        x1, y1  = self.x + self.w, self.y + self.w
        if opacity:
            image = self.adjust_opacity(image, opacity[0], opacity[1])

        cv2.line(image, (self.x, self.y), (self.x+ l, self.y), self.border_color, t)
        cv2.line(image, (self.x, self.y), (self.x, self.y + l), self.border_color, t)
        # Top Right
        cv2.line(image, (x1, self.y), (x1 - l, self.y), self.border_color, t)
        cv2.line(image, (x1, self.y), (x1, self.y + l), self.border_color, t)
        # Bottom Left
        cv2.line(image, (self.x, y1), (self.x+ l, y1), self.border_color, t)
        cv2.line(image, (self.x, y1), (self.x, y1 - l), self.border_color, t)
        # Bottom Right
        cv2.line(image, (x1, y1), (x1 - l, y1), self.border_color, t)
        cv2.line(image, (x1, y1), (x1, y1 - l), self.border_color, t)

        return image











