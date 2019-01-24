from flask import Flask,render_template, Response
from pymongo import MongoClient
from flask import jsonify
from flask import request
from pymongo import MongoClient
import time
import json
import numpy as np
from sklearn.externals import joblib
import tryheatmap
import random

app = Flask(__name__)
##
conn = MongoClient()
db = conn.finalproject
result_set = db.project_test
##
leftclf = joblib.load('leftrfc.pkl')
rightclf = joblib.load('rightrfc.pkl')
bothclf = joblib.load('leftrfc.pkl')

counting = False
left_current = [random.randint(0,4095) for i in range(16)]
right_current = [random.randint(0,4095) for i in range(16)]

type_list = ('forefoot','heel','under_pron','over_pron','normalstanding','left_bias','right_bias')

@app.route('/')
def index():    
    return render_template('index.html')
@app.route('/leftdata',methods = ['GET','POST'])
def leftdata():
    global left_current
    global counting
    data = request.get_data()
    l_data = json.loads(data)
    left_current = l_data['data']
    tmp = l_data['data']
    print('left:',tmp)

    x_l = np.array([tmp])
    x_l.reshape(1,-1)
    y_l = leftclf.predict(x_l)       
    y_l = str(y_l[0])
    print('left result:',y_l)
    if counting is True:
        result_set.insert({'foot':'l',"type":y_l})

    tryheatmap.myheatmapleft(tmp)

    return 'left received'
@app.route('/rightdata',methods = ['GET','POST'])
def rightdata():
    global right_current
    global counting 
    data = request.get_data()
    r_data = json.loads(data)
    right_current = r_data['data']
    tmp = r_data['data']
    print('right:',tmp)
    x_r = np.array([tmp])
    x_r.reshape(1,-1)
    y_r = rightclf.predict(x_r)
    y_r = str(y_r[0])
    print('right result:',y_r)
    if counting is True:
        result_set.insert({'foot':'r','type':y_r})

    tryheatmap.myheatmapright(tmp)
    return 'right received'
@app.route('/show_bias')
def show_bias():
    according = [77,128,124,109,204,247,247,137,179,290,204,163,196,196,221,221]
    left_current[8] = min(left_current[8]-300,4095)
    left_current[9] = min(left_current[9]-300,4095)
    left_current[10] = min(left_current[10]-300,4095)
    left_current[11] = min(left_current[11]-300,4095)
    left_current[12] = min(left_current[12]+2200,4095)
    left_current[13] = min(left_current[13]+3000,4095)
    left_current[14] = min(left_current[14]+1100,4095)
    left_current[15] = min(left_current[15]+1100,4095)
    left_tmp = [4095 - i for i in left_current]
    right_tmp = [4095 - i for i in right_current]

    left_sum = sum(map(lambda (x,y):x*y, zip(left_tmp,according)))*1.0
    right_sum = sum(map(lambda (x,y):x*y,zip(right_tmp,according)))*1.0
    print(left_sum)
    print(right_sum)
    left_ratio = round(left_sum*100/((left_sum+right_sum)),2)
    right_ratio = round(right_sum*100/((left_sum+right_sum)),2)

    returndict = dict(left_ratio = left_ratio,right_ratio = right_ratio)
    return jsonify(returndict)
@app.route("/start_count",methods=['GET','POST'])
def start_count():
    global counting
    counting = True
    return 'receive start counting'

@app.route("/end_count",methods=["GET","POST"])
def end_count():
    global counting
    counting = False
    #default
    l_sum=1
    l_f = 0
    l_h = 0
    l_n = 0
    l_u = 0
    l_o = 0
    r_sum=1
    r_f = 0
    r_h = 0
    r_n = 0
    r_u = 0
    r_o = 0
    
    left_forefoot = result_set.find({"foot":'l',"type":"forefoot"}).count()
    left_heel = result_set.find({"foot":'l',"type":"heel"}).count()
    left_normalstanding = result_set.find({"foot":'l',"type":"normalstanding"}).count()
    left_under_pron = result_set.find({"foot":'l',"type":"under_pron"}).count()
    left_over_pron = result_set.find({"foot":'l',"type":"over_pron"}).count()
    l_sum = (left_forefoot+left_heel+left_normalstanding+left_under_pron+left_over_pron)*1.0
    l_f = round((left_forefoot*100/l_sum),2)
    l_h = round((left_heel*100/l_sum),2)
    l_n = round((left_normalstanding*100/l_sum),2)
    l_u = round((left_under_pron*100/l_sum),2)
    l_o = round((left_over_pron*100/l_sum),2)
    
    right_forefoot = result_set.find({"foot":'r',"type":"forefoot"}).count()
    right_heel = result_set.find({"foot":'r',"type":"heel"}).count()
    right_normalstanding = result_set.find({"foot":'r',"type":"normalstanding"}).count()
    right_under_pron = result_set.find({"foot":'r',"type":"under_pron"}).count()
    right_over_pron = result_set.find({"foot":'r',"type":"over_pron"}).count()
    r_sum = (right_forefoot+right_heel+right_normalstanding+right_under_pron+right_over_pron)*1.0
    r_f = round((right_forefoot*100/r_sum),2)
    r_h = round((right_heel*100/r_sum),2)
    r_n = round((right_normalstanding*100/r_sum),2)
    r_u = round((right_under_pron*100/r_sum),2)
    r_o = round((right_over_pron*100/r_sum),2)
    

    
    ###
    forefoottime = (l_f+r_f)//2*1.0
    normaltime = (l_n+r_n)//2*1.0
    heeltime = (l_h+r_h)//2*1.0
    timesum = forefoottime+normaltime+heeltime
    forefoottime = round(forefoottime/timesum*100,2)
    normaltime= round(normaltime/timesum*100,2)
    heeltime = round(heeltime/timesum*100,2)
    
    timeanalysis = 'Forefoot landing time:'+str(forefoottime)+'%.\n'+'Full-palm landing time:'+str(normaltime)+'%.\n'+'Heel-palm landing time:'+str(heeltime)+'%.\n'
    underpron = (l_u+r_u)//2
    overpron = (l_o+r_o)//2
    if underpron >=15:
        analysisurl = 'https://www.asics.com/us/en-us/underpronation-running-shoes/c/underpronation-running-shoes'
    elif overpron >=15:
        analysisurl = 'https://www.asics.com/us/en-us/overpronation-running-shoes/c/overpronation-running-shoes'
    else:
        analysisurl = 'https://www.asics.com/us/en-us/neutral-pronation-running-shoes/c/neutral-pronation-running-shoes'
    ###
    result = {'l_forefoot':l_f,'l_heel':l_h,'l_normalstanding':l_n,'l_under_pron':l_u,'l_over_pron':l_o,'r_forefoot':r_f,'r_heel':r_h,'r_normalstanding':r_n,'r_under_pron':r_u,'r_over_pron':r_o,'timeanalysis':timeanalysis,'url':analysisurl}

    if result_set.find().count() !=0:
        result_set.remove({})
    return jsonify(result)





if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=5000, type=int)
  def run(debug, threaded, host, port):
    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()

