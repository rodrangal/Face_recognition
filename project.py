import zipfile
import pytesseract
import PIL
from PIL import Image
from PIL import ImageDraw
import cv2 as cv
import numpy as np
from IPython.display import display
import math

name = input('Please input name:')

#Opens the zip file and creates a list of dictionaries that contain the file names and the files (images)
lst = []
c = 0
with zipfile.ZipFile('readonly/images.zip', 'r') as zip:
    for item in zip.infolist():
        image = Image.open(zip.extract(item))
        lst.append({})
        lst[c]['File_Name'] = item.filename
        lst[c]['Image'] = image
        c = c + 1

#This part does the face dtection
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
for dict in lst:
    img = cv.imread(dict['File_Name'])
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 6)
    pil_img = Image.fromarray(gray,mode="L")
    dict['Faces'] = []
    for x, y, w, h in faces:
        face = pil_img.crop((x, y, x+w, y+h))
        dict['Faces'].append(face)
        
#This part does the image to string conversion, creates the contact sheet and pastes the faces on the contact sheet
special_characters = [",", ".", "(", ")", "!", "?", "'"]
for dict2 in lst:
    image = Image.open(dict2['File_Name']).convert('1')
    text = pytesseract.image_to_string(image)
    str1 = ''
    for char in text:
        if char not in special_characters:
            str1 = str1 + char
    words = str1.split()
    if name in words:
        if dict2['Faces'] == []:
            print('Results were found in {}, but faces were not found in that file!'.format(dict2['File_Name']))
        else:
            first_image = dict2['Faces'][0]
            h = math.ceil(len(dict2['Faces']) / 5)
            contact_sheet = PIL.Image.new(first_image.mode, (first_image.width * 5, first_image.height * h))
            x = 0
            y = 0
            print('Results found in {}'.format(dict2['File_Name']))
            for elem in dict2['Faces']:
                resized_elem = elem.resize((first_image.width, first_image.height))
                contact_sheet.paste(resized_elem, (x, y))
                if x + first_image.width == contact_sheet.width:
                    x = 0
                    y = y + first_image.height
                else:
                    x = x + first_image.width
            display(contact_sheet)