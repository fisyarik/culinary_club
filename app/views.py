import os
from app import functions
from app import app
from flask import Flask, render_template, json, request, jsonify

#Обработка главной страницы
@app.route('/')
def index():
  return render_template('index.html')

#Страница со списком мастер-классов
@app.route('/master_classes')
def masterClasses():
    data = functions.getMasterClassList()
    return render_template('master_classes.html', data=data)

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
    participantName = request.form.get('participant_name', '')
    participantPhone = request.form.get('participant_phone', '')
    data = {'name': participantName, 'phone_number': participantPhone}
    
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    filePath = os.path.join(SITE_ROOT, "resources", "data_test.json")

    #Запись данных в файл
    with open(filePath, "w", encoding="utf-8") as f:
      json.dump(data, f)
    
    return render_template('add_participant.html', success=True)