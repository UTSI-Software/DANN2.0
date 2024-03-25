#!/usr/bin/env python
import os
import time
import tkinter as tk
from tkinter import filedialog, Text
import pandas as pd
import pdfquery
import PyPDF2

# TODO: 
# add each client found to a client column
# fetch all PDFs in output excel (zip?)
# make a client reference list (compare values gotten from path and reference list)


def ExtractMetaData(path, data_dict):
    # Open the PDF file in binary mode
    with open(path, 'rb') as file:
        creation_date = os.path.getctime(path)  # Get creation date of the file
        creation_datetime = time.ctime(creation_date)  # Convert creation date to human-readable format
        title = os.path.basename(path).split('/')[-1]  # Extract the file name from the path
        data_dict["Date"] = creation_datetime
        data_dict["Title"] = title
    
    # Return metadata as a dictionary
    

# Text should grab whole document content excluding metadata but grabs relevant parts of PDF
def ExtractElements(text):
    """
    Extracts and prints text elements from a PDF.

    Args:
    - text: Text elements obtained from PDFQuery.

    Prints:
    - Extracted text and coordinates for each text element.
    """

    outputtext = []
    coords = []
    # Print the extracted text
    print("Extracted Text:")
    for text_element in text:
        extracted_text = text.text()
        print("- ", text_element.text)
        outputtext.append(text_element.text)

        # Extract coordinates for each text element
        x0 = float(text_element.attrib['x0'])
        y0 = float(text_element.attrib['y0'])
        x1 = float(text_element.attrib['x1'])
        y1 = float(text_element.attrib['y1'])

        coords.append((x0, y0, x1, y1))

        print("  Coordinates: x0={}, y0={}, x1={}, y1={}".format(x0, y0, x1, y1))

    return(coords, outputtext)

def WriteToExcel(data_list, output_path='output_data.xlsx'):
    metadata_df = pd.DataFrame(data_list)
    length = len(data_list)
    metadata_df.iloc[length-1]
    metadata_df.to_excel(output_path, index=False)

def ProcessPDFs(pdf_directory, keywords_excel_path, dict_list):
    # Load the PDF files using pdfquery
    pdf_files = [file for file in os.listdir(pdf_directory) if file.endswith('.pdf')]

    # Read keywords from the Excel sheet
    keywords_df = pd.read_excel(keywords_excel_path)
    keyword_list = keywords_df['Keywords'].tolist()

    client_list = keywords_df['Clients'].tolist()
    # Process each PDF file
    for pdf_file in pdf_files:
        # create a new dictionary to house each pdf files info
        my_dict={}
        pdf_path = os.path.join(pdf_directory, pdf_file)
        my_dict["Path"] = pdf_path
        # Load the PDF file using pdfquery
        pdf = pdfquery.PDFQuery(pdf_path)
        #choose pdf2 or pdfquery
        pdf.load()
        pdf.tree.write('pdfXML.txt', pretty_print = True)
        #Collect Metadata
        ExtractMetaData(pdf_path, my_dict)
        #Check for keywords
        populate_keywords(pdf, keyword_list, my_dict, "Keywords")
        #Check for clients
        populate_keywords(pdf, client_list, my_dict, "Clients")
        # append this specific pdf's dictionary to the dicitonary list (dict_list)
        dict_list.append(my_dict)        

def populate_keywords(pdf, word_list, my_dict, column_name):      # Extract text containing the keywords
    found_words = []
    for word in word_list:
        # if (pdf.pq('LTTextLineHorizontal:contains("' + keyword + '")')):
            # found_words.append(keyword)
        if not pd.isnull(word):
            if (pdf.pq('LTPage:contains("' + word + '")')):
                found_words.append(word)
    my_dict[column_name] = " ,".join(found_words)


def ReadFromExcel(path):
    return pd.read_excel(path)

# Process multiple PDFs
path = "C:\\Users\\cjw\\Desktop\\testpdfs"
keywords_excel_path = "C:\\Users\\cjw\\Desktop\\GitHub\\DANN2.0\\Keywords.xlsx"
dict_list = []
ProcessPDFs(path, keywords_excel_path, dict_list)
WriteToExcel(dict_list)

#####################################################################
