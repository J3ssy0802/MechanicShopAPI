class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:poop2025@localhost/mechanic_shop_db'
    DEBUG = True
    
class TestingConfig:
    pass

class ProductionConfig:
    pass