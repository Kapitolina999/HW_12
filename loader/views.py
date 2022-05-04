from flask import Blueprint, request, render_template, send_from_directory
import logging
from exceptions import *
from classes.posts import Posts


logging.basicConfig(filename='logger.log', level=logging.INFO)

loader_blueprint = Blueprint('loader_blueprint', __name__,
                             template_folder='templates')

POST_PATH = "posts.json"
UPLOAD_FOLDER = "uploads/images"

# Экземпляр класса Posts
posts = Posts(POST_PATH, UPLOAD_FOLDER)


@loader_blueprint.route('/post')
def add_post_page():
    return render_template('post_form.html')


@loader_blueprint.route('/post', methods=['POST'])
def post_page():
    picture = request.files.get("picture")
    content = request.form.get("content")

    if not picture:
        logging.info('Картинки нет')
        return "Загрузи картинку"
    else:
        try:
            path = posts.save_picture(picture)
        except WrongImgType:
            return 'Неверный тип файла'
        return render_template('post_uploaded.html',
                               post=posts.add_post(path, content))

#
# @loader_blueprint.route('/uploads/<path:path>')
# def static_dir(path):
#     return send_from_directory('uploads', path)
#
