#coding=utf-8
from __future__ import unicode_literals
from pyecharts import Bar,Grid
from pyecharts_javascripthon.api import TRANSLATOR
from flask import Flask, render_template


REMOTE_HOST = "https://pyecharts.github.io/assets/js"

app = Flask(__name__)


@app.route("/")
def hello():
    _bar = bar_chart()
    javascript_snippet = TRANSLATOR.translate(_bar.options)
    return render_template(
        "pyecharts.html",
        chart_id=_bar.chart_id,
        host=REMOTE_HOST,
        renderer=_bar.renderer,
        my_width=250,
        my_height=600,
        custom_function=javascript_snippet.function_snippet,
        options=javascript_snippet.option_snippet,
        script_list=_bar.get_js_dependencies(),
    )


def bar_chart():
    bar1 = Bar("")
    bar2 = Bar()
    bar1.add("分数(分)", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [0.5, 0.20, 0.36, 0.10, 0.75, 0.90],is_more_utils=False,is_convert=False,legend_pos="65%",xaxis_name="分数(分)",is_label_show=True)
    bar2.add("检查次数(次)", ["羊毛衫", "衬衫", "雪纺衫", "裤子", "高跟鞋", "毛衣"], [5, 20, 36, 10, 75, 90],is_more_utils=False,is_convert=False,legend_pos="15%",xaxis_name="检查次数(次)",is_label_show=True)
    bar = Grid()
    bar.add(bar1,grid_top="55%")
    bar.add(bar2,grid_bottom="55%")

    return bar
if __name__ == '__main__':
    
    #app.run(debug=True,host='0.0.0.0')
    app.run(debug=True,host='0.0.0.0')
