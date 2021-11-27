# Date: May 2021
# AP CSP Create Performance Task
# 
# Python modules used:
#   Tkinter - a library that helps build GUI apps in Python
#   PIL - a library for manipulating images in Python
#
# This Python application allows users to upload images
# and apply various filters to alter the image.
#
# Environment:
#   Windows 10
#   Visual Studio Code
#   Python 3.9.5

import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

# This is the default directory for the file upload function
image_directory = "C:/Temp/images"

# This is the initial image that is displayed when the program starts
start_image_location = 'C:/Temp/images/Wallpaper.png'

buttonHeight = 3
buttonWidth = 60
canvasHeight = 600
canvasWidth = 600

# ---- functions ----

# This function gets called when the user clicks on the "Upload" button
# It allows the user to choose a file to upload and display it
# on the canvas.
def upload():
    global image_to_display
    global current_image

    uploaded_filename = filedialog.askopenfilename (initialdir = image_directory, title = "Select a file", filetypes = (("All files", "*.*"),("JPG files", "*.jpg"), ("PNG files", "*.png"), ("GIF files", "*.gif")))
    current_image = Image.open(uploaded_filename).convert('RGB')
    
    # resize the image to fit the canvas dimensions
    current_image.thumbnail((canvasWidth, canvasHeight))

    image_to_display = ImageTk.PhotoImage(current_image)

    # Put the image to display on the canvas
    canvas.itemconfig(image_id, image = image_to_display)
    return

# This function gets called when the user clicks on any of the filter buttons
# Depending on what button the user clicked, the filter value can be "grayscale",
# "one_bit_color_depth", "matrix" or "blade_runner". Based on what this filter value
# is, the function then calls another function to apply the filter formula that
# will transform each of the pixels in the image.
def apply_filter(filter):
    global image_to_display
    global current_image

    # Get the multiplier and addition values that are in the input box
    multiplier = float(multiplierBox.get())
    addition = float(additionBox.get())

    if (filter == "grayscale"):
        temp_image = grayscale_pixels(current_image)
    elif (filter == "one_bit_color_depth"):
        temp_image =  one_bit_color_depth_pixels(current_image)
    elif (filter == "matrix"):
        temp_image = matrix_pixels(current_image, multiplier, addition)
    elif (filter == "blade_runner"):
        temp_image = blade_runner_pixels(current_image, multiplier, addition)
    
    image_to_display = ImageTk.PhotoImage(temp_image)
    current_image = temp_image

    # Put the image to display on the canvas
    canvas.itemconfig(image_id, image = image_to_display)
    return    

# The apply_filter function calls the grayscale_pixels function
# when the filter value is "grayscale." It takes an image as the
# parameter and returns a new grayscale version of that image.
def grayscale_pixels(original_image):

    # Create a new image with the same dimensions as the image passed in to the function
    image = Image.new(original_image.mode, original_image.size)
    
    # Load the image's pixel information into pixels_new as a two-dimensional array
    pixels_new = image.load()

    # Loop through all the individual pixels in the new image
    for i in range(image.size[0]):
        for j in range(image.size[1]):

            # Get the pixel information for the image passed in to the function
            # and use it for creating the pixel in the new image
            pixel = original_image.getpixel((i, j))            

            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            # The grayscale value is stored in the "gray" variable below, 
            # and that value is based on a formula that takes into account
            # each of the red, green, and blue values for the original image.
            # The gray value is then filled in for the red, green and 
            # blue places of each individual pixel in the new image
            gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

            # Giving the pixel in the new image a new set of red, green and blue values
            pixels_new[i, j] = (int(gray), int(gray), int(gray), 255)
    
    # return the image with the new pixels
    return image

# The apply_filter function calls the one_bit_color_depth_pixels function
# when the filter value is "one_bit_color_depth". It takes an image as the
# parameter and returns a new one-bit color depth version of that image. The 
# returned image will be made up entirely of black and white pixels
def one_bit_color_depth_pixels(original_image):

    # Create a new image with the same dimensions as the image passed in to the function
    image = Image.new(original_image.mode, original_image.size)
    
    # Load the image's pixel information into pixels_new as a two-dimensional array
    pixels_new = image.load()

    # Loop through all the individual pixels in the new image
    for i in range(image.size[0]):
        for j in range(image.size[1]):

            # Get the pixel information for the image passed in to the function
            # and use it for creating the pixel in the new image
            pixel = original_image.getpixel((i, j))

            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            # Add up the red, green and blue values
            total = red + green + blue

            # If the sum of the red, green and blue values are greater 
            # than 382, then that pixel becomes white. If it less than 
            # or equal to 382, it becomes black.
            if total > 382:
                # Create values for a white pixel and put it in the new image
                pixels_new[i, j] = (255, 255, 255, 255)
            else:
                # Create values for a black pixel and put it in the new image
                pixels_new[i, j] = (0, 0, 0, 255)
    
    # return the image with the new pixels
    return image

# The apply_filter function calls the matrix_pixels function
# when the filter value is "matrix". As the parameters, it 
# takes an image, an multiplier value, and an addition value, and
# it returns a new image that is slightly greener. 
# 
# It goes through each pixel in the image that's passed in and
# increases its green value, based on what the user has input
# into the "Multiplier" and "Addition" fields. It leaves the red 
# and blue values alone.
def matrix_pixels(original_image, multiplier, addition):

    # Create a new image with the same dimensions as the image passed in to the function
    image = Image.new(original_image.mode, original_image.size)
    
    # Load the image's pixel information into pixels_new as a two-dimensional array
    pixels_new = image.load()

    # Loop through all the individual pixels in the new image
    for i in range(image.size[0]):
        for j in range(image.size[1]):

            # Get the pixel information for the image passed in to the function
            # and use it for creating the pixel in the new image
            pixel = original_image.getpixel((i, j))

            # keep the red value the same
            red = pixel[0]

            # modify the green value using the multiplier and addition parameters
            if pixel[1] * multiplier + addition > 255:
                green = 255
            else:
                green = int(pixel[1] * multiplier + addition)

            # keep the blue value the same
            blue = pixel[2]

            # Giving the pixel a new set of red, green and blue values
            pixels_new[i, j] = (red, green, blue, 255)

    # return the image with the new pixels 
    return image

# The apply_filter function calls the blade_runner_pixels function
# when the filter value is "blade_runner". As the parameters, it 
# takes an image, an multiplier value, and an addition value, and
# it returns a new image that is slightly redder.
#
# It goes through each pixel in the image that's passed in and
# increases its red value, based on what the user has input
# into the "Multiplier" and "Addition" fields. It leaves the green
# and blue values alone.
def blade_runner_pixels(original_image, multiplier, addition):

    # Create a new image with the same dimensions as the image passed in to the function
    image = Image.new(original_image.mode, original_image.size)
    
    # Load the image's pixel information into pixels_new as a two-dimensional array
    pixels_new = image.load()

    # Loop through all the individual pixels in the new image
    for i in range(image.size[0]):
        for j in range(image.size[1]):

            # Get the pixel information for the image passed in to the function
            # and use it for creating the pixel in the new image
            pixel = original_image.getpixel((i, j))

            # modify the red value using the multiplier and addition parameters
            if pixel[0] * multiplier + addition > 255:
                red = 255
            else:
                red = int(pixel[0] * multiplier + addition)

            # Keep the green and blue values the same
            green = pixel[1]
            blue = pixel[2]

            # Giving the pixel a new set of red, green and blue values
            pixels_new[i, j] = (red, green, blue, 255)
    
    # return the image with the new pixels
    return image

# ---- main ----
root = tk.Tk()
root.geometry('1200x1000')
root.title('Image Filter')

# canvas for displaying the image
canvas = tk.Canvas(root, width = canvasWidth, height = canvasHeight)
canvas.pack()

# ---- Instructions ----
instructionsLabel = Label(root, text = "Upload an image and apply the filters", font = "Arial 18 bold")
instructionsLabel.pack()

# ---- Buttons ----

# Upload button for uploading files 
button_upload = tk.Button(root, text = "Upload", command = upload, bg = 'light green', height = buttonHeight, width = buttonWidth)
button_upload.pack(pady = 5)

# Grayscale button for turning an image into grayscale
button_grayscale = tk.Button(root, text = "Grayscale", command = lambda: apply_filter("grayscale"), width = buttonWidth)
button_grayscale.pack(pady = 5)

# 1 bit color depth button for giving an image a depth of bits
button_1bit_color = tk.Button(root, text = "1 bit color depth", command = lambda: apply_filter("one_bit_color_depth"), width = buttonWidth)
button_1bit_color.pack(pady = 5)

# "Matrix" button for amplifying the green value of the pixels in the image
button_matrix = tk.Button(root, text = "Matrix", command = lambda: apply_filter("matrix"), width = buttonWidth)
button_matrix.pack(pady = 5)

# "Blade Runner" button for amplifying the red value of the pixels in the image
button_red = tk.Button(root, text = "Blade Runner", command = lambda: apply_filter("blade_runner"), width = buttonWidth)
button_red.pack(pady = 5)

# ---- Input boxes ----

# Input for the pixel value multiplier
# The Blade Runner and Matrix filters use it
multiplierLabel = Label (root, text = "Multiplier")
multiplierLabel.pack()

multiplierBox = Entry(root)
multiplierBox.insert(END, '1')
multiplierBox.pack()


# Input for the pixel value addition
# The Blade Runner and Matrix filters use it
additionLabel = Label (root, text = "Addition")
additionLabel.pack()

additionBox = Entry(root)
additionBox.insert(END, '0')
additionBox.pack()


# images
start_image = Image.open(start_image_location)
current_image = start_image
start_image.thumbnail((canvasWidth, canvasHeight))
image_to_display = ImageTk.PhotoImage(start_image)

# set first image on canvas
image_id = canvas.create_image(0, 0, anchor = 'nw', image = image_to_display)

root.mainloop()
