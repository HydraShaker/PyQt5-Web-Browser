# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 17:44:52 2020

@author: Hafikan Yesilyurt
"""

import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import QWebView , QWebPage
from PyQt5.QtPrintSupport import * 

class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
       
        self.setWindowTitle("Web Browser")
        self.setWindowIcon(QIcon("logo.png"))
        self.setMinimumSize(500,500)
        self.showMaximized()       
        self.tab = QTabWidget()
        self.tab.tabBarDoubleClicked.connect(self.tab_open_doubleclick) 
        self.setCentralWidget(self.tab)
        self.navBar = QToolBar(self)
        self.navBar.setStyleSheet("background:#333;color:white")
        self.navBar.setFixedHeight(55)
        self.navBar.setMovable(False)
        self.addToolBar(self.navBar)
        self.backBtn= QAction("<",self)
        self.backBtn.triggered.connect(lambda: self.tab.currentWidget().back())

        #barımıza fonksiyonları ekliyoruz
        self.navBar.addAction(self.backBtn)
        self.nextBtn =QAction(">",self)
        self.nextBtn.triggered.connect(lambda: self.tab.currentWidget().forward())
        self.navBar.addAction(self.nextBtn)
        
        self.reBtn = QAction("Reload",self)
        self.reBtn.triggered.connect(lambda: self.tab.currentWidget().reload())  
        self.navBar.addAction(self.reBtn)
        self.linkBar = QLineEdit(self)
        self.linkBar.returnPressed.connect(self.goLink)
        self.navBar.addWidget(self.linkBar)
        self.createNewTab(QUrl("https://www.google.com/"))
        
        
    def createNewTab(self,url):
        brw = QWebView()
        brw.setUrl(url)
        i = self.tab.addTab(brw,"HomePage")
        brw.urlChanged.connect(lambda url, brw = brw: self.updateLinkArea(url,brw))   

        
    def goLink(self):
        mainLink = self.linkBar.text()
        mainLink = mainLink.split("/")
        mainLink = mainLink[len(mainLink)-1]


        u = QUrl("https://www.google.com/search?q=" + mainLink)
        if u.scheme() == "":
            u.setScheme("http")
        self.tab.currentWidget().setUrl(u)
        

    def tab_open_doubleclick(self):
        self.newTab = QWebView()
        url = "https://www.google.com/"
        self.newTab.setUrl(QUrl(url))
        self.tab.addTab(self.newTab,"New Page")
        self.newTab.urlChanged.connect(lambda url, brw = self.newTab: self.updateLinkArea(url,self.newTab)) 
        self.linkBar.setCursorPosition(0)   

    def updateLinkArea(self, u, brw =None):
        self.linkBar.setText(u.toString())


app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
        
