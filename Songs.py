import os
import sys
import csv
import math
import unicodedata
from pathlib import Path
from datetime import datetime, date, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm

songsdata = []
maxsongs = 10
maxsongspage = 5

if sys.platform[0] == 'l':
    path = '/home/jan/git/Albums'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Albums"
os.chdir(path)
file_to_open = "Data/RSSongs2024.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        songsdata.append(row)
        count += 1
print(count)
col = 0
row = 10
colwidth = 200
rowheight = 20
leftmargin = 10
bottommargin = 20
my_canvas = canvas.Canvas("PDF/RSSongs2024.pdf")
my_canvas.setFillColor(HexColor('#000000'))
count = 0
for i in range(maxsongs):
    my_canvas.drawString(leftmargin + col * colwidth + 20, bottommargin + row * rowheight, songsdata[i][0])
    my_canvas.drawString(leftmargin + col * colwidth + 220, bottommargin + row * rowheight, songsdata[i][1])
    my_canvas.drawString(leftmargin + col * colwidth + 420, bottommargin + row * rowheight, songsdata[i][2])
    row -= 1
    count += 1
    if count == maxsongspage:
        my_canvas.showPage()
        count = 0
        row = 10
my_canvas.save()
key = input("Wait")
