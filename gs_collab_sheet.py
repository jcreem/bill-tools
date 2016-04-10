#!/usr/bin/env python
""" gs_collab_sheet.py: This module parses Gold Standard Collaboration
    worksheets and generates a well formatted PDF."""

import os
import re
import argparse
import logging

import gspread
from reportlab_goldstandard import generate
from oauth2client.client import GoogleCredentials

import bill


__author__      = "Jeffrey Creem"
__copyright__   = "Copyright 2016"
__license__     = "Mozilla Public License 2.0"


#
# These items must match the column titles in the googlesheet that we use
# collaborate on the Goldstandard. The columns in the sheet may be in any
# order and additional columns may be added.
#
Bill_Number_Header                  = "Bill #"
Title_Header                        = "Title"
Committee_Name_Header               = "Committee Name"
Committee_Recommendation_Header     = "Committee Recommendation"
NHLA_Recommendation_Header          = "NHLA Recommendation"
Pro_Anti_Liberty_Header             = "Pro/Anti Liberty"
NHLA_Summary_Header                 = "NHLA Summary"
Bullets_Header                      = "Bullets"
Contributors_Header                 = "Contributors"




def Bill_Is_DNI(NHLA_Recommendation):
  """
  Checks the given NHLA_Recommendation and returns true of the recommendation
  indicates that the bill is a "Do Not Include" for the Goldstandard.
  """
  return 'DNI' in NHLA_Recommendation.upper()

def Normalize_Sheet_Data(Item):
  """
  Given an item from the googlesheets collaoration sheet, this function
  normalizes the item into into an ASCII string if possible and if not
  possible, then it returns a null string
  """
  if type(Item) == type(str()):
    Return_Item = Item
  elif type(Item) == type(u""):
    Return_Item = Item.encode('ascii','ignore')
  else:
    Return_Item = ""

  return Return_Item

def To_Contributor_List(Bill_Contributors):
    """
    Given a string from the collaboration sheet that lists the contributors for
    a bill in a single string, this function parses the string and returns a
    list of each contributor
    """
    return Bill_Contributors.split(",")

def Create_Goldstandard_From_Sheet(
  Sheet_URL, GS_Title, Filename, JSON_Key_File, Background_Color):
  """
  Given a Sheet_URL to a googlesheet, this function builds a Gold Standard
  PDF File of the given Filename. The title of the standard (As it appears
  within the PDF file) is within GS_Title.

  JSON_Key_File provides the path to a .json file that is suitible to act as
  credentials that provide at least read access to the sheet. 

  The PDF will utilize the the given Background_Color

  Returns a Dictionary containing
  {Contributors : Set of contributors to the goldstandadard including DNI,
   Last_Update  : Date that the sheet was last updated}
  """

  scope = ['https://spreadsheets.google.com/feeds']

  os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = JSON_Key_File
  credentials = GoogleCredentials.get_application_default()
  credentials = credentials.create_scoped(scope)

  gss_client = gspread.authorize(credentials)

  sht1 = gss_client.open_by_url(Sheet_URL)


  #
  # Bill list will hold the bill data for the Gold Standard and it exlcudes
  # all bills that are marked as Do Not Include (DNI)
  #
  Bill_List = []

  Contributor_Set=set([])
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
    #
    # Note we call this contributors. Most often there is a single name per
    # bill but at times people collaborate so we allow for there to be
    # multiple people contributing to the bill.
    #
    Contributors = To_Contributor_List(Normalize_Sheet_Data(
      Sheet_Bill[Contributors_Header]))

    #
    # Add each contributor from this bill to the contributor Set
    #
    for Contributor in Contributors:
        if Contributor != "":
            Contributor_Set.add(Contributor.strip())

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
  # Bill_List.sort()
  gs = generate.Goldstandard(title=GS_Title, filename=Filename,
                             background=Background_Color)

  gs.Set_Bills(Bill_List)
  gs.save()

  return {'Contributors' : Contributor_Set,
          'Last_Update'  : sht1.sheet1.updated}


if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="")
  parser.add_argument("url")
  parser.add_argument("title")
  parser.add_argument("filename")
  parder.add_argument("json_filename")
  parser.add_argument("--gold", help="Makes the background gold",
                      action="store_true")
  args = parser.parse_args()

  logging.basicConfig(filename='gs_generation.log',level=logging.INFO)

  if args.gold:
    Background_Color=generate.Gold
  else:
    Background_Color=generate.White

  Create_Goldstandard_From_Sheet(
    Sheet_URL=args.url,
    GS_Title=args.title,
    Filename=args.filename,
    JSON_Key_File=args.json_filename,
    Background_Color=Background_Color)
