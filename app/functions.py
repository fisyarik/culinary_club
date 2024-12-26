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
    

