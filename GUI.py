import wx
import Search
import Crawler
import codecs
import time
from PIL import Image
import urllib.request
import io
import os
import json
from urllib.request import urlopen
from io import StringIO
import io
import urllib.request as urllib2
import webbrowser
import base64
import requests

class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(540, 580))
       	self.Centre()
        self.listFile = []
       	self.panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL) 
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.t1 = wx.TextCtrl(self.panel, size = ((400,30)))

        self.t1.SetPosition((65,120))
        hbox1.Add(self.t1,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

        self.t1.Bind(wx.EVT_TEXT,self.OnKeyTyped)
        self.btnDis = wx.Button(self.panel, -1, "Search by Distance")
        self.btnCosine = wx.Button(self.panel, -1, "Search by Cosine")
        self.btnCosine.SetPosition((65,160))
        self.btnDis.SetPosition((315,160))
        self.btnCosine.SetSize((150,25))
        self.btnDis.SetSize((150,25))
        self.btnDis.Bind(wx.EVT_BUTTON, self.getSearchDis)
        self.btnCosine.Bind(wx.EVT_BUTTON, self.getSearchCos)
       	self.t2 = wx.TextCtrl(self.panel, style = wx.TE_MULTILINE, size = ((292,200)))
       	self.t2.SetPosition((480,300))
           
        
       	image = wx.Image("logo.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        imageBitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(image))
        imageBitmap.SetPosition((95,0))
        self.label=wx.StaticText(self.panel, -1, label='', pos=(65,200), name='')
        self.label.Hide()



        self.mlist = []
       	self.listBox = wx.ListBox(self.panel, wx.ID_ANY, wx.Point(60,230), wx.Size(200, 292), self.mlist, style = wx.LB_HSCROLL)
       	self.listBox.Bind(wx.EVT_LISTBOX, self.get)
        self.listBox.Hide()
        self.t2.Hide()

        
       
       	hbox1.Add(self.t2) 
        hbox1.Add(self.btnCosine)
        hbox1.Add(self.btnDis)
        vbox.Add(hbox1) 

    def handleListSearchResult(self,result):
        self.listFile = [key for key in result.keys()]
        self.listBox.Clear()
        for item in self.listFile:
            self.listBox.Show()
            file = codecs.open('doc2/' + item, 'r', 'utf-8')
            dataTemp1=json.load(file)            
            line=dataTemp1['title']
            file.close()
            self.listBox.Append(line.strip())
       
       

    def searchProcess(self,searchTypeName,text,start):

        self.label.Hide()
        #search title
        resultTitle  = eval('Search.'+searchTypeName+'(text,"tf_idf1.txt")')
        self.handleListSearchResult(resultTitle)
        #search content
        resultContent  = eval('Search.'+searchTypeName+'(text,"tf_idf2.txt")')
        self.handleListSearchResult(resultContent)


        end = time.time()
        message = "About "+str(len(self.listBox.Items))+" results (" + str(int(end - start)) +" seconds)"
       

        self.label.SetLabel(message)
        self.label.Show()

 
    def OnQuit(self, e):
        self.Close()
    def OnKeyTyped(self, event): 
    	pass
    def getSearchCos(self, event):
        start = time.time()
        text = self.t1.GetValue()
        if(text != "" and len(text.strip()) != 0):
          
            self.searchProcess('finalCosine',text,start)
           
        elif(text == ""):
            dlg = wx.MessageDialog(self, "Query can not be empty", "Empty Query Error", wx.OK)
            val = dlg.ShowModal()
            dlg.Show()
        else:
            dlg = wx.MessageDialog(self, "Query can not contain only spaces", "Spaces Only Query Error",wx.OK)
            val = dlg.ShowModal()
            dlg.Show()
        
    
    def getSearchDis(self, event):
        start = time.time()
        text = self.t1.GetValue()
        text = str(text)
        if(text != "" and len(text.strip()) != 0):

            self.searchProcess('finalDistance',text,start)

      
        elif(text == ""):
            dlg = wx.MessageDialog(self, "Query can not be empty", "Empty Query Error", wx.OK)
            val = dlg.ShowModal()
            dlg.Show()
        else:
            dlg = wx.MessageDialog(self, "Query can not contain only spaces", "Spaces Only Query Error",wx.OK)
            val = dlg.ShowModal()
            dlg.Show()
    
    def goToDetailPage(self, e):
        i = self.listFile[self.listBox.GetSelection()]
        file = codecs.open('doc2/' + i, 'r', 'utf-8')
        texts = file.read()
        jsonContent= json.loads(texts)
       
        detailLink=jsonContent['detailLink']
        webbrowser.open_new_tab(detailLink)

    def get(self, e):
        i = self.listFile[self.listBox.GetSelection()]
        file = codecs.open('doc2/' + i, 'r', 'utf-8')
        texts = file.read()
        jsonContent= json.loads(texts)
        jsonLinkImage=jsonContent['thumpnail']
        buf = urllib2.urlopen(jsonLinkImage).read()
        sbuf = io.BytesIO(buf)
       	image = wx.Image(sbuf, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        imageBitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(image))
        imageBitmap.SetPosition((275,230))

        imageBitmap.Bind(wx.EVT_LEFT_DOWN, self.goToDetailPage)


        file.close()

def main():

    app = wx.App()
    ex = Example(None, title = "Simple Search")
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    #Crawler.bookCrawler()
    #Search.build_inverted_tf()
    main()