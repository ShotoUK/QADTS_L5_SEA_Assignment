from flask import Flask, request, redirect, abort, render_template
from flask_login import login_required,current_user
from app.main.forms import LoginForm, CreateUserForm, CreateCustomerForm \
    , CreateRoleForm, CreateNoteForm, EditUserForm
from .. import db
from app.models import User, Customer, Permission, Role, Note
from . import main
from app.decorators import permission_required, admin_required
import logging
from app.email import send_email

@main.route('/', methods=['GET','POST'])
@login_required
@permission_required(Permission.VIEW)
def index():
    logging.info('Rendering index page')

    # get all customers from the database, and pass them to the template
    customers = Customer.query.all()

    logging.info('Index page rendered')

    return render_template('index.html', customers=customers)

@main.route('/customer/<int:id>', methods=['GET','POST'])
@login_required
@permission_required(Permission.VIEW)
def customerdetail(id):
    # get the customer from the database using the id, and pass it to the template
    # if form submitted, save the note to the database
    form = CreateNoteForm()
    if request.method == 'POST':
        try:
            if form.validate_on_submit():

                logging.info('Creating new note for customer with id: {}'.format(id))

                newNote = Note()
                newNote.CustomerId = id
                newNote.Note = form.note.data
                db.session.add(newNote)
                db.session.commit()

                logging.info('Note created')

                return redirect('/customer/{}'.format(id))
        except:

            logging.error('Issue saving note to database')

            return render_template('error.html',message='There was an issue saving note to database')
        
    customer = db.session.query(Customer).filter_by(CustomerId=id).order_by(Customer.DateCreated.desc()).all()
    customerNotes = Note.query.filter_by(CustomerId=id).order_by(Note.DateCreated.desc()).all()
    return render_template('customer.html', customer=customer, current_user=current_user, form=form , customerNotes=customerNotes)
  
@main.route('/user/create', methods=['GET','POST'])
@login_required
@admin_required
def create_user():
    form = CreateUserForm()
    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                logging.info('Creating new user')

                newUser = User()
                
                # Generate password hash
                newUser.password = form.password.data

                # Set email and password
                newUser.Email = form.email.data
                newUser.FirstName = form.firstname.data
                newUser.LastName = form.lastname.data
                newUser.Role = form.role.data

                # Add to database
                db.session.add(newUser)
                db.session.commit()

                logging.info('User created')

            return render_template('usercreated.html')
        except:

            logging.error('Issue saving user to database')
            return render_template('error.html',message='There was an issue saving user to database')     
    else:

        logging.info('Request is not POST method, Rendering create user form')
        return render_template('createuser.html',form=form)
    
@main.route('/user/edit/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def edit_user(id):
    logging.info('Editing user with id: {}'.format(id))

    user = User.query.get_or_404(id)
    form = EditUserForm()
    form.email.data = user.Email
    form.firstname.data = user.FirstName
    form.lastname.data = user.LastName
    form.role.data = str(user.Role)
    form.password.label.text = 'New Password'

    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                logging.info('Updating user with id: {}'.format(id))

                user.Email = request.form['email']
                user.FirstName = request.form['firstname']
                user.LastName = request.form['lastname']
                user.Role = request.form['role']
                db.session.add(user)
                db.session.commit()

                logging.info('User updated')

            return redirect('/users/')
        except:

            logging.error('Issue saving update user data to database')
            return render_template('error.html',message= 'There was an issue saving user to database')
    else:

        logging.info('Request is not POST method, Rendering edit user form')
        return render_template('edituser.html', form=form, id=id)
    
@main.route('/user/changepassword/<int:id>', methods=['POST'])
@login_required
@admin_required
def change_user_password(id):
    try:
        logging.info('Changing user password with id: {}'.format(id))

        user = User.query.get_or_404(id)
        user.password = request.form['password']
        db.session.add(user)
        db.session.commit()

        logging.info('User passwor changed')

        return redirect('/users/')
    
    except:

        logging.error('Issue changing user password in database')
        return render_template('error.html',message= 'There was an issue changing user password in the database')
    
@main.route('/users/delete/<int:id>', methods=['GET'])
@login_required
@admin_required
def delete_user(id):
    try:
        logging.info('Deleting user with id: {}'.format(id))

        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()

        logging.info('User deleted')

        return redirect('/users/')
    
    except:

        logging.error('Issue deleting user from database')
        return render_template('error.html',message= 'There was an issue deleting user from database')
    
@main.route('/users/', methods=['GET'])
@login_required
@admin_required
def view_users():
    try:
        logging.info('Rendering users page')

        users = User.query.all()

        logging.info('Users page rendered')
        return render_template('users.html', users=users)
    
    except:

        logging.error('Issue rendering users page')
        return render_template('error.html',message= 'There was an issue rendering users page')
    
@main.route('/customer/create', methods=['GET','POST'])
@login_required
@permission_required(Permission.VIEW)
def create_customer():
    form = CreateCustomerForm()

    if request.method == 'POST':
        try:
            
            if form.validate_on_submit():

                logging.info('Creating new customer')

                newCustomer = Customer()
                newCustomer.Name = form.name.data
                newCustomer.ProductId = form.product.data
                newCustomer.Description = form.description.data
                newCustomer.Status = form.status.data
                newCustomer.ContactName = form.contactname.data
                newCustomer.ContactEmail = form.contactemail.data
                newCustomer.ContactPhone = form.contactphone.data
                newCustomer.AgentId = form.agent.data
                db.session.add(newCustomer)
                db.session.commit()

                logging.info('Customer created')

            return redirect('/')
        
        except:

            logging.error('Issue saving customer to database')
            return render_template('error.html',message= 'There was an issue saving customer to database')
    else:

        logging.info('Request is not POST method, Rendering create customer form')
        return render_template('createcustomer.html', form=form)
    
@main.route('/customer/edit/<int:id>', methods=['GET','POST'])
@login_required
@permission_required(Permission.VIEW)
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    form = CreateCustomerForm()
    form.name.data = customer.Name
    form.product.data = str(customer.ProductId)
    form.description.data = customer.Description
    form.status.data = customer.Status
    form.contactname.data = customer.ContactName
    form.contactemail.data = customer.ContactEmail
    form.contactphone.data = customer.ContactPhone
    form.agent.data = str(customer.AgentId)

    if request.method == 'POST':
        try:
            if form.validate_on_submit():

                logging.info('Updating customer with id: {}'.format(id))

                customer.Name = request.form['name']
                customer.ProductId = request.form['product']
                customer.Description = request.form['description']
                customer.Status = request.form['status']
                customer.ContactName = request.form['contactname']
                customer.ContactEmail = request.form['contactemail']
                customer.ContactPhone = request.form['contactphone']
                customer.AgentId = request.form['agent']
                

                db.session.add(customer)
                db.session.commit()

                logging.info('Customer updated')

            return redirect('/customer/{}'.format(id))
        
        except:

            logging.error('Issue saving customer to database')
            return render_template('error.html',message= 'There was an issue saving customer to database')
    else:

        logging.info('Request is not POST method, Rendering edit customer form')
        return render_template('editcustomer.html', form=form, id=id)
    
@main.route('/customer/note/delete/<int:id>', methods=['GET'])
@login_required
@admin_required
def view_notes():
    try:
        logging.info('Rendering notes page')

        notes = Note.query.all()

        logging.info('Notes page rendered')
        return render_template('notes.html', notes=notes)
    
    except:

        logging.error('Issue rendering notes page')
        return render_template('error.html',message= 'There was an issue rendering notes page')
    
@main.route('/customer/note/delete/<int:id>', methods=['GET'])
@login_required
@admin_required
def delete_note(id):

    try:
        logging.info('Deleting note with id: {}'.format(id))

        note = Note.query.get_or_404(id)
        db.session.delete(note)
        db.session.commit()

        logging.info('Note deleted')

        return redirect('/customer/{}'.format(note.CustomerId))
    
    except:

        logging.error('Issue deleting note from database')
        return render_template('error.html',message= 'There was an issue deleting note from database')
    
@main.route('/customer/delete/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def delete_customer(id):

    try:

        logging.info('Deleting customer with id: {}'.format(id))
    
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()

        logging.info('Customer deleted')

    except:

        logging.error('Issue deleting customer from database')
        return render_template('error.html',message= 'There was an issue deleting customer from database')

    return redirect('/')

    
@main.route('/security/roles/', methods=['GET'])
@login_required
@admin_required
def view_roles():

    try:

        logging.info('Rendering roles page')
        roles = Role.query.all()
        logging.info('Roles loaded from database')

        return render_template('roles.html', roles=roles)
    
    except:

        logging.error('Issue rendering roles page')
        return render_template('error.html',message= 'There was an issue rendering roles page')

@main.route('/security/roles/create', methods=['GET','POST'])
@login_required
@admin_required
def create_roles():
    form = CreateRoleForm()
    roles = Role.query.all()
    if request.method == 'POST':
        try:
            if form.validate_on_submit():

                logging.info('Creating new role')

                newRole = Role()
                newRole.Name = form.name.data

                permissionValue = 0

                for permission in form.permissions.data:
                    permissionValue += int(permission)

                newRole.Permissions = permissionValue             
                db.session.add(newRole)
                db.session.commit()

                logging.info('Role created')

            return render_template('rolecreated.html')
        
        except:

            logging.error('Issue saving role to database')
            return render_template('error.html',message= 'There was an issue saving role to database')
    else:

        logging.info('Request is not POST method, Rendering create role form')
        return render_template('createrole.html', form=form ,roles=roles)