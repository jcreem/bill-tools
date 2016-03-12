#!/usr/bin/env python
import gspread
import argparse
import json

from oauth2client.client import SignedJwtAssertionCredentials

parser = argparse.ArgumentParser(description="")
parser.add_argument("url")
args = parser.parse_args()

json_key = json.load(open('NHLAGS-e8b3911072d5.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

gss_client = gspread.authorize(credentials)

sht1 = gss_client.open_by_url(args.url)

