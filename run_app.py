from app.views import routes
from ship_framework.dubug import DebugApplication
from ship_framework.fake import FakeApplication
from ship_framework.main import Application

if __name__ == '__main__':
    fronts = []

    # application = Application(routes, fronts)
    application = DebugApplication(routes, fronts)
    # application = FakeApplication(routes, fronts)
