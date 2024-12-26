import os
from app import functions
from app import validation
from app import controllers
from app import app
from flask import Flask, render_template, json, request, jsonify

#Страница со списком мастер-классов
@app.route('/')
def index():
    return controllers.index()

#Форма добавления мастер-класса
@app.route('/master_classes/add_master_class', methods=['GET'])
def showAddMasterClassForm():
    return controllers.showAddMasterClassForm()

#Обработка введенных данных с формы добавления участника
@app.route('/master_classes/add_master_class', methods=['POST'])
def addMasterClass():
    return controllers.addMasterClass()

#Удаление мастер-класса
@app.route('/master_classes/delete/<int:id>', methods=['GET'])
def deleteMasterClass(id):
    return controllers.deleteMasterClass(id)  

#Форма добавления участника
@app.route('/master_classes/<int:id>/add_participant', methods=['GET'])
def showAddParticipantForm(id):
    return controllers.showAddParticipantForm(id)

#Обработка введенных данных с формы добавления участника
@app.route('/master_classes/<int:id>/add_participant', methods=['POST'])
def addParticipant(id):
    return controllers.addParticipant(id)
    
# Получить список участников в формате json
@app.route('/master_classes/<int:id>/get_participants', methods=['GET'])
def showParticipantList(id):
    return controllers.showParticipantList(id)

#Удаление мастер-класса
@app.route('/master_classes/<int:id>/remove_participant/<int:partId>', methods=['GET'])
def deletParticipant(id, partId):
    return controllers.deletParticipant(id, partId)