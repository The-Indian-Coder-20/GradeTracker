from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget, QLineEdit, QFrame, QMessageBox)
from backend import backend
import json
import os

SESSION_FILE = "session.json"

window_ref = None

def OpenNewWindow(currentWindow, newUiClass, use_mainwindow=True):
    global window_ref
    currentWindow.close()
    if use_mainwindow:
        window_ref = QMainWindow()
    else:
        window_ref = QWidget()
    ui = newUiClass()
    ui.setupUi(window_ref)
    window_ref.show()

def try_restore_session():
    if os.path.exists(SESSION_FILE) and os.path.getsize(SESSION_FILE) > 0:
        try:
            with open(SESSION_FILE, 'r') as f:
                session_data = json.load(f)

            access_token = session_data.get("access_token")
            refresh_token = session_data.get("refresh_token")

            if access_token and refresh_token:
                # Attempt to restore session
                backend.supabase.auth.set_session(access_token, refresh_token)

                # Verify user is valid
                user = backend.supabase.auth.get_user()
                if user and user.user:
                    # ✅ Save refreshed tokens to file
                    new_session = backend.supabase.auth.get_session()
                    with open(SESSION_FILE, 'w') as f:
                        json.dump({
                            "access_token": new_session.access_token,
                            "refresh_token": new_session.refresh_token
                        }, f)
                    return True
                else:
                    print("User not found after session restore.")
            else:
                print("Missing access_token or refresh_token in session file.")
        except Exception as e:
            print("Session restore failed:", e)
            os.remove(SESSION_FILE)  # Clean up corrupted/expired session
    return False

def sign_out():
    backend.supabase.auth.sign_out()
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

class LandingWindow(object):
    def setupUi(self, GradeTracker):
        self.mainWindow = GradeTracker
        if not GradeTracker.objectName():
            GradeTracker.setObjectName(u"GradeTracker")
        GradeTracker.resize(600, 400)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GradeTracker.sizePolicy().hasHeightForWidth())
        GradeTracker.setSizePolicy(sizePolicy)
        GradeTracker.setMinimumSize(QSize(600, 400))
        GradeTracker.setMaximumSize(QSize(600, 400))
        self.centralwidget = QWidget(GradeTracker)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalSpacer_2 = QSpacerItem(90, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.horizontalLayout.addItem(self.verticalSpacer_2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalSpacer = QSpacerItem(351, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.verticalLayout_2.addItem(self.horizontalSpacer)

        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_3 = QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 700 36pt \"Meiryo UI\";")

        self.verticalLayout_3.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.pushButton = QPushButton(self.widget_3)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"font: 700 12pt \"Meiryo UI\";")
        self.pushButton.clicked.connect(lambda: OpenNewWindow(self.mainWindow, SignInWindow))

        self.verticalLayout_3.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.widget_3)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"font: 700 12pt \"Meiryo UI\";")
        self.pushButton_2.clicked.connect(lambda: OpenNewWindow(self.mainWindow, SignUpWindow))

        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.horizontalSpacer_2 = QSpacerItem(351, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.verticalLayout_2.addItem(self.horizontalSpacer_2)
        self.verticalLayout.addWidget(self.widget_2)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalSpacer = QSpacerItem(90, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.horizontalLayout.addItem(self.verticalSpacer)
        GradeTracker.setCentralWidget(self.centralwidget)
        self.retranslateUi(GradeTracker)
        QMetaObject.connectSlotsByName(GradeTracker)
    # setupUi

    def retranslateUi(self, GradeTracker):
        GradeTracker.setWindowTitle("GradeTracker")
        self.label.setText(QCoreApplication.translate("GradeTracker", u"GradeTracker", None))
        self.pushButton.setText(QCoreApplication.translate("GradeTracker", u"Sign-in", None))
        self.pushButton_2.setText(QCoreApplication.translate("GradeTracker", u"Sign-up", None))

class SignInWindow(object):
    def attempt_signin(self):
        email = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()

        if not email or not password:
            QMessageBox.warning(self.widget, "Error", "Email and password cannot be empty.")
            return

        response = backend.LoginEmailPassword(email, password)

        if response and response.user:
            with open(SESSION_FILE, 'w') as f:
                f.write(response.session.model_dump_json())
            QMessageBox.information(self.widget, "Success", "Sign-in successful!")
            # redirect to app dashboard here
        else:
            QMessageBox.critical(self.widget, "Error", "Sign-in failed. Check credentials or try again.")
    def setupUi(self, Widget):
        Widget.setObjectName(u"SignInWidget")
        Widget.setWindowTitle("Sign-in")
        Widget.resize(636, 400)

        if isinstance(Widget, QMainWindow):
            self.container = QWidget()
            self.horizontalLayout = QHBoxLayout(self.container)
            Widget.setCentralWidget(self.container)
        else:
            self.horizontalLayout = QHBoxLayout(Widget)

        self.horizontalLayout.addSpacerItem(QSpacerItem(100, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.widget = QWidget()
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(15)

        # --- Title ---
        self.label_3 = QLabel("Sign-in")
        self.label_3.setStyleSheet(u"font: 700 36pt 'Meiryo UI';")
        self.verticalLayout.addWidget(self.label_3, 0, Qt.AlignHCenter)

        # --- E-mail Row ---
        self.email_row = QWidget()
        self.email_row_layout = QHBoxLayout(self.email_row)
        self.email_row_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel("E-mail")
        self.label.setFixedWidth(60)
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("john.doe@email.com")
        self.email_row_layout.addWidget(self.label)
        self.email_row_layout.addWidget(self.lineEdit)
        self.verticalLayout.addWidget(self.email_row)

        # --- Password Row ---
        self.password_row = QWidget()
        self.password_row_layout = QHBoxLayout(self.password_row)
        self.password_row_layout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel("Password")
        self.label_2.setFixedWidth(60)
        self.lineEdit_2 = QLineEdit()
        self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_row_layout.addWidget(self.label_2)
        self.password_row_layout.addWidget(self.lineEdit_2)
        self.verticalLayout.addWidget(self.password_row)

        self.email_row.setFixedHeight(40)
        self.password_row.setFixedHeight(40)

        # --- Sign-in Button ---
        self.pushButton = QPushButton("Sign-in")
        self.pushButton.setStyleSheet("font: 700 12pt 'Meiryo UI'; padding: 6px;")
        self.pushButton.clicked.connect(lambda: self.attempt_signin())
        self.verticalLayout.addWidget(self.pushButton)

        # --- Separator Line ---
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout.addWidget(self.separator)

        # --- Back Button ---
        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.setStyleSheet(u"font: 700 10pt 'Meiryo UI'; padding: 6px;")
        self.verticalLayout.addWidget(self.back_button)
        self.back_button.clicked.connect(lambda: OpenNewWindow(Widget, LandingWindow, use_mainwindow=True))

        self.horizontalLayout.addWidget(self.widget)
        self.horizontalLayout.addSpacerItem(QSpacerItem(100, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))


class SignUpWindow(object):
    def attempt_signup(self):
        email = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()

        if not email or not password:
            QMessageBox.warning(self.widget, "Error", "Email and password cannot be empty.")
            return

        response = backend.LoginEmailPassword(email, password)

        if response and response.user:
            with open(SESSION_FILE, 'w') as f:
                f.write(response.session.model_dump_json())
            QMessageBox.information(self.widget, "Success", "Sign-up successful!")
        else:
            QMessageBox.critical(self.widget, "Error", "Sign-up failed. Check credentials or try again.")

    def setupUi(self, Widget):
        Widget.setObjectName(u"SignUpWidget")
        Widget.setWindowTitle("Sign-up")
        Widget.resize(636, 400)

        if isinstance(Widget, QMainWindow):
            self.container = QWidget()
            self.horizontalLayout = QHBoxLayout(self.container)
            Widget.setCentralWidget(self.container)
        else:
            self.horizontalLayout = QHBoxLayout(Widget)

        self.horizontalLayout.addSpacerItem(QSpacerItem(100, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.widget = QWidget()
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(15)

        # --- Title ---
        self.label_3 = QLabel("Sign-up")
        self.label_3.setStyleSheet(u"font: 700 36pt 'Meiryo UI';")
        self.verticalLayout.addWidget(self.label_3, 0, Qt.AlignHCenter)

        # --- E-mail Row ---
        self.email_row = QWidget()
        self.email_row_layout = QHBoxLayout(self.email_row)
        self.email_row_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel("E-mail")
        self.label.setFixedWidth(60)
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("john.doe@email.com")
        self.email_row_layout.addWidget(self.label)
        self.email_row_layout.addWidget(self.lineEdit)
        self.verticalLayout.addWidget(self.email_row)

        # --- Password Row ---
        self.password_row = QWidget()
        self.password_row_layout = QHBoxLayout(self.password_row)
        self.password_row_layout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel("Password")
        self.label_2.setFixedWidth(60)
        self.lineEdit_2 = QLineEdit()
        self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_row_layout.addWidget(self.label_2)
        self.password_row_layout.addWidget(self.lineEdit_2)
        self.verticalLayout.addWidget(self.password_row)

        self.email_row.setFixedHeight(40)
        self.password_row.setFixedHeight(40)

        # --- Sign-in Button ---
        self.pushButton = QPushButton("Sign-in")
        self.pushButton.setStyleSheet("font: 700 12pt 'Meiryo UI'; padding: 6px;")
        self.pushButton.clicked.connect(lambda: self.attempt_signup())
        self.verticalLayout.addWidget(self.pushButton)

        # --- Separator Line ---
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout.addWidget(self.separator)

        # --- Back Button ---
        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.setStyleSheet(u"font: 700 10pt 'Meiryo UI'; padding: 6px;")
        self.verticalLayout.addWidget(self.back_button)
        self.back_button.clicked.connect(lambda: OpenNewWindow(Widget, LandingWindow, use_mainwindow=True))

        self.horizontalLayout.addWidget(self.widget)
        self.horizontalLayout.addSpacerItem(QSpacerItem(100, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    MainWindow = QMainWindow()

    if try_restore_session():
        # Go straight to your dashboard or home screen
        from frontend.dashboard import DashboardWindow
        ui = DashboardWindow()
    else:
        ui = LandingWindow()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
