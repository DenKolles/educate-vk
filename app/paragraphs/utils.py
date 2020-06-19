import os
from flask import current_app


def save_file(form_file):
    file_path = os.path.join(current_app.root_path, 'static/prediction_images', form_file.filename)
    form_file.write(file_path)
    form_file.close()
    return form_file.filename
