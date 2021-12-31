from app.urls import routes
from ship_framework.main import Application

if __name__ == '__main__':
    fronts = []

    application = Application(routes, fronts)
