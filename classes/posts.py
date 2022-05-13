import json

from exceptions import WrongImgType, DataSourceReadError
from logging_exemplar import logger_main


class Posts:
    """
    класс Posts с полями:
    - path - путь json файла, из которого выгружается необходимая информация
    с постами;
    - path_load - путь загрузки файла пользователя.
    Методы: load_posts, get_posts_by_word, save_picture, add_post
    """

    def __init__(self, path, path_load):
        self.path = path
        self.path_load = path_load

    def load_posts(self):
        """
        :return: вложенный список постов
        """
        with open(self.path, encoding='utf-8') as file:
            try:
                data = json.load(file)
            except FileNotFoundError:
                logger_main.exception('Файл не найден')
                raise DataSourceReadError('Файл не найден')
            except json.JSONDecodeError:
                raise json.JSONDecodeError('Ошибка при чтении данных '
                                           'в JSON из файла')
            if type(data) != list:
                raise DataSourceReadError('Данные не список')
            return data 

    def get_posts_by_word(self, word):
        """
        :param word: слово, по которому ведется поиск постов
        :return: список найденных постов, содержащих слово 'word'
        """
        posts_founded = [post for post in self.load_posts() if
                         word.lower() in post["content"].lower()]
        return posts_founded

    def save_picture(self, picture):
        """
        Проверяет допустимость формата загружаемого файла
        :param picture: загружаемый файл пользователя
        :return: путь к сохраненному файлу
        """
        allowed_extentions = ['png', 'jpeg', 'jpg']
        if picture.filename.split('.')[-1] not in allowed_extentions:
            raise WrongImgType(f'Можно загрузить файл формата:'
                               f'{",".join(allowed_extentions)}')
        picture_path = f'{self.path_load}/{picture.filename}'
        picture.save(picture_path)
        return picture_path

    def add_post(self, picture_path, content):
        """
        :param picture_path: путь к сохраненному файлу пользователя
        :param content: текст пользователя к загруженному файлу
        :return: пост из загруженного файла и текста к нему
        """
        post = {'pic': picture_path, 'content': content}
        posts = self.load_posts()
        posts.append(post)
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(posts, file, ensure_ascii=False)
        return post

