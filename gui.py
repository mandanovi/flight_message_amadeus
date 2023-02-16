from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QHeaderView, QTableWidgetItem, QPushButton, QCalendarWidget, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import QDate
from flight_data import FlightData


class FlightReader(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a calendar picker widget
        self.calendar = QCalendarWidget(self)

        # Create a label to display the selected date
        self.date_label = QLabel('Selected date ', self)
        self.date_edit = QLineEdit(self)
        self.origin_label = QLabel('Origin code   ', self)
        self.origin_edit = QLineEdit(self)

        # Connect the QDate selection signal of the calendar widget to a slot that updates the text in the QLineEdit widget
        self.calendar.selectionChanged.connect(self.update_date_edit)

        # Create a table widget to display flight data
        self.table = QTableWidget(self)
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels([""])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Create buttons to get lowest price from specific date and get random date with lowest price
        self.lowest_price_button = QPushButton("Get Lowest Price from Specific Date", self)
        self.lowest_price_button.clicked.connect(self.get_lowest_price)
        self.random_date_button = QPushButton("On Time Airport Performance", self)
        self.random_date_button.clicked.connect(self.handle_airport_prediction)

        # Create layouts for the calendar and table widgets
        calendar_layout = QVBoxLayout()
        calendar_layout.addWidget(self.calendar)
        date_layout = QHBoxLayout()
        date_layout.addWidget(self.date_label)
        date_layout.addWidget(self.date_edit)
        origin_layout = QHBoxLayout()
        origin_layout.addWidget(self.origin_label)
        origin_layout.addWidget(self.origin_edit)
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)


        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.lowest_price_button)
        button_layout.addWidget(self.random_date_button)

        # Create a vertical layout for the whole GUI
        main_layout = QVBoxLayout()
        main_layout.addLayout(calendar_layout)
        main_layout.addLayout(date_layout)
        main_layout.addLayout(origin_layout)
        main_layout.addLayout(table_layout)
        main_layout.addLayout(button_layout)

        # Initialize selected_date to today's date
        self.selected_date = QDate.currentDate()
        self.origin_edit.editingFinished.connect(self.handle_origin_edit)

        # Set the main layout for the window
        self.setLayout(main_layout)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Flight Reader Connected to Spreadsheet')
        self.show()

    def handle_origin_edit(self):
        self.origin_code = self.origin_edit.text()

    def update_date_edit(self):
        date = self.calendar.selectedDate()
        self.selected_date = date.toString("yyyy-MM-dd")
        self.date_edit.setText(date.toString("yyyy-MM-dd"))

    def get_lowest_price(self):
        origin_code = self.origin_code
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        print(origin_code)
        print(selected_date)
        flight = FlightData()
        flight.get_lowest_price_for_specific_date(selected_date, 'YIA')
        self.table.setRowCount(2)
        updated = QTableWidgetItem("Price found has been updated to spreadsheet")
        sendtomail = QTableWidgetItem("and lower flight price has been sent to e-mail")
        self.table.setItem(0, 0, updated)
        self.table.setItem(1, 0, sendtomail)

    def handle_airport_prediction(self):
        origin_code = self.origin_code
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        print(origin_code)
        print(selected_date)
        flight = FlightData()
        data = flight.airport_prediction_data(origin_code, selected_date)
        prob = data['data']['probability']
        percentage = "{:.1%}".format(float(prob))
        self.table.setRowCount(2)
        updated = QTableWidgetItem(f"Probability on-time in {origin_code} airport : {percentage}")
        sendtomail = QTableWidgetItem("")
        self.table.setItem(0, 0, updated)
        self.table.setItem(1, 0, sendtomail)





