#!/usr/bin/env python
import gspread
import argparse
import json
import logging
from reportlab_goldstandard import generate

import bill

import re

#from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import GoogleCredentials


#
# These items must match the column titles in the googlesheet that we use
# collaborate on the Goldstandard
#
Bill_Number_Header = "Bill #"
Title_Header = "Title"
Committee_Name_Header = "Committee Name"
Committee_Recommendation_Header = "Committee Recommendation"
NHLA_Recommendation_Header = "NHLA Recommendation"
Pro_Anti_Liberty_Header = "Pro/Anti Liberty"
NHLA_Summary_Header = "NHLA Summary"
Bullets_Header = "Bullets"
Contributors_Header="Contributors"




def Bill_Is_DNI(NHLA_Recommendation):
  #
  # Checks the given NHLA_Recommendation and returns true of the recommendation
  # indicates that the bill is a "Do Not Include" for the Goldstandard.
  #
  return 'DNI' in NHLA_Recommendation.upper()

def Normalize_Sheet_Data(Item):
  #
  # Given an item from the googlesheets collaoration sheet, this function
  # normalizes the item into into an ASCII string if possible and if not
  # possible, then it returns a null string
  #
  if type(Item) == type(str()):
    return Item
  elif type(Item) == type(u""):
    return Item.encode('ascii','ignore')
  else:
    return ""


def Create_Goldstandard_From_Sheet(
  Sheet_URL, GS_Title, Filename, JSON_Key_File, Background_Color):

  json_key = json.load(open('NHLAGS-e8b3911072d5.json'))
  scope = ['https://spreadsheets.google.com/feeds']

  credentials = GoogleCredentials.get_application_default()
  credentials = credentials.create_scoped(scope)

  gss_client = gspread.authorize(credentials)

  sht1 = gss_client.open_by_url(Sheet_URL)

  Bill_List = []
  All_Data = sht1.sheet1.get_all_records()
  #
  # Each time through this loop, we grab the bill information
  # for a single bill from the worksheet. If the bill is not
  # explicitly excluded based on the NHLA recommendation, then
  # we include it in the bill list
  #
  for Sheet_Bill in All_Data:
    Bill_Number = bill.Normalize_Bill_Number(Sheet_Bill[Bill_Number_Header])
    Title = Normalize_Sheet_Data(Sheet_Bill[Title_Header])
    Committee = Normalize_Sheet_Data(Sheet_Bill[Committee_Name_Header])
    Committee_Recommendation = Normalize_Sheet_Data(
      Sheet_Bill[Committee_Recommendation_Header])
    NHLA_Recommendation = Normalize_Sheet_Data(
      Sheet_Bill[NHLA_Recommendation_Header])
    Liberty_Type = Normalize_Sheet_Data(Sheet_Bill[Pro_Anti_Liberty_Header])
    NHLA_Summary = Normalize_Sheet_Data(Sheet_Bill[NHLA_Summary_Header])
    Bullets = Normalize_Sheet_Data(Sheet_Bill[Bullets_Header])

    if not Bill_Is_DNI(NHLA_Recommendation):

      This_Bill = bill.Bill(Number=Bill_Number, Title=Title,
                            Committee=Committee,
                            Committee_Recommendation=Committee_Recommendation,
                            Liberty_Type=Liberty_Type,
                            NHLA_Summary=NHLA_Summary,
                            NHLA_Recommendation = NHLA_Recommendation,
                            GS_Blurb=Bullets)

      Bill_List.append(This_Bill)
    else:
      logging.info(Bill_Number + \
        ' excluded because DNI found in recommendation')

  #
  # So, at this point we have a list with the current data from
  # the sheet excluding only those bills that were explicitly excluded.
  #
  Bill_List.sort()
  gs = generate.Goldstandard(title=Title,filename=Filename,
                             background=Background_Color)

  gs.Set_Bills(Bill_List)
  gs.save()



if __name__ == "__main__":


  parser = argparse.ArgumentParser(description="")
  parser.add_argument("url")
  parser.add_argument("title")
  parser.add_argument("filename")
  parser.add_argument("--gold", help="Makes the background gold",
                      action="store_true")
  args = parser.parse_args()

  logging.basicConfig(filename='gs_generation.log',level=logging.INFO)
  if args.gold:
    Background_Color=generate.White
  else:
    Background_Color=generate.Gold

  Create_Goldstandard_From_Sheet(
    Sheet_URL=args.url,
    GS_Title=args.title,
    Filename=args.filename,
    JSON_Key_File='NHLAGS-e8b3911072d5.json',
    Background_Color=Background_Color)
