from flask import Flask

app=Flask(__name__)
app.config['UPLOAD_FOLDER']='/home/attu/Desktop/ScratchNest/uploads/' #path to upload folder
app.config['SECRET_KEY']="asdadvadfsdfs"      #random secret key

from gdmApp import gdm
