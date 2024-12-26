import re

# Валидация данных, введенных на форме добавления мастер-класса
def validateMasterClassData(masterClassData):
    errors = []
    invalidFieldsList = []
    pattern = re.compile("^[\w\d\s\:\-\"]+$")
    if not re.match(pattern, masterClassData['title']):
        errors.append({'fieldName': 'title', 'description': 'Некорректно заполнено поле Название'})
        invalidFieldsList.append('title')
    pattern = re.compile("^[\w\d\s\:\-\.]+$")
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
    pattern = re.compile("^[\w\d\s\:\-\"]+$")
    if not re.match(pattern, masterClassData['description']):
        errors.append({'fieldName': 'description', 'description': 'Некорректно заполнено поле Описание'})
        invalidFieldsList.append('description')

    return {'errors': errors, 'invalidFields': invalidFieldsList} 

# Валидация данных, введенных на форме добавления участника
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