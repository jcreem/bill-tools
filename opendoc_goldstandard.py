
#
# Unfortunately, the lpod python documentation is substantially lacking
# I've had modest good luck looking at
# the perl version of the docs here
# http://search.cpan.org/~jmgdoc/ODF-lpOD-1.126/lpOD/Style.pod
# and supplimenting them with some other python examples from
# https://github.com/lpod/lpod-python-recipes/blob/master/Examples/create_a_text_document_from_plain_text_with_layout.py
#

from lpod.document import odf_new_document
from lpod.heading import odf_create_heading
from lpod.paragraph import odf_create_paragraph
from lpod.style import odf_create_style
from lpod.element import odf_create_element


class Opendoc_Goldstandard:

  def __init__(self):
    self.document = odf_new_document('text')
    self.document.delete_styles()


    _style_page = odf_create_element(u"""\
      <style:page-layout style:name="MyLayout">
      <style:page-layout-properties fo:page-width="21.00cm" fo:page-height="29.70cm" \
      style:num-format="1" style:print-orientation="portrait" fo:margin-top="0.5cm" \
      fo:margin-bottom="0.5cm" fo:margin-left="0.5cm" fo:margin-right="0.5cm" \
      style:writing-mode="lr-tb" style:footnote-max-height="0cm"><style:footnote-sep \
      style:width="0.018cm" style:distance-before-sep="0.10cm" \
      style:distance-after-sep="0.10cm" style:line-style="solid" \
      style:adjustment="left" style:rel-width="25%" style:color="#000000"/>
      </style:page-layout-properties><style:footer-style>
      <style:header-footer-properties fo:min-height="0.6cm" fo:margin-left="0cm" \
      fo:margin-right="0cm" fo:margin-top="0.3cm" style:dynamic-spacing="false"/>
      </style:footer-style></style:page-layout>""")

    # master style, using the precedent layout for the actual document
    _style_master = odf_create_element(u"""\
      <style:master-page style:name="Standard" \
      style:page-layout-name="MyLayout"><style:footer><text:p text:style-name="Footer">\
      <text:tab/><text:tab/><text:page-number \
      text:select-page="current"/> / <text:page-count \
      style:num-format="1">15</text:page-count></text:p></style:footer>\
      </style:master-page>""")


    # some footer
    _style_footer = odf_create_element(u"""\
      <style:style style:name="Footer" style:family="paragraph" style:class="extra" \
      style:master-page-name=""><style:paragraph-properties style:page-number="auto" \
      text:number-lines="false" text:line-number="0"><style:tab-stops>\
      <style:tab-stop style:position="8.90cm" style:type="center"/><style:tab-stop \
      style:position="17.80cm" style:type="right"/></style:tab-stops>
      </style:paragraph-properties><style:text-properties \
      style:font-name="Liberation Sans" fo:font-size="7pt"/></style:style>""")

    p = odf_create_paragraph("The New Hampshire Liberty Alliance is a non-partisan coalition working to increase individual liberty, and encourage citizen involvement in the legislative process. Bills on the Gold Standard are evaluated based on their effects on, among other things; civil liberties, personal responsibility, property rights, accountability, constitutionality, and taxation. Roll call votes on Gold Standard bills are the foundation for our annual Liberty Rating report card.")

    self.document.insert_style(_style_page, automatic = True)
    self.document.insert_style(_style_master)
    self.document.insert_style(_style_footer)
     
    footer=_style_master.set_footer(p)
    print footer
#    footer.append_element(p)

   
  def save(self, name):
    self.document.save(target=name) 
