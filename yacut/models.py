from random import choices
import string
from datetime import datetime

from yacut import db


def get_unique_short_id():
    short_link = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
    return short_link


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(6), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def get_unique_short_id(self):
        short_link = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
        setattr(self, 'short', short_link)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.short
        )

    def from_dict(self, data, original_key, short_key):
        setattr(self, 'original', data[original_key])
        if 'custom_id' in data and data[short_key] != '' and data[short_key] is not None:
            setattr(self, 'short', data[short_key])
        else:
            self.get_unique_short_id()

        # # Для каждого поля модели, которое можно заполнить...
        # for field in ['original_link', 'custom_id',]:
        #     # ...выполняется проверка: есть ли ключ с таким же именем в словаре
        #     if field in data:
        #         # Если есть — добавляем значение из словаря
        #         # в соответствующее поле объекта модели:
        #         setattr(self, field, data[field])