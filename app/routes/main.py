import os
from flask import Blueprint, render_template, send_file, redirect, url_for, jsonify, request
from app.services.settings_manager import SettingsManager
from app.services.print_service import PrintService

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    if not SettingsManager.settings_exist():
        return redirect(url_for('settings.settings'))
    
    return render_template('main.html')

@main_blueprint.route('/print/new', methods=['GET', 'POST'])
def new_print():
    if not SettingsManager.settings_exist():
        return redirect(url_for('settings.settings'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        tags = request.form['tags'].split(',')
        files = request.files.getlist('files')
        
        success, message = PrintService.create_new_print(name, description, tags, files)
        
        return jsonify({'success': success, 'message': message})
    
    return render_template('new_print.html')
