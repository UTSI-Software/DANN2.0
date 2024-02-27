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
        pdf_reader = PyPDF2.PdfReader(file)

        # Retrieve metadata from the PDF
        metadata = pdf_reader.metadata  # Access it as an attribute

        # Access specific metadata properties
        author = metadata.author
        creator = metadata.creator
        creation_date = metadata.get('/CreationDate', 'Unknown')
        creation_date = os.path.getctime(path)  # Get creation date of the file
        creation_datetime = time.ctime(creation_date)  # Convert creation date to human-readable format
        subject = metadata.subject
        title = os.path.basename(path).split('/')[-1]  # Extract the file name from the path

    # Return metadata as a dictionary
    return {"Title": title, "Path": path, "Author": author, "Creation Date": creation_datetime, "Subject": subject,
            "Creator": creator}

def ExtractElements(text):
    """
    Extracts and prints text elements from a PDF.

    Args:
    - text: Text elements obtained from PDFQuery.

    Prints:
    - Extracted text and coordinates for each text element.
    """
    # Print the extracted text
    print("Extracted Text:")
    for text_element in text:
        extracted_text = text.text()
        print("- ", extracted_text)

        # Extract coordinates for each text element
        x0 = float(text_element.attrib['x0'])
        y0 = float(text_element.attrib['y0'])
        x1 = float(text_element.attrib['x1'])
        y1 = float(text_element.attrib['y1'])

        print("  Coordinates: x0={}, y0={}, x1={}, y1={}".format(x0, y0, x1, y1))

def WriteToExcel(data, output_path='output_data.xlsx'):
    data_list = [data]
    metadata_df = pd.DataFrame(data_list)
    metadata_df.to_excel(output_path, index=False)

def ProcessPDFs(pdf_directory, keywords_excel_path, output_directory):
    # Load the PDF files using pdfquery
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

    # Read keywords from the Excel sheet
    keywords_df = pd.read_excel(keywords_excel_path)
    keyword_list = keywords_df['Keywords'].tolist()

    # Process each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)

        # Load the PDF file using pdfquery
        pdf = pdfquery.PDFQuery(pdf_path)
        pdf.load()

        # Extract text containing the keywords
        extracted_text = ""
        for keyword in keyword_list:
            text = pdf.pq('LTTextLineHorizontal:contains(' + keyword + ')')
            extracted_text += f"Keyword: {keyword}\n"
            ExtractElements(text)

        # Write metadata to Excel
        metadata_list = ExtractMetaData(pdf_path)
        output_path = os.path.join(output_directory, f"{os.path.splitext(pdf_file)[0]}_output.xlsx")
        WriteToExcel(metadata_list, output_path)

def ReadFromExcel(path):
    return pd.read_excel(path)

# # Path to the PDF file
# path = "C:/Users/bkl/Desktop/UTSI Quotations Sample/Q2023130-Citgo IRP and TTX_Combined (26 Oct 23).pdf"

# # Load the PDF file using pdfquery
# pdf = pdfquery.PDFQuery(path)
# pdf.load()

# # Extract text containing the keyword "gas"
# keyword = "gas"
# text = pdf.pq('LTTextLineHorizontal:contains(' + keyword + ')')
# ExtractElements(text)

# # Write metadata to Excel
# metadata_list = ExtractMetaData(path)
# WriteToExcel(metadata_list)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("1000x500")
        self.createWidgets()
    
    def createWidgets(self):
        # Quit button
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=0, column=0, sticky="ew")

        # Directory selection buttons
        self.select_pdf_button = tk.Button(self, text="Select PDF Directory", command=self.select_pdf_directory)
        self.select_pdf_button.grid(row=1, column=0, pady=10, sticky="ew")

        self.select_keywords_button = tk.Button(self, text="Select Keywords Excel", command=self.select_keywords_excel)
        self.select_keywords_button.grid(row=2, column=0, pady=10, sticky="ew")

        self.select_output_button = tk.Button(self, text="Select Output Directory", command=self.select_output_directory)
        self.select_output_button.grid(row=3, column=0, pady=10, sticky="ew")

        # Label to display selected directory
        # self.directory_label = tk.Label(self, text="#")
        # self.directory_label.grid(row=2, column=0, pady=5)

        # Text widget to display output
        self.output_text = Text(self, height=20, width=50)
        self.output_text.grid(row=3, column=0, pady=10)

        # Additional labels for selected directories
        self.pdf_label = tk.Label(self, text="")
        self.pdf_label.grid(row=4, column=0, pady=5)

        self.keywords_label = tk.Label(self, text="")
        self.keywords_label.grid(row=5, column=0, pady=5)

        self.output_label = tk.Label(self, text="")
        self.output_label.grid(row=6, column=0, pady=5)



    def select_pdf_directory(self):
        self.pdf_directory = filedialog.askdirectory()
        if self.pdf_directory:
            self.pdf_label.config(text=f"Selected PDF Directory: {self.pdf_directory}")

    def select_keywords_excel(self):
        self.keywords_excel_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if self.keywords_excel_path:
            self.keywords_label.config(text=f"Selected Keywords Excel: {self.keywords_excel_path}")

    def select_output_directory(self):
        self.output_directory = filedialog.askdirectory(initialdir="./")  # Set a default location
        if self.output_directory:
            self.output_label.config(text=f"Selected Output Directory: {self.output_directory}")

    def run_functions_on_directory(self):
        if hasattr(self, 'pdf_directory') and hasattr(self, 'keywords_excel_path') and hasattr(self, 'output_directory'):
            ProcessPDFs(self.pdf_directory, self.keywords_excel_path, self.output_directory)


def main():
    root = tk.Tk()
    root.title('DANN 2.0 Path Selector')
    app = Application(master=root)
    app.grid(sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    app.mainloop()

if __name__ == "__main__":
    main()



#####################################################################
