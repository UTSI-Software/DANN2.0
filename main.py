#!/usr/bin/env python
import os
import time
import tkinter as tk
from tkinter import filedialog, Text
import pandas as pd
import pdfquery
import PyPDF2


def ExtractMetaData(path):
    """
    Extracts metadata from a PDF file.

    Args:
    - path (str): Path to the PDF file.

    Returns:
    dict: Dictionary containing metadata information (Title, Path, Author, Creation Date, Subject, Creator).
    """
    # Open the PDF file in binary mode
    with open(path, 'rb') as file:
        # Create a PDF reader object
        pdf = PyPDF2.PdfReader(file)
        
        # Retrieve metadata from the PDF
        metadata = pdf.metadata  # Access it as an attribute

        # Access specific metadata properties
        author = metadata.author
        creator = metadata.creator
        # creation_date = metadata.get('/CreationDate', 'Unknown')
        creation_date = os.path.getctime(path)  # Get creation date of the file
        creation_datetime = time.ctime(creation_date)  # Convert creation date to human-readable format
        subject = metadata.subject
        title = os.path.basename(path).split('/')[-1]  # Extract the file name from the path

    # Return metadata as a dictionary
    return {"Title": title, "Path": path, "Author": author, "Creation Date": creation_datetime, "Subject": subject,
            "Creator": creator}

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

def WriteToExcel(data, output_path='output_data.xlsx'):
    data_list = [data]
    metadata_df = pd.DataFrame(data_list)
    metadata_df.to_excel(output_path, index=False)

def ProcessPDFs(pdf_directory, keywords_excel_path):
    # Load the PDF files using pdfquery
    pdf_files = [file for file in os.listdir(pdf_directory) if file.endswith('.pdf')]

    # Read keywords from the Excel sheet
    keywords_df = pd.read_excel(keywords_excel_path)
    keyword_list = keywords_df['Keywords'].tolist()
    # Process each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)

        # Load the PDF file using pdfquery
        pdf = pdfquery.PDFQuery(pdf_path)
        #choose pdf2 or pdfquery
        pdf.load()
        pdf.tree.write('pdfXML.txt', pretty_print = True)
        #Collect Metadata
        metadata_list = ExtractMetaData(pdf_path)
        #Check for keywords
        populate_keywords(pdf, keyword_list)
        #Check for clients
        # Write metadata to Excel
        
        # output_path = os.path.join(output_directory, f"{os.path.splitext(pdf_file)[0]}_output.xlsx")
        WriteToExcel(metadata_list)

def populate_keywords(pdf, keyword_list):      # Extract text containing the keywords
        extracted_text = ""
        for keyword in keyword_list:
            text = pdf.pq('LTTextLineHorizontal:contains("' + keyword + '")')
            # extracted_text += f"Keyword: {keyword}\n"
            # ExtractElements(text)
            



def ReadFromExcel(path):
    return pd.read_excel(path)

# Process multiple PDFs
path = "C:\\Users\\cjw\\Desktop\\testpdfs"
keywords_excel_path = "C:\\Users\\cjw\\Desktop\\GitHub\\DANN2.0\\Keywords.xlsx"
ProcessPDFs(path, keywords_excel_path)

# # # Write metadata to Excel
# metadata_list = ExtractMetaData(path) 
# WriteToExcel(metadata_list)


#####################################################################
