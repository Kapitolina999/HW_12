import json
from exceptions import *


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
            return json.load(file)

    def get_posts_by_word(self, word):
        """
        :param word: слово, по которому ведется поиск постов
        :return: список найденных постов, содержащих слово 'word'
        """
        posts_founded = []
        for post in self.load_posts():
            if word.lower() in post["content"].lower():
                posts_founded.append(post)
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

