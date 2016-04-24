#!/usr/bin/env python
""" decorate_gs_collab_sheet.py: Given an existing google docs gold standard
    collabration sheet, this module will decorate it by adding information
    from various data sources.
"""

import os
import argparse
import gspread
import bill
import gs_utils


__author__      = "Jeffrey Creem"
__copyright__   = "Copyright 2016"
__license__     = "Mozilla Public License 2.0"

Bill_Text_URL_Prefix="http://wwww.nhliberty.org/bulls/view/2016"


def Decorate(Sheet_URL, JSON_Key_File):
    """
    Given a Sheet_URL to a googlesheet, this function populates field of the
    sheet with information from various data sources

    JSON_Key_File provides the path to a .json file that is suitible to act as
    credentials that provide at write access to the sheet.

    """

    sht1=gs_utils.get_sheet(Sheet_URL, JSON_Key_File)
    All_Data = sht1.sheet1.get_all_records()
    for Sheet_Bill in All_Data:
        print Sheet_Bill
        Bill_Number = bill.Normalize_Bill_Number(
            Sheet_Bill[gs_utils.Bill_Number_Header])
        Bill_Number_URL_Name=bill.Brief_Bill_Number(Bill_Number,'')
        Bill_URL=Bill_Text_URL_Prefix + '/' + Bill_Number_URL_Name
        print Bill_URL


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("url")
    parser.add_argument("json_filename")

    args = parser.parse_args()


    Decorate(
    Sheet_URL=args.url,
    JSON_Key_File=args.json_filename)
