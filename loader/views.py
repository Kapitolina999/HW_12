from flask import Blueprint, request, render_template, send_from_directory

from logging_exemplar import logger_main
from exceptions import WrongImgType
from classes.posts import Posts


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
        logger_main.info('Не загрузили картинку')
        return "Загрузи картинку"

    try:
        path = posts.save_picture(picture)
    except WrongImgType:
        logger_main.exception('Загрузили не картинку')
        return 'Неверный тип файла'
    return render_template('post_uploaded.html',
                            post=posts.add_post(path, content))


@loader_blueprint.route('/uploads/<path:path>')
def static_dir(path):
    return send_from_directory('uploads', path)

