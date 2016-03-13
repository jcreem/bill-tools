class Bill:

  def __init__(self, Number, Title, Committee, Committee_Recommendation, Liberty_Type, NHLA_Summary, NHLA_Recommendation, GS_Blurb):
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
    Prefix_A, Number_A = self.Number.split()
    Prefix_B, Number_B = other.Number.split()

    return cmp(Prefix_A, Prefix_B) or cmp(int(Number_A), int(Number_B))
