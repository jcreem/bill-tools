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

def Page_Setup(canvas, doc):
    canvas.saveState()

    canvas.setFillColor(colors.HexColor(0xdab600))
    canvas.rect(0,0,8.5*inch, 11*inch,fill=1)

    #canvas.setFont("Helvetica", 240)
    #canvas.setStrokeGray(0.90)
    #canvas.setFillGray(0.90)
    #canvas.drawCentredString(5.5 * inch, 3.25 * inch, doc.watermark)


    #print "Called" + doc.watermark

    Normal_Style=ParagraphStyle('normal')
    Footer_Style = ParagraphStyle('my-footer-style', parent=Normal_Style,
      textColor=colors.white, backColor=colors.black, alignment=TA_CENTER,
      fontSize=8, leading=9,font='Courier')
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

def AllPageSetup(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor(0xdab600))
    canvas.rect(0,0,8.5*inch, 11*inch,fill=1)

    canvas.setFont("Helvetica", 240)
    canvas.setStrokeGray(0.90)
    canvas.setFillGray(0.90)
    canvas.drawCentredString(5.5 * inch, 3.25 * inch, doc.watermark)


    print "Called" + doc.watermark

    canvas.restoreState()


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
            alignment=TA_LEFT, leftIndent=6, spaceBefore=0,spaceAfter=0, font='Helvetica', fontSize=11)

      for Blurb in GS_Blurb.splitlines():
          Bullet_Para = Paragraph(Normalize_Text(Blurb),Blurbs_Style)
          Bullet_List_Item=ListItem(Bullet_Para, leftIndent=25, bulletColor=colors.black,bulletType='bullet')
          Paragraph_List.append(Bullet_List_Item)
      return ListFlowable(Paragraph_List, leftIndent=10, bulletType='bullet', start='bulletchar', bulletFontSize=11)


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
    template = PageTemplate(id='test', frames=frame, onPage=Page_Setup)
    self.doc.addPageTemplates([template])

    self.doc.elements=[]




  def Insert_First_Page_Header(self):
    Normal_Style=ParagraphStyle('normal')
    NHLA_Style = ParagraphStyle('nhla-style', parent=Normal_Style,
      alignment=TA_CENTER,spaceBefore=0,spaceAfter=0)
    GS_Header_Style = ParagraphStyle('gs-header-style', parent=Normal_Style,
     alignment=TA_CENTER,leading=45,spaceBefore=0,spaceAfter=0)
    GS_Title_Style = ParagraphStyle('gs-title-style', parent=Normal_Style,
     alignment=TA_CENTER, spaceBefore=0,spaceAfter=5)

    NHLA_Title_Para=Paragraph('<font name="Copperplate-Bold" size=20>New Hampshire Liberty Alliance</font>', NHLA_Style)
    GS_Header_Para=Paragraph('<font name="Copperplate-Bold" size=71>Gold Standard</font>', GS_Header_Style)
    GS_Title_Para=Paragraph('<font name="Copperplate" size=15>' + self.title + '</font>', GS_Title_Style)
    I=Image('logo_grayscale.png', width=0.99*inch, height=1.89*inch)
    t=Table([[I,NHLA_Title_Para,''],
            ['',GS_Header_Para, ''],
            ['NHLIBERTY.ORG',GS_Title_Para,'']], [1.25*inch, 6*inch, 1.25*inch],
            [0.2*inch, 1.75*inch, 0.24*inch])
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

    Right_Para_Style=ParagraphStyle(
      'right-col-style',
      parent=ParagraphStyle('normal'),
      alignment=TA_CENTER,
      fontSize=28,
      leading=27,
      spaceBefore=0,
      spaceAfter=0,
      backColor=colors.black,
      textColor=colors.white,
      fontName='Helvetica-Bold')


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

    #
    # Convert the bill data into table format
    RL_Bill_Table=[]
    RL_Bill_Table_Style=TableStyle([
      ('LEFTPADDING',(0,0),(-1,-1),0),
      ('RIGHTPADDING',(0,0),(-1,-1),0),
      ('TOPPADDING',(0,0),(-1,-1),0),
      ('BOTTOMPADDING',(0,0),(-1,-1),2),
      ('VALIGN',(1,0),(1,-1),'MIDDLE'),
      ('BACKGROUND',(1,0),(1,-1),colors.black)
      ])

    #
    # Each time through this loop, we add all of the rows to the RL_Bill_Table
    Base_Row=0
    for Bill in Bill_List:
        Number_And_Title_Para=Paragraph(Bill.Number + ', ' +
          Normalize_Text(Bill.Title), Number_And_Title_Para_Style)
        Number_Only_Para = Paragraph(Bill.Number, Right_Para_Style)
        RL_Bill_Table.append([Number_And_Title_Para, Number_Only_Para])

        Committee_And_Recommendation_Para=Paragraph(Bill.Committee + ': ' +
          Bill.Committee_Recommendation, Committee_And_Recommend_Para_Style)
        RL_Bill_Table.append([Committee_And_Recommendation_Para, ''])

        Liberty_Type_And_Summary_Para=Paragraph(Bill.Liberty_Type + ': ' +
          Normalize_Text(Bill.NHLA_Summary), Liberty_Type_And_Summary_Para_Style)
        NHLA_Recommend_Para=Paragraph(Bill.NHLA_Recommendation, Right_Para_Style)
        RL_Bill_Table.append([Liberty_Type_And_Summary_Para, NHLA_Recommend_Para])

        RL_Bill_Table.append([To_Bullet_List(Bill.GS_Blurb), ''])
        RL_Bill_Table_Style.add('BACKGROUND',(0,Base_Row),(0,Base_Row), colors.black)
        RL_Bill_Table_Style.add('BACKGROUND',(0,Base_Row+1),(0,Base_Row+1), colors.grey)
        RL_Bill_Table_Style.add('BACKGROUND',(0,Base_Row+2), (0,Base_Row+3), colors.transparent)
        RL_Bill_Table_Style.add('VALIGN',(0,Base_Row),(0,Base_Row+3),"TOP")
        RL_Bill_Table_Style.add('SPAN', (1,Base_Row), (1,Base_Row+1))
        RL_Bill_Table_Style.add('SPAN', (1,Base_Row+2), (1,Base_Row+3))
        RL_Bill_Table_Style.add('NOSPLIT', (0,Base_Row),(1,Base_Row+3))
        Base_Row=Base_Row+4


    t=Table(RL_Bill_Table, [7.06*inch, 1.44*inch])
#    print RL_Bill_Table_Style.getCommands()
    t.setStyle(RL_Bill_Table_Style)
#    t.setStyle(Bill_Table_Style)
    self.doc.elements.append(t)


  def save(self):
    self.doc.elements.append(PageBreak())
    self.doc.watermark="DRAFT"
    self.doc.build(self.doc.elements)
