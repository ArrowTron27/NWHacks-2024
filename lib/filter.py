import cv2
import pytesseract
import imutils
import numpy as np
from PIL import ImageGrab
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import re
import dateutil.parser as dparse

def parseString(string_input):
    try:
        date = dparse.parse(string_input)
        return date
    except ValueError:
        return None

def findDates(string_input):
    copy = string_input
    list = copy.split()
    date_list = []
    while len(list) > 1:
        string = list[0] + list[1]
        dates = parseString(string)
        if dates != None:
            list.pop(0)
            list.pop(0)
            date_list.append(dates)
        else:
            list.pop(0)
    return date_list

def extractSentences(PATH_TESSERACT, PATH_PDF):
    pytesseract.pytesseract.tesseract_cmd = r"/bin/tesseract"
    path_pdf = r"test/Schneider_Electric_Resume.pdf"
    image = np.asarray(convert_from_path(path_pdf))[0]
    greyscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(greyscale, 0, 255, cv2.THRESH_OTSU)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,50))
    contours, hiearchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    letters = []
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        rect = cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)
        cropped = image[y:y+h, x:x+w]
        text = pytesseract.image_to_string(cropped)
    sentences = []
    sen = []
    for i in text:
        if i != "\n":
            sen.append(i)
        else:
            # print(sen)
            sentences.append(''.join(sen))
            sen=[]
    return sentences

def extractYears(sentences, min_time):
    place = None
    for i in range(len(sentences)):
        if (re.search("experience", sentences[i], re.IGNORECASE)) != None:
            place = i + 1
            break

    dates = []
    for j in range(place, len(sentences)):
        sen = sentences[j]
        if (re.search("experience", sen, re.IGNORECASE) != None):
            break
        elif (re.search("project", sen, re.IGNORECASE) != None):
            break
        elif (re.search("education", sen, re.IGNORECASE) != None):
            break
        elif (re.search("extracurricular", sen, re.IGNORECASE) != None):
            break
        else:
            dates = dates + findDates(sen)

    years = []
    for i in range(len(dates)):
        years.append(dates[i].year)
    years = np.asarray(years)
    years = years[years > 999]
    return((np.amax(years)-np.amin(years)) >= min_time)

def filter(PATH_TESSERACT, PATH_PDF, min_time):
    sentences = extractSentences(PATH_TESSERACT, PATH_PDF)
    status = extractYears(sentences, min_time)
    return status

def main():
    PATH_TESSERACT = ""
    PATH_PDF = ""
    min_time = 0
    filter(PATH_TESSERACT, PATH_PDF, min_time)

if __name__ == "__main__":
    main()