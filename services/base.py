import models
#import models_old


class BaseService:
    def __init__(self, db: models.Db):
        self.db = db

    def get_all(self):
        pass

    def create(self, instance):
        pass
