from time import sleep
import pickle
import requests
import wikipedia
import message
import keys

with open('diseases-data.txt') as f:
    chronic_diseases = eval(f.read())


def get_weather_response(user_input):
    try:
        api_key = keys.open_weather_api
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = user_input
        complete_url = base_url + "q=" + city_name + "&appid=" + api_key
        response = requests.get(complete_url)
        x = response.json()
                 
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = round(y["temp"]-273.15,3)
            current_pressure = y["pressure"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            return " Temperature = " +str(current_temperature)+"Celsius"+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description)
        else:
            return " City Not Found "
    except Exception as e:
        return 'Invalid API key cannot connect'

class Noter:
    def __init__(self, filename='notes.pkl'):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.filename, 'rb') as file:
                notes = pickle.load(file)
        except (FileNotFoundError, EOFError):
            notes = []
        return notes

    def save_notes(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.notes, file)

    def remember(self, note):
        self.notes.append(note)
        self.save_notes()
        return f"Note remembered: {note}"

    def what_do_you_remember(self):
        if not self.notes:
            return "I don't remember anything."
        return "I remember the following notes:\n" + "\n".join(self.notes)

    def forget_last(self):
        if self.notes:
            forgotten_note = self.notes.pop()
            self.save_notes()
            return f"Forgot the last note: {forgotten_note}"
        return "I don't have any notes to forget."

    def forget_everything(self):
        self.notes = []
        self.save_notes()
        return "Forgot all notes."
pen=Noter()

def get_response_note_this(user_input):
    return pen.remember(user_input)

def get_reminder(user_input):
    print(user_input)
    a,b,c,d=eval(user_input)
    data=message.generate_reminder_times(a,b,c,d)
    x=''
    for i in data[0]:
        x+=i.ctime()+'\n'
    return x


def get_response(user_input):
    query=user_input.lower()
    sleep(0.2)
    split=query.split()
    for i in split:
        if i in chronic_diseases:
            if 'manage' in query or 'treat' in query:
                return chronic_diseases[i][1]
            elif 'medic' in query or 'drug' in query:
                return chronic_diseases[i][2]
            else:
                return chronic_diseases[i][0]
    
    if 'how are you' in query:
        return "I am fine, Thank you\nHow are you"
    elif 'hi ' in query or 'hello' in query:
        return 'hi there, how can I help you'
    elif ('fine' in query or "good" in query) and 'I am' in query:
        return "It's good to know that your fine"
    elif ('who' in query and 'I' in query) or ('what' in query and 'my name' in query):
        with open('register.dat','rb') as f:
            return f"your name is {pickle.load(f)['Name']}"

    elif 'my name' in query:
        l=query.split()
        for i in ['name','is','my','to','change']:
            try:
                l.remove(i)
            except:
                pass
        with open('register.dat','rb') as f:
            dic=pickle.load(f)
        dic['Name']=' '.join(l)
        with open('register.dat','wb') as f:
            pickle.dump(dic,f)
        return f"ok, your name is {' '.join(l)}"
    
    elif ('who are you' in query) or ('your name' in query):
        return 'I am text-based bot designed to be your health buddy'
    
    elif "who made you" in query or "who created you" in query:
        return 'I was made by Arnav and Arjun S, Team members of Group 7@SFH, NIE, Mysore under the project "Management of Chronic Illnesses"'

    elif 'what can you do' in query or 'abilities' in query or 'reason for you' in query:
        return 'Explore me'

    elif "weather" in query or 'temperature' in query:
        return 'city name?'

    elif "good morning" in query or "good evening" in query or "good afternoon" in query:
        return "A warm" +query

    elif 'forget' in query:
        if 'everything' in query:
            return pen.forget_everything()
        elif 'last':
            return pen.forget_last()

    elif 'remember' in query or 'note' in query:
        if 'what' in query:
            if 'remember' in query:
                if query.index('what')<query.index('remember'):
                    return pen.what_do_you_remember()
                else:
                    return 'Write your note here:'

            elif 'note' in query:
                if query.index('what')<query.index('note'):
                    return pen.what_do_you_remember()
                else:
                    return 'Write your note here:'
        else:
            return 'Write your note here:'

    elif 'wikipedia' in query:
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences = 5)
        except Exception as e:
            results=e
            return "According to Wikipedia\n"+str(results)

    elif 'reminder' in query:
        return "Give your reminder in format\n([time1, time2...],'days','till_date(%y-%m-%d)','message'"
        
    else:
        return ''
