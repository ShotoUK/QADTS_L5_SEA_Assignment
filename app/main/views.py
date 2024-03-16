from flask import Flask, request, redirect, abort, render_template
from flask_login import login_required,current_user
from app.main.forms import NameForm, LoginForm, CreateUserForm, CreateCustomerForm \
    , CreateRoleForm, CreateNoteForm
from .. import db
from app.models import User, Customer, Permission, Role, Note
from . import main
from app.decorators import permission_required, admin_required

@main.route('/', methods=['GET','POST'])
@login_required
@permission_required(Permission.VIEW)
def index():
    customers = Customer.query.all()
    form = NameForm()

    return render_template('index.html', form=form, customers=customers)

@main.route('/customer/<int:id>', methods=['GET','POST'])
@login_required
@permission_required(Permission.VIEW)
def customerdetail(id):
    form = CreateNoteForm()
    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                newNote = Note()
                newNote.CustomerId = id
                newNote.Note = form.note.data
                db.session.add(newNote)
                db.session.commit()

                return redirect('/customer/{}'.format(id))
        except:
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
            return render_template('usercreated.html')
        except:
            return render_template('error.html',message='There was an issue saving user to database')
    else:
        return render_template('createuser.html',form=form)
    
@main.route('/user/edit/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = CreateUserForm()
    form.email.data = user.Email
    form.firstname.data = user.FirstName
    form.lastname.data = user.LastName
    form.role.data = str(user.Role)

    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                user.Email = request.form['email']
                user.FirstName = request.form['firstname']
                user.LastName = request.form['lastname']
                user.Role = request.form['role']
                db.session.add(user)
                db.session.commit()
            return redirect('/users/')
        except:
            return render_template('error.html',message= 'There was an issue saving user to database')
    else:
        return render_template('edituser.html', form=form, id=id)
    
@main.route('/user/delete/<int:id>', methods=['GET'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users/')
    
@main.route('/users/', methods=['GET'])
@login_required
@admin_required
def view_users():
    users = User.query.all()
    return render_template('users.html', users=users)
    
@main.route('/customer/create', methods=['GET','POST'])
@login_required
@permission_required(Permission.VIEW)
def create_customer():
    form = CreateCustomerForm()

    if request.method == 'POST':
        try:
            
            if form.validate_on_submit():
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

            return redirect('/')
        except:
            return render_template('error.html',message= 'There was an issue saving customer to database')
    else:
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
            return redirect('/customer/{}'.format(id))
        except:
            return render_template('error.html',message= 'There was an issue saving customer to database')
    else:
        return render_template('editcustomer.html', form=form, id=id)
    
@main.route('/customer/note/delete/<int:id>', methods=['GET'])
@login_required
@admin_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect('/customer/{}'.format(note.CustomerId))
    
@main.route('/customer/delete/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return redirect('/')

    
@main.route('/security/roles/', methods=['GET'])
@login_required
@admin_required
def view_roles():
    roles = Role.query.all()

    return render_template('roles.html', roles=roles)

@main.route('/security/roles/create', methods=['GET','POST'])
@login_required
@admin_required
def create_roles():
    form = CreateRoleForm()
    roles = Role.query.all()
    if request.method == 'POST':
        try:
            if form.validate_on_submit():
                newRole = Role()
                newRole.Name = form.name.data

                permissionValue = 0

                for permission in form.permissions.data:
                    permissionValue += int(permission)

                newRole.Permissions = permissionValue             
                db.session.add(newRole)
                db.session.commit()
            return render_template('rolecreated.html')
        except:
            return render_template('error.html',message= 'There was an issue saving role to database')
    else:
        return render_template('createrole.html', form=form ,roles=roles)