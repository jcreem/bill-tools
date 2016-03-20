#!/usr/local/bin/python

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def footer(canvas, doc):
    canvas.saveState()
    Normal_Style=ParagraphStyle('normal')
    Footer_Style = ParagraphStyle('my-footer-style', parent=Normal_Style,
      textColor=colors.white, backColor=colors.black, alignment=TA_CENTER)
    P = Paragraph("The New Hampshire Liberty Alliance is a non-partisan coalition "
        "working to increase individual liberty, and encourage citizen "
        "involvement in the legislative process. Bills on the Gold Standard "
        "are evaluated based on their effects on, among other things; civil "
        "liberties, personal responsibility, property rights, "
        "accountability, constitutionality, and taxation. Roll call votes on "
        "Gold Standard bills are the foundation for our annual Liberty "
        "Rating report card.", Footer_Style)
    w,h = P.wrap(doc.width, doc.bottomMargin)
    P.drawOn(canvas, doc.leftMargin,h)
    canvas.restoreState()

#class flowable_fig(reportlab.platypus.Flowable):
#    def __init__(self, imgdata):
#        reportlab.platypus.Flowable.__init__(self)
#        self.img = reportlab.lib.utils.ImageReader(imgdata)
#
#    def draw(self):
#        self.canv.drawImage(self.img, 0, 0, height = -2*inch, width=4*inch)
#        # http://www.reportlab.com/apis/reportlab/2.4/pdfgen.html


class Reportlab_Goldstandard:

  def __init__(self, title, filename):
    self.doc = BaseDocTemplate(filename, pagesize=letter)
    self.doc.leftMargin=0.25
    self.doc.rightMargin=0.25
    self.doc.bottomMargin=0.1
    self.doc.topMArgin=0.1
    frame = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width,
                  self.doc.height, id='normal')
    template = PageTemplate(id='test', frames=frame, onPage=footer)
    self.doc.addPageTemplates([template])

    self.doc.elements=[]


    Normal_Style=ParagraphStyle('normal')
    NHLA_Style = ParagraphStyle('my-footer-style', parent=Normal_Style,
      alignment=TA_CENTER,fontSize=14)
    GS_Header_Style = ParagraphStyle('my-footer-style', parent=Normal_Style,
     alignment=TA_CENTER, fontSize=72)
    Title_Styles = ParagraphStyle('my-footer-style', parent=Normal_Style,
     alignment=TA_CENTER, fontSize=14)

    P = Paragraph("New Hampshire Liberty Alliance", NHLA_Style)
    self.doc.elements.append(P)
    P = Paragraph("Gold\nStandard", GS_Header_Style)
    self.doc.elements.append(P)
    P = Paragraph(title, Title_Styles)
    self.doc.elements.append(P)
    self.doc.elements.append(PageBreak())

  def Set_Bills(self, Bill_List):
    #
    # Convert the bill data into table format
    RL_Bill_Table=[]
    for Bill in Bill_List:
        RL_Bill_Table.append('Left','Right')

    t=Table(RL_Bill_Table,[7*inch, 3*inch])


  def save(self):
    self.doc.build(self.doc.elements)
