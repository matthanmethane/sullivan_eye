import pyttsx3

class Speaker():
    def __init__(self,gender=True, speed=150):
        self.gender = gender
        self.speed = speed
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', speed)
        self.voices = self.engine.getProperty('voices')
        if (gender): #Male
            self.engine.setProperty('voice',self.voices[0].id)  
        else: #Female
            self.engine.setProperty('voice',self.voices[1].id)

    def set_speed(self,speed):
        self.speed = speed
        self.engine.setProperty('rate', speed)

    def set_gender(self, male_flag):
        if(male_flag):
            self.engine.setProperty('voice', self.voices[0].id )
        else:
            self.engine.setProperty('voice', self.voices[1].id )

    def say(self, text):
        self.engine.say(text)

    def run(self):
        self.engine.runAndWait()

