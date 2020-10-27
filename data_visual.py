from pyecharts.charts import Bar, Line 
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QFrame
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pyecharts.globals import ThemeType
import globalvar as gl
import Tabel
import sys


class ChartGenerater():

    def genetatePlot(self):
        # V1 版本开始支持链式调用
        gl.set_value("filename","bar.html")
        bar = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
            .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
            .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
            .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
            .set_global_opts()
        )
        bar.render("C:\\Users\\dell\\Desktop\\bar.html")

    def genetateLineArea(self,dates,scores,trainning):
        x_data = dates
        y_data = scores

        background_color_js = (
            "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
            "[{offset: 0, color: '#0a243D'}, {offset: 1, color: '#133457'}], false)"
        )
        area_color_js = (
            "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
            "[{offset: 0, color: '#FF6295'}, {offset: 1, color: '#3fbbff0d'}], false)"
        )

        c = (
            Line(init_opts=opts.InitOpts(bg_color=JsCode(background_color_js)))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name="注册总量",
                y_axis=y_data,
                is_smooth=True,
                is_symbol_show=True,
                symbol="circle",
                symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(color="#fff"),
                label_opts=opts.LabelOpts(is_show=True, position="top", color="white"),
                itemstyle_opts=opts.ItemStyleOpts(
                    color="red", border_color="#fff", border_width=3
                ),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=trainning+"\n历史成绩",
                    pos_bottom="5%",
                    pos_left="center",
                    title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=22),
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    boundary_gap=False,
                    axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
                    axisline_opts=opts.AxisLineOpts(is_show=False),
                    axistick_opts=opts.AxisTickOpts(
                        is_show=True,
                        length=25,
                        linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                    ),
                    splitline_opts=opts.SplitLineOpts(
                        is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                    ),
                ),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    position="right",
                    axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                    ),
                    axistick_opts=opts.AxisTickOpts(
                        is_show=True,
                        length=15,
                        linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                    ),
                    splitline_opts=opts.SplitLineOpts(
                        is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                    ),
                ),
                legend_opts=opts.LegendOpts(is_show=False),
            )
            .render("C:\\Users\\dell\\Desktop\\line.html")
            # .render("./datavisual/"+trainning+".html")
        )
        gl.set_value("filename",trainning+".html")
        



class Tabel(QWidget,Tabel.Ui_TabelP):
    def __init__(self):
        super(Tabel, self).__init__()
        #self.initUI()
        #self.mainLayout()
        self.setupUi(self)
        print("init..")
        self.imageL.setPixmap(QtGui.QPixmap("C:\\Users\\dell\\Desktop\\patten2.png"))
        self.mainLayout()
 
    def initUI(self):
        self.setGeometry(400,400,800,600)
        # self.setWindowTitle("demo1")
 
    def mainLayout(self):
        #self.mainhboxLayout = QHBoxLayout(self)
        # self.frame = QFrame(self)
        # self.mainhboxLayout.addWidget(self.frame)
        self.hboxLayout = QHBoxLayout()
        #self.hboxLayout = QHBoxLayout(self.frame)
        self.myHtml = QWebEngineView()
        # url = "http://www.baidu.com"
        # #打开本地html文件
        filepath="file:///C:/Users/dell/Desktop/line.html"
        # filepath="file:///system/ftproot/aa/win/datavisual"+gl.get_value("filename")
        print(filepath)
        self.myHtml.load(QUrl(filepath))
        # self.myHtml.load(QUrl("bar1.html"))   #无法显示，要使用绝对地址定位，在地址前面加上 file:/// ，将地址的 \ 改为/
        #打开网页url
        # self.myHtml.load(QUrl(url))
 
        self.hboxLayout.addWidget(self.myHtml)

        self.setLayout(self.hboxLayout)
 
if __name__ == '__main__':
    gl._init()
    app = QApplication(sys.argv)
    cg=ChartGenerater()
    # cg.genetatePlot()
    dates=['2020-07-16 15:32','2020-07-16 16:32', '2020-07-16 16:50', '2020-07-17 15:32']
    scores=[88,83,92,89]
    cg.genetateLineArea(dates,scores,"卷腹")
    ex = Tabel()
    ex.show()
    sys.exit(app.exec_())