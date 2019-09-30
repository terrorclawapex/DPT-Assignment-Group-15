import pyodbc
import socket
import functools
import os, traceback
from kivy import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition, SwapTransition, FadeTransition
from kivymd.theming import ThemeManager
from kivymd.toast import toast
from kivy.properties import ListProperty
from kivymd.uix.card import MDCard
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from decimal import Decimal
from kivymd.uix.picker import MDDatePicker
import datetime

# Global variables start here
#hostname = socket.gethostname()
#$conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + hostname + '\\SQLEXPRESS;DATABASE=UniversityScholarship;Trusted_Connection=yes;')
#cursor = conn.cursor()
# #Test if tables exist, if not, run the procedure to create them
# # TODO
#try:
#	cursor.execute("Select * From Person")
#except:
#	cursor.execute("createTables")
# Attempt DB connection
# def connectDB():
#		conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+hostname+'\SQLEXPRESS;DATABASE=UniversityScholarship;Trusted_Connection=yes;')
#		#
#		global cursor = conn.cursor()
#		conn.close()
# try:
#	connectDB()
# except Exception as e:
#	print("Error accessing database:")
#	print(str(e))
#	if ("Cannot open database \"UniversityScholarship\"" in str(e)):
#		createDB()
#		connectDB()


# GL Error
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
Config.set('graphics', 'multisamples', '0')

# Builder
Builder.load_string("""#:include kv/landingScreen.kv
#:include kv/viewApplicantScreen.kv
#:include kv/addScreen.kv
#:include kv/applicantInfoScreen.kv


#:import utils kivy.utils
""")


def createDB():
    print("Attempting to create DB")
    tableSQL = open("SQL Files/Table.sql").read()
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + hostname + '\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes;',
        autocommit=True)
    cursor = conn.cursor()
    cursor.execute(tableSQL)


def antiSQLi(key):
	key = str(key)
	if isinstance(key, str):
		key = key.replace(";", " ")
		key = key.replace("--", " ")
		key = key.replace("'", " ")
		key = key.replace("\"", " ")
		key = key.replace("=", " ")
		key = key.replace(".", " ")
		key = key.replace("/", " ")
	if isinstance(key, int):
		key = Decimal(key.strip(' "'))
	return key


# Search for Firstname
def searchFirstname(key):
    global cursor
    asqlikey = antiSQLi(key)
    cursor.execute("EXEC spSearchPersonFirstName @SearchString=" + asqlikey)
    result = cursor.fetchall()
    return result

# Add new Applicant
def insertPerson(idNumber, FirstName, Surname, dob):
	try:
		idNumber = antiSQLi(idNumber)
		FirstName = antiSQLi(FirstName)
		Surname = antiSQLi(Surname)
		dob = antiSQLi(dob)
		print("@insert: "+str(idNumber)+" "+FirstName+" "+Surname+" "+str(dob))
		p = (idNumber, FirstName, Surname, dob)
		cursor.execute("EXEC spAddPerson @PersonIDNumber=?, @PersonFirstname=?, @PersonLastname=?, @PersonDoB=?", p)
		cursor.commit()
	except Exception as e:
		print(str(e))
		
class ItemList(MDCard):
    def prepare_viewing_of_applicant(self):
        print(self.applicant_id)


class AddScreen(Screen):
    def __init__(self, **kwargs):
        super(AddScreen, self).__init__(**kwargs)
        self.idNumDateConfLabel = self.ids["idNumDateConfLabel"]
        self.snameTextField = self.ids["snameTextField"]
        self.fnameTextField = self.ids["fnameTextField"]
        self.idNumTextField = self.ids["idNumTextField"]
        self.dateOfBirth = datetime.datetime.now()

    def showDatePicker(self, *args):
        try:
            MDDatePicker(self.handleDate).open()
        except AttributeError:
            MDDatePicker(self.handleDate).open()
    def handleDate(self, date):
        self.dateOfBirth = date
        self.updateDateLabel()
        #print(self.dateOfBirth)

    def addPerson(self, *args):
        insertPerson(self.idNumTextField.text, self.fnameTextField.text, self.snameTextField.text, self.dateOfBirth)

    def on_enter(self, *args):
        self.updateDateLabel()

    def updateDateLabel(self, *args):
        self.idNumDateConfLabel.text = datetime.datetime.strftime(self.dateOfBirth,"%A, %d %B %Y")

    def on_back_pressed(self, *args):
        UI().change_screen("splash_screen")
        UI().manage_screens("add_screen", "remove")


class StudentInfo(Screen):
    def __init__(self, **kwargs):
        super(StudentInfo, self).__init__(**kwargs)
        self.firstnameLabel = self.ids["firstnameLabel"]
        self.surnameLabel = self.ids["surnameLabel"]
        self.idnumberLabel = self.ids["idnumberLabel"]
        self.dateofbirthLabel = self.ids["dateofbirthLabel"]

    def on_enter(self, *args):
        cursor.execute("EXEC spFindPersonFromID @ID=?", antiSQLi(UI.currentID))
        result = cursor.fetchone()
        self.firstnameLabel.text = str(result[1])
        self.surnameLabel.text = str(result[2])
        self.idnumberLabel.text = str(result[0])
        self.dateofbirthLabel.text = str(result[3])


    def on_back_pressed(self, *args):
        UI().manage_screens("view_screen", "add")
        UI().change_screen("view_screen")
        UI().manage_screens("student_info", "remove")


class ViewScreen(Screen):
    def __init__(self, **kwargs):
        super(ViewScreen, self).__init__(**kwargs)
        self.searchbar = self.ids['searchbar']
        self.searchButton = self.ids['searchButton']
        self.studentResult = self.ids['studentResult']
        self.resultText = self.ids['resultText']

    def viewStudent(self, name, id_num, *args):
        #print(name, id_num)
        UI().manage_screens("student_info", "add")
        UI().change_screen("student_info")
        UI().manage_screens("view_screen", "remove")

    def runSearch(self):
        self.studentResult.clear_widgets()
        result = (searchFirstname(self.searchbar.text))
        i = 0
        for row in result:
            i = i + 1
            firstname = str(row[0])
            secondname = str(row[1])
            IDNumber = str(row[2])
            person = firstname + " " + secondname + " (" + IDNumber + ")"

        self.h = 1
        self.studentResult.size = (200, 400)
        

    applicantData = ListProperty()

    def add_applicant(self, name, id_num):
        self.studentResult.add_widget(Button(text=name, on_release=functools.partial(self.viewStudent, name, id_num)))
        UI.currentID = int(id_num)

    def on_back_pressed(self, *args):
        UI().change_screen("splash_screen")
        UI().manage_screens("view_screen", "remove")


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)


class UI(App):
    global sm
    theme_cls = ThemeManager()
    theme_cls.primary_palette = "Red"
    theme_cls.theme_style = "Dark"
    sm = ScreenManager()
    currentID = 0

    def manage_screens(self, screen_name, action):
        scns = {
            "student_info": StudentInfo,
            "splash_screen": SplashScreen,
            "view_screen": ViewScreen,
            "add_screen": AddScreen

        }
        try:
            if action == "remove":
                if sm.has_screen(screen_name):
                    sm.remove_widget(sm.get_screen(screen_name))
            elif action == "add":
                if sm.has_screen(screen_name):
                   
                    print("Screen already exists")
                else:
                    sm.add_widget(scns[screen_name](name=screen_name))
        except:
            print(traceback.format_exc())
            print("Traceback ^.^")

    def change_screen(self, sc):
        try:
            sm.current = sc
        except:
            print(traceback.format_exc())

    def build(self):
        global sm
        self.bind(on_start=self.post_build_init)
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(SplashScreen(name="splash_screen"))
        return sm

    def post_build_init(self, ev):
        win = self._app_window
        win.bind(on_keyboard=self._key_handler)

    def _key_handler(self, *args):
        key = args[1]
        if key in (1000, 27):
            try:
                sm.current_screen.dispatch("on_back_pressed")
            except Exception as e:
                print(e)
            return True
        elif key == 1001:
            try:
                sm.current_screen.dispatch("on_menu_pressed")
            except Exception as e:
                print(e)
        return True

    
        

if __name__ == "__main__":
    UI().run()
