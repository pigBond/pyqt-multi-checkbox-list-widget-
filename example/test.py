import os
import sys

sys.path.append(os.getcwd())

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QVBoxLayout,
    QWidget,
    QApplication,
    QPushButton,
    QMessageBox,
)
from pyqt_multi_checkbox_list_widget import MultiCheckBoxListWidget


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.filterConditions = {
            "algorithm": None,
            "environment": None,
            "task": None
        }  # 定义筛选条件的字典
        self.multiCheckBoxListWidget = None

        self.jsonData = [
            {
                "model": "A1_run_on_B1",
                "algorithm": "A1",
                "environment": "B1",
                "task": "run",
            },
            {
                "model": "A2_run_on_B1",
                "algorithm": "A2",
                "environment": "B1",
                "task": "run",
            },
            {
                "model": "A1_run_on_B2",
                "algorithm": "A1",
                "environment": "B2",
                "task": "run",
            },
            {
                "model": "X2_run_on_Y2",
                "algorithm": "X2",
                "environment": "Y2",
                "task": "run",
            },
            {
                "model": "Z3_walk_on_W3",
                "algorithm": "Z3",
                "environment": "W3",
                "task": "walk",
            },
            {
                "model": "V4_run_on_U4",
                "algorithm": "V4",
                "environment": "U4",
                "task": "run",
            },
        ]
        self.__initUi()

    def updateFilterConditions(self, algorithm=None, environment=None, task=None):
        print("切换--", algorithm, "--", environment, "--", task)
        if algorithm is not None:
            if self.filterConditions["algorithm"] is None:
                self.filterConditions["algorithm"] = [algorithm]
            else:
                if algorithm in self.filterConditions["algorithm"]:
                    self.filterConditions["algorithm"].remove(algorithm)
                else:
                    self.filterConditions["algorithm"].append(algorithm)
        else:
            self.filterConditions["algorithm"] = None

        if environment is not None:
            if self.filterConditions["environment"] is None:
                self.filterConditions["environment"] = [environment]
            else:
                if environment in self.filterConditions["environment"]:
                    self.filterConditions["environment"].remove(environment)
                else:
                    self.filterConditions["environment"].append(environment)
        else:
            self.filterConditions["environment"] = None

        if task is not None:
            if self.filterConditions["task"] is None:
                self.filterConditions["task"] = [task]
            else:
                if task in self.filterConditions["task"]:
                    self.filterConditions["task"].remove(task)
                else:
                    self.filterConditions["task"].append(task)
        else:
            self.filterConditions["task"] = None

        print("筛选字典 = ", self.filterConditions)
        # 应用当前的筛选条件
        self.multiCheckBoxListWidget.filterItems(
            algorithm=self.filterConditions["algorithm"],
            environment=self.filterConditions["environment"],
            task=self.filterConditions["task"]
        )


    def __initUi(self):

    #-------------------------------------复选框------------------------------------------------------
        # 全选复选框
        allCheckBox = QCheckBox("Check all")
        # 算法筛选复选框
        algorithmCheckBoxes = []
        for algorithm in set(item["algorithm"] for item in self.jsonData):
            checkBox = QCheckBox(algorithm)
            checkBox.stateChanged.connect(
                lambda state, algo=algorithm: self.updateFilterConditions(
                    algorithm=algo if state == 2 else None,
                    environment=self.filterConditions["environment"],
                    task=self.filterConditions["task"]
                )
            )
            algorithmCheckBoxes.append(checkBox)
        
        # 环境筛选复选框
        environmentCheckBoxes = []
        for environment in set(item["environment"] for item in self.jsonData):
            checkBox = QCheckBox(environment)
            checkBox.stateChanged.connect(
                lambda state, env=environment: self.updateFilterConditions(
                    algorithm=self.filterConditions["algorithm"],
                    environment=env if state == 2 else None,
                    task=self.filterConditions["task"]
                )
            )
            environmentCheckBoxes.append(checkBox)
        
        # 任务筛选复选框
        taskCheckBoxes = []
        for task in set(item["task"] for item in self.jsonData):
            checkBox = QCheckBox(task)
            checkBox.stateChanged.connect(
                lambda state, t=task: self.updateFilterConditions(
                    algorithm=self.filterConditions["algorithm"],
                    environment=self.filterConditions["environment"],
                    task=t if state == 2 else None
                )
            )
            taskCheckBoxes.append(checkBox)
    #----------------------------------------------------------------------------------------------


        # 测试输出代码
        getAllChecked_btn = QPushButton("Get All Checked")
        unCheckAll_btn = QPushButton("Uncheck ALl")

        self.multiCheckBoxListWidget = MultiCheckBoxListWidget()

        self.multiCheckBoxListWidget.addItems(self.jsonData)


    #-------------------------------------按钮click------------------------------------------------------
        def on_button_2_clicked():
            allCheckBox.setCheckState(Qt.Unchecked)
            for checkBox in algorithmCheckBoxes + environmentCheckBoxes + taskCheckBoxes:
                checkBox.setCheckState(Qt.Unchecked)
            self.multiCheckBoxListWidget.uncheckAllRows()

        def on_button_clicked():
            self.confirmAction()

        getAllChecked_btn.clicked.connect(on_button_clicked)
        unCheckAll_btn.clicked.connect(on_button_2_clicked)
    #---------------------------------------------------------------------------------------------------


        # 连接全选复选框的状态变化信号到相应的槽函数
        allCheckBox.stateChanged.connect(
            lambda state: self.multiCheckBoxListWidget.toggleState(state)
        )

        self.multiCheckBoxListWidget.getAllItems()
        

        # 布局设置
        lay = QVBoxLayout()
        lay.addWidget(allCheckBox)
        for checkBox in algorithmCheckBoxes:
            lay.addWidget(checkBox)
        for checkBox in environmentCheckBoxes:
            lay.addWidget(checkBox)
        for checkBox in taskCheckBoxes:
            lay.addWidget(checkBox)
        lay.addWidget(self.multiCheckBoxListWidget)
        lay.addWidget(getAllChecked_btn)
        lay.addWidget(unCheckAll_btn)
        self.setLayout(lay)

    def getAllChecked_btn_function(self):
        # checked_data = self.multiCheckBoxListWidget.getCheckedItemsData()
        checked_data = self.multiCheckBoxListWidget.getCheckedRows()
        print("Checked items:", checked_data)
        for i in checked_data:
            print("-- ", self.jsonData[i])

    def confirmAction(self):
        reply = QMessageBox.question(
            self,
            "确认操作",
            "是否输出？选择是或否",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.getAllChecked_btn_function()
        else:
            print("操作取消")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    app.exec_()
