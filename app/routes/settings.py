from flask import Blueprint, render_template, jsonify, request
from app.services.settings_manager import SettingsManager

settings_blueprint = Blueprint('settings', __name__)

@settings_blueprint.route('/settings')
def settings():
    #get all settings 
    settings = SettingsManager.get_all_settings()
    if(len(settings) == 0):
        #if no settings found, create default settings
        SettingsManager.set_defualt_settings()
        settings = SettingsManager.get_all_settings()

    return render_template('settings.html', settings=settings)

@settings_blueprint.route('/settings/update', methods=['POST'])
def update_settings():
    try:
        data = request.json
        for key, value in data.items():
            SettingsManager.set_setting(key, value)
        return jsonify({"success": True, "message": "Settings updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400