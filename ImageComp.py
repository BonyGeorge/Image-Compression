from PIL import Image, ImageDraw, ImageFont
import os

print('*** Program Started ***')

image_name_input = 'image0.jpg'

im = Image.open(image_name_input)
print('Input file size   : ', im.size)
print('Input file name   : ', image_name_input)
print('Input Image Size  : ', os.path.getsize(image_name_input))

image_name_output = 'Outputimage0.jpg'

# quality = input("Please Enter Quantity : ")

im.save(image_name_output, optimize=True, quality=50)

print('Output file size  : ', im.size)
print('Output file name  : ', image_name_output)
print('Output Image Size : ', os.path.getsize(image_name_output))

print('*** Program Ended ***')
