import PyQt5
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
# x轴是时间，一天为一增
# y轴是掌握程度，每个章节一条线
# 导入所需模块
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg
from datetime import datetime
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtGui import QPainter, QFont, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel


# 定义学生错误问题数据的数据结构
class ErrorData:
    def __init__(self, timestamp, type):
        self.timestamp = timestamp  # 错误问题的时间戳（格式为日期或时间戳）
        self.type = type  # 错误问题的类型


# 生成学生能力随时间的变化图表
def generateStudentAbilityChart(errorData):
    categorizedData = categorizeErrorDataByTimeAndType(errorData)
    timePoints, abilityLevels = extractChartData(categorizedData)
    plotChart(timePoints, abilityLevels)


# 按照时间和类型分类整理学生错误问题数据
def categorizeErrorDataByTimeAndType(errorData):
    categorizedData = {}

    for error in errorData:
        timestamp = error.timestamp
        errorType = error.type

        if timestamp not in categorizedData:
            categorizedData[timestamp] = {}

        if errorType not in categorizedData[timestamp]:
            categorizedData[timestamp][errorType] = 1
        else:
            categorizedData[timestamp][errorType] += 1

    return categorizedData


# 提取图表绘制所需的横坐标和纵坐标数据
def extractChartData(categorizedData):
    timePoints = []
    abilityLevels = []

    # 根据时间顺序遍历数据，并计算每个时间点的能力水平
    sortedTimes = sorted(categorizedData.keys())
    previousAbilityLevel = 100  # 初始能力水平为100

    for time in sortedTimes:
        timePoints.append(time)

        totalErrors = sum(categorizedData[time].values())
        errorWeight = totalErrors * 10
        currentAbilityLevel = previousAbilityLevel - errorWeight

        abilityLevels.append(currentAbilityLevel)
        previousAbilityLevel = currentAbilityLevel

    return timePoints, abilityLevels


# 绘制图表（使用 PyQtGraph 库）
def plotChart(xData, yData):
    chart = QChart()
    chart.setTitle("简单折线图")
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.legend().hide()
    line_series = QLineSeries()  # Using line charts for this example
    x_values = [1, 2, 3, 4, 5, 6, 7]
    y_values = [1, 2, 4, 3, 1, 3, 5]
    for value in range(0, len(x_values)):
        line_series.append(x_values[value], y_values[value])
    chart.addSeries(line_series)  # Add line series to chart instance
    axis_x = QValueAxis()
    axis_x.setLabelFormat("%d")
    chart.addAxis(axis_x, Qt.AlignBottom)
    line_series.attachAxis(axis_x)

    axis_y = QValueAxis()
    axis_y.setLabelFormat("%d")
    chart.addAxis(axis_y, Qt.AlignLeft)
    line_series.attachAxis(axis_y)
    chart_view = QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)
    v_box = QVBoxLayout()
    v_box.addWidget(chart_view)
    W = QWidget()
    W.setLayout(v_box)
    W.show()


# 创建示例错误问题数据
def createSampleErrorData():
    errorData = [
        ErrorData('2023-01-01', '语法错误'),
        ErrorData('2023-01-03', '语法错误'),
        ErrorData('2023-01-03', '拼写错误'),
        ErrorData('2023-01-04', '逻辑错误'),
        ErrorData('2023-01-05', '逻辑错误'),
        ErrorData('2023-01-07', '语法错误'),
        ErrorData('2023-01-08', '拼写错误'),
        ErrorData('2023-01-09', '语法错误'),
        ErrorData('2023-01-09', '拼写错误'),
        ErrorData('2023-01-12', '逻辑错误'),
    ]
    return errorData


class SeriesNameDelegate(PyQt5.QtWidgets.QGraphicsItem):
    def __init__(self, series, parent=None):
        super().__init__(parent)
        self.series = series

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 100, 20)

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(self.series.pen().color()))
        painter.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
        painter.drawText(self.boundingRect(), self.series.name())


if __name__ == '__main__':
    # 示例用法
    # errorData = createSampleErrorData()
    # generateStudentAbilityChart(errorData)
    app = QApplication(sys.argv)
    chart = QChart()
    # 设置图表旁边的空白大小
    chart.setMargins(QMargins(100, 50, 100, 50))  # 左、上、右、下边距都设置为50

    chart.setTitle("能力分析图")
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.legend().hide()

    pen = QPen()
    pen.setColor(Qt.blue)  # 设置为红色
    pen.setWidth(2)  # 设置线宽

    line_series = QLineSeries()  # 申请一条折线
    line_series.setPen(pen)

    pen = QPen()
    pen.setColor(Qt.blue)  # 设置为红色
    pen.setWidth(2)  # 设置线宽

    line_series2 = QLineSeries()  # 申请一条折线
    line_series2.setPen(pen)

    pen = QPen()
    pen.setColor(Qt.blue)  # 设置为红色
    pen.setWidth(2)  # 设置线宽

    line_series3 = QLineSeries()  # 申请一条折线
    line_series3.setPen(pen)

    pen = QPen()
    pen.setColor(Qt.blue)  # 设置为红色
    pen.setWidth(2)  # 设置线宽

    line_series4 = QLineSeries()  # 申请一条折线
    line_series4.setPen(pen)

    pen = QPen()
    pen.setColor(Qt.blue)  # 设置为红色
    pen.setWidth(2)  # 设置线宽

    line_series5 = QLineSeries()  # 申请一条折线
    line_series5.setPen(pen)

    pen = QPen()
    pen.setColor(Qt.blue)  # 设置为红色
    pen.setWidth(2)  # 设置线宽

    line_series6 = QLineSeries()  # 申请一条折线
    line_series6.setPen(pen)

    pen = QPen()
    pen.setColor(Qt.blue)  # 设置为红色
    pen.setWidth(2)  # 设置线宽

    line_series7 = QLineSeries()  # 申请一条折线
    line_series7.setPen(pen)

    x_values = [1, 2, 3, 4, 5, 6, 7]
    y_values = [1, 2, 4, 3, 1, 3, 5]
    for value in range(0, len(x_values)):
        line_series.append(x_values[value], y_values[value])
    x_values = [7, 2, 3, 4, 5, 6, 7]
    y_values = [1, 2, 4, 3, 1, 3, 5]
    line_series1 = QLineSeries()
    for value in range(0, len(x_values)):
        line_series1.append(x_values[value], y_values[value])

    chart.addSeries(line_series)
    chart.addSeries(line_series2)  # 加入
    chart.addSeries(line_series3)  # 加入
    chart.addSeries(line_series4)  # 加入
    chart.addSeries(line_series5)  # 加入
    chart.addSeries(line_series6)  # 加入
    chart.addSeries(line_series7)  # 加入

    axis_x = QValueAxis()  # 创建x轴
    axis_x.setTitleText('日期(七天)')
    axis_x.setLabelFormat("%d")
    chart.addAxis(axis_x, Qt.AlignBottom)
    line_series.attachAxis(axis_x)

    axis_y = QValueAxis()
    axis_y.setTitleText('掌握能力')
    axis_y.setLabelFormat("%d")
    chart.addAxis(axis_y, Qt.AlignLeft)
    line_series.attachAxis(axis_y)

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
    W = QWidget()
    W.setLayout(v_box)
    W.show()
    sys.exit(app.exec_())
