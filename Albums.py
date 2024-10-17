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

styles = getSampleStyleSheet()
titleStyle = ParagraphStyle('title', 
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 10,
    leading = 11,
    borderWidth = 1, borderColor =  black)
artistStyle = ParagraphStyle('artist',
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 10,
    leading = 11,
    borderWidth = 1, borderColor = black)
yearStyle = ParagraphStyle('year', 
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 8,
    leading = 9,
    borderWidth = 1, borderColor = black)
genreStyle = ParagraphStyle('genre',
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 8,
    lrading = 9,
    borderWidth = 1, borderColor = black)

class AlbumReport:
    album = [[] for _ in range(2)]

    def append_Cover(self, col, cover):
        self.album[col].append(cover)

    def append_Title(self, col, title, style):
        textpar = Paragraph(title, style)
        self.album[col].append(textpar)

    def append_Artist(self, col, artist, style):
        textpar = Paragraph(artist, style)
        self.album[col].append(textpar)

    def append_Table(self, col, testtable):
        self.album[col].append(testtable)

    def clear(self):
        for i in range(2):
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
    img = lookupCover(albums[0].cover)
    albumreps[0].append_Cover(0, img)
    titlepara = Paragraph(albums[0].title, titleStyle)
    genrepara = Paragraph(albums[0].genre, genreStyle)
    titlegenretable = Table([[titlepara, genrepara]], colWidths=[1.0 * inch, 0.5 * inch],  rowHeights=[0.2 * inch])
    albumreps[0].append_Table(0, titlegenretable)
    artistpara = Paragraph(albums[0].artist, artistStyle)
    yearpara = Paragraph(albums[0].year, yearStyle)
    artistyeartable = Table([[artistpara, yearpara]], colWidths=[1.0 * inch, 0.5 * inch],  rowHeights=[0.2 * inch])
    albumreps[0].append_Table(0, artistyeartable)
    img = lookupCover(albums[1].cover)
    albumreps[0].append_Cover(1, img)
    titlepara = Paragraph(albums[1].title, titleStyle)
    genrepara = Paragraph(albums[1].genre, genreStyle)
    titlegenretable = Table([[titlepara, genrepara]], colWidths=[1.0 * inch, 0.5 * inch],  rowHeights=[0.2 * inch])
    albumreps[0].append_Table(1, titlegenretable)
    artistpara = Paragraph(albums[1].artist, artistStyle)
    yearpara = Paragraph(albums[1].year, yearStyle)
    artistyeartable = Table([[artistpara, yearpara]], colWidths=[1.0 * inch, 0.5 * inch],  rowHeights=[0.2 * inch])
    albumreps[0].append_Table(1, artistyeartable)
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