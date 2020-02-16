from imageclassifier.Labelfinder import imageClassifier

imgclassifier = imageClassifier()
import numpy
from PIL import Image
im = Image.open("capturedProduct.jpg")
print(imgclassifier.checkForKnownLabel(numpy.array(im)))