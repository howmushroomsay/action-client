import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QLabel, QLineEdit


class FormPage(QWidget):
    def __init__(self):
        super(FormPage, self).__init__()

        # 初始化数据
        self.data = [
            {"Name": "John", "Age": 30, "Occupation": "Engineer"},
            {"Name": "Alice", "Age": 25, "Occupation": "Teacher"},
            {"Name": "Bob", "Age": 35, "Occupation": "Doctor"},
            # ... 更多数据
        ]

        # 当前页码
        self.current_page = 0

        # 每页显示的行数
        self.rows_per_page = 2

        # 创建表格和按钮
        self.table_widget = QTableWidget()
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.delete_button = QPushButton("Delete")

        # 显示当前页码和总页数的 QLabel
        self.page_info_label = QLabel()

        # 输入跳转页码的 QLineEdit
        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("Enter page number")

        # 执行跳转的按钮
        self.jump_button = QPushButton("Jump")

        # 初始化界面
        self.init_ui()

    def init_ui(self):
        # 设置表格列数
        self.table_widget.setColumnCount(len(self.data[0]))

        # 设置表格表头
        header_labels = list(self.data[0].keys())
        self.table_widget.setHorizontalHeaderLabels(header_labels)

        # 显示第一页的数据
        self.show_data()

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.prev_button)
        layout.addWidget(self.next_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.page_info_label)
        layout.addWidget(self.page_input)
        layout.addWidget(self.jump_button)  # 添加跳转按钮

        # 连接按钮点击事件
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.delete_button.clicked.connect(self.delete_data)
        self.jump_button.clicked.connect(self.jump_to_page)  # 连接跳转按钮的点击事件

        # 设置主布局
        self.setLayout(layout)

        # 显示窗口
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Form Page')
        self.show()

    def show_data(self):
        # 计算当前页的数据范围
        start_index = self.current_page * self.rows_per_page
        end_index = start_index + self.rows_per_page

        # 清空表格
        self.table_widget.setRowCount(0)

        # 显示当前页的数据
        for row, data in enumerate(self.data[start_index:end_index]):
            self.table_widget.insertRow(row)
            for col, value in enumerate(data.values()):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row, col, item)

        # 更新页码信息
        self.update_page_info()

    def update_page_info(self):
        total_pages = (len(self.data) + self.rows_per_page - 1) // self.rows_per_page
        self.page_info_label.setText(f"Page {self.current_page + 1} of {total_pages}")

    def prev_page(self):
        # 切换到上一页
        if self.current_page > 0:
            self.current_page -= 1
            self.show_data()

    def next_page(self):
        # 切换到下一页
        last_page = len(self.data) // self.rows_per_page
        if self.current_page < last_page:
            self.current_page += 1
            self.show_data()

    def delete_data(self):
        # 删除选中行的数据
        selected_rows = set()
        for item in self.table_widget.selectedItems():
            selected_rows.add(item.row())

        # 删除数据
        new_data = [data for i, data in enumerate(self.data) if i not in selected_rows]
        self.data = new_data

        # 重新显示当前页数据
        self.show_data()

    def jump_to_page(self):
        # 跳转到指定页码
        try:
            target_page = int(self.page_input.text()) - 1
            last_page = len(self.data) // self.rows_per_page
            if 0 <= target_page <= last_page:
                self.current_page = target_page
                self.show_data()
            else:
                print("Invalid page number")
        except ValueError:
            print("Invalid input. Please enter a valid page number.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form_page = FormPage()
    sys.exit(app.exec_())
