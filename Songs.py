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
my_canvas = canvas.Canvas("PDF/RSSongs2024.pdf")
my_canvas.setFillColor(HexColor('#FECDE5'))
p = my_canvas.beginPath()
p.arc(2.0, 12.0, 22.0, 32.0, startAng = 90, extent = 90)
my_canvas.drawPath(p, fill=1, stroke=1)
my_canvas.save()
key = input("Wait")
