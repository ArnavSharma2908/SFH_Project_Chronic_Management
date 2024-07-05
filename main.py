import PySimpleGUI as sg
from chatbot import *
import threading
import datetime
from time import sleep
import pickle
import message
import mysql.connector

# Configure your database connection
db_config = {
    'user': 'root',
    'password': 'arnavmysql',
    'host': 'localhost',
    'database': 'arnav'
}
flag=True
def log_message(message):
    global flag
    if flag:
        try:
            # Connect to the database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert the message and current timestamp
            query = "INSERT INTO logs (message) VALUES (%s)"
            cursor.execute(query, (message,))

            # Commit the transaction
            conn.commit()

            # Close the connection
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            flag=False



sg.theme("Dark Amber")
# Define colors for messages
USER_COLOR = '#ADD8E6'
BOT_COLOR = '#F0E68C'

# Define the welcome window
welcome_layout = [
    [sg.Text("Welcome to Health Buddy app", size=(40, 1), justification='center', font=("Helvetica", 20))],
    [sg.Button('Start Chat')]
]

# Create the welcome window
welcome_window = sg.Window('Welcome to Health Buddy app', welcome_layout, finalize=True)

# Event loop for the welcome window
while True:
    event, values = welcome_window.read()
    
    if event == sg.WINDOW_CLOSED:
        break
    
    if event == 'Start Chat':
        welcome_window.close()
        break

# Define the chat window
layout = [
    [sg.Text("Health Buddy app", size=(40, 1), justification='center', font=("Helvetica", 20))],
    [sg.Multiline(size=(60, 20), key='-OUTPUT-', autoscroll=True, disabled=True, 
                  background_color='#F0F0F0', text_color='black', font=("Helvetica", 12))],
    [sg.Input(key='-INPUT-', size=(50, 1)), sg.Button('Send', bind_return_key=True)],
    [sg.Button('Exit')]
]

# Create the chat window
window = sg.Window('Health Buddy app', layout, default_button_element_size=(12,1), 
                   use_default_focus=False, finalize=True)

# Function to format the message for multiline
def format_message(message, is_user=True):
    color = USER_COLOR if is_user else BOT_COLOR
    justification = 'right' if is_user else 'left'
    formatted_message = f'[{message}]' if is_user else f'{message}'
    return f"{formatted_message}\n"

# Display the initial bot message
initial_message = format_message("Hello I'm your health buddy. How can I assist you today?", is_user=False)
window['-OUTPUT-'].print(initial_message, text_color='black', background_color=BOT_COLOR)
response=''
# Event loop        

def thread():
    while True:
        with open('reminder.dat','rb') as f:
            data=pickle.load(f)
            for i in data:
                for j in i[0]:
                    x=datetime.datetime.now()
                    delta=j-datetime.datetime(x.year,x.month,x.day,x.hour,x.minute)
                    #print(str(delta))
                    if delta.seconds==0 and delta.days==0:
                        message.send_twilio_msg('+919311775381',i[1])
                        print("Reminder sent just now:",i[1])
                        sleep(60)
        sleep(1)
trd = threading.Thread(target=thread)
trd.start()

while True:
    
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    
    if event == 'Send':
        user_input = values['-INPUT-']
        log_message('Sent:'+user_input)
        if user_input:
            # Display user message
            formatted_user_message = format_message(user_input, is_user=True)
            window['-OUTPUT-'].print(formatted_user_message, text_color='black', background_color=USER_COLOR)
            window.refresh()  # Refresh the window to update the chat screen immediately

            if response=='city name?':
                response=get_weather_response(user_input)
            elif response=='Write your note here:':
                response=get_response_note_this(user_input)
            elif 'Give your reminder in format' in response:
                response=get_reminder(user_input)
            else:
                response = get_response(user_input)
            log_message('Recieved:'+response)
            # Display bot response
            formatted_bot_response = format_message(response, is_user=False)
            window['-OUTPUT-'].print(formatted_bot_response, text_color='black', background_color=BOT_COLOR)
            window.refresh()  # Refresh the window to update the chat screen immediately
            
            # Clear the input field
            window['-INPUT-'].update('')
            window['-INPUT-'].set_focus()  # Set focus back to the input field

# Finish up by removing from the screen
window.close()
