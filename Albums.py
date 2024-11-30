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
albumdata = []
luumlaut = u"\xC3\xBC"
wuumlaut = u"\xFC"
leaigu = u"\xC3\xA9"
weaigu = u"\xE9"
loumlaut = u"\xC3\xB6"
woumlaut = u"\xF6"
lagrave = u"\xC3\xA0"
wagrave = u"\xE0"
lacirconflexe = u"\xC3\xA2"
wacirconflexe = u"\xE2"
liaigu = u"\xC3\xAD"
wiaigu = u"\xED"
laaigu = u"\xC3\xA1"
waaigu = u"\xE1"
loaigu = u"\xC3\xB3"
woaigu = u"\xF3"

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
    def __init__(self, title, artist, cover, year, genre, rank, type):
        self.title = title
        self.artist = artist
        self.cover = cover
        self.year = year
        self.genre = genre
        self.rank = rank
        self.type = type

def process_2bytesymbol(line, pos, wsymbol):
    processed = line[:pos] + wsymbol + line[pos+2:]
    return processed

def process_2bytesymbols(line, pos, wsymbol):
    processed = line
    for i in range(len(pos), 0, -1):
        processed = process_2bytesymbol(processed, pos[i-1], wsymbol)
    return processed

def find_all_occurrences(line, sub, f, t):
    index_of_occurrences = []
    current_index = f
    while True:
        current_index = line.find(sub, current_index)
        if current_index == -1 or current_index >= t:
            return index_of_occurrences
        else:
            index_of_occurrences.append(current_index)
            current_index += len(sub)

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
    for i in range(20):
        if os.path.isfile("PDF/Album" + str(i) + ".pdf"):
            os.remove("PDF/Album" + str(i) + ".pdf")

def processcsv(csvfile):
    with open(file_to_open, 'r') as file:
        csvreader = csv.reader(file, delimiter = ';')
        count = 0
        for row in csvreader:
            if count > 0:
                albumdata.append(row)
            count += 1

def processdiacritic(text):
    processed = text
    uumlauts = find_all_occurrences(processed, luumlaut, 0, len(processed))
    processed = process_2bytesymbols(processed, uumlauts, wuumlaut)
    oumlauts = find_all_occurrences(processed, loumlaut, 0, len(processed))
    processed = process_2bytesymbols(processed, oumlauts, woumlaut)
    eaigus = find_all_occurrences(processed, leaigu, 0, len(processed))
    processed = process_2bytesymbols(processed, eaigus, weaigu)
    agraves = find_all_occurrences(processed, lagrave, 0, len(processed))
    processed = process_2bytesymbols(processed, agraves, wagrave)
    iaigus = find_all_occurrences(processed, liaigu, 0, len(processed))
    processed = process_2bytesymbols(processed, iaigus, wiaigu)
    aaigus = find_all_occurrences(processed, laaigu, 0, len(processed))
    processed = process_2bytesymbols(processed, aaigus, waaigu)
    oaigus = find_all_occurrences(processed, loaigu, 0, len(processed))
    processed = process_2bytesymbols(processed, oaigus, woaigu)
    acirconflexes = find_all_occurrences(processed, lacirconflexe, 0, len(processed))
    processed = process_2bytesymbols(processed, acirconflexes, wacirconflexe)
    return processed

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
                type = albums[index].type
                print("Type", type)
                if type == "a":
                    typeimg = "Type/album.png"
                if type == "s":
                    typeimg = "Type/soundtrack.png"
                if type == "t":
                    typeimg = "Type/tape.png"
                if type == "l":
                    typeimg = "Type/live.png"
                if type == "c":
                    typeimg = "Type/compilation.png"
                yeargenrepara = Paragraph(albums[index].year + " " + 
                    "<img src=" + rankimg + " width='20' height='20' valign='-2'/>" + " " + 
                    albums[index].genre +
                     "<img src=" + typeimg + " width='20' height='20' valign='-2'/>",
                    yeargenreStyle)
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
albums = []
if len(params) > 0:
    if params[0] == "0":
        file_to_open = "Data/Albums25/Albums001-025.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums026-050.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums051-075.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums076-100.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums101-125.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums126-150.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums151-175.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums176-200.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums201-225.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums226-250.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums251-275.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums276-300.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums301-325.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums326-350.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums351-375.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums376-400.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums401-425.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums426-450.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums451-475.csv" 
        processcsv(file_to_open)
        file_to_open = "Data/Albums25/Albums476-500.csv" 
        processcsv(file_to_open)
    if params[0] == "1":
        file_to_open = "Data/Albums25/Albums001-025.csv" 
        processcsv(file_to_open)
    if params[0] == "2":
        file_to_open = "Data/Albums25/Albums026-050.csv" 
        processcsv(file_to_open)
    if params[0] == "3":
        file_to_open = "Data/Albums25/Albums051-075.csv" 
        processcsv(file_to_open)
    if params[0] == "4":
        file_to_open = "Data/Albums25/Albums076-100.csv" 
        processcsv(file_to_open)
    if params[0] == "5":
        file_to_open = "Data/Albums25/Albums101-125.csv" 
        processcsv(file_to_open)
    if params[0] == "6":
        file_to_open = "Data/Albums25/Albums126-150.csv" 
        processcsv(file_to_open)
    if params[0] == "7":
        file_to_open = "Data/Albums25/Albums151-175.csv" 
        processcsv(file_to_open)
    if params[0] == "8":
        file_to_open = "Data/Albums25/Albums176-200.csv" 
        processcsv(file_to_open)
    if params[0] == "9":
        file_to_open = "Data/Albums25/Albums201-225.csv" 
        processcsv(file_to_open)
    if params[0] == "10":
        file_to_open = "Data/Albums25/Albums226-250.csv" 
        processcsv(file_to_open)
    if params[0] == "11":
        file_to_open = "Data/Albums25/Albums251-275.csv" 
        processcsv(file_to_open)
    if params[0] == "12":
        file_to_open = "Data/Albums25/Albums276-300.csv" 
        processcsv(file_to_open)
    if params[0] == "13":
        file_to_open = "Data/Albums25/Albums301-325.csv" 
        processcsv(file_to_open)
    if params[0] == "14":
        file_to_open = "Data/Albums25/Albums326-350.csv" 
        processcsv(file_to_open)
    if params[0] == "15":
        file_to_open = "Data/Albums25/Albums351-375.csv" 
        processcsv(file_to_open)
    if params[0] == "16":
        file_to_open = "Data/Albums25/Albums376-400.csv" 
        processcsv(file_to_open)
    if params[0] == "17":
        file_to_open = "Data/Albums25/Albums401-425.csv" 
        processcsv(file_to_open)
    if params[0] == "18":
        file_to_open = "Data/Albums25/Albums426-450.csv" 
        processcsv(file_to_open)
    if params[0] == "19":
        file_to_open = "Data/Albums25/Albums451-475.csv" 
        processcsv(file_to_open)
    if params[0] == "20":
        file_to_open = "Data/Albums25/Albums476-500.csv" 
        processcsv(file_to_open)
if len(params) == 0:
    file_to_open = "Data/Albums.csv"
    processcsv(file_to_open)
for i in range(len(albumdata)):
    title = processdiacritic(albumdata[i][0])
    artist = processdiacritic(albumdata[i][1])
    albums.append(Album(title, artist, albumdata[i][2], albumdata[i][3], albumdata[i][4], albumdata[i][5], albumdata[i][6]))
print("Length albums", len(albums))
for i in range(len(albums)):
    print(i, "Album", albums[i].title, albums[i].artist, albums[i].cover, albums[i].year, albums[i].genre, albums[i].rank, albums[i].type)
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