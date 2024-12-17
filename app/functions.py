import json, os, pprint, re

# Определяем максимальное значение поля id по всем записям мастер-классов в файле data.json
def getLastMasterClassId():
    data = getMasterClassList()
    maxId = 0
    for masterClass in data:
        currentId = masterClass['id']
        if currentId > maxId:
            maxId = currentId
    
    return maxId

# Определяем максимальное значение поля id по всем участникам мастер-класса
def getLastMasterClassParticipantId(masterClass):
    maxId = 0
    for participant in masterClass['participants']:
        currentId = participant['id']
        if currentId > maxId:
            maxId = currentId
    
    return maxId

# Получить список мастер-классов из файла
def getMasterClassById(id):
    data = getMasterClassList()
    maxId = 0
    for masterClass in data:
        currentId = masterClass['id']
        if currentId == id:
            return masterClass
    
    return None

# Получить список мастер-классов из файла
def getMasterClassList():
    data = getMasterClassData()
    return data['master_classes']

# Получить данные из файла мастер-классов
def getMasterClassData():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "resources", "data.json")
    return json.load(open(json_url, "r", encoding="utf-8"))

# Получить список мастер-классов из файла
def updateMasterClassFile(masterClassData):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "resources", "data.json")

    # write json to file with human-friendly formatting
    pretty_json_str = json.dumps(masterClassData, sort_keys=True, indent=4, ensure_ascii=False)

    #Запись данных в файл
    with open(json_url, "w", encoding="utf-8") as f:
      #json.dump(masterClassData, f)
      f.write(pretty_json_str)

def updateMasterClassInFile(masterClass):
    masterClassData = getMasterClassData()
    newMasterClassData = {'master_classes': []}
    # Проходим по всем мастер-классам в файле
    for existedMasterClass in masterClassData['master_classes']:
        currentId = existedMasterClass['id']
        # Обновляем данные выбранного мастер класса
        if currentId == masterClass['id']:
            newMasterClassData['master_classes'].append(masterClass)
        else:
            newMasterClassData['master_classes'].append(existedMasterClass)
    
    # Переписываем данные в файле
    updateMasterClassFile(newMasterClassData)
    

def validateMasterClassData(masterClassData):
    errors = []
    invalidFieldsList = []
    pattern = re.compile("^[\w\d\s\:\-]+$")
    if not re.match(pattern, masterClassData['title']):
        errors.append({'fieldName': 'title', 'description': 'Некорректно заполнено поле Название'})
        invalidFieldsList.append('title')
    pattern = re.compile("^[\w\d\s\:\-]+$")
    if not re.match(pattern, masterClassData['date_time']):
        errors.append({'fieldName': 'date_time', 'description': 'Некорректно заполнено поле Дата проведения'})
        invalidFieldsList.append('date_time')
    pattern = re.compile("^([0-9])+$")
    if not re.match(pattern, masterClassData['duration']):
        errors.append({'fieldName': 'duration', 'description': 'Некорректно заполнено поле Длительность'})
        invalidFieldsList.append('duration')
    pattern = re.compile("^([0-9])+$")
    if not re.match(pattern, masterClassData['places']):
        errors.append({'fieldName': 'places', 'description': 'Некорректно заполнено поле Количество мест'})
        invalidFieldsList.append('places')
    pattern = re.compile("^[\w\d\s\:\-]+$")
    if not re.match(pattern, masterClassData['description']):
        errors.append({'fieldName': 'description', 'description': 'Некорректно заполнено поле Описание'})
        invalidFieldsList.append('description')

    return {'errors': errors, 'invalidFields': invalidFieldsList} 

def validateParticipantData(participantData):
    errors = []
    invalidFieldsList = []
    pattern = re.compile("^.+$")
    if not re.match(pattern, participantData['name']):
        errors.append({'fieldName': 'participant_name', 'description': 'Некорректно заполнено Имя'})
        invalidFieldsList.append('participant_name')
    pattern = re.compile("^(\+7|8)\s\([0-9]{3}\)\s[0-9]{3}\-[0-9]{2}\-[0-9]{2}$")
    if not re.match(pattern, participantData['phone_number']):
        errors.append({'fieldName': 'phone_number', 'description': 'Некорректно заполнено поле Телефон'})
        invalidFieldsList.append('phone_number')
    
    return {'errors': errors, 'invalidFields': invalidFieldsList} 