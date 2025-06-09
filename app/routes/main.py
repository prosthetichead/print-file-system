import os
from flask import Blueprint, render_template, send_file, redirect, url_for, jsonify, request, flash
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
    
    form_data = {}
    if request.method == 'POST':
        name = request.form['name']
        creator = request.form['creator']
        description = request.form['description']
        tags = request.form['tags'].split(',')
        files = request.files.getlist('files')

        success, message = PrintService.create_new_print(name, creator, description, tags, files)        
        success = False
        if success:
            flash('Print added successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash(f'Error adding print: {message}', 'danger')
            form_data = {
                'name': name,
                'description': description,
                'tags': tags
            }
    
    return render_template('new_print.html', form_data=form_data)


@main_blueprint.route('/api/prints', methods=['GET'])
def api_get_prints():
    '''
    api endpoint to get all print records
    returns: json response with all print records or error message if no prints found

    params: 
    page (int): page number for pagination, default is 1per_page (int): number of items per page, default is 10
    order_by (str): field to order by, default is 'name'
    order (str): order direction, 'asc' or 'desc', default is 'asc'
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    order_by = request.args.get('order_by', 'name')
    order = request.args.get('order', 'asc')
    search = request.args.get('search', None)
    tags = request.args.get('tags', None)
    if tags:
        tags = tags.split(',')
        tags = [tag.strip() for tag in tags]
        
    prints = PrintService.get_prints(search=search, tags=tags, order_by=order_by, order=order, page=page, per_page=per_page)
    if prints:
        return jsonify(prints)
    else:
        return jsonify({'error': 'An error occurred while fetching prints'}), 500
    

# API Endpoints
@main_blueprint.route('/api/print/<int:print_id>', methods=['GET'])
def api_get_print(print_id):
    '''
    api endpoint to get print data for a specific print record
    args: print_id (int): the id of the print record
    returns: json response with print data or error message if print not found
    '''    
    print_data = PrintService.get_print_data(print_id)
    if(print_data):
        return jsonify(print_data)
    else:
        return jsonify({'error': 'Print not found'}), 404
    


