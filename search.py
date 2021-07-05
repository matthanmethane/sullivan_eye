

def search(text, word, speaker):
    sentence_list = text.split('.')
    for sentence in range(len(sentence_list)):
        if(word in sentence):
            speaker.say(sentence)
        speaker.say("If you want to listen to next result, press N. If you want to listen further, press R. Otherwise, press q to return to main menu")
