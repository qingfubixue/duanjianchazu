# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyecharts import Bar,Grid
from pyecharts_javascripthon.api import TRANSLATOR
import os

import math
import datetime
from flask import Flask, render_template, flash, redirect, url_for, Markup,request,flash
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
import pyodbc
import time
##reload(sys)
##sys.setdefaultencoding('utf-8') 
conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=G:\zdpf223\Database2.accdb')
# #print "Opened database successfully"
#
global cur
cur = conn.cursor()
# cur.execute('''CREATE TABLE COMPANY
#        (ID INT PRIMARY KEY     NOT NULL,
#        NAME           TEXT    NOT NULL,
#        AGE            INT     NOT NULL,
#        ADDRESS        CHAR(50),
#        SALARY         REAL);''')
# print "Table created successfully"
#
# conn.commit()
#
global wentizidian
wentizidian={}
wentixiang=[]
cur.execute("SELECT * FROM changjianwenti;")
ww=cur.fetchall()

for i in ww:
    wentizidian[i[0]]=[i[2],i[3]]
    wentixiang.append(i[1])
# cur.close()
# conn.close()
# conn1 = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=G:\zdpf223\Database2.accdb')

# cur1 = conn1.cursor()
global renyuanzidian
renyuanzidian={}

renyuanxiang=[]

cur.execute("SELECT * FROM jiancharenyuan;")
ww1=cur.fetchall()

for i in ww1:
    renyuanzidian[i[1]]=i[2]
    
    renyuanxiang.append(i[1])
renyuanzidian[""]=""
renyuanxiang.append("")
# cur1.close()    
global zhandianzidian#站号-地点
zhandianzidian={}
global zhandianzidian2#部门-站点
zhandianzidian2={}
global zhandianzidian3#地点-部门
zhandianzidian3={}
cur.execute("SELECT * FROM zhandianxinxi;")
ww2=cur.fetchall()
global zdl#部门
zdl=[""]
global ddl
ddl=[]
zhandianzidian2[""]=ddl  
for i in ww2:
    zhandianzidian[i[1]]=i[3]
    zhandianzidian3[i[3]]=i[2]
    ddl.append(i[3])
    if i[2] in zdl:
        zhandianzidian2[i[2]].append(i[3])
    else:
        zdl.append(i[2])
        zhandianzidian2[i[2]]=[i[3]]
  
#ww2.append(("",)*len(ww2[1]))    

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

cur.execute(u"SELECT [站号],AVG([总评分]) FROM fenshujilu GROUP BY [站号] ORDER BY AVG([总评分]) DESC;")
wwz=cur.fetchall()
global zhanhaolist
zhanhaolist=[]
global pingjvnfenlist
pingjvnfenlist=[]
cur.execute(u"SELECT [日期] FROM fenshujilu ORDER BY [日期] DESC;")
wwr=cur.fetchall()
riqilist=[]
for i in wwr:
    riqilist.append(i[0].strftime('%Y-%m-%d'))
    
for i in wwz:
    zhanhaolist.append(zhandianzidian[i[0]])
    pingjvnfenlist.append(i[1])
    
global riqi1
global riqi2
riqi1=riqilist[-1]   
riqi2=riqilist[0]
cur.execute(u"SELECT [站号],COUNT([站号]) FROM fenshujilu GROUP BY [站号] ORDER BY COUNT([站号]) DESC;")
wwz2=cur.fetchall()
global zhanhaolist2
zhanhaolist2=[]
global cishulist
cishulist=[]
for i in wwz2:
    zhanhaolist2.append(zhandianzidian[i[0]])
    
    cishulist.append(i[1])


@app.route("/",methods=['GET', 'POST'])
def hello():
    
    if request.method == "POST":
        yujv=u"SELECT [站号],AVG([总评分]) FROM fenshujilu where [日期]>=#"+str(request.values.get('qsn'))+"# and [日期]<=#"+str(request.values.get('zzn'))+"# GROUP BY [站号] ORDER BY AVG([总评分]) DESC;"
        cur.execute(yujv)
        wwz=cur.fetchall()
        global zhanhaolist
        zhanhaolist=[]
        global pingjvnfenlist
        pingjvnfenlist=[]

        for i in wwz:
            zhanhaolist.append(zhandianzidian[i[0]])
            pingjvnfenlist.append(i[1])
        global riqi1    
        global riqi2 
        riqi1=str(request.values.get('qsn'))
        riqi2=str(request.values.get('zzn'))
        yujv=u"SELECT [站号],COUNT([站号]) FROM fenshujilu where [日期]>=#"+str(request.values.get('qsn'))+"# and [日期]<=#"+str(request.values.get('zzn'))+"# GROUP BY [站号] ORDER BY COUNT([站号]) DESC;"
        cur.execute(yujv)
        wwz2=cur.fetchall()
        global zhanhaolist2
        zhanhaolist2=[]
        global cishulist
        cishulist=[]
        for i in wwz2:
            zhanhaolist2.append(zhandianzidian[i[0]])
            
            cishulist.append(i[1])
    
    _bar = bar_chart()
    javascript_snippet = TRANSLATOR.translate(_bar.options)
    return render_template(
        "pyecharts.html",
        fan="查询范围："+riqi1+"——"+riqi2,
        chart_id=_bar.chart_id,
        host=REMOTE_HOST,
        renderer=_bar.renderer,
        my_width=280,
        my_height=600,
        custom_function=javascript_snippet.function_snippet,
        options=javascript_snippet.option_snippet,
        script_list=_bar.get_js_dependencies(),
    )


def bar_chart():
    bar1 = Bar()
    bar2 = Bar()
    
    bar1.add("分数(分)", zhanhaolist, pingjvnfenlist,is_more_utils=False,is_convert=False,legend_pos="65%",yaxis_name="分数(分)",is_label_show=True,xaxis_interval=0,xaxis_rotate=-30,xaxis_name_gap=45,label_color=['#5AB5FF'])
    bar2.add("检查次数(次)", zhanhaolist2, cishulist,is_more_utils=False,is_convert=False,legend_pos="15%",yaxis_name="检查次数(次)",is_label_show=True,xaxis_interval=0,xaxis_rotate=-30,xaxis_name_gap=45,label_color=['#5AB5FF'])
    bar = Grid()
    bar.add(bar1,grid_top="60%")
    bar.add(bar2,grid_bottom="60%")

    return bar
@app.route('/1',methods=['GET', 'POST'])
def index():
    fenshu=100
    if request.method == "POST":
        
        charu=("insert into fenshujilu (站号,检查人,日期,开始,结束,1类别,1性质,1问题,1整改,图片地址1,2类别,2性质,2问题,2整改,图片地址2,3类别,3性质,3问题,3整改,图片地址3,4类别,4性质,4问题,4整改,图片地址4,5类别,5性质,5问题,5整改,图片地址5,总评分) values('"+ww2[int(request.values.get('zhn'))-1][1]+"','"+renyuanxiang[int(request.values.get('xmn'))-1]+"','"+request.values.get('rqn')+"','"+request.values.get('ksn')+"','"+request.values.get('jsn')+"'")
        xianshi=("您已提交如下内容：(站号——"+ww2[int(request.values.get('zhn'))-1][1]+",检查人——"+renyuanxiang[int(request.values.get('xmn'))-1]+",日期——"+request.values.get('rqn')+",开始时间——"+request.values.get('ksn')+",结束时间——"+request.values.get('jsn'))
        for i in range(1,6):
            if request.values.get('qyn'+str(i))=="on":
                fname = request.files.get('picn'+str(i))
                if fname:
                    
                    new_fname = r'/zdpf223/static/img/' +request.values.get('rqn')+"("+str(i)+")"+os.path.splitext(fname.filename)[1]
                    new_fname2 = 'static/img/' +request.values.get('rqn')+"("+str(i)+")"+os.path.splitext(fname.filename)[1]
                    fname.save(new_fname)  #保存文件到指定路径
                    charu+=(",'"+wentixiang[int(request.values.get('lbn'+str(i)))-1]+"','"+[u'一般',u'严重',u'典型'][int(request.values.get('xzn'+str(i)))-1]+"','"+request.values.get('wtn'+str(i))+"','"+request.values.get('zgn'+str(i))+"','"+str(new_fname2)+"'")
                    xianshi+=(",项目"+str(i)+"类别——"+wentixiang[int(request.values.get('lbn'+str(i)))-1]+",项目"+str(i)+"性质——"+[u'一般',u'严重',u'典型'][int(request.values.get('xzn'+str(i)))-1]+",项目"+str(i)+"问题描述——"+request.values.get('wtn'+str(i))+",项目"+str(i)+"整改措施——"+request.values.get('zgn'+str(i))+"保存图片——"+str(new_fname))
                    fenshu-=([10,20,30][int(request.values.get('xzn'+str(i)))-1])
                    
                else:
                    
                    charu+=(",'"+wentixiang[int(request.values.get('lbn'+str(i)))-1]+"','"+[u'一般',u'严重',u'典型'][int(request.values.get('xzn'+str(i)))-1]+"','"+request.values.get('wtn'+str(i))+"','"+request.values.get('zgn'+str(i))+"','"+""+"'")
                    xianshi+=(",项目"+str(i)+"类别——"+wentixiang[int(request.values.get('lbn'+str(i)))-1]+",项目"+str(i)+"性质——"+[u'一般',u'严重',u'典型'][int(request.values.get('xzn'+str(i)))-1]+",项目"+str(i)+"问题描述——"+request.values.get('wtn'+str(i))+",项目"+str(i)+"整改措施——"+request.values.get('zgn'+str(i)))
                    fenshu-=([10,20,30][int(request.values.get('xzn'+str(i)))-1])
            else:
                charu+=",NULL,NULL,NULL,NULL,NULL"
        charu+=(",'"+str(fenshu)+"');")
        xianshi+=(",总评分——"+str(fenshu))
        #return render_template('index2.html',charu=charu)
        global cur
        cur.execute(charu)
        cur.commit()
        return render_template('index2.html',xianshi=xianshi)
    else:
        global wentizidian
        global renyuanzidian
        return render_template('index.html',wentizidian=wentizidian,wentixiang=wentixiang,renyuanzidian=renyuanzidian,renyuanxiang=renyuanxiang,zhandianzidian=zhandianzidian,ww2=ww2)
@app.route('/2',methods=['GET', 'POST'])
def index2():
    
    return render_template('index3.html')
@app.route('/cha',methods=['GET', 'POST'])
def index3():
    chaxunzidian={}
    ids=[]
    cur.execute("SELECT * FROM fenshujilu;")
    wwc=cur.fetchall()
    t=0
    for i in wwc:
        qie=list(i)[1:]
        qie[2]=str(qie[2]).split(' ')[-2]
        qie[3]=str(qie[3]).split(' ')[-1]
        qie[4]=str(qie[4]).split(' ')[-1]
        qie.append(zhandianzidian3[zhandianzidian[i[1]]])
        qie.append(renyuanzidian[i[2]])
        
        chaxunzidian[i[0]]=qie
        ids.append(i[0])
        t+=1
    
    return render_template('indexcha.html',chaxunzidian=chaxunzidian,zhandianzidian=zhandianzidian,zhandianzidian2=zhandianzidian2,zdl=zdl,ddl=ddl,renyuanxiang=renyuanxiang,ids=ids)
    
if __name__ == '__main__':
    
    #app.run(debug=True,host='0.0.0.0')
    app.run(debug=True,host='0.0.0.0')
