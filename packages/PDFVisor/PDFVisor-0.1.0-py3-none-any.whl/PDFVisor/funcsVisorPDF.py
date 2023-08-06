from datetime import datetime
from PyPDF2 import PdfReader
from PIL import Image, ImageColor, ImageTk
import fitz
import cv2
import numpy as np
import os
import pathlib

global image_on_canvas

def grid_by_column(cuadro, columns, spacex=6, spacey=6):
    row = 0
    column = 0
    elem = 0
 
    widgets = [cuadro.children.get('!button'), cuadro.children.get('!canvas'), cuadro.children.get('!button2')]
            
    anclas = ["nw", "n", "ne"]
    
    for widget in widgets:
        widget.grid(row=0, column=column, sticky= anclas[elem])
            
        column += 1
    
        if(column >= columns):
           column = 0
            
           row += 1
    
        cuadro.rowconfigure(0, pad= spacex)
                # se hace lo mismo con las columnas. Se omite la ultima para evitar que haya espacio vacío en el borde inferior.
        for column in range(columns-1):
            cuadro.columnconfigure(column, pad= spacey)
        elem += 1        

def metaDataPDF(archivo):
    meses = ["Emnero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
     
    nomFilePag = archivo[:-4]           
    nomFilePag = nomFilePag + ".pdf"

    reader = PdfReader(nomFilePag, "rb")
    
    pdf_info = reader.metadata
    aux = str(pdf_info.creation_date)
    fecha_dt = datetime.strptime(aux[:-15], '%Y-%m-%d')
    curFecha = str(fecha_dt.day) + "-" + meses[fecha_dt.month - 1] + "-" + str(fecha_dt.year) + aux[10:-9]

    infoMetaDoc = {"Titulo": str(pdf_info.title), "Autor": str(pdf_info.author), "Fecha_creacion": curFecha}
    return infoMetaDoc

def defEstado(archivo):
    nomFilePag = archivo[:-4]           
    nomFilePag = nomFilePag[8:] + ".pdf"
    infoDataBoton = {"Estado": [], "imagStates": []}

    reader = PdfReader(archivo, "rb")
    if len(reader.pages) == 1:
       infoDataBoton["Estado"] = ["disabled", "disabled"]
       infoDataBoton["imagStates"] = ["avanceDeshabilitado.png",
                                      "retroDeshabilitado.png"]
    elif len(reader.pages) == 2:
       infoDataBoton["Estado"] = ["norma\l", "disabled"]
       infoDataBoton["imagStates"] = ["avanceNormal.png",
                                      "retroDeshabilitado.png"]
    reader = None
    
    return infoDataBoton

def desglosaPDF(archivo):
    open_pdf = fitz.open(archivo)
    pagenum = 0
    nomFilePag = ""

    for page in open_pdf:
        pix = page.get_pixmap()
        pix1 = fitz.Pixmap(pix,0) if pix.alpha else pix
                
        verNomPag = archivo[:-4]            
        verNomPag = verNomPag + "_Page-" + str(pagenum) + ".jpg"
                
        pix1.save(verNomPag)
        pagenum += 1


def relatRuta(archivo):
       #HERE =  os.path.dirname(os.path.abspath(__file__))
       HERE = pathlib.Path(__file__).parent 

       fullPath = os.path.join(HERE, "img", archivo)

       parcialPath = os.path.join("img",  archivo)

       return os.path.relpath(fullPath, parcialPath)


def outFondo(origen):
     src = cv2.imread(origen, cv2.IMREAD_UNCHANGED)

        #_,  thresh = cv2.threshold(img_grey,  127, 255,  cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
     _, mask = cv2.threshold(src[:, :, 3], 0, 255, cv2.THRESH_BINARY)
        
     src[:, :, 3] = mask
     arraySrc = np.mat(src)
     img = Image.new("RGB", (106,80), "#2596be")
     bg = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
     bg= bg.astype(float)
     fg = src.astype("uint8")
     alpha = cv2.resize(mask, (106, 80))
     alpha = alpha.astype(float)/255.0
     arrayFg = np.array(fg)
     arrayBg = np.array(bg)
     arrayAlpha = np.array(alpha)
     foreground = cv2.multiply(fg, alpha)
     background = cv2.multiply(bg, (255 - mask))
     outimage = cv2.add(foreground, background)
     return outimage

def cargaPagPDF(archivo, indice):
   nomFilePag = archivo[:-4]
   nomFilePag = nomFilePag[8:] + "_Page-{}.jpg".format(indice)
   return ImageTk.PhotoImage(file= r"D:/Temp/" + nomFilePag)
