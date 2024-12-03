import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt   # Qt is an engine to run things on

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()   # inherited from Qwidget obv
        self.city_label = QLabel("Enter city name:", self)  # creating an instance variable to label the text we gave it (and we add it to the self of the weather app)
        self.city_input = QLineEdit(self)  # adds a line for user input in the app
        self.get_weather_button = QPushButton("Get Weather", self)  # creating a button with the text we gave it and adding it to the app
        self.temperature_label = QLabel(self)  # the temperature label that will be shown and added to the app
        self.temperature_emoji = QLabel(self)  # an emoji shown and added to the app
        self.description_label = QLabel(self)  # a weather description
        self.initUI()

    def initUI(self):   # this is created to initialize (design) the interface
        self.setWindowTitle("Weather App")   # this changes the title on the app's window

        vbox = QVBoxLayout()  # this is a layout manager (making sure things are kept intact)

        vbox.addWidget(self.city_label)        # this means this widget is being now managed (later on you might tell it what to do with it stylistically)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.temperature_emoji)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)  # this will set the layouts we gave it from above

        # the styling part

        self.city_label.setAlignment(Qt.AlignCenter)  # this aligns city_label centrally
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)      # no need to align the weather button
        self.temperature_emoji.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")   # this sets a certain name into what now has become an object (because css requires to deal with objects)
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.temperature_emoji.setObjectName("temperature_emoji")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font_style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#temperature_emoji{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """)  # no need to explain

        self.get_weather_button.clicked.connect(self.get_weather)  # when clicked we will get the weather from our API

    def get_weather(self):   # this will be connected to the connect function above

        api_key = "" <------ # our api key (put your own there)
        city = self.city_input.text()   # this is how we will give the json file the name of the city
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"   # this is the specific url to gather the weather data for a certain city

        try:
            response = requests.get(url)   # requesting for the data, using the api key as permission
            response.raise_for_status()   # this is how you raise an exception because 'try' won't do it on its own ??
            data = response.json()    # to access our json file

            if data["cod"] == 200:   # cod means code and 200 means it is successful
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:   # a type of error found in the requests module, not built-in python (internet errors)
            match response.status_code:     # to check what type of error we have
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from server")
                case 503:
                    self.display_error("Service Unavailable:\nService is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from server")
                case _:
                    self.display_error(f"HTTP error occurred\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your Internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):  # this will display the errors where the parameter message, means it is any of the errors from above
        self.temperature_label.setStyleSheet("font-size: 30px;")   # this is obv styling the label (place where error will show)
        self.temperature_label.setText(message)    # this means that basically will show where the temperature label is supposed to be
        self.temperature_emoji.clear()    # to clear the emoji label in case of an error (it works after having used it at least once
        self.description_label.clear()    # same here

    def display_weather(self, data):  # all of our weather report will be here
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]  # returns the temperature which is in kelvin
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]  # 0 index because 'description' is within a LIST (this list has only one element which is the object containing the description key and its value)

        self.temperature_label.setText(f"{temperature_c:.0f}°C")  # :.0f removes decimals
        self.temperature_emoji.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description.title())  # on this label, there will be the description
                                                           # don't forget title() is to capitalize each word within a string
    @staticmethod  # when using a static method, you basically don't need any instance attributes like self or so
    def get_weather_emoji(weather_id):  # in our json file (weather data), each weather has an id, so we need it in order to suggest a specific emoji
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "☁"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id:
            return "☁☁"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)   # with this we are saying that if we have some arguments to send to our app, we would do it via command-line (in our case no)
    weather_app = WeatherApp()   # this means that this will create the weather app
    weather_app.show()   # this will make the app show
    sys.exit(app.exec_())  # we need this to exit the system (it allows us to view our app) and we do that by exiting at the same time we use the function for executions within the app (app.exec_())
