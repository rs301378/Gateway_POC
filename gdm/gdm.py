from flask import Flask, render_template, url_for, request
import subprocess

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/deviceConfig')
def deviceConfig():
    return render_template('deviceConfig.html')

@app.route('/cloudConfig',methods=['GET','POST'])
def cloudConfig():
    if request.method=="POST":
        print(request.form.get('server'))
        print(request.form.get('hostAdd'))
        print(request.form.get('port'))
    return render_template('cloudConfig.html')

@app.route('/nodeConfig')
def nodeConfig():
    return render_template('nodeConfig.html')

@app.route('/netConfig')
def networkConfig():
    return render_template('networkConfig.html')

@app.route('/debug')
def debug():
    cmdKey=request.args.get('cmd')
    if cmdKey:
        cmd={'1':['systemctl','status','apache2'],'2':['ls'],'3':['pwd']}
        if cmdKey in cmd:
            data=subprocess.Popen(cmd[cmdKey],stdout=subprocess.PIPE).communicate()[0]
            data=data.decode('utf-8')
            data=data.split('\n')
            return render_template('debug.html',data=data)
        else:
            return render_template('debug.html',data=['Wrong/No command selected try again.'])
    return render_template('debug.html',data=None)

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/dataManager')
def dataManager():
    return render_template('dataManager.html')





if __name__=="__main__":
    app.run(debug=True)
