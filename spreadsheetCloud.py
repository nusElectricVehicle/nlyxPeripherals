'''
This is the docs used. Signed in using willoughby.nuseco@gmail.com
https://docs.google.com/spreadsheets/d/12OdxolUzGm2LjfO5vwwMhhdhNAUsxQ7rdyF8dbFmCyE/edit#gid=0

Created on: 16 October 2020
Created by: Willoughby Niki (lynxDigital)
Last edited: 
'''

import numpy as np
import cv2

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("EcoCarSpreadsheetCars").sheet1

'''
We use ".sheet1" to mean the first sheet. Regardless of the sheet name.


'''

#Only put these in the loop
#This definiteion extracts and prints all of the values

def fetchData():
    list_of_hashes = sheet.get_all_records()
    print(list_of_hashes)


fetchData()
