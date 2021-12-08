from flask import render_template, redirect, url_for, request, flash, session
import os
from app import app
import re
import random

R_ABOUT = "Poli adalah asisten virtual yang akan membantu kamu untuk menjawab semua hal yang berhubungan dengan Prodi Teknik Informatika"
R_D4 = "Jenjang Sarjana Terapan memiliki lama waktu perkuliahan yang sama dengan jenjang sarjana yaitu empat tahun atau selama delapan semester"
R_visi = "Menjadi program studi unggul dalam bidang teknik informatika yang mampu beradaptasi terhadap perkembangan teknologi informasi, berjiwa kewirausahaan, berbasis kearifan lokal dan berdaya saing global pada tahun 2035"
def unknown():
    response = ["Maaf poli tidak mengerti tentang pertanyaan kamu.",
                "Bisa tanyakan pertanyaan yang lain ? Poli tidak mengerti"][
        random.randrange(2)]
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
    response('Semoga membantu!', ['oke', 'terimakasih','makasih'], single_response=True)
    response('Slamet Wiyono, S.Pd., M.Eng', ['kepala', 'program studi','siapa','kepala prodi'], single_response=True)
    response('Himpunan Mahasiswa, Himpunan Alumni, Study Club', ['organisasi', 'DIV TI',], single_response=True)
    response('Forum Observasi/Riset, Mobile dan Website, E-Sport, NCT, Plug-in, Smith, Hack me', ['study', 'club', 'studi','club'], single_response=True)
    response('Akreditasi B', ['akreditasi','akreditas','DIV teknik informatika'], single_response=True)
    response('Laboratorium RnD, Laboratorium Komputer D1, Laboratorium Komputer D2,Laboratorium Hardware', ['fasilitas','disediakan','fasilitas prodi'], single_response=True)
    response('Jl. Mataram No.9, Kel. pesurungan lor, Kel. Pesurungan Lor, Pesurungan Lor, Margadana, Kota Tegal, Jawa Tengah', ['alamat','lokasi','politeknik','harapan','bersama'], single_response=True)
    response('jam operasional admin hari senin s.d jumat pukul 08.00-17.00 WIB', ['jam','operasional','admin'], single_response=True)
    response('ruang dosen ada di gedung D lantai 2 politeknik harapan bersama', ['dimana','ruang','dosen'], single_response=True)
    response('ruang lab hardware ada di gedung D lantai 4 politeknik harapan bersama', ['dimana','ruang','laboratorium','lab','hardware'], single_response=True)
    response('ruang lab RnD ada di gedung D lantai 2 politekik harapan bersama', ['dimana','ruang','laboratorium','lab','rnd','r n d'], single_response=True)
    response('ruang kaprodi ada di gedung D lantai 2 politeknik harapan bersama', ['dimana','ruang','kaprodi','kepala prodi'], single_response=True)
    response('Absensi bisa di akses melalui www.syncnau.poltektegal.ac.id', ['bagaimana','absensi','mata kuliah','absen','mk'], single_response=True)
    response('Untuk tutorialnya kamu bisa cek di website kita di www.oase.poltek.ac.id, tentunya kamu harus sudah punya akun yaa!', ['cara','tutorial','bayar','spp','tutor'], single_response=True)

    #semester 1
    response('MUCHAMMAD SOFYAN FIRMANSYAH, S.S, M.A dan Nur Laeli, M.Pd', ['dosen','inggris','english','semester','1','smt 1'], single_response=True)
    response('RATRI WIKANINGTYAS, M.Pd.', ['dosen','bahasa indonesia','semester','1','smt 1'], single_response=True)
    response('Dr. Tuharso, S. Ag, M.PI', ['dosen','agama','islam','semester','1','smt 1'], single_response=True)
    response('Ginanjar Wiro Sasmito, M.Kom.', ['dosen','teknologi','informasi','semester','1','smt 1'], single_response=True)
    response('Dairoh, M.Sc.', ['dosen','kalkulus','semester','1','smt 1'], single_response=True)
    response('Riszki Wijayatun Pratiwi., M.CS.', ['dosen','logika','informatika','semester','1','smt 1'], single_response=True)
    response('Romi Muharyono, S.Ag.', ['dosen','arsitektur','semester','1','smt 1'], single_response=True)
    response('Ary Herijanto, S.Kom, MMSi', ['dosen','algoritma','struktur','data','semester','1','smt 1'], single_response=True)
    response('Dega Surono Wibowo, S.T., M.Kom.', ['dosen','sistem','operasi','semester','1','smt 1'], single_response=True)
    
    #semester 3
    response('M. Nishom, M.Kom.', ['dosen','pemrograman','komputer','pemkom','3','smt 3'], single_response=True)
    response('Dega Surono Wibowo, S.T., M.Kom.', ['dosen','jaringan','komputer','jarkom','semester','3','smt 3'], single_response=True)
    response('Firdaus Nur Sugiharto, S.Tr. Kom.', ['dosen','pemrograman','web','pemweb','3','smt 3'], single_response=True)
    response('Taufiq Abidin, M.Kom.', ['dosen','sistem','basis','data','semester','3','smt 3'], single_response=True)
    response('Dairoh, M.Sc.', ['dosen','matematika','numerik','matnum','3','smt 3'], single_response=True)
    response('Slamet Wiyono, S.Pd., M.Eng', ['dosen','statistika','semester','3','smt 3'], single_response=True)
    response('Dyah Apriliani, S.T., M.Kom.', ['dosen','enterprise','resource','planing','semester','3','smt 3'], single_response=True)
    response('Prasetyo Budi Mulyo, S.Sos.', ['dosen','desain','grafis','multimedia','semester','3','smt 3'], single_response=True)
    
    #semester 5
    response('Rosid Mustofa, M.Kom', ['dosen','mobile','programming','semester','5','smt 5'], single_response=True)
    response('Hendrawan Aprilia A, S.T.', ['dosen','komputasi','cloud','semester','5','smt 5'], single_response=True)
    response('Sharfina Febbi Handayani, M.Kom.', ['dosen','framework','programming','semester','5','smt 5'], single_response=True)
    response('Priyanto Tamami, S.Kom.', ['dosen','data','warehouse','semester','5','smt 5'], single_response=True)
    response('Ardi Susanto, S.Kom., M.Cs.', ['dosen','pengujian','perangkat','lunak','ppl','pengujian','software','semester','5','smt 5'], single_response=True)
    response('M. Fikri Hidayattullah, S.T., M.Kom.', ['dosen','machine','learning','semester','5','smt 5'], single_response=True)
    response('Dwi Intan Af\'idah, M.Kom.', ['dosen','pemrograman','sistem','cerdas','pemsiscer','semester','5','smt 5'], single_response=True)
    response('Hepatika Zidny Ilmadina, S.Pd., M.Kom.', ['dosen','pengolahan','citra','digital','pcd','semester','5','smt 5'], single_response=True)
    response('Taufiq Abidin, M.Kom.', ['dosen','leadership','semester','5','smt 5'], single_response=True)
    
    #semester 7
    response('Riszki Wijayatun Pratiwi., M.CS.', ['dosen','sistem','informasi','management','semester','7','smt 7'], single_response=True)
    response('Riszki Wijayatun Pratiwi., M.CS.', ['dosen','soft skill','semester','7','smt 7'], single_response=True)
    response('Ardi Susanto, S.Kom., M.Cs.', ['dosen','management','proyek','it','semester','7','smt 7'], single_response=True)
    

    # Longer responses
    response(R_ABOUT, ['apa', 'itu', 'poli'], required_words=['apa', 'poli'])
    response(R_D4,['Semester','Prodi TI','berapa'], required_words=['berapa','semester'])
    response(R_visi,['apa visi','program studi teknik informatika'], required_words=['visi','ti','teknik informatika'])
    
    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

@app.route('/bot')
def bot():
    return render_template('bot.html')

@app.route("/get")
def bot_answer():
    userText = request.args.get('msg')
    return get_response(userText)