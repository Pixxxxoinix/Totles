from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask)
import os
from PyQt5.QtWidgets import QApplication,  QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
from PIL import Image
from PyQt5.QtGui import QPixmap
app = QApplication([])
window = QWidget()
window.setWindowTitle('Easy Editor!')
window.resize(600,600)
lb_image = QLabel('Картинка')
button = QPushButton('Папка')
lv_files = QListWidget()
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')
horizon = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(button)
col1.addWidget(lv_files)
col2.addWidget(lb_image)
rove_tools = QHBoxLayout()
rove_tools.addWidget(btn_left)
rove_tools.addWidget(btn_right)
rove_tools.addWidget(btn_flip)
rove_tools.addWidget(btn_sharp)
rove_tools.addWidget(btn_bw)
col2.addLayout(rove_tools)
horizon.addLayout(col1,20)
horizon.addLayout(col2,80)
window.setLayout(horizon)
workdir = ''
def chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
def filter(files,extensions):
    result = list()
    for file in files:

        for satoshi in extensions:
            if file.endswith(satoshi):
                result.append(file)
    return result
def showfilenamelist():
    extensions = ['.jpeg','.bmp','.png','.jpg']
    chooseworkdir()
    filenames = filter(os.listdir(workdir),extensions)
    lv_files.clear()
    for file in filenames:
        lv_files.addItem(file)
button.clicked.connect(showfilenamelist)        
class ImageProcessor:
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'modifed/'    
    def load_image(self,filename):
        self.filename = filename
        image_path = os.path.join(workdir,filename)
        self.image = Image.open(image_path)
    def showImage(self,path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w,h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir,self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir,self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir,self.filename)
        self.showImage(image_path)
    def do_sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir,self.filename)
        self.showImage(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.save_image()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)
    def save_image(self):
        path = os.path.join(workdir,self.save_dir)
        if not(os.path.exists(path)or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename) 
        self.image.save(image_path)
def showChosenImage():
    if lv_files.currentRow() >= 0:
        filename = lv_files.currentItem().text()
        workImage.load_image(filename)
        workImage.showImage(os.path.join(workdir,workImage.filename))
workImage = ImageProcessor()

lv_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workImage.do_bw)
btn_right.clicked.connect(workImage.do_right)
btn_left.clicked.connect(workImage.do_left)
btn_flip.clicked.connect(workImage.do_flip)
btn_sharp.clicked.connect(workImage.do_sharp)
    








window.show()
app.exec_()
