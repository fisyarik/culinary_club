import os
from app import functions
from app import app
from flask import Flask, render_template, json, request, jsonify

#Страница со списком мастер-классов
@app.route('/')
def index():
    data = functions.getMasterClassList()
    return render_template('index.html', data=data)

#Форма добавления мастер-класса
@app.route('/master_classes/add_master_class', methods=['GET'])
def showAddMasterClassForm():
    return render_template('add_master_class.html')

#Обработка введенных данных с формы добавления участника
@app.route('/master_classes/add_master_class', methods=['POST'])
def addMasterClass():
    # Считываем данные, введенные на форме ввода
    title = request.form.get('title', '')
    description = request.form.get('description', '')
    dateTime = request.form.get('date_time', '')
    duration = request.form.get('duration', '')
    places = request.form.get('places', '')

    # Определяем максимальное значение id для всех мастер-классов
    maxId = functions.getLastMasterClassId()
    newMasterClass = {
       'title': title, 
       'description': description,
       'duration': duration,
       'date_time': dateTime,
       'places': places,
       'participants': [],
       'id': maxId + 1 # устанавливаем значение нового идентификатора
    }
    errorData = functions.validateMasterClassData(newMasterClass)
    if not errorData['errors']:
        masterClassData = functions.getMasterClassData()
        # Добавляем новый мастер-класс к списку
        masterClassData['master_classes'].append(newMasterClass)
    
        # Сохранить новый список в файл
        functions.updateMasterClassFile(masterClassData)
    
        return render_template('add_master_class.html', success=True)    
    else:
        return render_template('add_master_class.html', success=False, errorData=errorData, data=newMasterClass)

#Удаление мастер-класса
@app.route('/master_classes/delete/<int:id>', methods=['GET'])
def deleteMasterClass(id):
    masterClassData = functions.getMasterClassData()
    deletedMasterClass = None
    for masterClass in masterClassData['master_classes']:
        if masterClass['id'] == id:
            deletedMasterClass = masterClass
            masterClassData['master_classes'].remove(masterClass)
    
    if deletedMasterClass != None:
        # Сохранить новый список в файл
        functions.updateMasterClassFile(masterClassData)
        return render_template('delete_master_class.html', success=True, data=deletedMasterClass)
    else:
        return render_template('delete_master_class.html', success=False)   


#Форма добавления участника
@app.route('/master_classes/<int:id>/add_participant', methods=['GET'])
def showAddParticipantForm(id):
    masterClass = functions.getMasterClassById(id)
    return render_template('add_participant.html', masterClass = masterClass)

#Обработка введенных данных с формы добавления участника
@app.route('/master_classes/<int:id>/add_participant', methods=['POST'])
def addParticipant(id):
    masterClass = functions.getMasterClassById(id)
    participantName = request.form.get('participant_name', '')
    participantPhone = request.form.get('participant_phone', '')
    
    # Определяем максимальное значение id для всех участников выбранного мастер-класса
    maxId = functions.getLastMasterClassParticipantId(masterClass)
    participant = {
        'name': participantName, 
        'phone_number': participantPhone,
        'id': maxId + 1 # устанавливаем значение нового идентификатора
    }

    errorData = functions.validateParticipantData(participant)
    if not errorData['errors']:
        # Добавляем новый элемент к списку участников
        masterClass['participants'].append(participant)
    
        # Обновляем в файле данные по текущему мастер-классу
        functions.updateMasterClassInFile(masterClass)
    
        return render_template('add_participant.html', success=True, masterClass = masterClass)
    else:
        return render_template('add_participant.html', success=False, errorData=errorData, data=participant)
    
# Получить список участников в формате json
@app.route('/master_classes/<int:id>/get_participants', methods=['GET'])
def showParticipantList(id):
    masterClass = functions.getMasterClassById(id)
    return jsonify(masterClass['participants'])