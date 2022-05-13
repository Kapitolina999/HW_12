from flask import Blueprint, render_template, request
# from json import JSONDecodeError

from logging_exemplar import logger_main
from classes.posts import Posts


main_blueprint = Blueprint('main_blueprint', __name__,
                           template_folder='templates')

POST_PATH = "posts.json"
UPLOAD_FOLDER = "uploads/images"

posts = Posts(POST_PATH, UPLOAD_FOLDER)


@main_blueprint.route('/')
def index_page():
    logger_main.info('Главная страница открыта')
    return render_template('index.html')


@main_blueprint.route('/search')
def search_page():
    s = request.args.get('s')
    logger_main.info(f'Выполняется поиск "{s}"')
    posts_list = posts.get_posts_by_word(s)
    return render_template('post_list.html', search=s,
                           posts=posts_list, len_=len(posts_list))

