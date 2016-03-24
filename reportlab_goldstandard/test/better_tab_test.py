#!/usr/bin/env python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

import betterTables

PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()
Title = "Hello world"
pageinfo = "platypus example"


def myFirstPage(canvas, doc):
  canvas.saveState()
  canvas.setFont('Times-Bold',16)
  canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
  canvas.setFont('Times-Roman',9)
  canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
  canvas.restoreState()


def myLaterPages(canvas, doc):
  canvas.saveState()
  canvas.setFont('Times-Roman',9)
  canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
  canvas.restoreState()


def go():
  doc = SimpleDocTemplate("phello.pdf")
  Story = [Spacer(1,2*inch)]
  style = styles["Normal"]
  bogustext = ("This is Paragraph number ")
  p = Paragraph(bogustext, style)
  Story.append(p)

  data=[["Dog", "Cat"], ["Mouse","Bear"]]

  st=TableStyle([
        ('BACKGROUND', (0,0),(0,0), ["HORIZONTAL", colors.grey, colors.black]),
        ('BACKGROUND', (1,1),(1,1), ["VERTICAL", colors.red, colors.black])
        ])

  t=betterTables.BetterTable(data)
  t.setStyle(st)

  Story.append(t)
  doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

go()
