import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import drawNetwork
import DV as dv
import LS as ls
import copy

PAD_WIDTH = 2
matrix = []
length = 0
dv_columns = ("目的地址", "下一跳", "目的地跳数")
isDV_CLICK = False
isLS_CLICK = False
router_list = []
ls_res = ()


# 定义Application类表示应用/窗口，继承Frame类
class Application(tk.Frame):
    # Application构造函数，master为窗口的父控件
    def __init__(self, master=None):
        # 初始化Application的Frame部分
        tk.Frame.__init__(self, master)
        # 显示窗口，并使用grid布局
        self.grid()
        # 创建控件
        self.fm1 = tk.Frame(self)
        self.fm1.pack(side='left')
        self.fm2 = tk.Frame(self)
        self.fm2.pack(side='right', fill='y')

        self.createPointInput()
        # self.createPhoto()
        self.createWidgets()
        self.createButton()
        # self.createTable("")
        # self.createWays([1, 2, 3, 4, 5])

    # 创建控件
    def createWidgets(self):
        # 创建一个文字为'Quit'，点击会退出的按钮
        self.quitButton = tk.Button(self.fm1, text='生成图', command=self.createPhotoBtnCallback)
        # 显示按钮，并使用grid布局
        self.quitButton.pack()

    def createPhoto(self):
        self.img_open = Image.open('graph_total.png')

        self.img_png = ImageTk.PhotoImage(image=self.img_open)
        if hasattr(self, 'photoWidgets'):
            self.photoWidgets.destroy()
        if hasattr(self, 'error'):
            self.error.destroy()

        self.photoWidgets = tk.Label(self.fm1, image=self.img_png)
        self.photoWidgets.pack()

    def createPointInput(self):
        input_label_1 = tk.Label(self.fm2, text='源节点：')
        self.input_1 = tk.Entry(self.fm2, width=5)
        input_label_2 = tk.Label(self.fm2, text='目的节点：')
        self.input_2 = tk.Entry(self.fm2, width=5)

        input_label_1.grid(row=0, column=0, padx=PAD_WIDTH)
        self.input_1.grid(row=0, column=1, padx=PAD_WIDTH)
        input_label_2.grid(row=0, column=2, padx=PAD_WIDTH)
        self.input_2.grid(row=0, column=3, padx=PAD_WIDTH)

    def createButton(self):
        self.dvBtn = tk.Button(self.fm2, text='DV算法', command=self.dvBtnCallback)
        self.lsBtn = tk.Button(self.fm2, text='LS算法', command=self.lsBtnCallback)
        self.dvBtn.grid(row=0, column=4, padx=PAD_WIDTH)
        self.lsBtn.grid(row=0, column=5, padx=PAD_WIDTH)

    def createTable(self, columns, *args):

        if hasattr(self, 'treeview'):
            self.treeview.destroy()

        self.treeview = ttk.Treeview(self.fm2, show="headings", columns=columns)  # 表格

        for i in range(len(columns)):
            self.treeview.column(columns[i], width=100, anchor='center')
            self.treeview.heading(columns[i], text=columns[i])

        for i in range(min(len(args[0]), len(args[1]), len(args[2]))):
            self.treeview.insert('', i, values=(args[0][i], args[1][i], args[2][i]))

        self.treeview.grid(row=2, columnspan=6, padx=PAD_WIDTH * 6)

    def createWays(self, way_list):

        if hasattr(self, 'ways_label'):
            self.ways_label.destroy()

        way = ''

        for i in range(len(way_list)):
            way = way + str(way_list[i])
            if i != len(way_list) - 1:
                way = way + " -> "

        self.ways_label = tk.Label(self.fm2, text='路径为：' + way + '    跳数为：' + str(len(way_list) - 1))
        self.ways_label.grid(row=3, columnspan=6, padx=PAD_WIDTH * 6)

    def createComboBox(self, combo_list, index):
        if hasattr(self, 'comboBox'):
            self.comboBox.destroy()
            self.comboBox_label.destroy()

        self.comboBox = ttk.Combobox(self.fm2, width=5, textvariable='number')
        self.comboBox['value'] = tuple(combo_list)
        self.comboBox['state'] = 'readonly'
        self.comboBox.bind('<<ComboboxSelected>>', self.comboBoxCallback)
        self.comboBox.current(index)

        self.comboBox_label = tk.Label(self.fm2, text='选择路由表：')
        self.comboBox_label.grid(row=1, column=0, padx=PAD_WIDTH)

        self.comboBox.grid(row=1, column=1, padx=PAD_WIDTH)

    def comboBoxCallback(self, *args):
        global router_list
        index = int(self.comboBox.get())
        print(index)
        self.createTable(dv_columns, router_list[index].destination,
                         router_list[index].next, router_list[index].cost)

    def createPhotoBtnCallback(self):

        global matrix
        global length
        global isDV_CLICK
        global isLS_CLICK

        isDV_CLICK = False
        isLS_CLICK = False

        res = drawNetwork.createGraph()
        length = res[1]
        matrix = res[0]
        self.createPhoto()
        self.input_1.delete(0, 'end')
        self.input_2.delete(0, 'end')
        self.update()

        if hasattr(self, 'comboBox'):
            self.comboBox.destroy()
            self.comboBox_label.destroy()
        if hasattr(self, 'treeview'):
            self.treeview.destroy()
        if hasattr(self, 'ways_label'):
            self.ways_label.destroy()
        if hasattr(self, 'error'):
            self.error.destroy()

    def dvBtnCallback(self):
        global length
        global matrix
        global isDV_CLICK
        global router_list

        if hasattr(self, 'error'):
            self.error.destroy()

        if not isDV_CLICK:
            isDV_CLICK = True
            router_list = dv.calc_router(length, copy.deepcopy(matrix))

        v0 = int(self.input_1.get())
        v1 = int(self.input_2.get())

        dest_list = router_list[v0].destination
        next_list = router_list[v0].next
        cost_list = router_list[v0].cost

        if min(len(dest_list), len(next_list), len(cost_list)) == 0:
            self.createError()
            return

        self.createTable(dv_columns, dest_list, next_list, cost_list)

        source = router_list[v0].source
        destination = router_list[v0].next[v1]
        way = [source]
        while True:

            way.append(destination)

            if destination == v1:
                break
            if destination == 'null':
                self.createError()
                return
            destination = router_list[destination].next[v1]

        self.createWays(way)
        self.createComboBox(router_list[v0].destination, v0)
        drawNetwork.drawResult(way)
        self.createPhoto()

    def lsBtnCallback(self):
        global length
        global matrix
        global isLS_CLICK
        global ls_res

        v0 = int(self.input_1.get())
        v1 = int(self.input_2.get())

        if hasattr(self, 'comboBox'):
            self.comboBox.destroy()
            self.comboBox_label.destroy()
        if hasattr(self, 'treeview'):
            self.treeview.destroy()
        if hasattr(self, 'error'):
            self.error.destroy()

        if not isLS_CLICK:
            isLS_CLICK = True

        ls_res = ls.dijkstra(length, copy.deepcopy(matrix), v0)

        distance = ls_res[0]
        path = ls_res[1]
        print(distance)
        print(path)

        ways = ls.get_ways(v0, v1, path)
        print(ways)

        if len(ways) == 2:
            print('ssss')

        if type(ways) == 'NoneType':
            self.createError()
            return

        self.createWays(ways)
        drawNetwork.drawResult(ways)
        self.createPhoto()

    def createError(self):

        if hasattr(self, 'error'):
            self.error.destroy()

        self.error = tk.Label(self.fm2, text='没有路径或输入错误！')
        self.error.grid(row=5, columnspan=6, padx=PAD_WIDTH * 6)


app = Application()
app.master.title = 'First Tkinter'
app.mainloop()
