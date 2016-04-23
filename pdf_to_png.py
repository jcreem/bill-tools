#!/usr/bin/env python
""" pdf_to_png.py: This module converts a PDF file to a series of numbered PNG
                   images ."""
import PythonMagick
import pyPdf
import argparse
import os


def Convert(Input_PDF_Name, Image_DPI='90'):
    """ Given a PDF file in Input_PDF_Name, creates a series of output PNG
        files with one page per PNG using a Image_DPI dots per inch in creating
        the images.

        Output image names are based on the input name, removing a finame suffix
        from the Input_PDF_Naame and replacing it with a number and PNG suffix.

        For example the 3 page PDF road_to_serfdom.pdf would be turned into
        road_to_serfdom-0.png
        road_to_serfdom-1.png
        road_to_serfrom-2.png

        Leading zeros will be used as required so that all filenames are the
        same length.

        Returns a list of the names of files that were generated.

        """

    pdf_im = pyPdf.PdfFileReader(file(Input_PDF_Name, "rb"))
    npages = pdf_im.getNumPages()
    Base_Name = os.path.splitext(Input_PDF_Name)

    Max_Digits=len(str(npages))
    Images=[]
    #
    # Each time through this loop, we convert one page of the PDF to PNG
    # until complete
    #
    for p in range(npages):
        im = PythonMagick.Image()
        im.density(Image_DPI)
        im.read(Input_PDF_Name + '[' +str(p) +']')
        Output_Name=Base_Name[0] + '-' + str(p).zfill(Max_Digits) + '.png'
        im.write(Output_Name)
        Images.append(Output_Name)

    return Images
#
# If called as a command line tool, simply look for an input filename and
# run on it

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts a PDF to a series of PNGs")
    parser.add_argument("Input_Name")
    args = parser.parse_args()
    Convert(args.Input_Name)
