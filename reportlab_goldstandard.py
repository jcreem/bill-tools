#!/usr/local/bin/python

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import ListFlowable, ListItem

def footer(canvas, doc):
    #print canvas.getAvailableFonts()
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
    P.drawOn(canvas, doc.leftMargin,doc.bottomMargin)
    canvas.restoreState()

#class flowable_fig(reportlab.platypus.Flowable):
#    def __init__(self, imgdata):
#        reportlab.platypus.Flowable.__init__(self)
#        self.img = reportlab.lib.utils.ImageReader(imgdata)
#
#    def draw(self):
#        self.canv.drawImage(self.img, 0, 0, height = -2*inch, width=4*inch)
#        # http://www.reportlab.com/apis/reportlab/2.4/pdfgen.html


def get_python_image():
  f = open(filename, 'w')
  f.write(response.read())
  f.close()

def Normalize_Text(Text):
  return Text.strip("* .") + '.'

def To_Bullet_List(GS_Blurb):
      Normal_Style=ParagraphStyle('normal')
      Paragraph_List=[]

      Blurbs_Style = ParagraphStyle('blurb-style', parent=Normal_Style,
            alignment=TA_LEFT,spaceBefore=0,spaceAfter=0, font='Helvetica', fontSize=11)


      for Blurb in GS_Blurb.splitlines():
          Paragraph_List.append(Paragraph(Normalize_Text(Blurb),Normal_Style))
      return ListFlowable(Paragraph_List, bulletType='bullet', start='circle', bulletFontSize=6, leftIdent=14)


class Reportlab_Goldstandard:

  def __init__(self, title, filename):
    self.title=title
    pdfmetrics.registerFont(TTFont('Copperplate-Bold', 'COPRGTB.TTF'))
    pdfmetrics.registerFont(TTFont('Copperplate', 'COPRGTL.TTF'))
    registerFontFamily('Copperplate', normal='Copperplate',
                                      bold='Copperplate-Bold',
                                      italic='Copperplate',
                                      boldItalic='Copplerplate-Bold')
    self.doc = BaseDocTemplate(filename, pagesize=letter, leftMargin=0.0*inch,
    rightMargin=0.0*inch, topMargin=0.0*inch, bottomMargin=0.0*inch)

    frame = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width,
                  self.doc.height, id='normal', showBoundary=1)
    template = PageTemplate(id='test', frames=frame, onPage=footer)
    self.doc.addPageTemplates([template])

    self.doc.elements=[]




  def Insert_First_Page_Header(self):
    Normal_Style=ParagraphStyle('normal')
    NHLA_Style = ParagraphStyle('nhla-style', parent=Normal_Style,
      alignment=TA_CENTER,spaceBefore=0,spaceAfter=0)
    GS_Header_Style = ParagraphStyle('gs-header-style', parent=Normal_Style,
     alignment=TA_CENTER,leading=45,spaceBefore=0,spaceAfter=0)
    GS_Title_Style = ParagraphStyle('gs-title-style', parent=Normal_Style,
     alignment=TA_CENTER, spaceBefore=0,spaceAfter=0)

    NHLA_Title_Para=Paragraph('<font name="Copperplate-Bold" size=20>New Hampshire Liberty Alliance</font>', NHLA_Style)
    GS_Header_Para=Paragraph('<font name="Copperplate-Bold" size=71>Gold Standard</font>', GS_Header_Style)
    GS_Title_Para=Paragraph('<font name="Copperplate" size=15>' + self.title + '</font>', GS_Title_Style)
    I=Image('logo_grayscale.png', width=1.1*inch, height=2.1*inch)
    t=Table([[I,NHLA_Title_Para,''],
            ['',GS_Header_Para, ''],
            ['NHLIBERTY.ORG',GS_Title_Para,'']], [1.25*inch, 6*inch, 1.25*inch],
            [0.2*inch, 1.85*inch, 0.22*inch])
    Header_Table_Style=TableStyle([
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('VALIGN',(0,0),(-1,-1), 'TOP'),
    ('SPAN',(0,0), (0,1))
    ])
    t.setStyle(Header_Table_Style)
    self.doc.elements.append(t)




  def Set_Bills(self, Bill_List):
    self.Insert_First_Page_Header()
    Normal_Style=ParagraphStyle('normal')
    #
    # Convert the bill data into table format
    RL_Bill_Table=[]
    Left_Inner_Table_Style=TableStyle([
      ('FONT',(0,0),(-1,1), 'Helvetica'),
      ('FONTSIZE',(0,0),(-1,-1),12),
      ('BACKGROUND',(0,0),(0,0),colors.black),
      ('BACKGROUND',(0,1),(0,1),colors.grey),
      ('TEXTCOLOR',(0,0),(0,0),colors.white),
      ('LEFTPADDING',(0,0),(-1,-1),0),
      ('RIGHTPADDING',(0,0),(-1,-1),0),
      ('TOPPADDING',(0,0),(-1,-1),0),
      ('BOTTOMPADDING',(0,0),(-1,-1),0),
      ('ALIGN',(0,0),(-1,-1),'LEFT'),
      ('VALIGN',(0,0),(-1,-1),'MIDDLE')
    ])

    Right_Inner_Table_Style=TableStyle([
      ('FONT',(0,0),(-1,1), 'Helvetica'),
      ('FONTSIZE',(0,0),(-1,-1),25),
      ('BACKGROUND',(0,0),(-1,-1),colors.black),
      ('TEXTCOLOR',(0,0),(-1,-1), colors.white),
      ('TOPPADDING',(0,0),(-1,-1),0),
      ('BOTTOMPADDING',(0,0),(-1,-1),0),
      ('ALIGN',(0,0),(-1,-1),'CENTER'),
      ('VALIGN',(0,0),(-1,-1),'MIDDLE')
    ])
    Right_Inner_Para_Style=ParagraphStyle(
      'right-col-style',
      parent=ParagraphStyle('normal'),
      alignment=TA_CENTER,
      fontSize=25,
      leading=27,
      textColor=colors.white,
      backColor=colors.black,
      spaceBefore=0,
      spaceAfter=0,
      fontName='Helvetica')

    Bill_Table_Style=TableStyle([
      ('LEFTPADDING',(0,0),(-1,-1),0),
      ('RIGHTPADDING',(0,0),(-1,-1),0),
      ('TOPPADDING',(0,0),(-1,-1),0),
      ('BOTTOMPADDING',(0,0),(-1,-1),0),
      ('ALIGN',(0,0),(-1,-1),'LEFT')
    ])

    Number_And_Title_Para_Style=Normal_Style=ParagraphStyle('num-title-style',
      parent=Normal_Style, alignment=TA_LEFT,leftIndent=6, textColor=colors.white,
      fontName='Helvetica-Bold',fontSize=12, leading=16, spaceBefore=0,
            spaceAfter=0)

    Committee_And_Recommend_Para_Style=ParagraphStyle('commit-recommend-style',
      parent=Normal_Style, alignment=TA_LEFT,leftIndent=6, textColor=colors.white,
      fontName='Helvetica-Bold', fontSize=11, leading=15)

    Liberty_Type_And_Summary_Para_Style=ParagraphStyle('liberty-type-style',
      parent=Normal_Style, alignment=TA_LEFT,leftIndent=6, textColor=colors.black,
      fontName='Helvetica-Bold', fontSize=11, leading=15)

    for Bill in Bill_List:
        Right_Inner_Table=Table([[Paragraph(Bill.Number, Right_Inner_Para_Style)],
                                 [Paragraph(Bill.NHLA_Recommendation, Right_Inner_Para_Style)]],
          [1.5*inch])
        Right_Inner_Table.setStyle(Right_Inner_Table_Style)
        Number_And_Title_Para=Paragraph(Bill.Number + ', ' +
          Normalize_Text(Bill.Title), Number_And_Title_Para_Style)

        Committee_And_Recommendation_Para=Paragraph(Bill.Committee + ': ' +
          Bill.Committee_Recommendation, Committee_And_Recommend_Para_Style)

        Liberty_Type_And_Summary_Para=Paragraph(Bill.Liberty_Type + ': ' +
          Normalize_Text(Bill.NHLA_Summary), Liberty_Type_And_Summary_Para_Style)

        Left_Inner_Table=Table([[Number_And_Title_Para],
                                [Committee_And_Recommendation_Para],
                                [Liberty_Type_And_Summary_Para],
                                [To_Bullet_List(Bill.GS_Blurb)]], [7*inch])
        Left_Inner_Table.setStyle(Left_Inner_Table_Style)
        RL_Bill_Table.append([Left_Inner_Table,Right_Inner_Table])

    t=Table(RL_Bill_Table, [7*inch, 1.5*inch])
    t.setStyle(Bill_Table_Style)
    self.doc.elements.append(t)


  def save(self):
    self.doc.elements.append(PageBreak())
    self.doc.build(self.doc.elements)
