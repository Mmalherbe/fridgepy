from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Canvas
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle,RenderContext
from functools import partial
import cv2
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty

class GuiWindow(App):
    realtimeImageSource = StringProperty('capturedProduct.jpg')
    def __init__(self,controller,width = 480,height = 320, **kwargs):
        App.__init__(self)
        self.controller = controller
        self.productFound = ""
        self.wid = Widget()
        self.canvas = RenderContext()
        self.image_Found = None

        self.RealTimeImageOfProduct = None
        self.event = None
        self.lblProductName = None
        self.wid.height = height
        self.wid.width = width
        self.btnheight = 10
        self.btnwidth = 90
        self.stock_layout = None
        self.stock_root = None
        self.stocklblWdith = None
        self.stocklblHeight = 50
        self.imgSaving = False
        self.fontsize = '10sp'

    def build(self):
        label = Label(text='0')
        self.lblProductName = Label(text='', font_size=self.fontsize)
        self.lblAmountOfStock = Label(text='', font_size=self.fontsize)

        self.RealTimeImageOfProduct = Image(source=self.realtimeImageSource)
        btn_addOne = Button(text='+1',size=(self.btnwidth,self.btnheight),
                            on_press=partial(self.addOne))

        btn_SubtractOne = Button(text='-1',size=(self.btnwidth,self.btnheight),
                            on_press=partial(self.subtractOne))

        btn_Confirm = Button(text='Confirm',size=(self.btnwidth,self.btnheight),
                            on_press=partial(self.confirm))

        btn_reset = Button(text='Reset',size=(self.btnwidth,self.btnheight),
                           on_press=partial(self.reset))
        btn_cancel = Button(text='Cancel',size=(self.btnwidth,self.btnheight),
                           on_press=partial(self.cancel))  
        btn_closeApp = Button(text='shutdown',size=(self.btnwidth,self.btnheight),
                            on_press=partial(self.closeApp))    
        self.stock_layout = GridLayout(cols=1, spacing=50,padding=100, size_hint_y=None)
        self.stock_layout.bind(minimum_height=self.stock_layout.setter('height'))
        self.stock_root = ScrollView(height = (self.wid.height/3.5), size_hint=(0.8,1))
        self.stock_root.add_widget(self.stock_layout)
        self.fullLayout = BoxLayout(orientation='vertical')                                        
        self.imgLayout = BoxLayout(orientation='horizontal',size=(self.wid.height/3,self.wid.width/3))
        self.imgLayout.add_widget(self.RealTimeImageOfProduct)
        self.productFoundBox = BoxLayout(orientation='vertical',size=(self.wid.height/3,self.wid.width/3),padding=20)
        self.productFoundBox.add_widget(self.lblProductName)
        self.productFoundBox.add_widget(self.lblAmountOfStock)
        self.imgLayout.add_widget(self.productFoundBox)
        self.imgLayout.add_widget(self.stock_root)
        
        self.fullLayout.add_widget(self.imgLayout)
        self.btnLayout = BoxLayout(orientation='horizontal',width=self.wid.width,height=(self.wid.height/10))
        self.btnLayout.add_widget(btn_addOne)
        self.btnLayout.add_widget(btn_SubtractOne)
        self.btnLayout.add_widget(btn_Confirm)
        self.btnLayout.add_widget(btn_reset)
        self.btnLayout.add_widget(btn_cancel)
        self.btnLayout.add_widget(btn_closeApp)
        self.fullLayout.add_widget(self.btnLayout)

        self.root = BoxLayout(orientation='vertical',size=(self.wid.width,self.wid.height),padding=10)
        self.root.add_widget(self.fullLayout)
        self.showStock(self.controller.getFullStock())   
        return self.root

    def showFound(self,label,inStock):
        self.lblProductName.text = str(label)
        self.lblAmountOfStock.text = str(inStock)
        
    def showStock(self,_stock):
        self.stock_root = None
        self.stock_root = ScrollView(size_hint=(1,1))
        self.stock_layout.clear_widgets()
        for l in _stock :
            stock = Label(text = str(l + " : " + str(_stock[l])),height= self.stocklblHeight, size_hint=(1,1), font_size=self.fontsize)
            self.stock_layout.add_widget(stock)
        


    def setEvents(self):
        self.event = Clock.schedule_interval(self.redraw,0.5)
    def closeApp(self,*largs):
        self.controller.stop()
    def addOne(self, *largs):
        if self.lblProductName.text is not "":
            self.lblAmountOfStock.text = str(int(self.lblAmountOfStock.text) + 1)
    def subtractOne(self,*largs):
         if self.lblProductName.text is not "":
                self.lblAmountOfStock.text = str(int(self.lblAmountOfStock.text) -1)
    def confirm(self,*largs):
        if self.lblProductName.text is "":
            return
        self.controller.ProductChange(self.lblProductName.text,self.lblAmountOfStock.text)
        self.controller.mayLookForProduct = True
        self.lblProductName.text = ''
        self.lblAmountOfStock.text = ''
        self.showStock(self.controller.getFullStock())
    def reset(self,*largs):
        if self.lblProductName.text is "":
            return
        self.lblAmountOfStock.text = str(self.controller.dbController.getStock(self.lblProductName.text))
    def cancel(self,*largs):
        self.controller.mayLookForProduct = True
        self.lblProductName.text = ''
        self.lblAmountOfStock.text = ''
    def redraw(self,dt):
        if self.imgSaving is False:
            self.RealTimeImageOfProduct.reload()
    def updateUI(self,imgCaptured):
        self.imgSaving = True
        cv2.imwrite('capturedProduct.jpg',imgCaptured)
        self.imgSaving = False



    
