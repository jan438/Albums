import os
import sys
import csv
import math
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
rowsalbumreport = 5
columsalbumreport = 5
imgheight = 1.5 * inch

styles = getSampleStyleSheet()
titleStyle = ParagraphStyle('tit',
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 13, 
    textColor = black, 
    alignment=TA_CENTER, 
    leading = 14, 
    spaceAfter = 3)
artisttitleStyle = ParagraphStyle('artisttitle', 
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 10,
    leading = 11,
    textColor = white,
    hyphenationLang="en_GB",
    borderWidth = 0, borderColor = black,
    spaceBefore = 0, spaceAfter = 0,
    borderPadding = 0)
yeargenreStyle = ParagraphStyle('yeargenre', 
    parent=styles['Normal'],
    fontName = albumfont, fontSize = 8,
    leading = 9,
    textColor = white,
    borderWidth = 0, borderColor = black,
    spaceBefore = 0, spaceAfter = 0,
    borderPadding = 0)

albumStyle = [('VALIGN',(0,0),(-1,-1),'TOP'),
    ('LEFTPADDING',(0,0),(-1,-1), 0),
    ('RIGHTPADDING',(0,0),(-1,-1), 0),
    ("BACKGROUND",(0,0),(-1,-1), black)
]

pageStyle = [('BACKGROUND',(0,0),(-1,-1), black)
]

class AlbumReport:
    albums = [[0 for i in range(columsalbumreport)] for j in range(rowsalbumreport)] 

    def append_Table(self, row, col, table):
        self.albums[row][col].append(table)

    def clear(self):
        for r in self.albums:
            for c in r:
                try:
                    c.pop()
                except IndexError:
                    print(c)

    def tabledata(self):
        return [
        [self.albums[0][0], self.albums[0][1], self.albums[0][2], self.albums[0][3], self.albums[0][4]],
        [self.albums[1][0], self.albums[1][1], self.albums[1][2], self.albums[1][3], self.albums[1][4]],
        [self.albums[2][0], self.albums[2][1], self.albums[2][2], self.albums[2][3], self.albums[2][4]],
        [self.albums[3][0], self.albums[3][1], self.albums[3][2], self.albums[3][3], self.albums[3][4]],
        [self.albums[4][0], self.albums[4][1], self.albums[4][2], self.albums[4][3], self.albums[4][4]]
        ]

class Album:
    def __init__(self, title, artist, cover, year, genre, rank):
        self.title = title
        self.artist = artist
        self.cover = cover
        self.year = year
        self.genre = genre
        self.rank = rank

def processreport():
    merger = PdfWriter()
    for i in range(20):
        print(i)
        if os.path.isfile("PDF/Album" + str(i) + ".pdf"):
            inputpdf = open("PDF/Album" + str(i) + ".pdf", "rb")
            merger.append(inputpdf)
            inputpdf.close()
        else:
            break
    output = open("PDF/Total.pdf", "wb")
    merger.write(output)
    merger.close()
    output.close()
    for i in range(10):
        if os.path.isfile("PDF/Album" + str(i) + ".pdf"):
            os.remove("PDF/Album" + str(i) + ".pdf")

def lookupCover(cover):
    img = Image("Covers/" + cover)
    img.drawHeight = imgheight
    img.drawWidth = imgheight
    img.hAlign = TA_CENTER
    return img

def lookupRank(rank):
    img = Image("Ranks/" + rank)
    return True

def fillAlbumReport(count):
    print("fillAlbumReport", count)
    albumreps = []
    index = 0
    countalbumReports = math.ceil(count / (rowsalbumreport * columsalbumreport))
    for i in range(countalbumReports):
        albumreps.append(AlbumReport())
    print(count, rowsalbumreport, columsalbumreport, countalbumReports)
    indrep = 0
    for row in range(rowsalbumreport):
        for col in range(columsalbumreport):
            albumreps[indrep].albums[row][col] = []
    for i in range(countalbumReports):
        albumreportname = "PDF/Album" + str(i) + ".pdf"
        doc = SimpleDocTemplate(albumreportname, pagesize=portrait(A4), rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0)
        storypdf=[]
        for row in range(rowsalbumreport):
            for col in range(columsalbumreport):
                if index >= count:
                    break
                print(row, col, albums[index].title, "indrep", indrep)
                #key = input("Wait")
                img = lookupCover(albums[index].cover)
                artisttitlepara = Paragraph(
                "<font textColor = white size = 9>"  + albums[index].artist + "</font>,‘" + 
                "<font textColor = white>" + albums[index].title + "</font>" + "’", artisttitleStyle)
                rank = albums[index].rank
                found = lookupRank(rank + ".png")
                if found:
                    rankimg = "Ranks/" + rank + ".png"
                yeargenrepara = Paragraph(albums[index].year + " " + "<img src=" + rankimg + " width='20' height='20' valign='-2'/>" + " "+albums[index].genre, yeargenreStyle)
                index += 1
                sp = Spacer(0.1 * inch, 0.1 * inch)
                imartiyegetable = Table([[img, sp], [yeargenrepara], [artisttitlepara]], colWidths=[1.6 * inch], rowHeights=[imgheight, 0.15 * inch, 0.35 * inch])
                imartiyegetable.setStyle(albumStyle)
                albumreps[indrep].append_Table(row, col, imartiyegetable)
        key = input("Wait build")
        print("indrep", indrep)
        tbl_data = albumreps[indrep].tabledata()
        tbl = Table(tbl_data)
        tbl.setStyle(pageStyle)
        storypdf.append(Paragraph("RS 500 2023", titleStyle))
        storypdf.append(tbl)
        doc.build(storypdf)
        albumreps[indrep].clear()
        storypdf=[]
        indrep += 1
    return

if sys.platform[0] == 'l':
    path = '/home/jan/git/Albums'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Albums"
os.chdir(path)
params = sys.argv[1:]
count = 0
albumdata = []
albums = []
if len(params) > 0:
    if params[0] == "1":
        file_to_open = "Data/Albums25/Albums001-025.csv" 
        with open(file_to_open, 'r') as file:
            csvreader = csv.reader(file, delimiter = ';')
            for row in csvreader:
                if count > 0:
                    albumdata.append(row)
                count += 1 
else:
    file_to_open = "Data/Albums.csv"
    with open(file_to_open, 'r') as file:
        csvreader = csv.reader(file, delimiter = ';')
        for row in csvreader:
            if count > 0:
                albumdata.append(row)
            count += 1
for i in range(len(albumdata)):
    albums.append(Album(albumdata[i][0], albumdata[i][1], albumdata[i][2], albumdata[i][3], albumdata[i][4], albumdata[i][5]))
print("Length albums", len(albums))
for i in range(len(albums)):
    print(i, "Album", albums[i].title, albums[i].artist, albums[i].cover, albums[i].year, albums[i].genre, albums[i].rank)
pdfmetrics.registerFont(TTFont('Ubuntu', 'Ubuntu-Regular.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuBold', 'Ubuntu-Bold.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuItalic', 'Ubuntu-Italic.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuBoldItalic', 'Ubuntu-BoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))
fillAlbumReport(len(albums))
processreport()
key = input("Wait")