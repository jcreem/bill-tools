#!/usr/local/bin/python

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,\
   Spacer, BaseDocTemplate, Frame, PageTemplate, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import ListFlowable, ListItem
from betterTables import BetterTable
import gs_tools.bill
import os.path

import utils


Gold = colors.HexColor(0xdab600)
White = colors.white



class Goldstandard:

  def __init__(self, title, filename, background=Gold, \
               Top_Right_To_Inline_Summary_Cutover = 14):
    self.title=title
    self.Top_Right_To_Inline_Summary_Cutover = \
      Top_Right_To_Inline_Summary_Cutover

    self.Resource_Path=os.path.dirname(os.path.realpath( __file__ ))+"/../"

    pdfmetrics.registerFont(TTFont('Copperplate-Bold', \
      self.Resource_Path+'ufonts.com_copperplate-bold.ttf'))
    pdfmetrics.registerFont(TTFont('Copperplate', \
      self.Resource_Path+'ufonts.com_copperplate.ttf'))
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
      alignment=TA_CENTER)
    GS_Header_Style = ParagraphStyle('gs-header-style', parent=Normal_Style,
     alignment=TA_CENTER,leading=45,spaceBefore=0,spaceAfter=0)
    GS_Title_Style = ParagraphStyle('gs-title-style', parent=Normal_Style,
     alignment=TA_CENTER, spaceBefore=0,spaceAfter=5)



    NHLA_Title_Para=Paragraph(
      '<font name="Copperplate-Bold" size=20>' + \
      'New Hampshire Liberty Alliance</font>', NHLA_Style)
    GS_Header_Para=Paragraph(
      '<font name="Copperplate-Bold" size=68>Gold Standard</font>', \
        GS_Header_Style)
    GS_Title_Para=Paragraph('<font name="Copperplate" size=14>' +\
      self.title + '</font>', GS_Title_Style)
    NHLA_URL_Title=Paragraph('<font name="Copperplate-Bold" size=10>' + \
      "<a href=http://nhliberty.org/>NHLIBERTY.ORG</a>" + '</font>', \
      GS_Title_Style)


    self.doc.leftLogoFile=self.Resource_Path + 'logo_grayscale-new2.png'
    self.doc.rightLogoFile=self.Resource_Path + 'logo_grayscale-new2.png'

    #
    # We want the summary sorted but we want to leave the original bills
    # in original order
    #
    Summary_Bills=list(Bills)
    Summary_Bills.sort()

    #
    # Normally, we place a short summary voting recommendation in the top right
    # corner of the page. If that gets too long though, we will switch and
    # insert a summary voting block inline with the normal recommendations.
    # Check to see which case we are in
    #
    if len(Summary_Bills) <= self.Top_Right_To_Inline_Summary_Cutover:
      Summary_Recommend_Style= ParagraphStyle('summary-style', \
        parent=Normal_Style, alignment=TA_LEFT,spaceBefore=0,
        spaceAfter=0,fontName='Helvetica-Bold',size=8, leading=8)

      Bill_List=[]

      #
      # Each time through this loop, a bill summary recommendation (short bill
      # number and recommendation) is converted to a paragraph and inserted in
      # a list intended for the upper right corner of the first page.
      #
      for Bill in Summary_Bills:
        Bill_List.append(Paragraph(gs_tools.bill.Brief_Bill_Number(Bill.Number) + ' ' + \
          Bill.NHLA_Recommendation, Summary_Recommend_Style))

      Top_Row=['', NHLA_Title_Para, Bill_List]
      Bottom_Row=[NHLA_URL_Title, GS_Title_Para, '']

      self.doc.rightLogoFile=self.Resource_Path + 'logo_grayscale-trans.png'
    else:
      #
      # We are in the case where we will do the summary recommendations
      # inline, so don't do anything with the summary here. Just adapt the
      # header slightly to make it more visually pleasing in the absense
      # of the summary voting recommendation
      #
      Top_Row=['',NHLA_Title_Para,'']
      Bottom_Row=[NHLA_URL_Title, GS_Title_Para, NHLA_URL_Title]


    t=Table([Top_Row,
            ['',GS_Header_Para, ''],
            Bottom_Row], [1.4*inch, 5.6*inch, 1.4*inch])

    #
    # These odd negative and seemly random top and bottom paddings were required
    # to get reasonably tight packing of the header data. No combination of
    # vertical alignment request or forced cell heights came close enough
    # to what we would want here
    Header_Table_Style=TableStyle([
    ('TOPPADDING',(1,0),(1,0),-5),
    ('TOPPADDING',(1,1),(1,1),-20),
    ('TOPPADDING',(1,2),(1,2),-4),
    ('TOPPADDING',(0,2),(0,2),-1),
    ('TOPPADDING',(2,0),(2,0),-2),
    ('BOTTOMPADDING',(1,1),(1,1),27),
    ('BOTTOMPADDING',(1,2),(1,2),6),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('VALIGN',(0,0),(-1,-1),"TOP"),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('SPAN',(2,0), (2,2))
    ])
    t.setStyle(Header_Table_Style)
    self.doc.elements.append(t)

    #
    # Now that we spit out the header, check to see if we are in the case with
    # the summary voting recommendations 'inline' and if so, insert a
    # summary block here
    #
    if len(Summary_Bills)>self.Top_Right_To_Inline_Summary_Cutover:
        self.doc.elements.append(Spacer(8.5*inch, 0.05*inch))
        Cols=5
        Summary_Table=[]
        Bills_Per_Col=len(Bills)//Cols

        Summary_Recommend_Style=ParagraphStyle(
          'summary-style', parent=Normal_Style,
          alignment=TA_LEFT, spaceBefore=0, spaceAfter=0,\
          fontName='Helvetica',size=10,
          textColor=colors.white)

        for Base_Index in range(0, Bills_Per_Col):
            Row=[]
            for Col_Index in range(0, Cols):
              if Base_Index+Col_Index*Bills_Per_Col < len(Summary_Bills):
                Bill=Summary_Bills[Base_Index+Col_Index*Bills_Per_Col]
                Row.append(Paragraph(bill.Brief_Bill_Number(Bill.Number) + \
                  ' ' + Bill.NHLA_Recommendation, Summary_Recommend_Style))
            Summary_Table.append(Row)

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
      fontSize=26,
      leading=26,
      spaceBefore=0,
      spaceAfter=0,
      textColor=colors.white,
      fontName='Helvetica-Bold')


    Number_And_Title_Para_Style=Normal_Style=ParagraphStyle('num-title-style',
      parent=Normal_Style, alignment=TA_LEFT,leftIndent=6, \
      textColor=colors.white,
      fontName='Helvetica-Bold',fontSize=12, leading=16, spaceBefore=0,
            spaceAfter=0)

    Committee_And_Recommend_Para_Style=ParagraphStyle('commit-recommend-style',
      parent=Normal_Style, alignment=TA_LEFT,leftIndent=6, \
      textColor=colors.white,
      fontName='Helvetica-Bold', fontSize=11, leading=15)

    Liberty_Type_And_Summary_Para_Style=ParagraphStyle('liberty-type-style',
      parent=Normal_Style, alignment=TA_LEFT,leftIndent=6, \
      textColor=colors.black,
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
        URL_Text="<a href=http://www.nhliberty.org/bills/view/2016/" + \
          gs_tools.bill.Brief_Bill_Number(Bill.Number, Separator='') + ">"

        Number_And_Title_Para=Paragraph(URL_Text + Bill.Number + '</a>, ' +
          utils.Normalize_Text(Bill.Title), Number_And_Title_Para_Style)
        Number_Only_Para = Paragraph(gs_tools.bill.Brief_Bill_Number(Bill.Number), \
        Right_Para_Style)
        RL_Bill_Table.append([Number_And_Title_Para, Number_Only_Para])

        Committee_And_Recommendation_Para=Paragraph(Bill.Committee + ': ' +
          Bill.Committee_Recommendation, Committee_And_Recommend_Para_Style)
        RL_Bill_Table.append([Committee_And_Recommendation_Para, ''])

        Liberty_Type_And_Summary_Para=Paragraph(Bill.Liberty_Type.upper()\
           + ': ' + utils.Normalize_Text(Bill.NHLA_Summary), \
           Liberty_Type_And_Summary_Para_Style)
        NHLA_Recommend_Para=Paragraph(Bill.NHLA_Recommendation, \
                                      Right_Para_Style)
        RL_Bill_Table.append([Liberty_Type_And_Summary_Para, \
                             NHLA_Recommend_Para])

        RL_Bill_Table.append([utils.To_Bullet_List(Bill.GS_Blurb), ''])

        RL_Bill_Table_Style.add('BACKGROUND',(0,Base_Row), (0,Base_Row),\
           colors.black)
        RL_Bill_Table_Style.add('BACKGROUND',(0,Base_Row+1), (0,Base_Row+1),\
           ["HORIZONTAL", colors.HexColor(0x606060), colors.black])
        RL_Bill_Table_Style.add('BACKGROUND',(0,Base_Row+2), (0,Base_Row+3),\
           colors.transparent)
        RL_Bill_Table_Style.add('VALIGN',(0,Base_Row),(0,Base_Row+3),"TOP")
        RL_Bill_Table_Style.add('VALIGN',(1, Base_Row), (1, Base_Row), "TOP")
        RL_Bill_Table_Style.add('VALIGN',(1, Base_Row+2), (1, Base_Row+3),\
           "MIDDLE")
        RL_Bill_Table_Style.add('SPAN', (1,Base_Row), (1,Base_Row+1))
        RL_Bill_Table_Style.add('SPAN', (1,Base_Row+2), (1,Base_Row+3))
        RL_Bill_Table_Style.add('BACKGROUND', (1,Base_Row), (1,Base_Row+1), \
          colors.black)
        RL_Bill_Table_Style.add('BACKGROUND', (1,Base_Row+2), (1,Base_Row+3),\
          ["VERTICAL", colors.black, colors.HexColor(0x606060)])
        RL_Bill_Table_Style.add('TOPPADDING',(1,Base_Row+2), (1,Base_Row+3),7)
        RL_Bill_Table_Style.add('BOTTOMPADDING',(1,Base_Row+2),\
           (1,Base_Row+3),7)
        RL_Bill_Table_Style.add('BOTTOMPADDING',(0,Base_Row+3),\
           (0,Base_Row+3),3)
        RL_Bill_Table_Style.add('NOSPLIT', (0,Base_Row),(1,Base_Row+3))
        Base_Row=Base_Row+4

    #
    # Reportlab does not take kindly to inserting a table with no rows so
    # if we've ended up with a zero length table, don't insert it
    #
    if len(RL_Bill_Table) > 0:
      t=BetterTable(RL_Bill_Table, [7.06*inch, 1.44*inch])
      t.setStyle(RL_Bill_Table_Style)
      self.doc.elements.append(t)


  def save(self):
    self.doc.build(self.doc.elements)
