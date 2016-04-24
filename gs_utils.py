import os
import gspread
from oauth2client.client import GoogleCredentials



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


def get_sheet(Sheet_URL, JSON_Key_File):
    """
    Given a Sheet_URL to a googlesheet, this function builds a Gold Standard
    PDF File of the given Filename. The title of the standard (As it appears
    within the PDF file) is within GS_Title.

    JSON_Key_File provides the path to a .json file that is suitible to act as
    credentials that provide at least read access to the sheet.

    Returns the gspread sheet at the given URL
    """
    scope = ['https://spreadsheets.google.com/feeds']

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = JSON_Key_File
    credentials = GoogleCredentials.get_application_default()
    credentials = credentials.create_scoped(scope)
    gss_client = gspread.authorize(credentials)
    return gss_client.open_by_url(Sheet_URL)
