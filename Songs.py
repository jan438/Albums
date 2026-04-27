import os
import sys
import csv
import math
import unicodedata
from pathlib import Path
from datetime import datetime, date, timedelta
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm

songsdata = []
maxsongs = 500
maxsongspage = 25
position = 500
songsfont = "LiberationSerif"

if sys.platform[0] == 'l':
    path = '/home/jan/git/Albums'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Albums"
os.chdir(path)
pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))
file_to_open = "Data/RSSongs2024.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        songsdata.append(row)
        count += 1
print(count)
col = 0
row = 25
colwidth = 200
rowheight = 20
leftmargin = 10
bottommargin = 20
my_canvas = canvas.Canvas("PDF/RSSongs2024.pdf")
my_canvas.setFont(songsfont, 12)
my_canvas.setFillColor(HexColor('#000000'))
count = 0
for i in range(maxsongs):
    my_canvas.drawString(leftmargin + col * colwidth + 5, bottommargin + row * rowheight, str(position))
    artisttitle = songsdata[i][2] + ",‘"+ songsdata[i][1] + "’"
    my_canvas.drawString(leftmargin + col * colwidth + 50, bottommargin + row * rowheight, artisttitle)
    my_canvas.drawString(leftmargin + col * colwidth + 400, bottommargin + row * rowheight, songsdata[i][3])
    print(i, songsdata[i][4])
    row -= 1
    count += 1
    position -= 1
    if count == maxsongspage:
        my_canvas.showPage()
        count = 0
        row = 25
my_canvas.save()
key = input("Wait")
