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
columsalbumreport = 2

styles = getSampleStyleSheet()
titleStyle = ParagraphStyle('title', 
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 10,
    leading = 11,
    borderWidth = 1, borderColor = black,
    spaceBefore = 0, spaceAfter = 0,
    borderPadding = 0)
artistStyle = ParagraphStyle('artist',
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 10,
    leading = 11,
    borderWidth = 1, borderColor = black,
    spaceBefore = 0, spaceAfter = 0,
    borderPadding = 0)
yearStyle = ParagraphStyle('year', 
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 8,
    leading = 9,
    borderWidth = 1, borderColor = black,
    spaceBefore = 0, spaceAfter = 0,
    borderPadding = 0)
genreStyle = ParagraphStyle('genre',
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 8,
    lrading = 9,
    borderWidth = 1, borderColor = black,
    spaceBefore = 0, spaceAfter = 0,
    borderPadding = 0)

albumStyle = [('VALIGN',(0,0),(-1,-1),'TOP'),
    ('LEFTPADDING',(0,0),(-1,-1), 0),
    ('RIGHTPADDING',(0,0),(-1,-1), 0)
]

class AlbumReport:
    album = [[] for _ in range(columsalbumreport)]

    def append_Cover(self, col, cover):
        self.album[col].append(cover)

    def append_Table(self, col, table):
        self.album[col].append(table)

    def clear(self):
        for i in range(columsalbumreport):
            while len(self.album[i]) > 0:
                self.album[i].pop()

    def tabledata(self):
        return [[self.album[0], self.album[1]]]

class Album:
    def __init__(self, title, artist, cover, year, genre):
        self.title = title
        self.artist = artist
        self.cover = cover
        self.year = year
        self.genre = genre

def lookupCover(cover):
    img = Image("Covers/" + cover)
    img.drawHeight = 1.5 * inch
    img.drawWidth = 1.5 * inch
    img.hAlign = TA_CENTER
    return img

def fillAlbumReport(count):
    print("fillAlbumReport", count)
    albumreps = []
    albumreportname = "PDF/Album" + str(0) + ".pdf"
    doc = SimpleDocTemplate(albumreportname, pagesize=portrait(A4), rightMargin=5, leftMargin=5, topMargin=5, bottomMargin=5)
    storypdf=[]
    albumreps.append(AlbumReport())
    for col in range(columsalbumreport):
        img = lookupCover(albums[col].cover)
        albumreps[0].append_Cover(col, img)
        titlepara = Paragraph(albums[col].title, titleStyle)
        genrepara = Paragraph(albums[col].genre, genreStyle)
        artistpara = Paragraph(albums[col].artist, artistStyle)
        yearpara = Paragraph(albums[col].year, yearStyle)
        titlegenreartistyeartable = Table([[titlepara, genrepara], [artistpara, yearpara]], colWidths=[1.0 * inch, 0.5 * inch],  rowHeights=[0.2 * inch, 0.2 * inch])
        titlegenreartistyeartable.setStyle(albumStyle)
        albumreps[0].append_Table(col, titlegenreartistyeartable)
    print(len(albumreps))
    tbl_data = albumreps[0].tabledata()
    tbl = Table(tbl_data, repeatRows=0, colWidths=[1.75*inch])
    storypdf.append(tbl)
    doc.build(storypdf)
    albumreps[0].clear()
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