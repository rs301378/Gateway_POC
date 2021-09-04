from flask import render_template, request, redirect, session, url_for  #necessary Imports
import subprocess   #module import for dealing with execution of console command 
from gdmApp import app
from .database import p1 as db

@app.route('/login',methods=['GET','POST'])   #route for handling login
def login():
    if request.method=="POST":
        if request.form.get('user')=='admin' and request.form.get('pas')=='admin':
            session['logedIn']='admin'
            return redirect('/')
        return render_template('login.html',msg='Wrong Credentials')
    return render_template('login.html')

@app.route('/logOut')    #route for handling logout
def logOut():
    if 'logedIn' in session:
        session.pop('logedIn')    #removing session
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'logedIn' in session:                #verifying user is logedIn or not
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/deviceConfig')
def deviceConfig():
    if 'logedIn' in session:
        return render_template('deviceConfig.html')
    return redirect(url_for('login'))

@app.route('/cloudConfig',methods=['GET','POST'])
def cloudConfig():
    if 'logedIn' in session:
        if request.method=="POST":     #need db integration for here 
            if request.form.get('server')=='aws':
                root=request.files['rootFile']                  #accessing the uploaded files
                pvtKey=request.files['pvtKey']
                iotCert=request.files['iotCert']
                root.save('/home/attu/Desktop/ScratchNest/uploads/root')        #saving the uploaded files
                pvtKey.save('/home/attu/Desktop/ScratchNest/uploads/pvtKey')
                iotCert.save('/home/attu/Desktop/ScratchNest/uploads/iotCert')
        return render_template('cloudConfig.html')
    return redirect(url_for('login'))

@app.route('/nodeConfig')
def nodeConfig():
    if 'logedIn' in session:
        return render_template('nodeConfig.html')
    return redirect(url_for('login'))

@app.route('/netConfig')
def networkConfig():
    if 'logedIn' in session:
        return render_template('networkConfig.html')
    return redirect(url_for('login'))

@app.route('/debug')
def debug():
    if 'logedIn' in session:
        cmdKey=request.args.get('cmd')          #extracting the command key from the html form
        if cmdKey:
            cmd={'1':['systemctl','status','apache2'],'2':['ls'],'3':['pwd']}
            if cmdKey in cmd:
                data=subprocess.Popen(cmd[cmdKey],stdout=subprocess.PIPE).communicate()[0]      #executing the command and getting the data into string format
                data=data.decode('utf-8')                                                       #decoding the binary the data into string 
                data=data.split('\n')
                return render_template('debug.html',data=data)
            else:
                return render_template('debug.html',data=['Wrong/No command selected try again.'])
        return render_template('debug.html',data=None)
    return redirect(url_for('login'))

@app.route('/reports')
def reports():
    if 'logedIn' in session:
        return render_template('reports.html')
    return redirect(url_for('login'))

@app.route('/dataManager')
def dataManager():
    if 'logedIn' in session:
        return render_template('dataManager.html')
    return redirect(url_for('login'))


if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=8000)
