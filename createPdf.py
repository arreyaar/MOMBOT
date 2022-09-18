# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:02:33 2022

@author: iaman
"""

from fpdf import FPDF
import textwrap

def createPDF(fileName):
    pdf = FPDF()  
    # Add a page
    pdf.add_page()
    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size = 12)
     
    # open the text file in read mode
    f = open(fileName, "r")
    
    wrapper = textwrap.TextWrapper(width=101)
     
    # insert the texts in pdf
    for x in f:
        word_list = wrapper.wrap(text=x)
        for line in word_list:
            pdf.cell(200, 10, txt = line, ln = 1, align = 'L')
      
    # save the pdf with name .pdf
    pdf.output("minutes.pdf")  
