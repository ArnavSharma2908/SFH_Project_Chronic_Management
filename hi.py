import PySimpleGUI as sg

sg.theme('Dark Amber')
# Function to create the registration window
def registration_window():
    layout = [
        [sg.Text('Health Buddy App - Registration')],
        [sg.Text('Name'), sg.Input(key='-NAME-')],
        [sg.Text('Chronic Condition'), sg.Input(key='-CONDITION-')],
        [sg.Text('Medications'), sg.Input(key='-MEDICATIONS-')],
        [sg.Text('Allergies'), sg.Input(key='-ALLERGIES-')],
        [sg.Text('Lifestyle Preferences'), sg.Input(key='-LIFESTYLE-')],
        [sg.Button('Register'), sg.Button('Cancel')]
    ]
    return sg.Window('Registration', layout, finalize=True)

# Function to create the main dashboard window
def dashboard_window():
    layout = [
        [sg.Text('Health Buddy App - Dashboard')],
        [sg.Button('Health Data'), sg.Button('Medication Reminders'), sg.Button('Symptom Tracker')],
        [sg.Button('Nutrition & Exercise'), sg.Button('Community Support'), sg.Button('Telehealth')],
        [sg.Button('Emergency Assistance'), sg.Button('Educational Resources'), sg.Button('Integration with Wearables')],
        [sg.Button('Gamification'), sg.Button('Logout')]
    ]
    return sg.Window('Dashboard', layout, finalize=True)

# Function to create the medication reminders window
def medication_reminders_window():
    layout = [
        [sg.Text('Medication Reminders')],
        [sg.Text('Medication'), sg.Input(key='-MEDICATION-')],
        [sg.Text('Dosage'), sg.Input(key='-DOSAGE-')],
        [sg.Text('Time'), sg.Input(key='-TIME-')],
        [sg.Button('Set Reminder'), sg.Button('Back')]
    ]
    return sg.Window('Medication Reminders', layout, finalize=True)

# Main function to run the app
def main():
    window = registration_window()
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Register':
            window.close()
            window = dashboard_window()
        elif event == 'Logout':
            window.close()
            window = registration_window()
        elif event == 'Medication Reminders':
            window.close()
            window = medication_reminders_window()
        elif event == 'Back':
            window.close()
            window = dashboard_window()
        # Add additional event handling for other buttons and features here
    
    window.close()

if __name__ == "__main__":
    main()
