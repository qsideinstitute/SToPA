from pdf2image import convert_from_path

images = convert_from_path('Logs2019_10.pdf') #import pdf file

for i in range(len(images)):
      # Save pages as images in the pdf
    images[i].save('page'+ str(i) +'.jpg', 'JPEG')

from PIL import Image #package that will rotate images

with Image.open('page3.jpg') as im: #open image file
    im.rotate(0.5).show() #rotate image by 0.5 degrees






