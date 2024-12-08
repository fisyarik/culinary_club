import os
from app import app
from flask import Flask, render_template, json, request, jsonify

#Обработка главной страницы
@app.route('/')
def index():
  return render_template('index.html')

#Страница со списком мастер-классов
@app.route('/master_classes')
def masterClasses():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "resources", "data.json")
    data = json.load(open(json_url, "r", encoding="utf-8"))
    return render_template('master_classes.html', data=data)

#Форма добавления участника
@app.route('/master_classes/add_participant', methods=['GET'])
def showAddParticipantForm():
    return render_template('add_participant.html')

#Обработка введенных данных с формы добавления участника
@app.route('/master_classes/add_participant', methods=['POST'])
def addParticipant():
    participantName = request.form.get('participant_name', '')
    participantPhone = request.form.get('participant_phone', '')
    data = {'name': participantName, 'phone_number': participantPhone}
    
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    filePath = os.path.join(SITE_ROOT, "resources", "data_test.json")

    #Запись данных в файл
    with open(filePath, "w", encoding="utf-8") as f:
      json.dump(data, f)
    
    return render_template('add_participant.html', success=True)