#Python GUI imports
import tkinter as tk
from tkinter import font
#Excel and numbers usage
import pandas as pd
#Screen resolution imports
import pyautogui as pyg
#Graph usage imports
import matplotlib as mpl
mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

#Class containing client code
class StudyAppClient:
    def __init__(self):
        #List with open windows
        self.openWindows = []
        #Sets main menu window dimensions
        self.windowHeight = 600
        self.windowWidth = 400
        #Sets main menu position on screen relative to screen resolution
        self.screenResolution = pyg.size()
        self.screenMiddleX = int(self.screenResolution[0] / 2 - self.windowWidth / 2)
        self.screenMiddleY = int(self.screenResolution[1] / 2 - self.windowHeight / 2)
        #Init all functions that need to be called when the program is run
        self.MainMenuWindow()

    #Function to create a new window
    def NewWindow(self, windowName):
        #Destroys old window
        for window in self.openWindows:
            try:
                window.destroy()
            except:
                pass
        #Spawns new window and sets the position on screen, title, and makes it resizable
        self.newWindow = tk.Tk()
        self.newWindow.geometry("+%d+%d" % (self.screenMiddleX,self.screenMiddleY))
        self.newWindow.title(windowName)
        self.newWindow.resizable(True, True)

    def AutoResizeTextBox(self, varName):
        #Number of lines in the text box
        numLines = int(varName.index('end-1c').split('.')[0])
        #Resizes the text box
        varName.config(height=max(1, numLines))

    def NewPopupWindow(self, windowName):
        # Spawns new window and sets the position on screen, title, and makes it resizable
        self.newPopupWindow = tk.Tk()
        self.newPopupWindow.geometry("+%d+%d" % (self.screenMiddleX, self.screenMiddleY))
        self.newPopupWindow.title(windowName)
        self.newPopupWindow.resizable(False, False)

    def FontMaker(self):
        self.titleFont = font.Font(family="Poppins", size=36, weight="bold")
        self.buttonFont = font.Font(family="Poppins", size=18, weight="bold")

    def MainMenuWindow(self):
        for window in self.openWindows:
            try:
                window.destroy()
            except:
                pass
        self.mainMenu = tk.Tk()
        self.openWindows.append(self.mainMenu)
        self.mainMenu.title("StudyApp")
        self.mainMenu.geometry(f"{self.windowWidth}x{self.windowHeight}+{self.screenMiddleX}+{self.screenMiddleY}")
        self.mainMenu.resizable(True, True)

        #Init fonts
        self.FontMaker()

        title = tk.Label(self.mainMenu, text="StudyApp", font=self.titleFont)
        title.pack(pady = (30, 20))

        self.dashboard = tk.Button(self.mainMenu, height=1, width=12, text="Dashboard", font=self.buttonFont, border=5, command=lambda: self.DashboardWindow())
        self.dashboard.pack(pady=10)
        self.categories = tk.Button(self.mainMenu, height=1, width=12, text="Categories", font=self.buttonFont, border=5, command=lambda: self.CategoriesWindow())
        self.categories.pack(pady=10)
        self.excelButton = tk.Button(self.mainMenu, height=1, width=12, text="Open Excel", font=self.buttonFont, border=5, command=lambda: self.ExcelWindow())
        self.excelButton.pack(pady=10)
        self.settingsButton = tk.Button(self.mainMenu, height=1, width=12, text="Settings", font=self.buttonFont, border=5, command=lambda: self.SettingsWindow())
        self.settingsButton.pack(pady=10)
        self.exitButton = tk.Button(self.mainMenu, height=1, width=12, text="Exit", font=self.buttonFont, border=5, command=lambda: self.mainMenu.destroy())
        self.exitButton.pack(pady=10)

        self.mainMenu.mainloop()

    def DashboardWindow(self):
        #Init page
        self.NewWindow("Dashboard")
        #Change var name to name of page and appends page name to open windows list
        self.Dashboard = self.newWindow
        self.openWindows.append(self.Dashboard)
        #Page Title
        pageTitle = tk.Label(self.Dashboard, text="Dashboard", font=self.titleFont)
        pageTitle.pack(pady=(30, 20))
        #Study time and record graph

    def AddCategories(self):
        #Gives the popup window a proper name
        self.NewPopupWindow("New Category")
        #Change the var name to the name of the popup
        self.AddCategoriesPopup = self.newPopupWindow
        self.AddCategoriesPopup.geometry("300x120")
        #Input area for name of the category
        categoryName = tk.Text(self.AddCategoriesPopup, width=30)
        categoryName.pack(fill="x", pady=5, padx=10)
        #Makes it so that the text box automatically resizes as the lines increase
        categoryName.bind("<KeyRelease>", self.AutoResizeTextBox(categoryName))

    def CategoriesWindow(self):
        #Init page
        self.NewWindow("Categories")
        #Change var name to name of page and appends page name to open windows list
        self.Categories = self.newWindow
        self.openWindows.append(self.Categories)
        #Page title
        pageTitle = tk.Label(self.Categories, text="Categories", font=self.titleFont)
        pageTitle.pack(pady=(30, 20))
        #Categories List Frame
        categoriesListFrame = tk.Frame(self.Categories, width=400, height=400)
        categoriesListFrame.pack(pady=10, padx=5)
        #Add Categories button
        addCategoriesButton = tk.Button(self.Categories, height=1, width=25, text="Add Category", font=self.buttonFont, border=5, command=lambda: self.AddCategories())
        addCategoriesButton.pack(pady=1, padx=10)
        #Back to main menu button
        mainMenuButton = tk.Button(self.Categories, height=1, width=25, text="Back to main menu", font=self.buttonFont, border=5, command=lambda: self.MainMenuWindow())
        mainMenuButton.pack(pady=(1, 15), padx=10)


    """
    def ExcelWindow(self):

    def SettingsWindow(self):
    """

if __name__ == "__main__":
    StudyAppClient()
