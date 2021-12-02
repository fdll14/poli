from flask import render_template, redirect, url_for, request, flash, session
from app import app
import re
import random

R_ABOUT = "Poli adalah asisten virtual yang akan membantu kamu untuk menjawab semua hal yang berhubungan dengan Prodi Teknik Informatika"
R_D4 = "Jenjang diploma 4 memiliki lama waktu perkuliahan yang sama dengan jenjang sarjana yaitu empat tahun atau selama delapan semester"

def unknown():
    response = ["Could you please re-phrase that? ",
                "...",
                "Sounds about right.",
                "What does that mean?"][
        random.randrange(4)]
    return response

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['helo', 'hai', 'hi'], single_response=True)
    response('Pagi juga!', ['pagi', 'selamat pagi'], single_response=True)
    response('Siang juga!', ['siang', 'selamat siang'], single_response=True)
    response('Sore juga!', ['sore', 'selamat sore'], single_response=True)
    response('Malam juga!', ['malam', 'selamat malam'], single_response=True)
    response('Semoga membantu!', ['oke', 'terimakasih','oke','makasih'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('Semester','Prodi TI', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

    # Longer responses
    response(R_ABOUT, ['apa', 'itu', 'poli'], required_words=['apa', 'poli'])
    response(R_D4,['Semester','Prodi TI','berapa'], required_words=['berapa','semester'])
    
    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/bot')
def bot():
    return render_template('bot.html')

@app.route("/get")
def bot_answer():
    userText = request.args.get('msg')
    return get_response(userText)

@app.route('/login')
def login():
    return render_template('login.html')
