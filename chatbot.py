# chatbot.py
from time import sleep
import pickle
import requests
import wikipedia
import message

chronic_diseases = {
    "asthma": "a chronic disease that affects the airways in the lungs, causing wheezing, breathlessness, chest tightness, and coughing.",
    "diabetes": "a metabolic disorder where the body has high blood sugar levels over a prolonged period either because the body doesn't produce enough insulin or because cells don't respond to the insulin that is produced.",
    "hypertension": "a condition in which the blood pressure in the arteries is persistently elevated, often called high blood pressure.",
    "arthritis": "an inflammation of the joints, causing pain and stiffness that can worsen with age.",
    "chronic obstructive pulmonary disease (copd)": "a group of progressive lung diseases that block airflow and make it difficult to breathe.",
    "osteoporosis": "a condition in which bones become weak and brittle, making them more susceptible to fractures.",
    "alzheimer's disease": "a progressive neurological disorder that causes the brain to shrink and brain cells to die, leading to a decline in memory, thinking, and social skills.",
    "parkinson's disease": "a neurodegenerative disorder that affects predominately dopamine-producing neurons in a specific area of the brain, causing tremors, stiffness, and difficulty with balance and coordination.",
    "chronic kidney disease": "a long-term condition where the kidneys do not work effectively, often leading to kidney failure.",
    "heart disease": "a range of conditions that affect the heart, including coronary artery disease, arrhythmias, and heart defects.",
    "stroke": "a medical condition in which poor blood flow to the brain results in cell death, causing sudden loss of brain function.",
    "cystic fibrosis": "a hereditary disorder affecting the exocrine glands, leading to the production of abnormally thick mucus, causing respiratory and digestive problems.",
    "epilepsy": "a neurological disorder marked by sudden recurrent episodes of sensory disturbance, loss of consciousness, or convulsions, associated with abnormal electrical activity in the brain.",
    "multiple sclerosis": "a chronic illness of the nervous system where the immune system attacks the protective sheath that covers nerve fibers, causing communication problems between the brain and the rest of the body.",
    "crohn's disease": "a type of inflammatory bowel disease that causes inflammation of the digestive tract, which can lead to abdominal pain, severe diarrhea, fatigue, weight loss, and malnutrition.",
    "ulcerative colitis": "a chronic inflammatory bowel disease that causes inflammation and sores in the digestive tract, primarily affecting the innermost lining of the large intestine and rectum.",
    "lupus": "a systemic autoimmune disease that occurs when the body's immune system attacks its own tissues and organs, causing inflammation and damage to various body systems.",
    "hepatitis c": "a viral infection that causes liver inflammation, sometimes leading to serious liver damage.",
    "hiv/aids": "a chronic, potentially life-threatening condition caused by the human immunodeficiency virus (hiv), which damages the immune system and interferes with the body's ability to fight the organisms that cause disease.",
    "sickle cell disease": "a group of inherited red blood cell disorders in which the red blood cells contort into a sickle shape, leading to various complications including pain, anemia, and organ damage.",
    "chronic fatigue syndrome": "a complex disorder characterized by extreme fatigue that can't be explained by any underlying medical condition and may be worsened by physical or mental activity.",
    "fibromyalgia": "a chronic disorder characterized by widespread musculoskeletal pain, fatigue, and tenderness in localized areas.",
    "migraine": "a neurological condition that can cause multiple symptoms, including intense headaches, nausea, and sensitivity to light and sound.",
    "diverticulitis": "an inflammation or infection of small pouches called diverticula that develop along the walls of the intestines.",
    "irritable bowel syndrome": "a common disorder that affects the large intestine, causing symptoms like cramping, abdominal pain, bloating, gas, and diarrhea or constipation, or both.",
    "psoriasis": "a chronic skin condition that speeds up the life cycle of skin cells, causing cells to build up rapidly on the surface of the skin, leading to scaly, red patches.",
    "chronic pancreatitis": "a long-standing inflammation of the pancreas that alters its normal structure and functions.",
    "hypothyroidism": "a condition in which the thyroid gland doesn't produce enough thyroid hormone, leading to fatigue, weight gain, and other symptoms.",
    "hyperthyroidism": "a condition where the thyroid gland produces too much thyroid hormone, accelerating the body's metabolism and causing unintentional weight loss and a rapid or irregular heartbeat.",
    "addison's disease": "a disorder that occurs when the adrenal glands produce too little cortisol and aldosterone, leading to symptoms like fatigue, muscle weakness, and weight loss.",
    "cushing's syndrome": "a condition caused by prolonged exposure to high levels of cortisol, leading to symptoms such as weight gain, thin skin, and high blood pressure.",
    "polycystic ovary syndrome (pcos)": "a hormonal disorder common among women of reproductive age, characterized by irregular menstrual periods, excess hair growth, acne, and obesity.",
    "chronic sinusitis": "a condition where the spaces inside the nose and head (sinuses) are swollen and inflamed for three months or longer, despite treatment.",
    "celiac disease": "an immune reaction to eating gluten, a protein found in wheat, barley, and rye, leading to inflammation that damages the small intestine's lining.",
    "gout": "a form of arthritis characterized by severe pain, redness, and tenderness in joints, caused by an accumulation of urate crystals.",
    "glaucoma": "a group of eye conditions that damage the optic nerve, often due to high pressure in the eye, leading to vision loss.",
    "macular degeneration": "an eye disease that causes vision loss in the center of the field of vision due to the deterioration of the macula.",
    "huntington's disease": "a progressive brain disorder caused by a defective gene, leading to the degeneration of nerve cells in the brain and affecting movement, cognition, and behavior.",
    "amyotrophic lateral sclerosis": "a progressive neurodegenerative disease that affects nerve cells in the brain and the spinal cord, leading to loss of muscle control.",
    "rheumatoid arthritis": "an autoimmune disorder that causes chronic inflammation of joints, leading to pain, swelling, and potential joint deformity.",
    "systemic sclerosis": "an autoimmune disease characterized by hardening and tightening of the skin and connective tissues.",
    "myasthenia gravis": "a chronic autoimmune disorder that causes muscle weakness and fatigue, particularly in the muscles that control the eyes, face, and swallowing.",
    "hemophilia": "a rare disorder in which the blood doesn't clot normally because it lacks sufficient blood-clotting proteins.",
    "scleroderma": "a group of rare diseases that involve the hardening and tightening of the skin and connective tissues.",
    "sarcoidosis": "an inflammatory disease that affects multiple organs in the body, but mostly the lungs and lymph glands, causing small lumps of inflammatory cells.",
    "ankylosing spondylitis": "an inflammatory disease that can cause some of the vertebrae in the spine to fuse, leading to reduced flexibility and a hunched-forward posture.",
    "polymyalgia rheumatica": "an inflammatory disorder causing muscle pain and stiffness, especially in the shoulders and hips.",
    "temporal arteritis": "an inflammation of the blood vessels, often affecting the arteries in the head and causing headaches, jaw pain, and vision problems.",
    "raynaud's disease": "a condition where smaller arteries that supply blood to the skin constrict excessively in response to cold or stress, limiting blood supply to affected areas.",
    "sjogren's syndrome": "an autoimmune disorder characterized by dry eyes and dry mouth due to the body's immune system attacking its own moisture-producing glands.",
    "thyroiditis": "an inflammation of the thyroid gland that can cause either abnormally high or low levels of thyroid hormones in the blood.",
    "interstitial lung disease": "a group of lung disorders that cause progressive scarring of lung tissue, affecting the ability to breathe and get enough oxygen into the bloodstream.",
    "prostatitis": "an inflammation of the prostate gland, often causing painful or difficult urination.",
    "benign prostatic hyperplasia (bph)": "an enlargement of the prostate gland that can cause urinary problems.",
    "endometriosis": "a painful disorder in which tissue similar to the tissue that normally lines the inside of the uterus grows outside the uterus.",
    "pelvic inflammatory disease (pid)": "an infection of the female reproductive organs, often caused by sexually transmitted bacteria.",
    "lyme disease": "an infectious disease caused by bacteria transmitted through tick bites, leading to symptoms like fever, headache, fatigue, and a characteristic skin rash.",
    "chronic hepatitis b": "a long-term viral infection of the liver that can lead to liver damage, cirrhosis, and liver cancer.",
    "chronic hepatitis c": "a viral infection that causes inflammation and damage to the liver, potentially leading to liver failure or liver cancer.",
    "spinal stenosis": "a condition in which the spaces within the spine narrow, putting pressure on the nerves that travel through the spine.",
    "pseudogout": "a type of arthritis caused by the deposition of calcium pyrophosphate dihydrate crystals in the joints, leading to joint pain and inflammation.",
    "bursitis": "an inflammation of the bursae (small sacs of fluid that cushion the bones, tendons, and muscles near the joints), causing pain and swelling.",
    "tendinitis": "an inflammation or irritation of a tendon, causing pain and tenderness just outside a joint.",
    "carpal tunnel syndrome": "a condition caused by pressure on the median nerve as it travels through the wrist, leading to pain, numbness, and weakness in the hand.",
    "tenosynovitis": "an inflammation of the fluid-filled sheath (synovium) that surrounds a tendon, typically leading to joint pain, swelling, and stiffness.",
    "plantar fasciitis": "an inflammation of the thick band of tissue (plantar fascia) that runs across the bottom of the foot and connects the heel bone to the toes, causing heel pain.",
    "meniere's disease": "a disorder of the inner ear causing vertigo, ringing in the ear (tinnitus), hearing loss, and a feeling of fullness in the ear.",
    "cancer": "a group of diseases involving abnormal cell growth with the potential to invade or spread to other parts of the body.",
    "heart attack": "a medical emergency where the blood flow to the heart is suddenly blocked, usually by a blood clot, leading to damage to the heart muscle.",
    "cardiac arrest": "a sudden loss of heart function, breathing, and consciousness, usually due to an electrical disturbance in the heart.",
    "pneumonia": "an infection that inflames the air sacs in one or both lungs, which may fill with fluid or pus, causing cough, fever, and difficulty breathing.",
    "dementia": "a group of symptoms affecting memory, thinking, and social abilities severely enough to interfere with daily functioning.",
    "vision impairment": "a decrease in the ability to see to a significant degree that cannot be corrected with standard glasses, contact lenses, medicine, or surgery.",
    "kidney disease": "a general term for conditions affecting the kidneys, reducing their ability to filter waste from the blood and regulate other body functions.",
    "glioblastoma": "a fast-growing and aggressive type of central nervous system tumor that occurs in the brain or spinal cord."
}



def get_weather_response(user_input):
    api_key = "3fd08ccaff1741cd47f312b378a4a3b6"
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
    a,b,c,d=eval(user_input)
    data=message.generate_reminder_times(a,b,c,d)
    x=''
    for i in data[0]:
        x+=i.ctime()+'\n'
    return x


def get_response(user_input):
    query=user_input.lower()
    sleep(0.2)
    for i in query.split():
        if i in chronic_diseases:
            return chronic_diseases[i]
    
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
    




