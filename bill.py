import re

#
# This regular expression is splits apart a bill number string into meaningful
# pieces.
#
Title_Leading_Whitespace=1
Bill_Prefix=2               # Typically SB, HB, HCR, etc
Post_Prefix_Whitespace=3
Bill_Numeric_Portion=4
Post_Numeric_Whitespace=5
Post_Numeric_Suffix=6       # If present, typically -FN, or -LOCAL, etc

Bill_Number_Pattern = re.compile(
  '(\s*)([A-Za-z\-]*)(\s*)(\d*)(\s*)([A-Za-z\-]*)')

#
# Removes leading whitespace. Capitalizes all letters. Inserts single
# whitespace beteween prefix and number .. e.g. '  Sb  456' becomes
# 'SB 456'
#
def Normalize_Bill_Number(Bill_Number):
  m = Bill_Number_Pattern.match(Bill_Number)

  return m.group(Bill_Prefix).upper() + ' ' +\
    m.group(Bill_Numeric_Portion).upper()+m.group(Post_Numeric_Suffix).upper()

#
# Tables a normalized bill number and removes all text after the numeric
# portion of the bill (typically where things like -FN or Local are)
#
def Brief_Bill_Number(Bill_Number, Separator=' '):
  m = Bill_Number_Pattern.match(Bill_Number)

  return m.group(Bill_Prefix).upper() + Separator + m.group(Bill_Numeric_Portion)


class Bill:

  def __init__(self, Number, Title, Committee, Committee_Recommendation,
               Liberty_Type, NHLA_Summary, NHLA_Recommendation, GS_Blurb):
   self.Number = Number
   self.Title = Title
   self.Committee = Committee
   self.Committee_Recommendation = Committee_Recommendation
   self.Liberty_Type = Liberty_Type
   self.NHLA_Summary = NHLA_Summary
   self.NHLA_Recommendation = NHLA_Recommendation
   self.GS_Blurb = GS_Blurb

  def Get_Bill_Number(self):
    return self.Number

  def __cmp__(self, other):
    Groups_A=Number_A=Bill_Number_Pattern.match(self.Number)
    Groups_B=Bill_Number_Pattern.match(other.Number)

    Prefix_A = Groups_A.group(Bill_Prefix)
    Prefix_B = Groups_B.group(Bill_Prefix)
    Number_A = Groups_A.group(Bill_Numeric_Portion)
    Number_B = Groups_B.group(Bill_Numeric_Portion)
#    Prefix_A, Number_A = self.Number.split()
#    Prefix_B, Number_B = other.Number.split()

    return cmp(Prefix_A, Prefix_B) or cmp(int(Number_A), int(Number_B))
