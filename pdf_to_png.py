#!/usr/bin/env python
import PythonMagick
import pyPdf
import argparse
import os


def Convert(Input_PDF_Name, Image_DPI='90'):
    pdf_im = pyPdf.PdfFileReader(file(Input_PDF_Name, "rb"))
    npages = pdf_im.getNumPages()
    Base_Name = os.path.splitext(Input_PDF_Name)

    Images=[]
    for p in range(npages):
        im = PythonMagick.Image()
        im.density(Image_DPI)
        im.read(Input_PDF_Name + '[' +str(p) +']')
        im.write(Base_Name[0] + str(p) + '.png')
        Images.append(Base_Name[0] + str(p) + '.png')

    return Images

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts a PDF to a series of PNGs")
    parser.add_argument("Input_Name")
    args = parser.parse_args()
    Convert(args.Input_Name)
