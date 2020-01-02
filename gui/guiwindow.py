from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle,RenderContext
from functools import partial
import cv2
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty
from PIL import Image as pilimg
class Picture():
    source = StringProperty(None)

class GuiWindow(App):
    realtimeImageSource = StringProperty('capturedProduct.jpg')
    def __init__(self,controller, **kwargs):
        App.__init__(self)
        self.controller = controller
        self.productFound = ""
        self.wid = Widget()
        self.canvas = RenderContext()
        self.image_Found = None
        self.ProductFoundImage = None
        self.RealTimeImageOfProduct = None
        self.event = None
        self.lblProductName = None

    def build(self):
        
        label = Label(text='0')
        self.lblProductName = Label(text='{"broodjeAap" : 100}')
        self.lblAmountOfStock = Label(text='0')
        self.ProductFoundImage = Image(source="gui/Placeholder.png")
        self.RealTimeImageOfProduct = Image(source=self.realtimeImageSource)
        btn_addOne = Button(text='+1',
                            on_press=partial(self.addOne))

        btn_SubtractOne = Button(text='-1',
                            on_press=partial(self.subtractOne))

        btn_Confirm = Button(text='Confirm',
                            on_press=partial(self.confirm))

        btn_reset = Button(text='Reset',
                           on_press=partial(self.reset))
        btn_cancel = Button(text='Cancel',
                           on_press=partial(self.cancel))  
        btn_closeApp = Button(text='shutdown',
                            on_press=partial(self.closeApp))                         
        self.imgLayout = BoxLayout(height= self.wid.height - 160)
        self.imgLayout.add_widget(self.RealTimeImageOfProduct)
        self.imgLayout.add_widget(self.lblProductName)
        self.imgLayout.add_widget(self.lblAmountOfStock)
        self.imgLayout.add_widget(self.ProductFoundImage)
        self.btnLayout = BoxLayout(size_hint=(1, None), height=160)
        self.btnLayout.add_widget(btn_addOne)
        self.btnLayout.add_widget(btn_SubtractOne)
        self.btnLayout.add_widget(btn_Confirm)
        self.btnLayout.add_widget(btn_reset)
        self.btnLayout.add_widget(btn_cancel)
        self.btnLayout.add_widget(btn_closeApp)
        

        self.root = BoxLayout(orientation='vertical')
        self.root.add_widget(self.wid)
        self.root.add_widget(self.imgLayout)
        self.root.add_widget(self.btnLayout)
        return self.root
    def setEvents(self):
        self.event = Clock.schedule_interval(self.redraw,0.1)
    def closeApp(self,*largs):
        self.controller.stop()
        
    def addOne(self, *largs):
        self.lblAmountOfStock.text = int(self.lblAmountOfStock.text) + 1
    def subtractOne(self,*largs):
         self.lblAmountOfStock.text = int(self.lblAmountOfStock.text) -1
    def confirm(self,*largs):
        self.controller.ProductChange(self.lblProductName.text,self.lblAmountOfStock.text)
        self.controller.mayLookForProduct = True
    def reset(self,*largs):
        self.lblAmountOfStock.text = self.dbController.dataBase.getStock(self.lblProductName.text)
    def cancel(self,*largs):
        self.controller.mayLookForProduct = True
    def redraw(self,dt):
        self.RealTimeImageOfProduct.reload()
    def updateUI(self,imgCaptured):
        cv2.imwrite('capturedProduct.jpg',imgCaptured)
    def showFound(self,label,inStock):
        self.lblProductName.text = str(label)
        self.lblAmountOfStock.text = str(inStock)



    

