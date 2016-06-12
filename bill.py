import re
""" bill.py: This module contains a class and utilities for dealing with
             bills as they pertain to the Goldstandard.
             """
#
# This regular expression is splits apart a bill number string into meaningful
# pieces. Each of the defined values below specifies the match index of
# a portion of
#
Title_Leading_Whitespace=1  # Optional whitespace
Bill_Prefix=2               # Typically SB, HB, HCR, etc
Post_Prefix_Whitespace=3    # Optional whitespace
Bill_Numeric_Portion=4      # The numeric portion of the bill
Post_Numeric_Whitespace=5   # Potential whitespace before any suffix
Post_Numeric_Suffix=6       # If present, typically -FN, or -LOCAL, etc

Bill_Number_Pattern = re.compile(
  '(\s*)([A-Za-z\-]*)(\s*)(\d*)(\s*)([A-Za-z\-]*)')

#

#
def Normalize_Bill_Number(Bill_Number):
  """
  Removes leading whitespace. Capitalizes all letters. Inserts single
  whitespace beteween prefix and number .. e.g. '  Sb  456' becomes
  'SB 456'
  """
  try:
    m = Bill_Number_Pattern.match(Bill_Number)
    Return_Value= m.group(Bill_Prefix).upper() + ' ' +\
      m.group(Bill_Numeric_Portion).upper()+m.group(Post_Numeric_Suffix).upper()
  except:
    Return_Value="Malformed Bill# "

  return Return_Value


def Brief_Bill_Number(Bill_Number, Separator=' '):
  """
  Takes a normalized bill number string and removes all text after the numeric
  portion of the bill (typically where things like -FN or Local are). If
  significant issues are found then an error string will be returned instead.
  """
  try:
    m = Bill_Number_Pattern.match(Bill_Number)
    Return_Value=m.group(Bill_Prefix).upper() + Separator + m.group(Bill_Numeric_Portion)
  except:
    Return_Value="Malformed Bill#"

  return Return_Value

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

    #
    # It is almost always the case that what we are dealing with here
    # is something like HB 123 or SB 456 or some other small text followed
    # by a numeric prefix. But occasionally,  we need something special
    # and the bill is not a true bill number at all.
    # For now, we will arbitrarily just choose to do comparisons as
    # strings if we get errors trying to look at these as normal bills
    #
    Prefix_A = Groups_A.group(Bill_Prefix)
    Prefix_B = Groups_B.group(Bill_Prefix)
    Number_A = Groups_A.group(Bill_Numeric_Portion)
    Number_B = Groups_B.group(Bill_Numeric_Portion)
    
    try: 
      return cmp(Prefix_A, Prefix_B) or cmp(int(Number_A), int(Number_B))
    except:
      return cmp(self.Number, other.Number)
