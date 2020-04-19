from flask_script import Manager
from flask_migrate import MigrateCommand
from models import CovidWiki
from appvars import app

app.config.from_object("config.Config")

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def update_covid_data():
    """
    Update COVID-19 data
    """
    CovidWiki().update_data()


if __name__ == '__main__':
    manager.run()
