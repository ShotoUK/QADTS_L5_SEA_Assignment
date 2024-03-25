import os
from app import create_app, db
from app.models import User, Customer, Note, Role, Permission
from flask_migrate import Migrate, upgrade
from flask_mail import Mail, Message
import sys
import click
import coverage

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
mail = Mail(app)
migrate = Migrate(app, db)

# Code coverage
COV = None
if os.environ.get('FLASK_COVERAGE'): 
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Customer=Customer, Note=Note, Role=Role, Permission=Permission)

@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def deploy():
    # upgrade()
    db.create_all()
    Role.insert_roles()
    Customer.insert_customers()
    User.insert_adminuser()

@app.cli.command()
def send_email():
    msg = Message('Test Email',
                    sender=app.config['FLASKY_MAIL_SENDER'], recipients=['']
                    )
    msg.body = 'Test Body'
    msg.html = '<b>Test Body</b>'
    mail.send(msg)

# @app.cli.command()
# @click.option('--coverage/--no-coverage', default=False, help='Run tests under code coverage.')
# def test(coverage):
#     """Run the unit tests."""
#     if coverage and not os.environ.get('FLASK_COVERAGE'):
#         os.environ['FLASK_COVERAGE'] = '1'
#         os.execvp(sys.executable, [sys.executable] + sys.argv)
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)
#     if COV:
#         COV.stop()
#         COV.save()
#         print('Coverage Summary:')
#         COV.report()
#         basedir = os.path.abspath(os.path.dirname(__file__))
#         covdir = os.path.join(basedir, 'tmp/coverage')
#         COV.html_report(directory=covdir)
#         print('HTML version: file://%s/index.html' % covdir)
#         COV.erase()

    



