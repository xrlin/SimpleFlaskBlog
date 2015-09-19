from application import db, create_app
from flask.ext.script import Manager, Server, prompt_bool, Shell
from application.models import User, Category, Tag, Article, Comment
from flask_migrate import MigrateCommand

app = create_app()
manager = Manager(app)

@manager.command
def create_all():
    db.create_all()
    db.session.commit()
    for category in app.config['CATEGORIES']:
        Category(category).save()

@manager.command
def drop_all():
    if prompt_bool("Are you sure want to drop all you datas?"):
        db.drop_all()


def make_shell_context():
    return dict(app=app, db=db, User=User, send_mail=send_mail, Category=Category, Tag=Tag, Article=Article, Comment=Comment)

manager.add_command("runserver", Server(host="0.0.0.0", port=5000))
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    from application.utils.mail import send_mail
    manager.run()
