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
    #pretty_json_str = pprint.pformat(masterClassData, compact=True).replace("'",'"')
    pretty_json_str = json.dumps(masterClassData, sort_keys=True, indent=4, ensure_ascii=False)

    #Запись данных в файл
    with open(json_url, "w", encoding="utf-8") as f:
      #json.dump(masterClassData, f)
      f.write(pretty_json_str)

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
