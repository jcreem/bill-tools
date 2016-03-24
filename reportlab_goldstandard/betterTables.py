#
# The purpose of this module is to extend the default ReportLab table class
# providing support for gradient fill cells. This is sort of a hack and
# ideally we should contribute a slightly cleaned up version of this back
# to the reportlab opens source project. The reason I call it a hack is that
# while we are extendeding the default table class to implement this, the
# nature the method we need to override is such that we end up with
# ugly copy/paste of exiting code before getting into the code that
# we update.
#
# The approach to table gradients we've selected to implement is to extend the
# exiting TableStyle "BACKGROUND" keyword. In the base class this accepts a
# single argument which is a color. We maintain support for that usage but
# if we see that the argument is a list instead of a single item we assume
# gradient fill is desired. The list is then assumed to be of the format
# <DIRECTION> <START COLOR> <END COLOR>
# Where <Direction> is either HORIZONTAL or VERTICAL
#
from reportlab.platypus import Table

class BetterTable(Table):
  def _drawBkgrnd(self):
    nrows = self._nrows
    ncols = self._ncols
    canv = self.canv
    colpositions = self._colpositions
    rowpositions = self._rowpositions
    rowHeights = self._rowHeights
    colWidths = self._colWidths
    spanRects = getattr(self,'_spanRects',None)
    for cmd, (sc, sr), (ec, er), arg in self._bkgrndcmds:
        if sc < 0: sc = sc + ncols
        if ec < 0: ec = ec + ncols
        if sr < 0: sr = sr + nrows
        if er < 0: er = er + nrows
        x0 = colpositions[sc]
        y0 = rowpositions[sr]
        x1 = colpositions[min(ec+1,ncols)]
        y1 = rowpositions[min(er+1,nrows)]
        w, h = x1-x0, y1-y0
        if hasattr(arg,'__call__'):
            arg(self,canv, x0, y0, w, h)
        elif cmd == 'ROWBACKGROUNDS':
            #Need a list of colors to cycle through.  The arguments
            #might be already colours, or convertible to colors, or
            # None, or the str 'None'.
            #It's very common to alternate a pale shade with None.
            colorCycle = list(map(colors.toColorOrNone, arg))
            count = len(colorCycle)
            rowCount = er - sr + 1
            for i in xrange(rowCount):
                color = colorCycle[i%count]
                h = rowHeights[sr + i]
                if color:
                    canv.setFillColor(color)
                    canv.rect(x0, y0, w, -h, stroke=0,fill=1)
                y0 = y0 - h
        elif cmd == 'COLBACKGROUNDS':
            #cycle through colours columnwise
            colorCycle = list(map(colors.toColorOrNone, arg))
            count = len(colorCycle)
            colCount = ec - sc + 1
            for i in xrange(colCount):
                color = colorCycle[i%count]
                w = colWidths[sc + i]
                if color:
                    canv.setFillColor(color)
                    canv.rect(x0, y0, w, h, stroke=0,fill=1)
                x0 = x0 +w
        else:   #cmd=='BACKGROUND'

            if not type(arg) is list:

              color = colors.toColorOrNone(arg)
              if color:
                  if ec==sc and er==sr and spanRects:
                      xywh = spanRects.get((sc,sr))
                      if xywh:
                          #it's a single cell
                          x0, y0, w, h = xywh
                  canv.setFillColor(color)
                  canv.rect(x0, y0, w, h, stroke=0,fill=1)
            else:
              canv.saveState()

              if ec==sc and er==sr and spanRects:
                xywh = spanRects.get((sc,sr))
                if xywh:
                  #it's a single cell
                  x0, y0, w, h = xywh
              p = canv.beginPath()
              p.rect(x0, y0, w, h)
              canv.clipPath(p, stroke=0)
              Direction=arg.pop(0)
              if Direction=="HORIZONTAL":
                canv.linearGradient(x0,y0,x0+w,y0,arg,extend=False)
              else: # Assuming "VERTICAL"
                canv.linearGradient(x0,y0,x0,y0+h,arg,extend=False)
              canv.restoreState()
