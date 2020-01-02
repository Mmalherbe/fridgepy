from datastorage.fridgedb import FridgeDB
class dbController(object):
    def __init__(self):
        self.dataBase = FridgeDB('datastorage/fridge.db')
        #automatically add new products to DB from the label-list created by the Image classifier
        self.checkDbAndLabels()
    def getStock(self,product):
        a = self.dataBase.get(product)
        return a

    def checkDbAndLabels(self):
        with open('imageclassifier/class_labels.txt', 'r') as f:
            for line in f.readlines():
                if self.dataBase.get(line.rstrip()) is False:
                    self.dataBase.set(line.rstrip(),0)

