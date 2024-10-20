from app.models.print import Print
from app.models.print_file import PrintFile
from app.models.tag import Tag
from app.extensions import db
from app.services.settings_manager import SettingsManager
import os

class PrintService:
    @staticmethod
    def create_new_print(name, description, tags, files):
        try:
            new_print = Print(name=name, description=description)
            
            for tag_name in tags:
                tag = Tag.query.filter_by(name=tag_name.strip()).first()
                if not tag:
                    tag = Tag(name=tag_name.strip())
                new_print.tags.append(tag)

            db.session.add(new_print)
            db.session.flush()  # This assigns an ID to new_print
            
            for file in files:
                if file:
                    PrintService.save_print_file(new_print, file, commit=False)
            
            db.session.commit()
            return True, "Print created successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def save_print_file(print_obj, file, commit=True):
        try:
            filename = file.filename
            base_path = SettingsManager.get_setting('base_path')
            dir_path = os.path.join(base_path, f'{print_obj.name}')
            file_path = os.path.join(dir_path, filename)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            file.save(file_path)
            file_size = os.path.getsize(file_path)
            file_type = file.content_type
            
            new_file = PrintFile(
                print_id=print_obj.id,
                name=filename,
                size=file_size,
                file_name=filename,
                file_path=file_path,
                file_type=file_type
            )
            db.session.add(new_file)
            
            # Only commit if specified
            if commit:
                db.session.commit

        except Exception as e:
            db.session.rollback()
            return False, str(e)        
        return True, "File saved successfully"
        
