import os
from app import create_app, db
from app.models import User, Customer, Note, Role, Permission
from flask_migrate import Migrate, upgrade
from flask_mail import Mail, Message

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
mail = Mail(app)
migrate = Migrate(app, db)

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

