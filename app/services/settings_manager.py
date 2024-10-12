import os
from flask import current_app
from app.extensions import db
from app.models.settings import Settings

class SettingsManager:

    @staticmethod
    def settings_exist():
        exists = Settings.query.first() is not None
        return exists
    
    @staticmethod
    def get_all_settings():
        settings = Settings.query.all()
        return {setting.name: setting.value for setting in settings}

    @staticmethod
    def get_setting(name):
        setting = Settings.query.filter_by(name=name).first()
        return setting.value if setting else None
    
    @staticmethod
    def set_setting(name, value):
        setting = Settings.query.filter_by(name=name).first()
        if setting:
            setting.value = value
            db.session.commit()
        else:
            new_setting = Settings(name=name, value=value)
            db.session.add(new_setting)
            db.session.commit()

    @staticmethod
    def delete_setting(name):
        setting = Settings.query.filter_by(name=name).first
        if setting:
            db.session.delete(setting)
            db.session.commit
        else:
            raise ValueError(f"Setting '{name}' does not exist.")
        
    @staticmethod
    def set_defualt_settings():
        default_settings = {
            "base_path": os.path.join(current_app.instance_path, 'model_files'),            
        }
        for name, value in default_settings.items():
            SettingsManager.set_setting(name, value)

