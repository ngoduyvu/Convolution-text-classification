from xml.dom import minidom
import pandas as pd
import numpy as np
import re

def load_file(filename):
    # Loading XML file
    xmldoc = minidom.parse(filename)
    return xmldoc

# Clear all the unwant sign and lower the string.
def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

# One hot encoding label data
def label_encoding(labels_docs, multi_label):
    
    labels = np.asarray(labels_docs)                           # Convert normal array to numpy to do one_hot_encoding
    df = pd.DataFrame(labels, columns=['label'])               # Create data frame
    if multi_label:
        labels = df['label'].str.get_dummies(sep='*')          # Create dummies from column with multiple values                            
    else:
        labels = df['label'].str.strip('*').str[0].str.get_dummies()       # Only take one label for each document
    return labels

# Processing Data for Convolution Neural Network
def separate_data_label(document):
    
    counter = 0         # Counter how many label of each document
    ids = []            # List store id of documents
    label_docs = []     # List store label classified by CMC_MAJORITY
    text_docs = []      # List store text data for neural network
    
    text_store = []                                  # Temporary store text
    label_store = []                                 # Temporary store labels
    
    del ids[:]                                       # Reset the store array in case run the program multiple times
    del text_docs[:]                                 # Reset the store array in case run the program multiple times
    del label_docs[:]                                # Reset the store array in case run the program multiple times

    doc_list = document.getElementsByTagName("doc")
    for doc in doc_list:
        ### Extract Id Documents ###
        id_num = doc.getAttribute("id")
        ids.append(id_num.encode("utf-8"))
        # The code some home duplicate the first id and store it to the last.
        ids = list(set(ids))                        # Remove duplicate
        codesElement = doc.getElementsByTagName("code")
        
        ### Extract Label Documents ###
        for code in codesElement:
            if code.attributes["origin"].value == 'CMC_MAJORITY':
                if counter > 0:                                      # If the document has more than 1 label
                    label_store.append('*')                          # add the '*' separate labels of document
                label_store.append(code.firstChild.data)
                counter = counter + 1                                # Increase counter if the document have more than 1 label                             
        counter = 0        
        label_line = ''.join(label_store)
        label_docs.append(label_line.encode("utf-8"))
        del label_line                              # Delete value to save memory, minimize errors
        label_store[:] = []                         # Clear string
        
        ### Extract Text Documents ###
        textsElement = doc.getElementsByTagName("text")
        del text_store[:]
        for text in textsElement:
            textData = text.firstChild.data         # Store text data
            text_store.append(textData.encode("utf-8").strip())     # Strip detele '/n' character in string
        text_line = ''.join(text_store)             # Join 2 string for store in one document.
        text_docs.append(text_line)
        del text_line                               # Delete value to save memory, minimize errors
    for idx, item in enumerate(text_docs):          # Tokenization all strings and split into words
        #text_docs[idx] = clean_str(item).split()
        text_docs[idx] = clean_str(item)
    #label_docs = label_encoding(label_docs)         # Encoding label data
    
    return ids, label_docs, text_docs
    
