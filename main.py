# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 17:44:52 2020

@author: Hafikan Yesilyurt
"""


# -*- coding: utf-8 -*-
import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import * 

class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #uygulamamızın arayüz detaylarını belirliyoruz.
        self.setWindowTitle("Kerberos Web Browser")
        self.setWindowIcon(QIcon("logo.png"))
        self.setMinimumSize(500,500)
        self.showMaximized()       
        
        #İlgili modulümüzü dahil ediyourz
        self.tab = QTabWidget()

        #TabWidget uygulamasının Tab alanını gizlemek için aşağıdaki fonksiyonu çağırıyoruz.

        self.tab.tabBarDoubleClicked.connect(self.tab_open_doubleclick) 


        #Tab widgetımızı qt arayüzümüze yerleştiriyoruz
        self.setCentralWidget(self.tab)
    
        #Link alanımızı ve buttonlarımızı kapsıcak olan Navigation Barımızı çağırıyoruz
        self.navBar = QToolBar(self)

        #biraz da şuraya color katalım :)
        self.navBar.setStyleSheet("background:#333;color:white")

        #Nav barımızı yüksekliğini ve yer değiştirme özelliğini ayarlıyoruz
        self.navBar.setFixedHeight(55)
        self.navBar.setMovable(False)

        #arayüzümüze ekliyoruz
        self.addToolBar(self.navBar)
        
        #ileri geri ve reload buttonlarımız için QAction fonksiyonumuzu çağırıyoruz
        self.backBtn= QAction("<",self)

        #butonlara tıklandığında istenilen işlemleri gerçekleştirmesi için QTabWidget modulümüze at 'currentWidget'ı çağırıyoruz
        self.backBtn.triggered.connect(lambda: self.tab.currentWidget().back())

        #barımıza fonksiyonları ekliyoruz
        self.navBar.addAction(self.backBtn)

        #backBtn deki işlemleri sırasıyla next ve reload butonlarımıza uyguluyoruz  
        self.nextBtn =QAction(">",self)
        self.nextBtn.triggered.connect(lambda: self.tab.currentWidget().forward())
        self.navBar.addAction(self.nextBtn)
        
        self.reBtn = QAction("Reload",self)
        self.reBtn.triggered.connect(lambda: self.tab.currentWidget().reload())  
        self.navBar.addAction(self.reBtn)
        
        #link alanımız için QlineEdit modulümüzü çağırıyoruz
        self.linkBar = QLineEdit(self)

        #link alanı doldurup enter tuşuna bastıktan sonra ilgili fonksiyona bağlanmasını sağlıyoruz
        self.linkBar.returnPressed.connect(self.goLink)

        

        #link alanımızı barımıza ekliyoruz
        self.navBar.addWidget(self.linkBar)
        
        #başlangıçta açılacak sayfamızı ilgili fonksiyonla belirliyoruz
        self.createNewTab(QUrl("https://www.google.com/"))
        
        
    def createNewTab(self,url):

        #browserımızın temelini oluşturcak olan QWebEngineView modulünü çağırıyoruz
        brw = QWebEngineView()

        #belirtilen linke gitmesi için urlmizi belirliyoruz.
        brw.setUrl(url)
        
        #tab alanımıza browserımızı ekliyoruz ki browserımız tab widgetın altında çalışabilsin.
        i = self.tab.addTab(brw,"HomePage")
        
        #linkimiz yani üzerinde gezindiğimiz sayfamız değiştikçe link alanımızında girilen sayfaya göre değişmesini sağlıyoruz.
        brw.urlChanged.connect(lambda url, brw = brw: self.updateLinkArea(url,brw))   

        
    def goLink(self):
        #line edit alanımıza girilen texti url ye dönüştürüyoruz.
        mainLink = self.linkBar.text()
        mainLink = mainLink.split("/")
        mainLink = mainLink[len(mainLink)-1]


        u = QUrl("https://www.google.com/search?q=" + mainLink)
        
        #eğer linkimizi gerekli ağ protokolünü belirtmemişse 'http' protokolünü ekliyoruz.
        if u.scheme() == "":
            u.setScheme("http")

        #çalışıcak linkimizi belirliyoruz. 
        self.tab.currentWidget().setUrl(u)
        

    def tab_open_doubleclick(self):
        self.newTab = QWebEngineView()
        url = "https://www.google.com/"
        self.newTab.setUrl(QUrl(url))
        self.tab.addTab(self.newTab,"New Page")
        self.newTab.urlChanged.connect(lambda url, brw = self.newTab: self.updateLinkArea(url,self.newTab)) 
        self.linkBar.setCursorPosition(0)   

    def updateLinkArea(self, u, brw =None):
        #link alanımızı girilen sayfaya göre güncelliyoruz.
        self.linkBar.setText(u.toString())


#Qt Uygulamamızı yaratıyoruz
app = QApplication(sys.argv)

#çalıştırmamız için class yapımızı değerimize atıyoruz
main = MainWindow()

#uygulamayı çalıştırıyoruz
main.show()

#sağ üstteki 'x' butonuna tıklandığında uygulamamızın kapanmasını sağlıyoruz.
sys.exit(app.exec_())
        
