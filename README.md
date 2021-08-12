Loads an image using cv2 and converts it to grayscale before resizing it maually by using loops. The image is resized so that its braille representation is less than 2000
characters so it can be seen easily. Each group of 2x3 pixels is then looked at and given a number based on which pixels are above the average pixel intensity. Those numbers
are then compared with a bank of braille characters and matched to the corresponding character. This is done for each area of 2x3 pixels in the image. The final result is 
saved to a text file where it can be copied or shared.
