from PySide6.QtWidgets import QApplication

from package.main_window import MainWindow

app = QApplication([])

# Create a Qt widget, which will be our main window.
window = MainWindow()
window.show()

# Start the event loop.
app.exec()
