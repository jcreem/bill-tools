from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import ListFlowable, ListItem
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Image

def Page_Setup(canvas, doc):

    canvas.saveState()

    canvas.setFillColor(doc.gs_background)
    canvas.rect(0,0,8.5*inch, 11*inch,fill=1)

    if canvas.getPageNumber() == 1:

      canvas.drawImage(doc.leftLogoFile,x=0.3*inch, y=8.7*inch,\
                       width=0.92*inch, mask='auto', preserveAspectRatio=True)

      canvas.drawImage(doc.rightLogoFile,x=7.3*inch, y=8.7*inch,\
                       width=0.92*inch, mask='auto', preserveAspectRatio=True)



    Normal_Style=ParagraphStyle('normal')
    Footer_Style = ParagraphStyle('my-footer-style', parent=Normal_Style,
      textColor=colors.white, backColor=colors.black, alignment=TA_CENTER,
      fontSize=6, leading=7,fontName='Courier',borderPadding=(0,0,5,0))
    P = Paragraph("The New Hampshire Liberty Alliance is a non-partisan coalition "
        "working to increase individual liberty, and encourage citizen "
        "involvement in the legislative process. Bills on the Gold Standard "
        "are evaluated based on their effects on, among other things; civil "
        "liberties, personal responsibility, property rights, "
        "accountability, constitutionality, and taxation. Roll call votes on "
        "Gold Standard bills are the foundation for our annual Liberty "
        "Rating report card.", Footer_Style)
    w,h = P.wrap(doc.width, doc.bottomMargin)
    P.drawOn(canvas, doc.leftMargin,3)
    canvas.restoreState()



def AllPageSetup(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(doc.gs_background)
    canvas.rect(0,0,8.5*inch, 11*inch,fill=1)

    canvas.setFont("Helvetica", 240)
    canvas.setStrokeGray(0.90)
    canvas.setFillGray(0.90)
    canvas.drawCentredString(5.5 * inch, 3.25 * inch, doc.watermark)

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
            alignment=TA_LEFT, leftIndent=6, spaceBefore=0,spaceAfter=0, fontName='Helvetica', fontSize=11)

      for Blurb in GS_Blurb.splitlines():
          if len(Blurb) > 1:
            Bullet_Para = Paragraph(Normalize_Text(Blurb),Blurbs_Style)
            Bullet_List_Item=ListItem(Bullet_Para, leftIndent=25, bulletColor=colors.black,bulletType='bullet')
            Paragraph_List.append(Bullet_List_Item)
      return ListFlowable(Paragraph_List, leftIndent=10, bulletType='bullet', start='bulletchar', bulletFontSize=11)
