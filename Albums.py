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

styles = getSampleStyleSheet()

class AlbumReport:
    album =  [[] for _ in range(2)]

    def append_Cover(self, col, cover):
        self.album[col].append(cover)

    def clear(self):
        for i in range(2):
            while len(self.album[i]) > 0:
                self.album[i].pop()

class Album:
    def __init__(self, title, artist, cover):
        self.title = title
        self.artist = artist
        self.cover = cover

def lookupCover(cover):
    img = Image("Covers/" + cover)
    print(img)
    return img

def fillAlbumReport(count):
    print("fillAlbumReport", count)
    albumreps = []
    albumreps.append(AlbumReport())
    img = lookupCover(albums[0].cover)
    albumreps[0].append_Cover(0, img)
    img = lookupCover(albums[1].cover)
    albumreps[0].append_Cover(1, img)
    print(len(albumreps))
    key = input("Wait")
    return

if sys.platform[0] == 'l':
    path = '/home/jan/git/Albums'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Albums"
os.chdir(path)
file_to_open = "Data/Albums.csv"
count = 0
albumdata = []
albums = []
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    for row in csvreader:
        if count > 0:
            albumdata.append(row)
        count += 1
for i in range(len(albumdata)):
    albums.append(Album(albumdata[i][0], albumdata[i][1], albumdata[i][2]))
print("Length albums", len(albums))
for i in range(len(albums)):
    print(i, "Album", albums[i].title, albums[i].artist, albums[i].cover)
fillAlbumReport(len(albums))
key = input("Wait")