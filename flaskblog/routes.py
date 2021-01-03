import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt 
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PropertyForm, TenantForm
from flaskblog.models import User, Properties, Tenant, load_property 
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home(): 
    roommates = Tenant.query.all() 
    homes = Properties.query.all() 
    return render_template( 'home.html', homes= homes, roommates=roommates ) 

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated: 
        return redirect( url_for( 'home' )) 
    
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User( username=form.username.data, email=form.email.data, password=hashed_password )
        db.session.add( user ) 
        db.session.commit() # add user to the database 
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect( url_for( 'home' )) 

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by( email = form.email.data ).first() 
        if user and bcrypt.check_password_hash( user.password, form.password.data ): 
            # if user exists and pw is valid 
            login_user( user, remember= form.remember.data )
            # when user clicks link for logged-in users, then logs in, then redirects back to
            # original link they clicked
            next_page = request.args.get('next') 
            return redirect( next_page ) if next_page else redirect( url_for( 'home' )) 
        else: 
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET', 'POST' ] )
def logout():
    logout_user() 
    
    return redirect(url_for('home'))

def save_picture( form_picutre ): 
    random_hex = secrets.token_hex( 8 ) 
    _, f_ext = os.path.splitext( form_picutre.filename ) 
    picture_fn = random_hex + f_ext
    picture_path = os.path.join( app.root_path, 'static/profile_pics', picture_fn )
    output_size = ( 125, 125 ) 
    i = Image.open( form_picutre ) 
    i.thumbnail( output_size ) 
    i.save( picture_path )

    return picture_fn

@app.route("/account", methods=['GET', 'POST'] ) 
@login_required
def account():
    form = UpdateAccountForm() 
    if form.validate_on_submit():

        if form.picutre.data: 
            picture_file = save_picture( form.picutre.data )
            current_user.image_file = picture_file 

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit() # commit this to the database 
        flash( 'Your account has been updated!' ,  'success' ) 
        return redirect( url_for( 'account' )) 
    elif request.method =='GET': 
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for( 'static', filename='profile_pics/' + current_user.image_file )
    return render_template('account.html', title='Account', image_file= image_file, form=form )

@app.route("/property/new", methods= ['GET', 'POST'] )
@login_required
def add_new_property():
    form = PropertyForm()

    if form.validate_on_submit():
        new_house = Properties( address = form.address.data,
                                apartment=form.apartmentNo.data, 
                                zipCode = form.zipCode.data, 
                                author=current_user ) 

        db.session.add( new_house )  
        db.session.commit() # add to database
        flash( 'A new property has been added to your account!' , 'success' ) 
        return redirect( url_for( 'home' ) )
    return render_template( 'create_property.html', title='Add Property', form=form, 
                            legend='New Property')


@app.route("/property/<int:prop_id>")
@login_required
def property_detail( prop_id ):
    home = Properties.query.get_or_404( prop_id )
    roommates = Tenant.query.all() 
    return render_template( 'property_detail.html', title=home.address, home = home, roommates = roommates )

@app.route("/property/<int:prop_id>/update", methods= ['GET', 'POST'])
@login_required
def property_update( prop_id ):
    home = Properties.query.get_or_404( prop_id )
    roommates = Tenant.query.all()
    
    if home.author != current_user:
        abort( 403 )
    
    form = PropertyForm()
    
    if form.validate_on_submit():
        home.address = form.address.data 
        home.zipCode = form.zipCode.data
        home.apartment = form.apartmentNo.data 
        db.session.commit()
        flash("Your property has been updated!", "success")
        return redirect( url_for('property_detail', prop_id=home.property_id))
    
    elif request.method == 'GET': 
        form.address.data = home.address
        form.apartmentNo.data = home.apartment
        form.zipCode.data = home.zipCode
    
    return render_template( 'create_property.html', title='Update Property', form=form, home=home, roommates=roommates, legend="Update Property") 


@app.route("/property/<int:prop_id>/delete", methods= ['POST'])
@login_required
def delete_property( prop_id ):
    
    home = Properties.query.get_or_404( prop_id )
    roommates = Tenant.query.all()
    
    if home.author != current_user:
        abort( 403 )
    
    form = PropertyForm()
    db.session.delete( home )
    db.session.commit() 
    flash("Your property has been deleted!", "success")
    return redirect( url_for( 'home' )) 


@app.route("/tenant/<int:tenant_id>")
@login_required
def tenant_detail( tenant_id ):
    roommate = Tenant.query.get_or_404( tenant_id )
    home = Properties.query.get_or_404( roommate.id ) # get the speciic home id
    return render_template( 'tenant_detail.html', title=home.address, home = home, roommate = roommate )

@app.route("/tenant/<int:tenant_id>/update", methods= ['GET', 'POST'])
@login_required
def tenant_update( tenant_id ):
    roommate = Tenant.query.get_or_404( tenant_id )
    home = Properties.query.get_or_404( roommate.id ) 
    
    if home.author != current_user:
        abort( 403 )
    
    form = TenantForm()
    
    # TODO add move out date to your form AND database  
    if form.validate_on_submit():
        roommate.first_name = form.first_name.data  
        roommate.last_name = form.last_name.data  
        roommate.email = form.email.data  
        roommate.deposit = form.deposit.data 
        roommate.phone_number = form.phone_number.data 

        # get property id info 
        ps = Properties.query.all() 
        assert ps is not None 
        addy = 0

        form_address = str( form.property_address.data ) 
        idx = form_address.find( '=' )
        form_address = form_address[ idx+2 : -3 ]
        idx = form_address.find( "'" )
        
        if idx == ( -1 ): 
            form_address = int( form_address ) 
        else: 
            form_address = int( form_address[ idx+1: ] ) 

        for home in ps: 
            assert home.property_id > 0 
            if home.property_id == form_address: 
                addy = home.property_id
                break
        assert addy > 0 
        roommate.property_address = addy 
        
        # COMMIT HERE 
        db.session.commit()
        flash("This tenant's information has been updated!", "success")
        return redirect( url_for('tenant_detail', tenant_id = roommate.id))
    
    elif request.method == 'GET': 

        form.first_name.data = roommate.first_name
        form.last_name.data = roommate.last_name
        form.email.data = roommate.email
        form.deposit.data = roommate.deposit
        form.phone_number.data = roommate.phone_number
        form.moveIn_date.data = roommate.moveIn_date
        form.moveOut_date.data = roommate.moveOut_date
        form.phone_number.data = roommate.phone_number
        form.property_address.data = home.address 
    
    return render_template( 'create_tenant.html', title='Update Tenant Info', form=form, home=home, roommate=roommate, legend="Update Tenant Info") 

@app.route("/tenant/new", methods= ['GET', 'POST'] )
@login_required
def add_tenant():

    form = TenantForm() 
  
    if form.validate_on_submit(): 
    
        ps = Properties.query.all() 
        assert ps is not None 

        addy = 0

        form_address = str( form.property_address.data ) 
        idx = form_address.find( '=' )
        form_address = form_address[ idx+2 : -3 ]
        idx = form_address.find( "'" )
        
        if idx == ( -1 ): 
            form_address = int( form_address ) 
        else: 
            form_address = int( form_address[ idx+1: ] ) 

        for home in ps: 
            assert home.property_id > 0 
            if home.property_id == form_address: 
                addy = home.property_id
                break
        assert addy > 0 
        # # TODO develop a faster way to find this information!!!! 
        # for home_ids in ps:

        #     assert home_ids.property_id > 0

        #     if home_ids.property_id == form.property_address.data: 
        #         addy = home_ids.property_id
        #         break 

        # assert addy > 0                 
        new_person = Tenant( first_name = form.first_name.data,
                             last_name = form.last_name.data, 
                             email= form.email.data,
                             deposit = form.deposit.data,
                             moveIn_date = form.moveIn_date.data,
                             moveOut_date = form.moveOut_date.data, 
                             phone_number= form.phone_number.data,
                            #  prop_id = addy, 
                            #  property_address = addy, 
                             property_address = addy, 
                             author = current_user
                             )

        db.session.add( new_person ) 
        db.session.commit() 
        flash( 'You have successfully added a new tenant!', 'success' )
        return redirect( url_for( 'home') ) 

    return render_template( 'create_tenant.html', title='Add Tenant', form= form) 



@app.route("/tenant/<int:tenant_id>/delete", methods= ['POST'])
@login_required
def delete_tenant( tenant_id ):
    
    roommate = Tenant.query.get_or_404( tenant_id )
    home = Properties.query.all()

    if home.author != current_user:
        abort( 403 )
    
    form = PropertyForm()
    db.session.delete( roommate )
    db.session.commit() 
    flash("Your tenant has been deleted!", "success")
    return redirect( url_for( 'home' )) 