# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 07:18:10 2022

@author: Ikbal Maulana

It will use the structure of ReTD
"""

from PyQt5 import QtCore, QtGui, QtWidgets

import os, re, sys
#import multiprocessing
#import calendar
#import leidenalg as la

#import igraph as ig
#import leidenalg as la
#from collections import defaultdict

#from itertools import combinations
from collections import Counter
#from sklearn.feature_extraction.text import CountVectorizer

import xlsxwriter

#import subprocess

import pandas as pd
import collections
import numpy as np
import string

#from nltk.stem import WordNetLemmatizer
#from nltk.stem.snowball import SnowballStemmer
#from nltk.corpus import words

from datetime import datetime, timedelta

import webbrowser

import networkx as nx

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.ticker as mticker
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
       

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import QGridLayout, QFileDialog, QMainWindow, QSpinBox, QMessageBox, \
    QItemDelegate, QVBoxLayout, QHBoxLayout, QSizePolicy, QTabWidget, QApplication, \
        QTableView, QStatusBar, QMenu, QPushButton, QLabel, QComboBox, QMenuBar, \
        QAbstractItemView, QListWidget, QRadioButton, QLineEdit, QInputDialog

from PyQt5.QtGui import QBrush, QColor

from PyQt5.QtCore import QAbstractTableModel, Qt 

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation



from wordcloud import WordCloud

#from community import community_louvain
#partition = community_louvain.best_partition(G)

### Untuk Akar Kata
akhiran = ["ku" , "mu", "nya", "lah", "pun"]

imbuhanKata = ["be-", "be-an", "be-lah", "ber-", "ber-an", "ber-kan", "ber-lah", "berke-an", 
               "di-", "di-kan", "di-kanlah", "di-i", "di-in", "diper-", "diber-kan", "diper-kan", 
               "ke-", "ke-an", "keber-an", "kepe-an", "kepeng-an", 
               "ku-", "ku-i", "ku-kan",
               "me-", "me-kan", "me-i", "mem-", "mem-kan", "mem-i", 
               "member-kan", "memper-", "memper-kan", "men-", "men-kan", "men-i",
               "meng-", "meng-kan", "meng-i",
               "ng-", "ng-in",
               "pe-", "pe-an", "pem-", "pem-an", "pember-an", "pen-", "pen-an", "peng-", "peng-an", "per-", "per-an", "per-kan", 
               "se-", "ter-", "ter-i", "ter-kan", "-an", "-kah", "-kan", "-in", "-isasi", "-i", "-lah", "-wan"]

#For dealing with mobil2an or memukul2
ulang = re.compile(r'^[a-z]+2$')
year_pattern = re.compile(r'^[12]\d\d\d$')
number_pattern = re.compile(r'^\d+$')


#ENGLISH PART
englishSuffixes = ['s--', 'es--', 'es-i-y', 'd--','ed--', 'ied--y',
             'ing--', 'ing--e',
             'ize--y', 'izes--y', 'izer--y', 'ized--', 'ized--y', 'izing--y', 'ization--y', 'izations--y',
             'ize--', 'izes--', 'izer--', 'ized--', 'izing--', 'ization--', 'izations--', 'ization--',
             'ise--y', 'ises--y', 'iser--y', 'ised--y', 'ising--y', 'isation--y', 'isations--y',
             'ise--', 'ises--', 'iser--', 'ised--', 'ising--', 'isation--', 'isations--',
              'r--', 'rs--', 'er--', 'ers--',
              'ment--', 'ity--', 'ical--y',
              'tion--te', 'tion--e', 'tional--e', 'tion--', 'ion--',
              'al--', 'ly--', 'ally--'
             ]


def AkarKata(kata, kamus):
    if kata in kamus:
        return kata
    
    daftar1 = []
    daftar2 = []
    # daftar_di_kamus = []
    j = ""
    
    if ulang.match(kata):
        kata = kata[:-1]
        if kata in kamus:
            return kata
        
        
    for i in akhiran:
        if kata.endswith(i): 
            j = kata[0:len(kata)-len(i)]
            if j in kamus: return j
            
    if j != kata:
        #Kenapa ada daftar1 dan dafta2 
        daftar1 = berimbuhKata(kata, kamus)
        if j:
            daftar2 = berimbuhKata(j, kamus)   
            
    if not (daftar1 + daftar2):
        #return kata
        return ''
    else:
         return max(daftar1+daftar2, key=len)

def berimbuhKata(kata, kamus):
    daftar = []
    daftar_di_kamus = []
    for i in imbuhanKata:
        imbuhan = i.strip().split('-')
        if kata.startswith(imbuhan[0]) and kata.endswith(imbuhan[1]): 
            daftar.append(kata[len(imbuhan[0]):len(kata)-len(imbuhan[1])])
    #print(daftar)
    
    if not daftar and ulang.match(kata):
        daftar.append(kata[:-1])
    
    for j in daftar:
        pengganti_j = ''
        if ulang.match(j):
            j = j[:-1]
        if j in kamus:
            #print(j + ' in kamus')
            #Peluluhan kata
            if j.startswith('m') and ('p'+j[1:]) in kamus:
                daftar_di_kamus.append('p'+j[1:])
            elif j.startswith('n') and ('t'+j[1:]) in kamus:
                daftar_di_kamus.append('t'+j[1:])
            elif j.startswith('ng') and ('k'+j[2:]) in kamus:
                daftar_di_kamus.append('k'+j[2:])
            elif j.startswith('ny') and ('s'+j[2:]) in kamus:
                daftar_di_kamus.append('s'+j[2:])
            else:
                daftar_di_kamus.append(j)
                
            
    #print(daftar_di_kamus)
    return daftar_di_kamus

### Untuk Akar Kata
def createListSuffixes(suffixes):
    suffixes.sort(key = len, reverse = True)
    return [s.split('-') for s in suffixes]

def RootWord(word, kamus, listSuffix):
    if word not in kamus:
        return ''
    else:
        for suffix in listSuffix:
            if word.endswith(suffix[0]):
                #print('Masuk A')
                #print('-'.join(suffix))
                if suffix[1]:
                    #print('Masuk B')
                    
                    #print(word[:-len(suffix[0] + suffix[1])]+suffix[2])
                    if word[:-len(suffix[0] + suffix[1])]+suffix[2] in kamus:
                        #print('Masuk C')
                        
                        return word[:-len(suffix[0] + suffix[1])]+suffix[2]
                else:
                    if word[:-len(suffix[0])] + suffix[2] in kamus:
                        return word[:-len(suffix[0])] + suffix[2]
    return word


# Creating the main window 
class App(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        self.title = "TopMod Version 0.43"
        self.left = 50
        self.top = 50
        self.width = 800
        self.height = 600

        self.main_data = ''
        self.useDate = False
        #self.cleaned_data = ''
        self.stop_words = ''
        #self.model = ''
        self.lda_model = ''
        self.vectorizer = ''
        self.vectorized_data = ''
        self.cleaned_data = pd.DataFrame()
        self.topic_cleaned_data = pd.DataFrame()
        self.non_duplicate_data = pd.DataFrame()
        self.Indonesia = True
        
        #time series data for plotting
        #self.df_selected_data_value = pd.DataFrame()
        self.df_date = pd.DataFrame()
        self.df_datafile = pd.DataFrame()
        
        #kd = open("katadasar.txt", "r")
        #content = kd. read()
        self.kamus = []
                
        self.list_of_DataFiles = []
        
        
        
        self.WordsNotInKamus = pd.DataFrame()
        self.WordsInKamus = pd.DataFrame()
        self.df_DistributionOne = pd.DataFrame()
        self.df_DistributionAll = pd.DataFrame()
        self.df_topic_words = pd.DataFrame()
        

        self.msgBox = QMessageBox()

        self.setWindowTitle(self.title) 
        self.setGeometry(self.left, self.top, self.width, self.height) 
  
        self.tab_widget = MyTabWidget(parent=self) 
        self.setCentralWidget(self.tab_widget) 
  
        self.show() 
        
        
        self.statusbar = QStatusBar()
        #self.statusbar.setObjectName("statusbar")
        #MainWindow.setStatusBar(self.statusbar)
        self.setStatusBar(self.statusbar)
        
        self.menubar = QMenuBar()
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        #self.menubar.setObjectName("menubar")
        self.menuFiles = QMenu()
        self.menuFiles.setTitle("File")
        #self.menuFiles.setObjectName("menuFiles")
        
        self.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction()
        self.actionOpen.setText("Open")
        self.actionOpen.triggered.connect(self.openFile)
        
        self.actionOpenCleanedData = QtWidgets.QAction()
        self.actionOpenCleanedData.setText("Open Cleaned Data")
        self.actionOpenCleanedData.triggered.connect(self.openCleanedData)
        
        
        self.actionSave = QtWidgets.QAction()
        self.actionSave.setText("Save")
        self.actionSave.triggered.connect(self.saveData)
        
        self.actionExit = QtWidgets.QAction()
        self.actionExit.setText("Exit")
        self.actionExit.triggered.connect(self.exitApp)
        
        self.menuFiles.addAction(self.actionOpen)
        self.menuFiles.addAction(self.actionOpenCleanedData)
        self.menuFiles.addAction(self.actionSave)
        self.menuFiles.addAction(self.actionExit)
        self.menubar.addAction(self.menuFiles.menuAction())
        
        
    def exitApp(self):
        self.close()

    def openFile(self):
        # Read StopWords
        '''
        textfile  = open(os.getcwd()+"/stopwords-id.txt", "r")
        self.stop_words = textfile.read().split()
        '''
        #fnames = QFileDialog.getOpenFileNames(self, "Open CSV Files", "", "csv files (*.csv)")
        fnames = QFileDialog.getOpenFileNames(self, "Open CSV Files", "", "CSV and TXT files (*.csv *.txt);;CSV files (*.csv);;TXT files (*.txt)")
        
        #filter_str = "CSV and TXT files (*.csv *.txt);;CSV files (*.csv);;TXT files (*.txt)"
               
        if len(fnames[0]) == 0:
            self.msgBox.setText("There is no file to upload!")
            self.msgBox.setWindowTitle("TopMod Version 0.43")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()
            return
        
        #print(fnames[0])
        list_of_files = []
        listFileNames = []
        
        file_is_a_csv = True
        
        for idx, fn in enumerate(fnames[0]):
            if idx == 0:
                if fn.endswith('.csv'):
                    file_is_a_csv = True
                elif fn.endswith('.txt'):
                    file_is_a_csv = False
                else:
                    return
            else:
                if fn.endswith('.csv'):
                    if not file_is_a_csv:
                        print('Files must be the same')
                        return
                elif fn.endswith('.txt'):
                    if file_is_a_csv:
                        print('Files must be the same')
                        return
                else:
                    return
                
            print(fn)
        '''
        else:
            if fn.endswith('txt'):
                print('Selesai')
                return
        '''  
        
        if fnames[0][0].endswith('.csv'):
            for fn in fnames[0]:
                dfcsv = pd.read_csv(open(fn, encoding = 'utf-8', errors = 'backslashreplace'))
                #p = re.compile('.*\\([\w\-]*)\.csv')
                #fileName = p.findall(fn)[0]
                
                
                if len(fnames[0])>1:
                    fileName = os.path.basename(fn)[:-4]
                    self.list_of_DataFiles.append(fileName)
                    listData = [fileName]*len(dfcsv)
                    dfcsv.insert(loc=1, column='Data', value=listData)
                    listFileNames.append(fileName)
                
                
                list_of_files.append(dfcsv)
                
                #print('No ' + str(len(listFileNames)))
                #print(listFileNames)
        else:
            default_delimiter = "\\n"
            delimiter, ok = QInputDialog.getText(self, "Paragraph delimiter", "Enter custom paragraph delimiter:", text=default_delimiter)
            delimiter = delimiter.replace('\\n','\n')
            if not ok:
                return
            
            for fn in fnames[0]:
                with open(fn, 'r', encoding='utf-8') as file:
                    paragraphs = file.read().split(delimiter)
                    #text = file.read()
                    
                
                
                pars = [p for p in paragraphs if p]
                #pars = [p.replace('\n',' ') for p in paragraphs if p]
                #print("Pars is "+str(len(pars)))
                if len(fnames[0])>1:
                    fileName = os.path.basename(fn)[:-4]
                    self.list_of_DataFiles.append(fileName)
                    listData = [fileName]*len(pars)
                    #dfcsv.insert(loc=1, column='Data', value=listData)
                    dftext = pd.DataFrame({'Text':pars, 'Data': listData})
                    listFileNames.append(fileName)
                else:
                    dftext = pd.DataFrame({'Text': pars}) 
                
                list_of_files.append(dftext)
                    
                #df = pd.DataFrame({'Paragraphs': paragraphs})
        
        #print(len(list_of_files))
        
        listFileNames.sort()
        #print(listFileNames)
        self.tab_widget.tabTopicModel.lwListAllData.addItems(listFileNames)
        self.tab_widget.tabTime.lwListAllData.addItems(listFileNames)
        self.tab_widget.tabTime.lwListAllData.setVisible(True)
        
            
        df = pd.concat(list_of_files, ignore_index=True)
        #df.drop_duplicates(keep=False,inplace=True)
        df.drop_duplicates(inplace=True)
        
        
        self.main_data = df
        
        if not file_is_a_csv:
            #jump to tab_clean
            
            clean = df['Text'].str.lower().tolist()
            idx = df.columns.get_loc('Text')
            df.insert(loc=idx+1, column='Clean', value=clean)
            #df['Clean'] = df['Text'].str.lower()        
         
            #if self.cbLang.currentText() == 'Indonesia':
            if self.tab_widget.tabRawData.cbLang.currentText() == 'Indonesia':
                #print('Indonesia')
                #self.parent.parent.Indonesia = True
                self.Indonesia = True
                textfile  = open(os.getcwd()+"/stopwords-id.txt", "r")
                #self.parent.parent.stop_words = textfile.read().split()
                self.stop_words = textfile.read().split()
                
                worddictfile = open("katadasar.txt", "r")
                #self.parent.parent.kamus = worddictfile.read().split()
                self.kamus = worddictfile.read().split()
            else:
                #print('English')
                #self.parent.parent.Indonesia = False
                self.Indonesia = False
                textfile  = open(os.getcwd()+"/stopwords-en.txt", "r")
                #self.parent.parent.stop_words = textfile.read().split()
                self.stop_words = textfile.read().split()
                
                worddictfile = open("englishwords.txt", "r")
                #self.parent.parent.kamus = worddictfile.read().split()
                self.kamus = worddictfile.read().split()
                
            self.cleaned_data = df
            model = pandasModel(self.cleaned_data)
            self.tab_widget.tabCleanData.tvCleanData.setModel(model)
            
            for i in range(len(self.cleaned_data.columns)):
                if df.columns[i] != 'Clean' and df.columns[i] != 'Text':
                    self.tab_widget.tabCleanData.tvCleanData.hideColumn(i)
                #print(str(i)+'  '+ df.columns[i])
                
            
            self.tab_widget.tabRawData.setEnabled(False)
            self.tab_widget.tabCleanData.setEnabled(True)
            self.tab_widget.setCurrentIndex(1)
            
        
            self.cleaned_data = df
            model = pandasModel(self.cleaned_data)
            self.tab_widget.tabCleanData.tvCleanData.setModel(model)
            
            for i in range(len(self.cleaned_data.columns)):
                if df.columns[i] != 'Clean' and df.columns[i] != 'Text':
                    self.tab_widget.tabCleanData.tvCleanData.hideColumn(i)
            #print(str(i)+'  '+ df.columns[i])
            
        
            self.tab_widget.tabRawData.setEnabled(False)
            self.tab_widget.tabCleanData.setEnabled(True)
            self.tab_widget.tabs.setCurrentIndex(1)
            self.tab_widget.tabKata.setEnabled(True)

            
            
                       
        
        daftar_kolom = ['Select'] + list(df.columns)
        
        self.tab_widget.tabRawData.cbDate.addItems(daftar_kolom)
        self.tab_widget.tabRawData.cbText.addItems(daftar_kolom)
        
        
        model = pandasModel(df)
        self.tab_widget.tabRawData.tvRawData.setModel(model)
        
        self.actionOpen.setDisabled(True)
        self.actionOpenCleanedData.setDisabled(True)
        
    def openCleanedData(self):
        # Read StopWords
        '''
        textfile  = open(os.getcwd()+"/stopwords-id.txt", "r")
        self.stop_words = textfile.read().split()
        '''
        
        #fnames = QFileDialog.getOpenFileNames(self, "Open Data File", "", "CSV data files (*.csv)")
        fname = QFileDialog.getOpenFileNames(self, "Open Cleaned Data", "", "cleaned data files (*.cdf)")
        
               
        if len(fname[0]) == 0:
            self.msgBox.setText("There is no file to upload!")
            self.msgBox.setWindowTitle("TopMod Version 0.43")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()
            return
        
        df = pd.read_csv(open(fname[0][0], encoding = 'utf-8', errors = 'backslashreplace'))
        
        
        
        if 'Data' in df.columns:
            listData = list(df['Data'].unique())
            self.tab_widget.tabTopicModel.lwListAllData.addItems(listData)
            self.tab_widget.tabTime.lwListAllData.addItems(listData)
        
        if 'Date' in df.columns:
            self.useDate = True
            if len(str(df['Date'].iloc[0])) > 4:
                df['Date'] = pd.to_datetime(df['Date'],dayfirst=False).dt.date
            
            '''How to deal with day first or last '''
        
        if 'Text' in df.columns and 'Clean' in df.columns:
            self.cleaned_data = df
            model = pandasModel(self.cleaned_data)
            self.tab_widget.tabCleanData.tvCleanData.setModel(model)
            
            for i in range(len(self.cleaned_data.columns)):
                if df.columns[i] != 'Clean' and df.columns[i] != 'Text':
                    self.tab_widget.tabCleanData.tvCleanData.hideColumn(i)
                #print(str(i)+'  '+ df.columns[i])
                
            
            self.tab_widget.tabRawData.setEnabled(False)
            self.tab_widget.tabCleanData.setEnabled(True)
            self.tab_widget.setCurrentIndex(1)

        else:
            self.msgBox.setText("This is not data that has been cleaned with this application")
            self.msgBox.setWindowTitle("TopMod Version 0.43")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()
            return
        
        #self.main_data = df
        self.actionOpen.setDisabled(True)
        self.actionOpenCleanedData.setDisabled(True)
        
        #self.setEnabled(False)
        self.tab_widget.tabCleanData.setEnabled(True)
        self.tab_widget.tabs.setCurrentIndex(1)
        self.tab_widget.tabKata.setEnabled(True)
        
    
    def saveData(self):
        idx_tab = self.tab_widget.tabs.currentIndex()
        if idx_tab == 0:
            self.msgBox.setText("There is nothing to save!")
            self.msgBox.setWindowTitle("TopMod Version 0.43")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()
            return
        
           
        if idx_tab == 1:
            filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'cleaned data files (*.cdf)')
            savename = filename[0]
                   
            if len(savename.strip()) == 0:
                self.msgBox.setText("There is no file to save!")
                self.msgBox.setWindowTitle("TopMod Version 0.43")
                self.msgBox.setStandardButtons(QMessageBox.Ok)
                self.msgBox.show()
                return
            
            self.cleaned_data.to_csv(savename, date_format='%Y.%m.%d', encoding = 'utf-8')
        elif idx_tab == 2:
            if len(self.df_DistributionAll)  == 0 and len(self.df_DistributionOne) == 0:
                self.msgBox.setText("Please click \'Distribution\' and \'Distribution For Topic Value >\' buttons ")
                self.msgBox.setWindowTitle("TopMod Version 0.43")
                self.msgBox.setStandardButtons(QMessageBox.Ok)
                self.msgBox.show()
                return
            else:
                filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'xslx data files (*.xlsx)')
                savename = filename[0]
                
                if len(savename.strip()) == 0:
                    self.msgBox.setText("There is no file to save!")
                    self.msgBox.setWindowTitle("TopMod Version 0.43")
                    self.msgBox.setStandardButtons(QMessageBox.Ok)
                    self.msgBox.show()
                    return
                
                topicValue = self.tab_widget.tabTopicModel.cbTopicValue.currentText()
                try:                                                                                 
                    with pd.ExcelWriter(savename) as topic_file:  # doctest: +SKIP
                        self.df_DistributionAll.to_excel(topic_file, engine='xlsxwriter', sheet_name='All Topics')
                        self.df_DistributionOne.to_excel(topic_file, engine='xlsxwriter', sheet_name='Topics >' + topicValue)
                    
                except Exception as ex:
                    print(ex)
                
        elif idx_tab == 3:
            if len(self.df_topic_words) == 0:
                self.msgBox.setText("You have to create topic Modeling first!")
                self.msgBox.setWindowTitle("TopMod Version 0.43")
                self.msgBox.setStandardButtons(QMessageBox.Ok)
                self.msgBox.show()
                return
            
            filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'xslx data files (*.xlsx)')
            savename = filename[0]
            
            if len(savename.strip()) == 0:
                self.msgBox.setText("There is no file to save!")
                self.msgBox.setWindowTitle("TopMod Version 0.43")
                self.msgBox.setStandardButtons(QMessageBox.Ok)
                self.msgBox.show()
                return
            
            try:                                                                                 
                with pd.ExcelWriter(savename) as topic_file:  # doctest: +SKIP
                    self.df_topic_words.to_excel(topic_file, engine='xlsxwriter', sheet_name='Topic Words')
                    
                    
                    topic_list = self.topicList
                    topicValue = float(self.tab_widget.tabTopicModel.cbTopicValue.currentText())
                    
                    if 'Data' in self.topic_cleaned_data.columns:
                        df = self.topic_cleaned_data[['Data','Text', 'Clean'] + topic_list]
                    else:  
                        df = self.topic_cleaned_data[['Text', 'Clean'] + topic_list]
                    print('Ngecek data')
                    for column in topic_list:
                        df_selected_topic = df[df[column] > topicValue].sort_values(column, ascending = False)
                        #df_selected_topic = df_selected_topic[['Text', 'Clean', column]]
                        
                        if 'Data' in df_selected_topic.columns:
                            df_group = df_selected_topic[['Data', 'Text','Clean']+[column]]
                            
                            
                        else:
                            df_group = df_selected_topic[['Text','Clean']+[column]]
                            
                            '''
                            df_group = df_selected_topic.groupby(['Text','Clean']).size().to_frame().reset_index()
                            df_group.columns = ['Text', 'Clean', '#Docs']
                            df_group.sort_values('#Docs', ascending = False, inplace = True)
                            '''
                        print('Panjangnya df_group ' + str(len(df_group)))
                        df_group.drop_duplicates()
                        print('Panjangnya df_group ' + str(len(df_group)))
                        
                        df_group.sort_values(column, ascending = False, inplace = True)
                        
                        
                        df_group.to_excel(topic_file, engine='xlsxwriter', sheet_name = column)

                                                                                                                                       
            
            except Exception as ex:
                print(ex)
                print('Masuk Exception')
                   
        elif idx_tab == 4:
            if self.df_date is not None:
                filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV data files (*.csv)')
                savename = filename[0]
                
                if len(savename.strip()) == 0:
                    self.msgBox.setText("There is no file to save!")
                    self.msgBox.setWindowTitle("TopMod Version 0.43")
                    self.msgBox.setStandardButtons(QMessageBox.Ok)
                    self.msgBox.show()
                    return
                
                self.df_date.to_csv(savename)
            else:
                self.msgBox.setText("There is no file to save!")
                self.msgBox.setWindowTitle("TopMod Version 0.43")
                self.msgBox.setStandardButtons(QMessageBox.Ok)
                self.msgBox.show()
                return
        else:
            if self.tab_widget.tabCooccur.dfAllWords is not None:
                filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV data files (*.csv)')
                savename = filename[0]
                
                if len(savename.strip()) == 0:
                    self.msgBox.setText("There is no file to save!")
                    self.msgBox.setWindowTitle("TopMod Version 0.43")
                    self.msgBox.setStandardButtons(QMessageBox.Ok)
                    self.msgBox.show()
                    return
                
                self.tab_widget.tabCooccur.dfAllWords.to_csv(savename)
            else:
                self.msgBox.setText("There is no file to save!")
                self.msgBox.setWindowTitle("TopMod Version 0.43")
                self.msgBox.setStandardButtons(QMessageBox.Ok)
                self.msgBox.show()
                return
            
                
                
                
        #print('Save data and file name ' + savename[0])
  
# Creating tab widgets 
class MyTabWidget(QTabWidget): 
    def __init__(self, parent): 
        #super(QWidget, self).__init__(parent) 
        super(QTabWidget, self).__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self) 
        self.title = 'MyTabWidget'
  
        # Initialize tab screen 
        self.tabs = QTabWidget() 
        self.tabRawData = tabRawData(parent = self) 
        self.tabCleanData = tabCleanData(parent = self)
        self.tabCleanData.setDisabled(True)
        self.tabs.resize(600, 400)
        self.tabTopicModel = tabTopicModel(parent = self)
        self.tabTopicModel.setDisabled(True)
        self.tabTopic= tabTopic(parent = self)
        self.tabTopic.setDisabled(True)
        self.tabTime = tabTime(parent = self)
        self.tabTime.setDisabled(True)
        self.tabTime.setVisible(False)
        
        self.tabCooccur = tabCooccur(parent = self)
        self.tabCooccur.setDisabled(True)
        self.tabCooccur.setVisible(False)
        
        self.tabKata = tabKataDalamKonteks(parent = self)
        self.tabKata.setDisabled(True)
        self.tabKata.setVisible(False)
        
        # Add tabs 
        self.tabs.addTab(self.tabRawData, "Raw Data") 
        self.tabs.addTab(self.tabCleanData, "Clean Data")
        self.tabs.addTab(self.tabTopicModel,"Modeling")
        self.tabs.addTab(self.tabTopic, "Topic")
        self.tabs.addTab(self.tabTime,"Time Series")
        self.tabs.addTab(self.tabCooccur,'Word Cooccurence')
        self.tabs.addTab(self.tabKata,"KWIC")
        #self.tabs.addTab(self.tabData,"Data File Comparison")  
        # Add tabs to widget 
        self.layout.addWidget(self.tabs) 
        
        label = QLabel("Copyright © 2023 Ikbal Maulana")

        # Align the label to the bottom-right corner
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        self.layout.addWidget(label)
        
        self.setLayout(self.layout) 


        
    
    
        
class tabRawData(QTabWidget):
    def __init__(self, parent): 
        #super(QWidget, self).__init__(parent)
        super(QTabWidget, self).__init__(parent)
        
        self.parent = parent
        
        self.msgBox = QMessageBox()
        
        self.glRawData = QGridLayout()
        
        self.lbLang = QLabel()
        self.lbLang.setText('Language')
        self.lbLang.setAlignment(Qt.AlignRight)
        
        self.cbLang = QComboBox()
        self.cbLang.addItems(['Indonesia', 'English'])
        
        
        self.lbDate = QLabel()
        self.lbDate.setText('Date')
        self.lbDate.setAlignment(Qt.AlignRight)
        
        self.rbDayFirst = QRadioButton("Day First")
        
        self.cbDate = QComboBox()
        
        self.lbText = QLabel()
        self.lbText.setText("Text")
        self.lbText.setAlignment(Qt.AlignRight)
        
        self.cbText = QComboBox()
        
        
        
        self.btSelectColumns = QtWidgets.QPushButton()
        
        self.btSelectColumns.setText("Select Text")
        
        self.btSelectColumns.clicked.connect(self.selectColumns)
        
        self.tvRawData = QTableView()
        
        self.glRawData.addWidget(self.lbLang, 0, 0)
        self.glRawData.addWidget(self.cbLang, 0, 1)

        self.glRawData.addWidget(self.lbDate, 0, 2)
        self.glRawData.addWidget(self.cbDate, 0, 3)
        self.glRawData.addWidget(self.rbDayFirst, 0, 4)
        
        self.glRawData.addWidget(self.lbText, 0, 5)
        self.glRawData.addWidget(self.cbText, 0, 6)
        self.glRawData.addWidget(self.btSelectColumns, 0, 7)
        self.glRawData.addWidget(self.tvRawData, 1, 0, 6, 8)
        
        
        self.setLayout(self.glRawData)

        
        

    def selectColumns(self):
        df = self.parent.parent.main_data
        
        if self.cbText.currentText() == 'Select':
            self.msgBox.setText("Please select at least one item")
            self.msgBox.setWindowTitle("Warning")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()
            return
        else: 
            
            df = df.rename(columns={ self.cbText.currentText(): 'Text'}  )
            #df = df[['Text']]
            clean = df['Text'].str.lower().tolist()
            idx = df.columns.get_loc('Text')
            df.insert(loc=idx+1, column='Clean', value=clean)
            #df['Clean'] = df['Text'].str.lower()
            if self.cbDate.currentText() != 'Select':
                df = df.rename(columns={ self.cbDate.currentText(): 'Date'}  )
                self.parent.parent.useDate = True 
                
                if len(str(df['Date'].iloc[0])) > 4:
                    if self.rbDayFirst.isChecked():
                        dayfirst = True
                    else:
                        dayfirst = False
                        
                    df['Date'] = pd.to_datetime(df['Date'],dayfirst=dayfirst).dt.date
                    
                
         
        if self.cbLang.currentText() == 'Indonesia':
            #print('Indonesia')
            self.parent.parent.Indonesia = True
            textfile  = open(os.getcwd()+"/stopwords-id.txt", "r")
            self.parent.parent.stop_words = textfile.read().split()
            
            worddictfile = open("katadasar.txt", "r")
            self.parent.parent.kamus = worddictfile.read().split()
        else:
            #print('English')
            self.parent.parent.Indonesia = False
            textfile  = open(os.getcwd()+"/stopwords-en.txt", "r")
            self.parent.parent.stop_words = textfile.read().split()
            
            worddictfile = open("englishwords.txt", "r")
            self.parent.parent.kamus = worddictfile.read().split()
        
        self.parent.parent.cleaned_data = df
        model = pandasModel(self.parent.parent.cleaned_data)
        self.parent.tabCleanData.tvCleanData.setModel(model)
        
        for i in range(len(self.parent.parent.cleaned_data.columns)):
            if df.columns[i] != 'Clean' and df.columns[i] != 'Text':
                self.parent.tabCleanData.tvCleanData.hideColumn(i)
            #print(str(i)+'  '+ df.columns[i])
            
        
        self.setEnabled(False)
        self.parent.tabCleanData.setEnabled(True)
        self.parent.tabs.setCurrentIndex(1)
        self.parent.tabKata.setEnabled(True)
        
        #To avoid retyping
        '''
        theLastColumns = [self.cbLang.currentText() , self.cbDate.currentText(),\
                          self.cbText.currentText()]
        textfile  = open(os.getcwd()+"/lastcols.txt", "w+")
        for element in theLastColumns:
            textfile.write(element + "\n")
        textfile.close()
        '''
        

class tabCleanData(QTabWidget):
    def __init__(self, parent): 
        #super(QWidget, self).__init__(parent)
        super(QTabWidget, self).__init__(parent)
        
        self.parent = parent
             
        self.glCleanData = QGridLayout()
        
        self.tvCleanData = QTableView()
        
        self.btCleanData = QPushButton()
        self.btCleanData.setText('Clean')
        self.btCleanData.clicked.connect(self.cleanText)
        
        self.lbDrop = QLabel()
        self.lbDrop.setText('Drop')
        self.lbDrop.setAlignment(Qt.AlignRight)
        
        self.btStopWords = QPushButton()
        self.btStopWords.setText("Stop Words")
        self.btStopWords.clicked.connect(self.removeStopWords)
        
        self.btSingleLetter = QPushButton()
        self.btSingleLetter.setText('Single Letter')
        self.btSingleLetter.clicked.connect(self.removeSingleLetter)
        
        self.btRemoveYear = QPushButton()
        self.btRemoveYear.setText("Year")
        self.btRemoveYear.clicked.connect(self.removeYear)
        
        self.btRemoveNumber = QPushButton()
        self.btRemoveNumber.setText("Number")
        self.btRemoveNumber.clicked.connect(self.removeNumber)
                
        self.btCheckDict = QPushButton()
        self.btCheckDict.setText('Check Words')
        self.btCheckDict.clicked.connect(self.checkDictionary)
        
        self.btCheckLemma = QPushButton()
        self.btCheckLemma.setText('Check Lemma')
        self.btCheckLemma.clicked.connect(self.checkLemma)
        self.btCheckLemma.setEnabled(False)

        self.btAcceptDict = QPushButton()
        self.btAcceptDict.setText('Accept Words')
        self.btAcceptDict.clicked.connect(self.acceptDictionary)
        self.btAcceptDict.setEnabled(False)
                
        self.tvDict = QTableView()
        self.tvDict.setObjectName("tvDictionary")
        delegate = MyDelegate()
        self.tvDict.setItemDelegate(delegate)
        self.tvDict.setVisible(False)
        
        self.glCleanData.addWidget(self.btCleanData, 0, 0)
        self.glCleanData.addWidget(self.lbDrop, 0, 1)
        self.glCleanData.addWidget(self.btStopWords, 0, 2)
        self.glCleanData.addWidget(self.btSingleLetter, 0, 3) 
        self.glCleanData.addWidget(self.btRemoveYear, 0, 4)
        self.glCleanData.addWidget(self.btRemoveNumber, 0, 5)
        self.glCleanData.addWidget(self.btCheckDict, 0, 6)
        self.glCleanData.addWidget(self.btCheckLemma, 0, 7)
        self.glCleanData.addWidget(self.btAcceptDict, 0, 8)
        
        self.glCleanData.addWidget(self.tvCleanData, 1, 0, 6, 5)
        self.glCleanData.addWidget(self.tvDict, 1, 6, 6, 3)
        
        self.setLayout(self.glCleanData)
        
        
    def cleanText(self):
        self.btCleanData.setEnabled(False)
        def remove_punc(huruf):
            re_pattern = r'[()?!:;+*\.,\"\“\/&\']'
            re_obj = re.compile(re_pattern)
            match = re_obj.findall(huruf)
            if match:
                return ' '
            else:
                return huruf
        
        
        df = self.parent.parent.cleaned_data
        df = df.loc[df['Clean'].notna()]
        
        
        #.apply(lambda x: ' '.join([''.join([z for z in y if z not in '()?!:;\.,\"']) for y in x.split(' ')]) )\
        
        df.loc[:,'Clean'] = df['Clean'].apply(lambda x: ' '.join([e for e in x.split() if not "@" in e]))\
            .apply(lambda x: ' '.join([e for e in x.split() if not e.startswith('http')]))\
            .apply(lambda x: x.replace('-',' '))\
            .apply(lambda x: x.replace('\'',' '))\
            .apply(lambda x: ''.join([remove_punc(el) for el in x ]))\
            .apply(lambda x: ' '.join([''.join([z for z in y if z.isalnum() or z=='_']) for y in x.split(' ')]) )
        
            #.apply(lambda x: ' '.join([e for e in x.split() if not e.startswith('#')]))\
            
        
        
        df['Clean'].replace(r'^\s+', '', regex=True, inplace=True)
        df['Clean'].replace(r'\s+$', '', regex=True, inplace=True)
        df['Clean'].replace(r'\s+', ' ', regex=True, inplace=True)
        df['Clean'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
        
        df = df.loc[df['Clean'].notna()]
            
        self.parent.parent.cleaned_data = df
        model = pandasModel(self.parent.parent.cleaned_data)
        self.tvCleanData.setModel(model)

    def removeStopWords(self):
        self.btStopWords.setEnabled(False)
        #textfile = open(os.path.abspath()+"/stopwords-id.txt", "r")
        #self.stop_words = textfile.read().split()
        df = self.parent.parent.cleaned_data
        
        
        #print(len(self.parent.parent.stop_words))
        df['Clean'] = df['Clean'].apply(lambda x: ' '.join([a for a in x.split(' ') if a not in self.parent.parent.stop_words]))
        
        df = df.loc[df['Clean'].notna()]
        
        self.parent.parent.cleaned_data = df
        model = pandasModel(self.parent.parent.cleaned_data)
        self.tvCleanData.setModel(model)

    def removeYear(self):
        self.btRemoveYear.setEnabled(False)
        df = self.parent.parent.cleaned_data
        df['Clean'] = df['Clean'].apply(lambda x: ' '.join([a for a in x.split(' ') if not year_pattern.match(a)]))
        
        df = df.loc[df['Clean'].notna()]
        
        self.parent.parent.cleaned_data = df
        model = pandasModel(self.parent.parent.cleaned_data)
        self.tvCleanData.setModel(model)
        
    def removeNumber(self):
        self.btRemoveNumber.setEnabled(False)
        df = self.parent.parent.cleaned_data
        df['Clean'] = df['Clean'].apply(lambda x: ' '.join([a for a in x.split(' ') if not (number_pattern.match(a) and not year_pattern.match(a))]))
        
        df = df.loc[df['Clean'].notna()]
        
        self.parent.parent.cleaned_data = df
        model = pandasModel(self.parent.parent.cleaned_data)
        self.tvCleanData.setModel(model)
        
    def removeSingleLetter(self):
        self.btSingleLetter.setEnabled(False)
        df = self.parent.parent.cleaned_data
        df['Clean'] = df['Clean'].apply(lambda x: ' '.join([a for a in x.split(' ') if len(a)>1]))
        
        df = df.loc[df['Clean'].notna()]
        
        self.parent.parent.cleaned_data = df
        model = pandasModel(self.parent.parent.cleaned_data)
        self.tvCleanData.setModel(model)

    def checkDictionary(self):
        self.btCleanData.setEnabled(False)
        self.btStopWords.setEnabled(False)
        self.btSingleLetter.setEnabled(False)
        self.btRemoveYear.setEnabled(False)
        self.btRemoveNumber.setEnabled(False)
        self.btCheckDict.setEnabled(False)
        df = self.parent.parent.cleaned_data.loc[self.parent.parent.cleaned_data['Clean'].notna()]
        #df = df.loc[df['Clean'].notna()]
        all_words = ' '.join(df['Clean'].tolist()).split()
        '''
        if 'Clean'in list(df.columns):
            all_words = ' '.join(df['Clean'].tolist()).split()
        else:
            all_words = ' '.join(df['Text'].tolist()).split()
        '''
        
        count_words = collections.Counter(all_words)
        
        print(count_words.most_common(1000))
        
        df_words = pd.DataFrame(count_words.items(), columns=['word','count'])
        df_words = df_words.sort_values(by = 'count', ascending=False)
        
        if self.parent.parent.Indonesia:
            df_words['root'] = df_words['word'].apply(lambda x: AkarKata(x, self.parent.parent.kamus))
        else:
            #stemmer = SnowballStemmer("english")
            listSuffixes = createListSuffixes(englishSuffixes)
            df_words['root'] = df_words['word'].apply(lambda x: RootWord(x, self.parent.parent.kamus, listSuffixes))
        
        #print('Panjang kamus ' + str(len(df_words)))
        df_words_no_root = df_words.loc[df_words['root'] == ''] 
        
        #print(df_words_no_root.head())
        
        self.parent.parent.WordsInKamus = df_words.loc[df_words['root'] != ''] 
        self.parent.parent.WordsNotInKamus = df_words_no_root[['word','count']]
        
        self.parent.parent.WordsNotInKamus['root'] = self.parent.parent.WordsNotInKamus['word']
        #print('Panjang kata tidak di kamus ' + str(len(self.parent.parent.WordsNotInKamus)))
        model = dictionaryModel(self.parent.parent.WordsNotInKamus)
        self.tvDict.setModel(model)
        self.tvDict.setVisible(True)
        self.btAcceptDict.setEnabled(True)
        self.btCheckLemma.setEnabled(True)
        
        
    def checkLemma(self):
        self.btCheckLemma.setEnabled(False)
        df = self.parent.parent.WordsInKamus
        if len(df) == 0:
            return
        model = dictionaryModel(df)
        self.tvDict.setModel(model)
        self.tvDict.setVisible(True)
        self.btAcceptDict.setEnabled(True)

    def acceptDictionary(self):
        df0 = self.parent.parent.WordsInKamus[['word', 'root']]
        df1 = self.parent.parent.WordsNotInKamus[['word', 'root']]
        #df = df0.append(df1)
        df = pd.concat([df0,df1], ignore_index= True)
        number_of_words = len(df)
        
        dict_from_df = df.set_index('word').to_dict()['root']
        
        #print(dict_from_df)
        
        dfc = self.parent.parent.cleaned_data.loc[self.parent.parent.cleaned_data['Clean'].notna()]
        #print(len(dfc))
        
        dfc['Clean'] = dfc['Clean'].apply(lambda x: x.strip()).replace('', np.nan)
        dfc.dropna(subset=['Clean'], inplace=True)
        dfc.loc[:,'Clean'] = dfc['Clean'].apply(lambda x: ' '.join([dict_from_df[w] for w in x.split()]))

        #print(len(self.parent.parent.cleaned_data))
        self.parent.parent.cleaned_data = dfc[dfc['Clean'].apply(lambda x: len(x.split(' '))>2)]
        #print(len(self.parent.parent.cleaned_data))
        
        self.tvDict.setVisible(False)
        
        #DocNumber = [i for i in range(len(dfc))]
        DocNumber = [i for i in range(len(self.parent.parent.cleaned_data))]
        
        idx = self.parent.parent.cleaned_data.columns.get_loc('Clean')
        if 'No' in self.parent.parent.cleaned_data.columns:
            self.parent.parent.cleaned_data.drop('No', axis=1, inplace = True)
            
        self.parent.parent.cleaned_data.insert(loc=idx+1, column='No', value=DocNumber)
        
        
        
        self.parent.parent.non_duplicate_data = self.parent.parent.cleaned_data.groupby(['Text','Clean'])['No'].apply(list).to_frame().reset_index()
        #print(df_non_duplicate_data.columns)
        #print(df_non_duplicate_data.head(3))
        model = pandasModel(self.parent.parent.non_duplicate_data)
        self.tvCleanData.setModel(model)
        
        for i in range(len(self.parent.parent.non_duplicate_data.columns)):
            #if self.parent.parent.non_duplicate_data.columns[i] != 'Clean' and self.parent.parent.non_duplicate_data.columns[i] != 'Text':
            if self.parent.parent.non_duplicate_data.columns[i] != 'Clean':
                #print(self.parent.parent.non_duplicate_data.columns[i])
                self.tvCleanData.hideColumn(i)
            else:
                self.tvCleanData.showColumn(i)
        
        self.setEnabled(False)
        self.parent.tabTopicModel.setEnabled(True)
        self.parent.tabCooccur.setEnabled(True)
        #self.parent.tabCooccur.sbTopWords.setMaximum(number_of_words)
        #self.parent.tabs.setCurrentIndex(2)


class tabTopicModel(QTabWidget):
    #import pyLDAvis.sklearn 
    #from pyLDAvis_local import sklearn as skl
    #from pyLDAvis_local import save_html
    
    def __init__(self, parent): 
        #super(QWidget, self).__init__(parent)
        super(QTabWidget, self).__init__(parent)
        
        self.parent = parent
        
        self.glResult = QGridLayout()
        
        self.lbTopic = QLabel()
        self.lbTopic.setText('Number of Topics')
        
        self.sbNumberOfTopics = QSpinBox()
        self.sbNumberOfTopics.setRange(5, 60)
        self.sbNumberOfTopics.valueChanged.connect(self.changedNumberOfTopics)
        
        self.btTopicModeling = QPushButton()
        self.btTopicModeling.setText('Topic Modeling')
        self.btTopicModeling.clicked.connect(self.topicModeling)
        
        self.btBarAll = QPushButton()
        self.btBarAll.setText('Distribution')
        self.btBarAll.clicked.connect(self.createBarAll)
        self.btBarAll.setEnabled(False)
        
        self.btBarOne = QPushButton()
        self.btBarOne.setText('Distribution For Value >')
        self.btBarOne.clicked.connect(self.createBarOne)
        self.btBarOne.setEnabled(False)
        
        self.cbTopicValue = QComboBox()
        self.cbTopicValue.addItems(['0.5','0.6','0.7','0.8','0.9'])
        self.cbTopicValue.currentTextChanged.connect(self.changeTopicValue)
        
        '''
        self.btLDAvis = QPushButton()
        self.btLDAvis.setText('Visualization')
        self.btLDAvis.clicked.connect(self.openBrowser)
        self.btLDAvis.setEnabled(False)
        '''
        self.btSaveGraph = QPushButton()
        self.btSaveGraph.setText('Save Graph')
        self.btSaveGraph.clicked.connect(self.saveGraph)
        self.btSaveGraph.setEnabled(False)
        
        self.lbTitleTable = QLabel()

        self.lwListAllData = QListWidget()
        self.lwListAllData.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )
        self.lwListAllData.setVisible(False)
        self.lwListAllData.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        
        self.tvTopics = QTableView()
        self.tvTopics.setVisible(False)
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.canvas.setVisible(False)
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setVisible(False)
        
        
        self.glResult.addWidget(self.lbTopic, 0, 0)
        self.glResult.addWidget(self.sbNumberOfTopics, 0, 1)
        self.glResult.addWidget(self.btTopicModeling, 0, 2)
        self.glResult.addWidget(self.btBarAll, 0, 3)
        self.glResult.addWidget(self.btBarOne, 0, 4)
        self.glResult.addWidget(self.cbTopicValue, 0, 5)
        #self.glResult.addWidget(self.btLDAvis, 0, 6)
        self.glResult.addWidget(self.btSaveGraph, 0, 7)
        #self.glResult.addWidget(self.btShowDocs, 0, 5)
        self.glResult.addWidget(self.toolbar, 1, 0, 1, 4)
        self.glResult.addWidget(self.lbTitleTable, 1, 4, 1, 4)
        self.glResult.addWidget(self.tvTopics, 2, 0, 7, 8)
        self.glResult.addWidget(self.lwListAllData, 2, 0, 7, 1)
        self.glResult.addWidget(self.canvas, 2, 1, 7, 7)
        #self.glResult.addWidget(self.htmlOutput, 2, 0, 7, 7)
        
        self.setLayout(self.glResult)
        
        
    
    
    def changeTopicValue(self):
        self.parent.parent.df_DistributionOne = pd.DataFrame()
        #self.parent.parent.df_DistributionAll = pd.DataFrame()
        
        

    def changedNumberOfTopics(self):
        self.btBarAll.setEnabled(False)
        self.btBarOne.setEnabled(False)
        #self.btLDAvis.setEnabled(False)
        self.btSaveGraph.setEnabled(False)
        
        self.btTopicModeling.setEnabled(True)
        self.tvTopics.setVisible(False)
        self.canvas.setVisible(False)
        self.toolbar.setVisible(False)
        self.lwListAllData.setVisible(False)
        self.parent.tabTopic.setEnabled(False)
        self.parent.parent.df_topic_words = pd.DataFrame()
        self.parent.parent.selected_topic = pd.DataFrame()
        
        self.parent.parent.topicList = []
        
        #This is for Textnets
        self.parent.parent.corpus_to_plot = ''
        self.parent.parent.topic_to_plot = {}
        self.parent.parent.df_DistributionOne = pd.DataFrame()
        self.parent.parent.df_DistributionAll = pd.DataFrame()
        
        
        
        
    
    def topicModeling(self):
        self.tvTopics.setVisible(True)
        self.canvas.setVisible(False)
        self.toolbar.setVisible(False)
        self.lwListAllData.setVisible(False)
        #self.htmlOutput.setVisible(False)
        
        self.parent.parent.df_DistributionOne = ''
        number_of_topics = self.sbNumberOfTopics.value()
        topic_list = ['Topic ' + str(i) for i in range(number_of_topics)]
        
        self.parent.tabTopic.cbTopics.clear()
        self.parent.tabTopic.cbTopics.addItems(['Select']+topic_list)
        self.parent.tabTopic.cbTopics.setEnabled(True)
        
        self.parent.parent.topicList = topic_list
        
        
        print('start topic')
        
        min_number_doc = int(0.005*len(self.parent.parent.non_duplicate_data))
        #print(min_number_doc)
        
        #vectorizer = CountVectorizer(max_df=0.9, min_df = min_number_doc, token_pattern='\w+|\$[\d\.]+|\S+')
        #vectorizer = CountVectorizer(max_df=0.9, min_df = 20, token_pattern='\w+|\$[\d\.]+|\S+')
        vectorizer = CountVectorizer(max_df=0.9, min_df = min_number_doc, token_pattern=r'[\w\d]+')
        self.parent.parent.vectorizer = vectorizer
        tf = vectorizer.fit_transform(self.parent.parent.non_duplicate_data['Clean'].tolist())
        
        self.parent.parent.vectorized_data =  tf
        
        
        # tf_feature_names tells us what word each column in the matric represents
        tf_feature_names = vectorizer.get_feature_names()
        
               
        print('Prepare model')

        self.parent.parent.lda_model = LatentDirichletAllocation(n_components=number_of_topics, random_state=0)

        self.parent.parent.lda_model.fit(tf)
        
        self.parent.parent.Log_Likelihood = self.parent.parent.lda_model.score(tf)
        
        self.parent.parent.Perplexity = self.parent.parent.lda_model.perplexity(tf)
        
        no_top_words = 20
               
        print('Model is finished')
               
        self.parent.parent.df_topic_words = self.display_topics(self.parent.parent.lda_model, tf_feature_names, no_top_words)
        
        model = pandasModel(self.parent.parent.df_topic_words)
        self.tvTopics.setModel(model)
        #self.tvTopics.setVisible(True)
        self.lbTitleTable.setText('Ten top words for each of ' + str(number_of_topics) + ' topic')
        
        #Create dataframe doc and topics
        doc_topic = self.parent.parent.lda_model.transform(tf)
        df_topic_distribution = pd.DataFrame(doc_topic, columns = topic_list)
        
        # Dominant topics
        # Get dominant topic for each document
        dominant_topic = np.argmax(df_topic_distribution.values, axis=1)
        df_topic_distribution['Dominant'] = dominant_topic
        
        #self.parent.parent.non_duplicate_data
        
        self.parent.parent.df_doc_topic = pd.concat([self.parent.parent.non_duplicate_data['No'],df_topic_distribution], axis = 1, ignore_index = True)
        #self.parent.parent.df_doc_topic.columns = list(self.parent.parent.non_duplicate_data.columns) + list(df_topic_distribution.columns)
        self.parent.parent.df_doc_topic.columns = ['No'] + list(df_topic_distribution.columns)
        self.parent.parent.df_doc_topic['Length'] = self.parent.parent.df_doc_topic['No'].apply(lambda x: len(x))
        
        
        #Explode No
        df_all = self.parent.parent.df_doc_topic.explode('No').reset_index()
        df_all.sort_values('No', inplace = True)
        
        #print(self.parent.parent.df_doc_topic.columns)
        #self.parent.parent.cleaned_data = df_all.merge(self.parent.parent.cleaned_data, on = 'No', how = 'left')
        self.parent.parent.topic_cleaned_data = df_all.merge(self.parent.parent.cleaned_data, on = 'No', how = 'left')
        #print(self.parent.parent.topic_cleaned_data.columns)
        #print('--Atas kolom topic_cleaned_data .....')
        self.parent.tabTopic.setEnabled(True)  
        #self.parent.tabTime.setEnabled(True)
        
        self.parent.parent.df_DistributionOne = pd.DataFrame()
        self.parent.parent.df_DistributionAll = pd.DataFrame()
        
        self.btTopicModeling.setEnabled(False)
        
        if self.parent.parent.useDate:
            #print('Ini masuk tabTime')
            self.parent.tabTime.setVisible(True)
            self.parent.tabTime.setEnabled(True)
            
            #self.parent.tabTime.setVisible(True)
            self.parent.tabTime.lwListAllTopics.clear()
            #print(list(df_topic_distribution.columns))
            self.parent.tabTime.lwListAllTopics.addItems(list(df_topic_distribution.columns[:-1]))
        
        self.btBarAll.setEnabled(True)
        self.btBarOne.setEnabled(True)
        #self.btLDAvis.setEnabled(True)
        self.btSaveGraph.setEnabled(True)
        
    def saveGraph(self):
        filetypes = "GML (*.gml);;GRAPHML (*.graphml)"
        #filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'graph files (*.graphml)')
        filename = QFileDialog.getSaveFileName(self, 'Save File', '', filetypes)
        savename = filename[0]
               
        if len(savename.strip()) == 0:
            self.msgBox.setText("There is no file to save!")
            self.msgBox.setWindowTitle("TopMod Version 0.43")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()
            return
        
        #self.cleaned_data.to_csv(savename, date_format='%Y.%m.%d', encoding = 'utf-8')
        
        
        df = self.parent.parent.df_topic_words
        topics = []
        for i in range(round(len(df.columns)/2)):
            keywords = df[df.columns[i*2]].tolist()
            weights = df[df.columns[i*2+1]].tolist()
            weights = list(map(float, weights))
            topics.append(dict(zip(keywords,weights)))
        
        '''
        print('Topic 0')
        print(topics[0])
        print('Topic terakhir')
        print(topics[-1])
        '''
        # Create list of topics
       

        # Assuming 'topics' is a list of dictionaries containing keywords and their weights for each topic
        '''
        topics = [{'apple': 3, 'banana': 2, 'orange': 1},
                  {'banana': 4, 'kiwi': 3, 'grape': 2},
                  {'apple': 2, 'orange': 1, 'kiwi': 4}]
        '''
        # Create a NetworkX graph
        G = nx.Graph()
        
        # Add nodes with weights
        for topic_keywords in topics:
            for keyword, weight in topic_keywords.items():
                if G.has_node(keyword):
                    G.nodes[keyword]['weight'] += weight
                else:
                    G.add_node(keyword, weight=weight)
        
        # Add edges with weights
        for topic_keywords in topics:
            for keyword_i, weight_i in topic_keywords.items():
                for keyword_j, weight_j in topic_keywords.items():
                    if keyword_i != keyword_j:
                        edge = tuple(sorted([keyword_i, keyword_j]))
                        if G.has_edge(edge[0], edge[1]):
                            G.edges[edge[0], edge[1]]['weight'] += min(weight_i, weight_j)
                        else:
                            G.add_edge(edge[0], edge[1], weight=min(weight_i, weight_j))
        
        # Save the graph as a GML file
        #nx.write_gml(G, 'co_occurrence_graph_with_weights.gml')

        '''
        lst_target = []
        lst_weight = []
        lst_source = []
        for i in range(round(len(df.columns)/2)):
            lst_target = lst_target + df[df.columns[i*2]].tolist()
            lst_weight = lst_weight + df[df.columns[i*2+1]].tolist()
            lst_source = lst_source + ['T'+str(i)]*len(df)
            
        data = {'Source': lst_source, 'Target':lst_target, 'Weight': lst_weight}
        df_data = pd.DataFrame(data)
        
        #print(df_data.head())
        
        df_data = df_data[df_data['Weight'].apply(lambda x: float(x) >0.2)]
        
        G = nx.from_pandas_edgelist(df_data, source='Source', target='Target', edge_attr='Weight', create_using=nx.DiGraph())
        
            
            
        # Assuming 'topics' is a list of lists containing keywords for each topic
        topics = [['apple', 'banana', 'orange'],
                  ['banana', 'kiwi', 'grape'],
                  ['apple', 'orange', 'kiwi']]
        
        # Create a co-occurrence matrix
        co_occurrence_matrix = {}
        for topic in topics:
            for i, keyword_i in enumerate(topic):
                for keyword_j in topic[i + 1:]:
                    edge = tuple(sorted([keyword_i, keyword_j]))
                    co_occurrence_matrix[edge] = co_occurrence_matrix.get(edge, 0) + 1
        
        # Create a NetworkX graph
        # Create a NetworkX graph
        G = nx.Graph()
        for edge, weight in co_occurrence_matrix.items():
            G.add_edge(edge[0], edge[1], weight=weight)    
        '''
        if savename.endswith('graphml'):
            nx.write_graphml(G,savename)
        elif savename.endswith('gml'):
            nx.write_gml(G,savename)    
    
    def display_topics(self, model, feature_names, no_top_words):
        topic_dict = {}
        for topic_idx, topic in enumerate(model.components_):
            topic_dict["T-%d Words" % (topic_idx)]= ['{}'.format(feature_names[i])
                            for i in topic.argsort()[:-no_top_words - 1:-1]]
            topic_dict["T-%d Weights" % (topic_idx)]= ['{:.1f}'.format(topic[i])
                            for i in topic.argsort()[:-no_top_words - 1:-1]]
        return pd.DataFrame(topic_dict)
    
    
    def createBarOne(self):
        '''Create bar chart in which only documents having value greater than topic value
        are counted'''
        
        self.tvTopics.setVisible(False)
        self.canvas.setVisible(True)
        self.toolbar.setVisible(True)
        self.lwListAllData.setVisible(True)
        
        #What if the number of topics has been changed???
        AllTopics = self.parent.parent.topicList
        
        if len(self.parent.parent.df_DistributionOne) == 0:
            topicValue = float(self.cbTopicValue.currentText())
            
            if 'Data' in self.parent.parent.cleaned_data.columns:
                #print('----')
                #print(len(AllTopics))
                #print(AllTopics[:3])
                df = self.parent.parent.topic_cleaned_data[['Data','Text','Clean'] + AllTopics]
            
                
                #df[AllTopics] = df[AllTopics].where(df[AllTopics]>topicValue).notnull().astype('int')
                df[AllTopics] = df[AllTopics].where(df[AllTopics]>topicValue).notnull().astype('int')
                dfgb_data = df.groupby('Data')[AllTopics].sum().reset_index()
                self.parent.parent.df_DistributionOne = dfgb_data
                #print(dfgb_data)
                
            else:
                df = self.parent.parent.topic_cleaned_data[['Text','Clean'] + AllTopics]
                #df[AllTopics] = df[AllTopics].where(df[AllTopics]>topicValue).notnull().astype('int')
                df[AllTopics] = df[AllTopics].where(df[AllTopics]>topicValue).notnull().astype('int')
                self.parent.parent.df_DistributionOne =  df[AllTopics].sum().to_frame().T
                #print(self.parent.parent.df_DistributionOne)
           
        ''' If df_DistributionOne already exist '''
        
        self.figure.clear()
        
        self.axes = self.figure.add_subplot() 
        
        
        df = self.parent.parent.df_DistributionOne
        if 'Data' in df.columns:
            selectedData = [item.text() for item in self.lwListAllData.selectedItems()]
            
            if len(selectedData)>0:
                df_selected = df[df['Data'].isin(selectedData)]
                
                df_selected.set_index('Data', inplace=True)
                #print(df_selected[['Data']+AllTopics[:3]])
                df_selected = df_selected.T
                df_selected.plot.bar(ax = self.axes, logy=True, tick_label = AllTopics)
                
                self.axes.get_yaxis().set_minor_formatter(mticker.FormatStrFormatter('%d'))
                #selectedData = selectedData.sort()
                selectedData.sort()
                self.axes.legend(selectedData)
            else:
                valueAllTopics = df[AllTopics].sum().tolist()
                self.axes.bar(AllTopics, valueAllTopics, tick_label = AllTopics)
                self.axes.tick_params(axis='x', rotation=45)
                self.axes.set_title('Distribution of Topics in ' + str(round(sum(valueAllTopics))) + ' Documents')
            
        else:
            valueAllTopics = self.parent.parent.df_DistributionOne.iloc[0].tolist()
            self.axes.bar(AllTopics, valueAllTopics, tick_label = AllTopics)
            self.axes.tick_params(axis='x', rotation=45)
            self.axes.set_title('Distribution of Topics in ' + str(round(sum(valueAllTopics))) + ' Documents')
        
        self.axes.tick_params(axis='x', rotation=45)
        
        self.canvas.draw()
        
    def createBarAll(self):
        '''Create bar chart in which all topic values of each documents having value are counted'''
        
        self.tvTopics.setVisible(False)
        self.canvas.setVisible(True)
        self.toolbar.setVisible(True)
        self.lwListAllData.setVisible(True)
        
        AllTopics = self.parent.parent.topicList
        
        if len(self.parent.parent.df_DistributionAll) == 0:
            #topicValue = float(self.cbTopicValue.currentText())
            
            if 'Data' in self.parent.parent.topic_cleaned_data.columns:
                self.parent.parent.df_DistributionAll = self.parent.parent.topic_cleaned_data.groupby('Data')[AllTopics].sum().reset_index()
                
            else:
                self.parent.parent.df_DistributionAll = self.parent.parent.topic_cleaned_data[AllTopics].sum().to_frame().T
                
        ''' If df_DistributionOne already exist '''
        
        self.figure.clear()
        
        self.axes = self.figure.add_subplot() 
        
        
        df = self.parent.parent.df_DistributionAll
        if 'Data' in df.columns:
            selectedData = [item.text() for item in self.lwListAllData.selectedItems()]
            
            if len(selectedData)>0:
                #print(selectedData)
                df_selected = df[df['Data'].isin(selectedData)]
                
                df_selected.set_index('Data', inplace=True)
                #print(df_selected[['Data']+AllTopics[:3]])
                df_selected = df_selected.T
                df_selected.plot.bar(ax = self.axes, logy=True, tick_label = AllTopics)
                
                self.axes.get_yaxis().set_minor_formatter(mticker.FormatStrFormatter('%d'))
                #selectedData = selectedData.sort()
                selectedData.sort()
                self.axes.legend(selectedData)
            else:
                valueAllTopics = df[AllTopics].sum().tolist()
                self.axes.bar(AllTopics, valueAllTopics, tick_label = AllTopics)
                self.axes.tick_params(axis='x', rotation=45)
                self.axes.set_title('Distribution of Topics in ' + str(round(sum(valueAllTopics))) + ' Documents')
            
        else:
            valueAllTopics = self.parent.parent.df_DistributionAll.iloc[0].tolist()
            self.axes.bar(AllTopics, valueAllTopics, tick_label = AllTopics)
            self.axes.tick_params(axis='x', rotation=45)
            self.axes.set_title('Distribution of Topics in ' + str(round(sum(valueAllTopics))) + ' Documents')
        
        self.axes.tick_params(axis='x', rotation=45)
        
        self.canvas.draw()
        



class tabTopic(QTabWidget):
    def __init__(self, parent): 
        #super(QWidget, self).__init__(parent)
        super(QTabWidget, self).__init__(parent)
        
        self.parent = parent
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setVisible(False)
        
        self.tvTopics = QTableView()
        self.tvTopics.setVisible(False)
        
        self.msgBox = QMessageBox()
        
        self.lbSelectTopic = QLabel()
        self.lbSelectTopic.setText('Select ')
        self.lbSelectTopic.setAlignment(Qt.AlignRight)
        
        self.cbTopics = QComboBox()
        self.cbTopics.setEnabled(False)
        self.cbTopics.currentTextChanged.connect(self.changedTopic)
               
        self.btShowDocs = QPushButton()
        self.btShowDocs.setText('Show Docs per Topic')
        self.btShowDocs.clicked.connect(self.showDocs)
        
        self.btCreateWordCloud = QPushButton('WordCloud')
        self.btCreateWordCloud.clicked.connect(self.createWordCloud)
        self.btCreateWordCloud.setEnabled(False)
        
        self.lbTitleTable = QLabel()
        
        self.glayout = QGridLayout()
        
        self.glayout.addWidget(self.lbSelectTopic, 0, 0)
        self.glayout.addWidget(self.cbTopics, 0, 1)
        self.glayout.addWidget(self.btShowDocs, 0, 2)
        self.glayout.addWidget(self.btCreateWordCloud, 0, 3)
        self.glayout.addWidget(self.toolbar, 1, 0, 1, 2)
        self.glayout.addWidget(self.lbTitleTable, 1,2,1,2)
        self.glayout.addWidget(self.canvas, 2, 0, 5, 4)
        self.glayout.addWidget(self.tvTopics, 2, 0, 5, 4)
        
        self.setLayout(self.glayout)
        
       
        
    def changedTopic(self):
        self.tvTopics.setVisible(False)
        self.canvas.setVisible(False)
        self.toolbar.setVisible(False)
        self.parent.parent.selected_topic = pd.DataFrame()
        self.btShowDocs.setEnabled(True)
        self.btCreateWordCloud.setEnabled(False)
    
    def showDocs(self):
        #print('show Docs')
        self.tvTopics.setVisible(True)
        self.canvas.setVisible(False)
        self.toolbar.setVisible(False)
        
        topicValue = float(self.parent.tabTopicModel.cbTopicValue.currentText())
        
        selected_column = self.cbTopics.currentText()
        
        if selected_column == 'Select':
            return
        
        self.parent.tabTopic.btCreateWordCloud.setVisible(True)
        
        
        #df = self.parent.parent.df_selected_data_value
        
        df = self.parent.parent.topic_cleaned_data
        #print(df.columns)
        
        df = df[df[selected_column]>topicValue]
        
        
        if 'Data' in df.columns:
            df = df[['Data', 'Text','Clean', selected_column]]
            #print(df.columns)
            selectedData = [item.text() for item in self.parent.tabTopicModel.lwListAllData.selectedItems()]
            #print(df.head())
            df.sort_values(selected_column, ascending = False, inplace = True)
            #print(df.columns)
            
            if len(selectedData)>0:
                df = df[df['Data'].isin(selectedData)]
                
                
            else:
                pass
        else:
            df = df[['Text','Clean', selected_column]]
            df.sort_values(selected_column, ascending = False, inplace = True)
            
            
        model = pandasModel(df)
        #self.parent.parent.selected_topic = group_selected_topic
        self.parent.parent.selected_topic = df
        
        self.tvTopics.setModel(model)
        self.tvTopics.setVisible(True)
        
        self.tvTopics.setVisible(True)
        self.btShowDocs.setEnabled(False)
        self.btCreateWordCloud.setEnabled(True)
        
        
        
    def createWordCloud(self):
        self.tvTopics.setVisible(False)
        self.canvas.setVisible(True)
        self.toolbar.setVisible(True)
        
        df = self.parent.parent.selected_topic
        
        if df.empty:
            self.msgBox.setText("Please select topic and click \"Show Docs per Topic\" button")
            self.msgBox.setWindowTitle("Select topic")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()
            return
        
        wordcloud = WordCloud(max_words = 30, background_color = 'white').generate(' '.join(df['Clean'].to_list()[:30]))
        #print(len(self.parent.parent.stopWords))
        
        self.figure.clear()
        self.axes = self.figure.add_subplot()    
        self.axes.set_title('The wordcloud of ' + self.cbTopics.currentText())
        #self.canvas.axes.clear()
        #self.canvas.axes.axis("off")
        self.axes.axis("off")
        #self.canvas.axes.imshow(wordcloud)
        self.axes.imshow(wordcloud)
        self.canvas.draw()
        self.btShowDocs.setEnabled(True)
        self.btCreateWordCloud.setEnabled(False)
            
        
class tabTime(QTabWidget):
    def __init__(self, parent): 
        #super(QWidget, self).__init__(parent)
        super(QTabWidget, self).__init__(parent)
        
        self.parent = parent
        
        #To see if the data is user of hashtag
        #self.type_of_data = ''
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
                
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        
        
        
        self.msgBox = QMessageBox()
        self.glayout = QGridLayout()
        #self.graph_hlayout = QHBoxLayout() 
        
        self.lbUserHashtag = QLabel()
        
        self.lwListAllTopics = QListWidget()
        self.lwListAllTopics.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )
        
        self.lwListAllData = QListWidget()
        self.lwListAllData.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )
        
               
        self.btAllTime = QPushButton()
        self.btAllTime.setText('Chart for All Time')
        self.btAllTime.clicked.connect(self.createPlotAllTime)
        
        
        #Row labels
        #self.glayout.addWidget(self.lbUserHashtag, 0, 0)
        self.glayout.addWidget(self.btAllTime, 0, 1)
        
        
        self.glayout.addWidget(self.toolbar, 0, 1, 1, 4)
        
        self.glayout.addWidget(self.lwListAllTopics, 0, 0, 3, 1)
        self.glayout.addWidget(self.lwListAllData, 3, 0, 1, 1)
        
        
        self.glayout.addWidget(self.canvas, 1, 1, 4, 5)
        
        
        self.glayout.setRowStretch(1, 5)
        self.glayout.setColumnStretch(2,4)
 
        self.setLayout(self.glayout)

        
    def createPlotAllTime(self):
        self.figure.clear()
        self.canvas.draw()
        
        selectedTopics = [item.text() for item in self.lwListAllTopics.selectedItems()]
        
        if len(selectedTopics) == 0:
            self.msgBox.setText("Please select at least one topic")
            self.msgBox.setWindowTitle("Select topic")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()
            return
        
        if 'Data' in self.parent.parent.topic_cleaned_data.columns:
            
            selectedData = [item.text() for item in self.lwListAllData.selectedItems()]
            
            df = self.parent.parent.topic_cleaned_data[['Date', 'Data']+self.parent.parent.topicList]
            self.parent.parent.df_date = df.groupby(['Date', 'Data'])[self.parent.parent.topicList].agg('sum').reset_index()
            
            self.parent.parent.df_date.sort_values(['Date','Data'], ascending = True, inplace = True)
            
            if len(selectedData)>0:
                
                df = df[df['Data'].isin(selectedData)]
                
            else:
                df = df[['Date']+self.parent.parent.topicList]
                #self.parent.parent.df_date = df.sort_values(['Date','Data'], ascending = True)
        else:
            df = self.parent.parent.topic_cleaned_data[['Date']+self.parent.parent.topicList]
            self.parent.parent.df_date = df.groupby('Date')[self.parent.parent.topicList].agg('sum').reset_index()
            
            self.parent.parent.df_date.sort_values('Date', ascending = True, inplace = True)
            
        df_date = df.groupby(['Date'])[selectedTopics].agg('sum').reset_index()
        from_date = df_date['Date'].min()
        to_date = df_date['Date'].max()
        
        if len(str(df_date['Date'].iloc[0])) > 4:
            #self.parent.parent.df_date.set_index('Date', inplace = True)
            df_date.set_index('Date', inplace = True)
            
            
            #if from_date == to_date:
            d = timedelta(days = 2)
            from_date = from_date - d
            to_date = to_date + d
                
            idx = pd.date_range(from_date, to_date)
            df_date = df_date.reindex(idx, fill_value=0)
        else:
            df_date.set_index('Date', inplace = True)
        
        self.figure.clear()
        #df_temp = df_overtime.groupby([df_overtime.index, df_overtime.columns[0]])[df_overtime.columns[-1]].first().unstack()
        
        self.axes = self.figure.subplots()
        
        #df_date.fillna(0).plot(ax = self.axes)
        df_date.plot(ax = self.axes)
        
        self.axes.set_title('Plot from ' + str(from_date) + ' to ' + str(to_date))
        
        self.axes.legend(selectedTopics)
        self.canvas.draw()
        
        
class tabCooccur(QTabWidget):
    def __init__(self, parent): 
        #super(QWidget, self).__init__(parent)
        super(QTabWidget, self).__init__(parent)
        
        self.parent = parent
                
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setVisible(False)
        
        self.msgBox = QMessageBox()
        
        self.btShowAllWords = QPushButton()
        self.btShowAllWords.setText('Show All Words')
        self.btShowAllWords.clicked.connect(self.showAllWords)
        
        self.tvWords = QTableView()
        
        self.dfAllWords = pd.DataFrame()
        
        self.lbMinFreq = QLabel('Minimum Frequency')
        self.sbFreq = QSpinBox()
        
        #self.lbWords = QLabel('Words')
        
        self.lbWindowSpan = QLabel('Window Span')
        self.sbWindowSpan = QSpinBox()
        self.sbWindowSpan.setMinimum(1)
        self.sbWindowSpan.setMaximum(10)
        self.sbWindowSpan.setValue(5)
        
        
        self.btCreateCooccurence = QPushButton()
        self.btCreateCooccurence.setText('Create Word Cooccurence')
        self.btCreateCooccurence.clicked.connect(self.createWordCooccurence)
        self.btCreateCooccurence.setEnabled(False)
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setVisible(False)
        
        self.glayout = QGridLayout()
        
        self.glayout.addWidget(self.btShowAllWords, 0, 0)
        self.glayout.addWidget(self.lbMinFreq, 0, 1)
        self.glayout.addWidget(self.sbFreq, 0, 2)
        self.glayout.addWidget(self.lbWindowSpan,0,4)
        self.glayout.addWidget(self.sbWindowSpan,0,5)
        self.glayout.addWidget(self.btCreateCooccurence, 0, 6)
        self.glayout.addWidget(self.tvWords,1, 0, 5, 1)
        self.glayout.addWidget(self.toolbar, 1, 1, 1, 5)
        #self.glayout.addWidget(self.lbTitleTable, 1,2,1,2)
        self.glayout.addWidget(self.canvas, 2, 1, 4, 6)
        #self.glayout.addWidget(self.tvTopics, 2, 0, 5, 4)
        
        self.setLayout(self.glayout)
        
        
    def showAllWords(self):
        # Function to count words in a single sentence
        def count_words(sentence):
            words = sentence.split()
            return len(words)
        
        def calculate_median(sorted_list):
            length = len(sorted_list)
        
            if length % 2 == 0:
                # If the length is even, calculate the average of the middle two elements
                mid1 = sorted_list[length // 2 - 1]
                mid2 = sorted_list[length // 2]
                median = (mid1 + mid2) / 2
            else:
                # If the length is odd, the median is the middle element
                median = sorted_list[length // 2]
        
            return median

        
        df = self.parent.parent.cleaned_data
        #df = df.loc[df['Clean'].notna()]
        #print(df.columns)
        all_words = ' '.join(df['Clean'].tolist()).split()
        total_number_of_words = df['Clean'].apply(count_words).sum()
        #print('tota words ' + str(total_number_of_words))
        self.total_words = total_number_of_words
        
        count_words = collections.Counter(all_words)
        self.count_words = count_words
        
        df_words = pd.DataFrame(count_words.items(), columns=['word','count'])
        df_words = df_words.sort_values(by = 'count', ascending=False)
        df_words.reset_index()
        
        highest_freq = count_words.most_common(1)[0][1]
        lowest_freq = count_words.most_common()[-1][1]
        
        self.sbFreq.setRange(lowest_freq,highest_freq)
        
        median = calculate_median(list(set(df_words['count'].to_list())))
                
        self.sbFreq.setValue(median)
        
        
        self.dfAllWords = df_words        
        model = dictionaryModel(self.dfAllWords)
        #model = SelectedWordsModel(self.dfAllWords)
        self.tvWords.setModel(model)
        self.tvWords.setVisible(True)
        self.btCreateCooccurence.setEnabled(True)
        
        
    def createWordCooccurence(self):
        minFreq = self.sbFreq.value()
        self.dfAllWords = self.dfAllWords.loc[self.dfAllWords['count']>(minFreq-1)]
        model = dictionaryModel(self.dfAllWords)
        self.tvWords.setModel(model)
        self.tvWords.setVisible(True)
        
        filetypes = "GML (*.gml);;GRAPHML (*.graphml)"
        #filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'graph files (*.graphml)')
        filename = QFileDialog.getSaveFileName(self, 'Save File', '', filetypes)
        savename = filename[0]
               
        if len(savename.strip()) == 0:
            self.msgBox.setText("There is no file to save!")
            self.msgBox.setWindowTitle("LitNetwork Version 0.25")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()
            return
        
        selected_words = self.dfAllWords['word'].tolist()
        selected_counts = self.dfAllWords['count'].tolist()
        #print(self.dfAllWords.head())
        
        print(selected_words[:10])
        
        dtopwords = {}
        for idx,w in enumerate(selected_words):
            dtopwords[w] = selected_counts[idx]
        
        df = self.parent.parent.cleaned_data  
        
        # Get the selected window span (n)
        window_span = self.sbWindowSpan.value()
        
        # Initialize an empty co-occurrence matrix with zeros
        #co_occurrence_matrix = np.zeros((len(top_words), len(top_words)), dtype=int)
        co_occurrence_matrix = np.zeros((len(selected_words), len(selected_words)), dtype=int)
        
        # Function to update the co-occurrence matrix
        def update_co_occurrence(text, matrix, selected_words, window_span):
            
            words = text.split()
            for i in range(len(selected_words)):
                if selected_words[i] in words:
                    for j in range(len(selected_words)):
                        if selected_words[j] in words:
                            if abs(words.index(selected_words[i]) - words.index(selected_words[j])) < window_span + 1:
                                matrix[i][j] += 1
            
        # Apply the function to update the co-occurrence matrix for each row in the DataFrame
        for text in df['Clean']:
            update_co_occurrence(text, co_occurrence_matrix, selected_words, window_span)
        
        # Create a DataFrame from the co-occurrence matrix
        co_occurrence_df = pd.DataFrame(co_occurrence_matrix, columns=selected_words, index=selected_words)
        
        #From Jupyter notebook
        
        def calculate_pmi(co_occurrence_matrix):
            total_docs = co_occurrence_matrix.sum()
            word_counts = np.array(co_occurrence_matrix.sum(axis=0)).flatten()
            pmi_matrix = np.log(co_occurrence_matrix * total_docs / (word_counts.reshape(-1, 1) * word_counts))
            pmi_matrix[np.isinf(pmi_matrix)] = 0  # Handle cases where the PMI is -inf (due to zero co-occurrences)
            return pmi_matrix
        
        pmi_matrix = calculate_pmi(co_occurrence_matrix)
        
        # Create a DataFrame from the PMI matrix
        pmi_df = pd.DataFrame(pmi_matrix, columns=selected_words, index=selected_words)
        
        
        G = nx.Graph()

        # Add nodes to the graph
        for word in selected_words:
            G.add_node(word, weight = dtopwords[word])
        
        # Add weighted edges based on PMI scores
        for i in range(len(selected_words)):
            for j in range(i + 1, len(selected_words)):
                word1 = selected_words[i]
                word2 = selected_words[j]
                pmi_score = pmi_matrix[i][j]
                if pmi_score > 0:
                    G.add_edge(word1, word2, value=pmi_score)

              
        
        
        if savename.endswith('graphml'):
            nx.write_graphml(G,savename)
            #iG.write_graphml(savename)
            #G.save(savename, format = "graphml")
        elif savename.endswith('gml'):
            #iG.write_gml(savename)
            #G.save(savename, format = "gml")
            nx.write_gml(G, savename)
        
        
        
        
        self.canvas.draw_idle()
        self.canvas.setVisible(True)
        
         
        #nx.write_gml(G, 'test.gml')
        
        #print(cooccurrence)
        
class tabData(QTabWidget):
    def __init__(self, parent): 
        #super(QWidget, self).__init__(parent)
        super(QTabWidget, self).__init__(parent)
        
        self.parent = parent
        
        #To see if the data is user of hashtag
        #self.type_of_data = ''
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
                
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        
        
        
        self.msgBox = QMessageBox()
        self.glayout = QGridLayout()
        #self.graph_hlayout = QHBoxLayout() 
        
        self.lbUserHashtag = QLabel()
        
        self.lwListAllData = QListWidget()
        self.lwListAllData.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )
        self.lwListAllData.setVisible(False)
        
               
        self.btData = QPushButton()
        self.btData.setText('Plot Data')
        self.btData.clicked.connect(self.createPlotData)
        
        self.glayout.addWidget(self.btData, 0, 0)
        self.glayout.addWidget(self.toolbar, 0, 1, 1, 4)
        
        self.glayout.addWidget(self.lwListAllData, 1, 0, 4, 1)
        
        self.glayout.addWidget(self.canvas, 1, 1, 3, 3)
        
        
        self.glayout.setRowStretch(1, 4)
        self.glayout.setColumnStretch(1, 4)
 
        self.setLayout(self.glayout)

        
    def createPlotData(self):
        self.figure.clear()
        self.canvas.draw()
        #df = self.parent.parent.df_doc_topic
        
        #topicList = [self.lwListAllTopics.item(idx) for idx in range(self.lwListAllTopics.count())]
        AllTopics = self.parent.parent.topicList
          
        #print(topicList)
        if len(self.parent.parent.df_datafile) == 0:
            df = self.parent.parent.cleaned_data[['Data']+AllTopics]
            self.parent.parent.df_datafile = df.groupby(['Data'])[AllTopics].agg('sum').reset_index()
        
        selectedData = [item.text() for item in self.lwListAllData.selectedItems()]
                
        self.figure.clear()
        
        df_selected = self.parent.parent.df_datafile[self.parent.parent.df_datafile['Data'].isin(selectedData)]
        self.axes = self.figure.add_subplot() 
        df_selected.set_index('Data', inplace=True)
        #print(df_selected[['Data']+AllTopics[:3]])
        df_selected = df_selected.T
        df_selected.plot.bar(ax = self.axes, logy=True, tick_label = AllTopics)
        
        self.axes.get_yaxis().set_minor_formatter(mticker.FormatStrFormatter('%d'))
        
        self.axes.tick_params(axis='x', rotation=45)
        self.axes.legend(selectedData)
        self.canvas.draw()
        
class tabKataDalamKonteks(QTabWidget):
    def __init__(self, parent): 
        #super(QWidget, self).__init__(parent) 
        super(QTabWidget, self).__init__(parent)
        
        self.parent = parent
        
        self.df_hasil = pd.DataFrame()
        #Ada di baris pertama
        self.glayout = QGridLayout()
        
        #self.btVisual = QPushButton('Visualization')
        #self.btVisual.clicked.connect(self.visualizingData)
        
        self.lbCariKata = QLabel()
        self.lbCariKata.setText('Search')
        self.leCariKata = QLineEdit()
                
            
        self.lbSearch = QLabel('Search')
        self.btCariKataKotor = QPushButton()
        self.btCariKataKotor.setText('Original')
        self.btCariKataKotor.clicked.connect(lambda x: self.cariKataDiData('Text'))
        self.btCariKataBersih = QPushButton()
        self.btCariKataBersih.setText('Cleaned')
        self.btCariKataBersih.clicked.connect(lambda x: self.cariKataDiData('Clean'))
        #self.lbTweet = QLabel('Tweets')
        self.btHapusDuplikasi = QPushButton()
        self.btHapusDuplikasi.setText('Eliminate Duplications')
        self.btHapusDuplikasi.setEnabled(False)
        self.btHapusDuplikasi.clicked.connect(self.hapusDuplikasi)
        
        self.lbJumlahCuitan = QLabel()
        self.lbJumlahCuitan.setAlignment(Qt.AlignCenter)
        self.btSimpanKWIC = QPushButton()
        self.btSimpanKWIC.setText('Save') 
        self.btSimpanKWIC.clicked.connect(self.simpanKWIC)
        
        self.tblKataData = QTableView()
        
        
        self.glayout.addWidget(self.lbCariKata, 0, 0)
        self.glayout.addWidget(self.leCariKata, 0, 1)
        
        self.glayout.addWidget(self.lbSearch, 0, 6)
        self.glayout.addWidget(self.btCariKataKotor, 0, 7)
        self.glayout.addWidget(self.btCariKataBersih, 0, 8)
        #self.glayout.addWidget(self.lbTweet, 0, 9)
        #self.glayout.addWidget(self.btHapusDuplikasi, 0, 10)
        
        #self.glayout.addWidget(self.btVisual, 1, 0, 1, 2)
        self.glayout.addWidget(self.lbJumlahCuitan, 1, 2, 1, 8)
        self.glayout.addWidget(self.btSimpanKWIC, 1, 10, 1, 2) 
        
        self.glayout.addWidget(self.tblKataData, 2, 0, 7, 12)
        
        self.setLayout(self.glayout)
        
    
    def visualizingData(self):
        #print("Masuk visualizing")
        
        self.parent.parent.all_data = self.df_hasil
        self.parent.tabFrequency.btMainData.setText("Back to Main Data")
        self.parent.tabFrequency.btMainData.setEnabled(True)
        #self.parent.tabFrequency.dataForGraph = {}
        #self.parent.tabFrequency.turnPlot("off")
        self.parent.tabFrequency.figure.clear()
        self.parent.tabFrequency.canvas.draw()
        self.parent.tabFrequency.tblCategory.setVisible(False)
        self.parent.tabFrequency.cbDariTanggal.setCurrentText(self.parent.parent.list_of_dates[0])
        self.parent.tabFrequency.cbDariTanggal.setEnabled(False)
        self.parent.tabFrequency.cbSampaiTanggal.setCurrentText(self.parent.parent.list_of_dates[-1])
        self.parent.tabFrequency.cbSampaiTanggal.setEnabled(False)
        
        #This is just to make the program check the data
        self.parent.tabFrequency.boolChangedDateDate = True
        
        
        self.parent.tabs.setCurrentIndex(1)
        self.parent.tabKata.setEnabled(False)
    
    
    def simpanKWIC(self):
        filename = QFileDialog.getSaveFileName(self, "Save Plot As", "data.csv", "*.csv")
        savename = filename[0]
        if savename:
            self.df_hasil.to_csv(savename)
        
    def hapusDuplikasi(self):
        #df = self.df_hasil.groupby(['Left','Keywords','Right']).size().to_frame()
        df = self.df_hasil.groupby(['Left','Keywords','Right','RT'])['User'].count().to_frame().reset_index()
        df = df.reset_index().sort_values('User', ascending = False)
        
        df.rename(columns = {'User':'#Users'}, inplace=True)
        df = df[['#Users','Left','Keywords','Right','RT']]
        model = pandasModelKWIC(df)
        self.tblKataData.setModel(model)
        self.btHapusDuplikasi.setEnabled(False)
        #self.lbJumlahCuitan.setText('Number of Tweets = ' + str(len(self.df_hasil)))
        self.lbJumlahCuitan.setText('Number of Tweets = ' + str(len(df)))
        
        
    def cariKataDiData(self, kolom):
        self.tblKataData.setVisible(True)
        cari_kata = self.leCariKata.text().split()
        if not cari_kata:
            return
        
        #print('Kata yang dicari adalah ') 
        #print(cari_kata)
        
        #df = self.parent.parent.all_data[kolom].to_frame()
        df = self.parent.parent.cleaned_data
        #df = df[['User', kolom, 'RT']].copy()
        #df = df[[kolom]]
        
        keyword_list = []
        left_list = []
        right_list = []
        
        daftar_cari = '|'.join([r'\b' + re.escape(kata).replace(r'\*', r'\w*') + r'\b' for kata in cari_kata])
        #print(daftar_cari)
        text_list = df.loc[df[kolom].str.contains(daftar_cari, regex=True, case=False)][kolom].to_list()
        
        for text in text_list:
            #daftar_cari = '|'.join([r'\b' + re.escape(kata).replace(r'\*', r'\w*') + r'\b' for kata in term.split()])    
            match = re.search(daftar_cari, text, re.IGNORECASE)
            #print(match[0])
            keyword = match[0]
            text_list = text.split(keyword)
            left_context = text_list[0]
            right_context = ' '.join(text_list[1:])
            
            window_span = 9
            left_context = ' '.join(left_context.split(' ')[-min(window_span,len(left_context)):])
            right_context = ' '.join(right_context.split(' ')[:min(window_span, len(right_context))])
            
            left_list.append(left_context)
            right_list.append(right_context)
            keyword_list.append(keyword)
        
        self.df_hasil = pd.DataFrame({'Left': left_list, 'Keyword': keyword_list, 'Right': right_list})
            
        
        '''
        #daftar_cari = '|'.join([ '(?<!\w)'+ kata.replace(r'*',r'\w*')+'(?!\w)' for kata in cari_kata])
        #daftar_cari = '|'.join([ r'(?<!\w)'+ kata.replace(r'*',r'\w*')+r'(?!\w)' for kata in cari_kata])
        #daftar_cari = '|'.join([ r'\b'+ kata.replace(r'*',r'\w*')+r'\b' for kata in cari_kata])
        
        daftar_cari = '|'.join([r'\b' + re.escape(kata).replace(r'\*', r'\w*') + r'\b' for kata in cari_kata])

        
        self.df_hasil = df.loc[df[kolom].str.contains(daftar_cari, regex=True, case=False)].copy()
        if len(self.df_hasil) == 0:
            self.pesanTiadaCuitan()            
            return

        self.df_hasil['Keywords'] = self.df_hasil[kolom].\
            apply(lambda x: re.search(daftar_cari, x, re.IGNORECASE)[0] if re.search(daftar_cari, x) is not None else '').copy()
            
        #self.df_hasil['Left'] = self.df_hasil.apply(lambda x: x[kolom][:x[kolom].find(x['Keywords'])], axis=1).copy()
        Left_Part = self.df_hasil.apply(lambda x: x[kolom][:x[kolom].find(x['Keywords'])], axis=1).copy()
        self.df_hasil['Left'] = Left_Part.apply(lambda x: x if len(x.split(' '))<10 else ' '.join(x.split(' ')[-10:]))
        
        #self.df_hasil['Right'] = self.df_hasil.apply(lambda x: x[kolom][x[kolom].find(x['Keywords'])+len(x['Keywords']):], axis=1).copy()
        Right_Part = self.df_hasil.apply(lambda x: x[kolom][x[kolom].find(x['Keywords'])+len(x['Keywords']):], axis=1).copy()
        self.df_hasil['Right'] = Right_Part.apply(lambda x: x if len(x.split(' '))<10 else ' '.join(x.split(' ')[:10]))
        '''
        
        
        if len(self.df_hasil) == 0:
            self.pesanTiadaCuitan() 
            return
        
        #df = self.df_hasil[['User','Left', 'Keywords','Right', 'RT']]
        #df = self.df_hasil[['Text', 'Clean']]
        #model = pandasModelKWIC(self.df_hasil)
        model = pandasModelKWIC(self.df_hasil[['Left','Keyword', 'Right']])
        '''
        print(self.df_hasil.columns)
        print(self.df_hasil['Keywords'])
        print('Left')
        print(self.df_hasil['Left'])
        '''
        self.tblKataData.setModel(model)
        self.tblKataData.resizeColumnToContents(1)
        self.tblKataData.setColumnWidth(1,400)
        self.tblKataData.setColumnWidth(3,400)
        
        #self.btHapusDuplikasi.setEnabled(True)
        
        self.lbJumlahCuitan.setText('Number of Texts = ' + str(len(self.df_hasil)))
        
    def pesanTiadaCuitan(self):
        QMessageBox.about(self, "Warning", "There is no Text")
        self.tblKataData.setVisible(False)
        self.lbJumlahCuitan.setText('')

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None
    

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class pandasModelKWIC(pandasModel):
    def data(self, index, role = Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        elif role == Qt.BackgroundRole:
            if index.column() == 1:
                return QBrush(QColor(230,230,230))
                #return QBrush(Qt.green)
            elif index.row() % 2 == 0:
                return QBrush(QColor(240,240,240))
            else:
                return QBrush(Qt.white)
            
            
            #return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            if index.column() == 0:
                return Qt.AlignRight
            if index.column() == 1:
                return Qt.AlignCenter
            elif index.column() == 2:
                return Qt.AlignLeft
            if index.column() == 3:
                return Qt.AlignLeft
            else:
                return Qt.AlignLeft

        return None
    

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        elif role == Qt.BackgroundRole:
            return QBrush(Qt.green)
        return None
    
class dictionaryModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)
    

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
        
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        self._data.iloc[index.row(),index.column()] = value
        self.dataChanged.emit(index, index, (QtCore.Qt.DisplayRole, ))
        return True 
    



class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None
    

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
    
#This class to make tableview editable

class MyDelegate(QItemDelegate):

    def createEditor(self, parent, option, index):
        if index.column() == 2:
            return super(MyDelegate, self).createEditor(parent, option, index)
        return None

    def setEditorData(self, editor, index):
        if index.column() == 2:
            # Gets display text if edit data hasn't been set.
            text = index.data(Qt.EditRole) or index.data(Qt.DisplayRole)
            editor.setText(text)

def main():
       
    
    app = QApplication(sys.argv) 
    ex = App() 
    sys.exit(app.exec_()) 
  
if __name__ == '__main__': 
    # Pyinstaller fix
    #multiprocessing.freeze_support()
    
    main()
    
    '''
    app = QApplication(sys.argv) 
    ex = App() 
    sys.exit(app.exec_()) 
    '''
