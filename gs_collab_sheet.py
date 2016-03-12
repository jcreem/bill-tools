#!/usr/bin/env python
import gspread
import argparse
import json

#from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import GoogleCredentials

parser = argparse.ArgumentParser(description="")
parser.add_argument("url")
args = parser.parse_args()

json_key = json.load(open('NHLAGS-e8b3911072d5.json'))
scope = ['https://spreadsheets.google.com/feeds']

#credentials = ServiceAccountCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
credentials = GoogleCredentials.get_application_default()
credentials = credentials.create_scoped(scope)

gss_client = gspread.authorize(credentials)

sht1 = gss_client.open_by_url(args.url)

