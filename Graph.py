import PyQt5
import numpy as np
from PyQt5.QtChart import QChart, QScatterSeries, QValueAxis, QChartView

import Stu
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
# x轴是时间，一天为一增
# y轴是掌握程度，每个章节一条线
# 导入所需模块
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtGui import QPainter, QFont, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel


# 定义学生错误问题数据的数据结构
class MainWindow(QDialog):
    def __init__(self, user):
        super().__init__()

        self.setWindowTitle("Graph")
        # 示例用法

        chart = QChart()
        # 设置图表旁边的空白大小
        chart.setMargins(QMargins(100, 50, 100, 50))  # 左、上、右、下边距都设置为50

        chart.setTitle("能力分析图")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().hide()
        # 第一个章节
        pen = QPen()
        pen.setColor(Qt.blue)
        pen.setWidth(2)

        line_series = QScatterSeries()
        line_series.setPen(pen)
        # 第二个章节
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(2)  # 设置线宽

        line_series2 = QScatterSeries()
        line_series2.setPen(pen)
        # 第三个章节
        pen = QPen()
        pen.setColor(Qt.red)  # 设置为红色
        pen.setWidth(2)  # 设置线宽

        line_series3 = QScatterSeries()
        line_series3.setPen(pen)
        # 第四个章节
        pen = QPen()
        pen.setColor(Qt.darkYellow)
        pen.setWidth(2)  # 设置线宽

        line_series4 = QScatterSeries()
        line_series4.setPen(pen)
        # 第五个章节
        pen = QPen()
        pen.setColor(Qt.green)
        pen.setWidth(2)  # 设置线宽

        line_series5 = QScatterSeries()
        line_series5.setPen(pen)
        # 第六个章节
        pen = QPen()
        pen.setColor(Qt.gray)
        pen.setWidth(2)  # 设置线宽

        line_series6 = QScatterSeries()
        line_series6.setPen(pen)
        # 第七个章节
        pen = QPen()
        pen.setColor(Qt.darkGreen)
        pen.setWidth(2)  # 设置线宽

        line_series7 = QScatterSeries()
        line_series7.setPen(pen)

        accurate_rate = Stu.get_accurate_rate(user)  # 每个章节的做题数,正确率[[],[]]

        # 创建散点图系列对象，并添加数据点

        line_series.append(accurate_rate[0][0], accurate_rate[0][1])
        line_series2.append(accurate_rate[1][0], accurate_rate[1][1])
        line_series3.append(accurate_rate[2][0], accurate_rate[2][1])
        line_series4.append(accurate_rate[3][0], accurate_rate[3][1])
        line_series5.append(accurate_rate[4][0], accurate_rate[4][1])
        line_series6.append(accurate_rate[5][0], accurate_rate[5][1])
        line_series7.append(accurate_rate[6][0], accurate_rate[6][1])

        # 设置点的样式和大小
        line_series.setMarkerShape(QScatterSeries.MarkerShapeCircle)  # 设置点的形状为圆形
        line_series.setMarkerSize(10)  # 设置点的大小为 10

        line_series2.setMarkerShape(QScatterSeries.MarkerShapeCircle)  # 设置点的形状为圆形
        line_series2.setMarkerSize(10)  # 设置点的大小为 10

        line_series3.setMarkerShape(QScatterSeries.MarkerShapeCircle)  # 设置点的形状为圆形
        line_series3.setMarkerSize(10)  # 设置点的大小为 10

        line_series4.setMarkerShape(QScatterSeries.MarkerShapeCircle)  # 设置点的形状为圆形
        line_series4.setMarkerSize(10)  # 设置点的大小为 10

        line_series5.setMarkerShape(QScatterSeries.MarkerShapeCircle)  # 设置点的形状为圆形
        line_series5.setMarkerSize(10)  # 设置点的大小为 10

        line_series6.setMarkerShape(QScatterSeries.MarkerShapeCircle)  # 设置点的形状为圆形
        line_series6.setMarkerSize(10)  # 设置点的大小为 10

        line_series7.setMarkerShape(QScatterSeries.MarkerShapeCircle)  # 设置点的形状为圆形
        line_series7.setMarkerSize(10)  # 设置点的大小为 10

        chart.addSeries(line_series)
        chart.addSeries(line_series2)  # 加入
        chart.addSeries(line_series3)  # 加入
        chart.addSeries(line_series4)  # 加入
        chart.addSeries(line_series5)  # 加入
        chart.addSeries(line_series6)  # 加入
        chart.addSeries(line_series7)  # 加入

        axis_x = QValueAxis()  # 创建x轴
        axis_x.setTitleText('做题数量')
        axis_x.setLabelFormat("%d")
        axis_x.setRange(0, 100)  # 设置 Y 轴范围
        axis_x.setTickCount(11)  # 设置 Y 轴刻度数量
        chart.addAxis(axis_x, Qt.AlignBottom)
        line_series.attachAxis(axis_x)
        line_series2.attachAxis(axis_x)
        line_series3.attachAxis(axis_x)
        line_series4.attachAxis(axis_x)
        line_series5.attachAxis(axis_x)
        line_series6.attachAxis(axis_x)
        line_series7.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTitleText('掌握能力')
        axis_y.setLabelFormat("%lf")
        axis_y.setRange(0, 1)  # 设置 Y 轴范围
        axis_y.setTickCount(11)  # 设置 Y 轴刻度数量
        chart.addAxis(axis_y, Qt.AlignLeft)
        line_series.attachAxis(axis_y)
        line_series7.attachAxis(axis_y)
        line_series2.attachAxis(axis_y)
        line_series3.attachAxis(axis_y)
        line_series4.attachAxis(axis_y)
        line_series5.attachAxis(axis_y)
        line_series6.attachAxis(axis_y)

        chart_view = QChartView(chart)

        # # 创建标签，在折线上方显示系列名称
        font = QFont("Arial", 10, QFont.Bold)
        series1_label = chart_view.scene().addText("Chapter 1", font)
        series1_label.setDefaultTextColor(Qt.blue)
        series1_label.setPos(700, 20)

        series2_label = chart_view.scene().addText("Chapter 2", font)
        series2_label.setDefaultTextColor(Qt.black)
        series2_label.setPos(700, 40)

        series3_label = chart_view.scene().addText("Chapter 3", font)
        series3_label.setDefaultTextColor(Qt.red)
        series3_label.setPos(700, 60)

        series4_label = chart_view.scene().addText("Chapter 4", font)
        series4_label.setDefaultTextColor(Qt.darkYellow)
        series4_label.setPos(700, 80)

        series5_label = chart_view.scene().addText("Chapter 5", font)
        series5_label.setDefaultTextColor(Qt.green)
        series5_label.setPos(700, 100)

        series6_label = chart_view.scene().addText("Chapter 6", font)
        series6_label.setDefaultTextColor(Qt.gray)
        series6_label.setPos(700, 120)

        series7_label = chart_view.scene().addText("Chapter 7", font)
        series7_label.setDefaultTextColor(Qt.darkGreen)
        series7_label.setPos(700, 140)

        chart_view.setMinimumSize(800, 600)
        chart_view.setMaximumSize(800, 600)
        chart_view.setRenderHint(QPainter.Antialiasing)
        v_box = QVBoxLayout()
        v_box.addWidget(chart_view)
        W = QWidget(self)
        W.setLayout(v_box)
        W.show()
