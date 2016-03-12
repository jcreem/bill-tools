class Bill:
  Number=""
  Title=""
  Committee=""
  Majority_Recommendation=""
  Committee_Vote=""
  Committee_Comments=""

  def __init__(self, Number, Title, Committee, Majority_Recommendation, Committee_Vote, Liberty_Type, NHLA_Recommendation, GS_Blurb):
   self.Number = Number
   self.Title = Title
   self.Committee = Committee
   self.Majority_Recommendation = Majority_Recommendation
   self.Committee_Vote = Committee_Vote
   self.Liberty_Type = Liberty_Type
   self.NHLA_Recommendation = NHLA_Recommendation
   self.GS_Blurb = GS_Blurb
  
  def Get_Bill_Number(self):
    return self.Number

  def __cmp__(self, other):
    Prefix_A, Number_A = self.Number.split()
    Prefix_B, Number_B = other.Number.split()

    return cmp(Prefix_A, Prefix_B) or cmp(int(Number_A), int(Number_B))
