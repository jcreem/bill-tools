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


def Normalize_Bill_Number(Bill_Number):
  p = re.compile('(\s*)([A-Za-z]*)(\s*)(\d*)')
  m = p.match(Bill_Number)
#  print m.group(1) + '_' +m.group(2) + '_' + m.group(3) + m.group(4)
  return m.group(2) + ' ' + m.group(4)

def Bill_Is_DNI(NHLA_Recommendation):
  return 'DNI' in NHLA_Recommendation

def Normalize_Sheet_Data(Item):
    if type(Item) == type(str()):
      return Item
    elif type(Item) == type(u""):
      return Item.encode('ascii','ignore')
    else:
      #      print type(Item)
      #           print Item.encode('ascii','ignore')
      return ""


Bill_Number_Header = "Bill #"
Title_Header = "Title"
Committee_Name_Header = "Committee Name"
Committee_Recommendation_Header = "Committee Recommendation"
NHLA_Recommendation_Header = "NHLA Recommendation"
Pro_Anti_Liberty_Header = "Pro/Anti Liberty"
NHLA_Summary_Header = "NHLA Summary"
Bullets_Header = "Bullets"
Contributors_Header="Contributors"

parser = argparse.ArgumentParser(description="")
parser.add_argument("url")
parser.add_argument("title")
parser.add_argument("filename")
parser.add_argument("--gold", help="Makes the background gold",
 action="store_true")
args = parser.parse_args()

logging.basicConfig(filename='gs_generation.log',level=logging.INFO)

json_key = json.load(open('NHLAGS-e8b3911072d5.json'))
scope = ['https://spreadsheets.google.com/feeds']

#credentials = ServiceAccountCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
credentials = GoogleCredentials.get_application_default()
credentials = credentials.create_scoped(scope)

gss_client = gspread.authorize(credentials)

sht1 = gss_client.open_by_url(args.url)


Bill_List = []
All_Data = sht1.sheet1.get_all_records()
#
# Each time through this loop, we grab the bill information
# for a single bill from the worksheet. If the bill is not
# explicitly excluded based on the NHLA recommendation, then
# we include it in the bill list
#
for Sheet_Bill in All_Data:
  Bill_Number = Normalize_Bill_Number(Sheet_Bill[Bill_Number_Header])
  Title = Normalize_Sheet_Data(Sheet_Bill[Title_Header])
  Committee = Normalize_Sheet_Data(Sheet_Bill[Committee_Name_Header])
  Committee_Recommendation = Normalize_Sheet_Data(Sheet_Bill[Committee_Recommendation_Header])
  NHLA_Recommendation = Normalize_Sheet_Data(Sheet_Bill[NHLA_Recommendation_Header])
  Liberty_Type = Normalize_Sheet_Data(Sheet_Bill[Pro_Anti_Liberty_Header])
  NHLA_Summary = Normalize_Sheet_Data(Sheet_Bill[NHLA_Summary_Header])
  Bullets = Normalize_Sheet_Data(Sheet_Bill[Bullets_Header])

  if not Bill_Is_DNI(NHLA_Recommendation):

    This_Bill = bill.Bill(Number=Bill_Number, Title=Title, Committee=Committee,
                     Committee_Recommendation=Committee_Recommendation,
                     Liberty_Type=Liberty_Type,
                     NHLA_Summary=NHLA_Summary,
                     NHLA_Recommendation = NHLA_Recommendation,
                     GS_Blurb=Bullets)

    Bill_List.append(This_Bill)
  else:
    logging.info(Bill_Number + ' excluded because DNI found in recommendation')

#
# So, at this point we have a list with the current data from
# the sheet excluding only those bills that were explicitly excluded.
#
Bill_List.sort()
if args.gold:
  gs = generate.Goldstandard(title=args.title,filename=args.filename,background=generate.Gold)
else:
  gs = generate.Goldstandard(title=args.title,filename=args.filename,background=generate.White)

gs.Set_Bills(Bill_List)
gs.save()
#for GS_Bill in Bill_List:
#  print GS_Bill.Number
