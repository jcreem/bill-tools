#!/usr/local/bin/python

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import ListFlowable, ListItem
from betterTables import BetterTable

import utils


Gold = colors.HexColor(0xdab600)
White = colors.white

Top_Right_To_Inline_Summary_Cutover = 13


class Goldstandard:

  def __init__(self, title, filename,background=Gold):
    self.title=title

    pdfmetrics.registerFont(TTFont('Copperplate-Bold', 'COPRGTB.TTF'))
    pdfmetrics.registerFont(TTFont('Copperplate', 'COPRGTL.TTF'))
    registerFontFamily('Copperplate', normal='Copperplate',
                                      bold='Copperplate-Bold',
                                      italic='Copperplate',
                                      boldItalic='Copplerplate-Bold')
    self.doc = BaseDocTemplate(filename, pagesize=letter, leftMargin=0.0*inch,
    rightMargin=0.0*inch, topMargin=0.0*inch, bottomMargin=0.5*inch)

    self.doc.gs_background = background


    frame = Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width,
                  self.doc.height, id='normal')
    template = PageTemplate(id='test', frames=frame, onPage=utils.Page_Setup)
    self.doc.addPageTemplates([template])

    self.doc.elements=[]




  def Insert_First_Page_Header(self, Bills):
    Normal_Style=ParagraphStyle('normal')
    NHLA_Style = ParagraphStyle('nhla-style', parent=Normal_Style,
      alignment=TA_CENTER,spaceBefore=0,spaceAfter=0)
    GS_Header_Style = ParagraphStyle('gs-header-style', parent=Normal_Style,
     alignment=TA_CENTER,leading=45,spaceBefore=0,spaceAfter=0)
    GS_Title_Style = ParagraphStyle('gs-title-style', parent=Normal_Style,
     alignment=TA_CENTER, spaceBefore=0,spaceAfter=5)



    NHLA_Title_Para=Paragraph('<font name="Copperplate-Bold" size=20>New Hampshire Liberty Alliance</font>', NHLA_Style)
    GS_Header_Para=Paragraph('<font name="Copperplate-Bold" size=70>Gold Standard</font>', GS_Header_Style)
    GS_Title_Para=Paragraph('<font name="Copperplate" size=14>' + self.title + '</font>', GS_Title_Style)
    NHLA_URL_Title=Paragraph('<font name="Copperplate-Bold" size=10>' + "NHLIBERTY.ORG" + '</font>', GS_Title_Style)
    I=Image('logo_grayscale-new2.png', width=0.99*inch, height=1.877*inch,mask='auto')
    I_Trans=Image('logo_grayscale-trans.png', width=0.99*inch, height=1.877*inch,mask='auto')
    if len(Bills) <= Top_Right_To_Inline_Summary_Cutover:
      Summary_Recommend_Style= ParagraphStyle('summary-style', parent=Normal_Style,
        alignment=TA_LEFT,spaceBefore=0,spaceAfter=0,font='Helvetica',size=9)

      Bill_List=[]

      for Bill in Bills:
        Bill_List.append(Paragraph(Bill.Number + ' ' + Bill.NHLA_Recommendation, Summary_Recommend_Style))
      Top_Row=[I, NHLA_Title_Para, Bill_List]
    else:
      Top_Row=[I,NHLA_Title_Para,I]
    t=Table([Top_Row,
            ['',GS_Header_Para, ''],
            [NHLA_URL_Title, GS_Title_Para, '']], [1.4*inch, 5.6*inch, 1.4*inch],
            [0.2*inch, 1.55*inch, 0.24*inch])
    Header_Table_Style=TableStyle([
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1), 'TOP'),
    ('SPAN',(0,0), (0,1)),
    ('SPAN',(2,0), (2,2))
    ])
    t.setStyle(Header_Table_Style)
    self.doc.elements.append(t)


    if len(Bills)>Top_Right_To_Inline_Summary_Cutover:
        self.doc.elements.append(Spacer(8.5*inch, 0.05*inch))
        Cols=5
        Summary_Table=[]
        Bills_Per_Col=len(Bills)//Cols

        Summary_Recommend_Style= ParagraphStyle('summary-style', parent=Normal_Style,
          alignment=TA_LEFT,spaceBefore=0,spaceAfter=0,font='Helvetica',size=10,
          textColor=colors.white)

        for Base_Index in range(0, Bills_Per_Col):
            Row=[]
            for Col_Index in range(0, Cols):
              if Base_Index+Col_Index*Bills_Per_Col < len(Bills):
                Bill=Bills[Base_Index+Col_Index*Bills_Per_Col]
                Row.append(Paragraph(Bill.Number + ' ' + Bill.NHLA_Recommendation, Summary_Recommend_Style))
            Summary_Table.append(Row)

#        print Summary_Table
        Summary_Table_Style=TableStyle([
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.black, colors.grey])
        ])
        t=Table(data=Summary_Table,colWidths=[(8.5*inch)/Cols]*Cols)
        t.setStyle(Summary_Table_Style)
        self.doc.elements.append(t)
        self.doc.elements.append(Spacer(8.5*inch, 0.05*inch))




  def Set_Bills(self, Bill_List):
    self.Insert_First_Page_Header(Bill_List)
    Normal_Style=ParagraphStyle('normal')

    Right_Para_Style=ParagraphStyle(
      'right-col-style',
      parent=ParagraphStyle('normal'),
      alignment=TA_CENTER,
      fontSize=28,
      leading=27,
      spaceBefore=0,
      spaceAfter=0,
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
      ('BOTTOMPADDING',(0,0),(-1,-1),0)
      ])

    #
    # Each time through this loop, we add all of the rows to the RL_Bill_Table
    Base_Row=0
    for Bill in Bill_List:
        Number_And_Title_Para=Paragraph(Bill.Number + ', ' +
          utils.Normalize_Text(Bill.Title), Number_And_Title_Para_Style)
        Number_Only_Para = Paragraph(Bill.Number, Right_Para_Style)
        RL_Bill_Table.append([Number_And_Title_Para, Number_Only_Para])

        Committee_And_Recommendation_Para=Paragraph(Bill.Committee + ': ' +
          Bill.Committee_Recommendation, Committee_And_Recommend_Para_Style)
        RL_Bill_Table.append([Committee_And_Recommendation_Para, ''])

        Liberty_Type_And_Summary_Para=Paragraph(Bill.Liberty_Type.upper() + ': ' +
          utils.Normalize_Text(Bill.NHLA_Summary), Liberty_Type_And_Summary_Para_Style)
        NHLA_Recommend_Para=Paragraph(Bill.NHLA_Recommendation, Right_Para_Style)
        RL_Bill_Table.append([Liberty_Type_And_Summary_Para, NHLA_Recommend_Para])

        RL_Bill_Table.append([utils.To_Bullet_List(Bill.GS_Blurb), ''])

        RL_Bill_Table_Style.add('BACKGROUND',(0,Base_Row), (0,Base_Row), colors.black)
        RL_Bill_Table_Style.add('BACKGROUND',(0,Base_Row+1), (0,Base_Row+1), ["HORIZONTAL", colors.HexColor(0x606060), colors.black])
        RL_Bill_Table_Style.add('BACKGROUND',(0,Base_Row+2), (0,Base_Row+3), colors.transparent)
        RL_Bill_Table_Style.add('VALIGN',(0,Base_Row),(0,Base_Row+3),"TOP")
        RL_Bill_Table_Style.add('VALIGN',(1, Base_Row), (1, Base_Row), "TOP")
        RL_Bill_Table_Style.add('VALIGN',(1, Base_Row+2), (1, Base_Row+3), "MIDDLE")
        RL_Bill_Table_Style.add('SPAN', (1,Base_Row), (1,Base_Row+1))
        RL_Bill_Table_Style.add('SPAN', (1,Base_Row+2), (1,Base_Row+3))
        RL_Bill_Table_Style.add('BACKGROUND', (1,Base_Row), (1,Base_Row+1), colors.black)
        RL_Bill_Table_Style.add('BACKGROUND', (1,Base_Row+2), (1,Base_Row+3), ["VERTICAL", colors.black, colors.HexColor(0x606060)])
        RL_Bill_Table_Style.add('TOPPADDING',(1,Base_Row+2), (1,Base_Row+3),15)
        RL_Bill_Table_Style.add('BOTTOMPADDING',(1,Base_Row+2), (1,Base_Row+3),15)
        RL_Bill_Table_Style.add('NOSPLIT', (0,Base_Row),(1,Base_Row+3))
        Base_Row=Base_Row+4


    t=BetterTable(RL_Bill_Table, [7.06*inch, 1.44*inch])
    t.setStyle(RL_Bill_Table_Style)
    self.doc.elements.append(t)


  def save(self):
    self.doc.elements.append(PageBreak())
    self.doc.watermark="DRAFT"
    self.doc.build(self.doc.elements)
