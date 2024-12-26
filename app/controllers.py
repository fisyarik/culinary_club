import os
from app import functions
from app import validation
from app import app
from flask import Flask, render_template, json, request, jsonify

# Функция вывода главной страницы
def index():
    data = functions.getMasterClassList()
    return render_template('index.html', data=data)

# Вывод формы добавления мастер-класса
def showAddMasterClassForm():
    return render_template('add_master_class.html')

# Добавление мастер-класса с валидацией данных
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
    errorData = validation.validateMasterClassData(newMasterClass)
    if not errorData['errors']:
        masterClassData = functions.getMasterClassData()
        # Добавляем новый мастер-класс к списку
        masterClassData['master_classes'].append(newMasterClass)
    
        # Сохранить новый список в файл
        functions.updateMasterClassFile(masterClassData)
    
        return render_template('add_master_class.html', success=True)    
    else:
        return render_template('add_master_class.html', success=False, errorData=errorData, data=newMasterClass)
    
# Удаление мастер-класса
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
    
# Вывод формы добавления участника
def showAddParticipantForm(id):
    masterClass = functions.getMasterClassById(id)
    return render_template('add_participant.html', masterClass = masterClass)

# Добавление участника с валидацией данных
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

    errorData = validation.validateParticipantData(participant)
    if not errorData['errors']:
        # Добавляем новый элемент к списку участников
        masterClass['participants'].append(participant)
    
        # Обновляем в файле данные по текущему мастер-классу
        functions.updateMasterClassInFile(masterClass)
    
        return render_template('add_participant.html', success=True, masterClass = masterClass)
    else:
        return render_template('add_participant.html', success=False, errorData=errorData, data=participant)
    
# Вывод списка участников в формате HTML
def showParticipantList(id):
    masterClass = functions.getMasterClassById(id)
    return render_template('participant_list.html', data=masterClass['participants'], masterClassId=id)

# Удаление участника и вывод обновленного списка в формате HTML
def deletParticipant(id, partId):
    masterClass = functions.getMasterClassById(id)
    for participant in masterClass['participants']:
        if participant['id'] == partId:
            masterClass['participants'].remove(participant)
            break
    
    # Обновляем в файле данные по текущему мастер-классу
    functions.updateMasterClassInFile(masterClass)
    return render_template('participant_list.html', data=masterClass['participants'], masterClassId=id)