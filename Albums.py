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

albumfont = "Ubuntu"
rowsalbumreport = 2
columsalbumreport = 5

styles = getSampleStyleSheet()
titleStyle = ParagraphStyle('title', 
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 10,
    leading = 11,
    borderWidth = 0, borderColor = black,
    spaceBefore = 0, spaceAfter = 0,
    borderPadding = 0)
artistStyle = ParagraphStyle('artist',
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 10,
    leading = 11,
    borderWidth = 0, borderColor = black,
    spaceBefore = 0, spaceAfter = 0,
    borderPadding = 0)
yearStyle = ParagraphStyle('year', 
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 8,
    leading = 9,
    borderWidth = 0, borderColor = black,
    spaceBefore = 0, spaceAfter = 0,
    borderPadding = 0)
genreStyle = ParagraphStyle('genre',
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 8,
    leading = 9,
    borderWidth = 0, borderColor = black,
    spaceBefore = 0, spaceAfter = 0,
    borderPadding = 0)

albumStyle = [('VALIGN',(0,0),(-1,-1),'TOP'),
    ('LEFTPADDING',(0,0),(-1,-1), 0),
    ('RIGHTPADDING',(0,0),(-1,-1), 0)
]

class AlbumReport:
    albums = [[0 for i in range(columsalbumreport)] for j in range(rowsalbumreport)] 

    def append_Table(self, row, col, table):
        self.albums[row][col].append(table)

    def clear(self):
        for a in self.albums:
            try:
                a.pop()
            except IndexError:
                print(a)

    def tabledata(self):
        return [
        [self.albums[0][0], self.albums[0][1], self.albums[0][2], self.albums[0][3], self.albums[0][4]],
        [self.albums[1][0], self.albums[1][1], self.albums[1][2], self.albums[1][3], self.albums[1][4]]
        ]

class Album:
    def __init__(self, title, artist, cover, year, genre):
        self.title = title
        self.artist = artist
        self.cover = cover
        self.year = year
        self.genre = genre

def lookupCover(cover):
    img = Image("Covers/" + cover)
    img.drawHeight = 1.4 * inch
    img.drawWidth = 1.4 * inch
    img.hAlign = TA_CENTER
    return img

def fillAlbumReport(count):
    print("fillAlbumReport", count)
    albumreps = []
    albumreportname = "PDF/Album" + str(0) + ".pdf"
    doc = SimpleDocTemplate(albumreportname, pagesize=portrait(A4), rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0)
    storypdf=[]
    albumreps.append(AlbumReport())
    indrep = 0
    for row in range(rowsalbumreport):
        for col in range(columsalbumreport):
            albumreps[indrep].albums[row][col] = []
    index = 0
    for row in range(rowsalbumreport):
        for col in range(columsalbumreport):
            print(albums[index].title)
            key = input("Wait")
            img = lookupCover(albums[index].cover)
            titlepara = Paragraph(albums[index].title, titleStyle)
            genrepara = Paragraph(albums[index].genre, genreStyle)
            artistpara = Paragraph(albums[index].artist, artistStyle)
            yearpara = Paragraph(albums[index].year, yearStyle)
            index += 1
            titlegenreartistyeartable = Table([[img], [titlepara], [yearpara]])
            titlegenreartistyeartable.setStyle(albumStyle)
            albumreps[indrep].append_Table(row, col, titlegenreartistyeartable)
    print("Len albumreps", len(albumreps))
    tbl_data = albumreps[indrep].tabledata()
    tbl = Table(tbl_data)
    storypdf.append(tbl)
    doc.build(storypdf)
    albumreps[indrep].clear()
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
    albums.append(Album(albumdata[i][0], albumdata[i][1], albumdata[i][2], albumdata[i][3], albumdata[i][4]))
print("Length albums", len(albums))
for i in range(len(albums)):
    print(i, "Album", albums[i].title, albums[i].artist, albums[i].cover, albums[i].year, albums[i].genre)
pdfmetrics.registerFont(TTFont('Ubuntu', 'Ubuntu-Regular.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuBold', 'Ubuntu-Bold.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuItalic', 'Ubuntu-Italic.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuBoldItalic', 'Ubuntu-BoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))
fillAlbumReport(len(albums))
key = input("Wait")