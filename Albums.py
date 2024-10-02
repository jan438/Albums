import os
import sys
import csv
import unicodedata
from pathlib import Path
from datetime import datetime, date, timedelta
from ics import Calendar, Event
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import LETTER, A4, landscape, portrait
from reportlab.lib.units import inch
from reportlab.lib.colors import blue, green, black, red, pink, gray, brown, purple, orange, yellow, white
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Image, Spacer, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

if sys.platform[0] == 'l':
    path = '/home/jan/git/Albums/Data'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Albums/Data"
os.chdir(path)
file_to_open = "Albums.csv"
count = 0
albumdata = []
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    for row in csvreader:
        print("Hallo")
print("Length", len(albumdata))
styles = getSampleStyleSheet()
key = input("Wait")