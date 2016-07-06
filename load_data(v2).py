""" 
Reading data file by ElementTree package which could used to process XML file in python. 
"""
from xml.etree import ElementTree

def load_file(filename):
    # Loading XML file
    document = ElementTree.parse(filename)
    return document
    
def separate_data_label(document):   
    
    chars = ',.?<>?:;{}[]|!@#$%^&*()-_+='                                              # List of unwant character         
    # Saving id of Reports
    id_doc = list(doc.attrib['id'] for doc in document.findall('doc'))
    # Saving label which classified by CMC_MAJORITY
    label = list(code.text for code in document.findall('doc/codes/code') if 
             code.attrib['origin'] == 'CMC_MAJORITY')
    # Saving text document for Neural Network
    text_data = list(text.text.split() for text in document.findall('doc/texts/text')) # Extracting sentences
    text_data = [item for sublist in text_data for item in sublist]                    # Turn multi-dimension array in 1D array
    # Find all unwant character and place them with space
    for index in range(len(text_data)):
        for char in chars:
            text_data[index] = text_data[index].replace(char," ") 
            
    text_data = filter(None, text_data)        
       
    return id_doc, label, text_data
    