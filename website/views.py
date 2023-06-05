import os
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from flask import Blueprint, render_template, request, current_app, flash, send_file, redirect, session, url_for, \
    jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from website.airtime_statistics import get_montly_sales, get_buddie_sold, get_buddie_available, \
    get_available_value_counts, get_available_denominations
from website.api import get_wallet_balance, voice_recharge, get_airtime_bundles, bundle_recharge, \
    get_wallet_balance_usd, get_airtime_bundles_usd
from website.models import User
from website.utils import upload_file, generate_pdf

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        selected_currency = session.get('selectedOption', 'ZWL')
        return render_template("general/home.html", user=current_user, selected_currency=selected_currency)
    else:
        # m_sales = get_montly_sales()
        wallet_balance = float(get_wallet_balance())
        sold, total = get_buddie_sold(), get_buddie_available() + get_buddie_sold()
        sold_percentage = round(((sold / total) * 100), 0)

        user_data = User.query.filter_by(id=current_user.id).first()
        img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'
        selected_currency = session.get('selectedOption', 'ZWL')
        return render_template("general/home.html", user=current_user, sold=sold, total_buddie_sold=total,
                               sold_percentage=sold_percentage, wallet_balance=wallet_balance, img_path=img_path,
                               selected_currency=selected_currency)


@views.route('/upload-text-file', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == "POST":
        # file_path = request.files['fileUpload']
        f = request.files['uploadedFile']

        path_to_file = os.path.join(current_app.instance_path, 'text_file_uploads', secure_filename(f.filename))

        if len(f.filename) == 0:
            flash("Please upload a file to continue.", category="error")
            selected_currency = session.get('selectedOption', 'ZWL')
            return render_template("general/upload-text-file.html", selected_currency=selected_currency,
                                   user=current_user)
        else:
            if os.path.exists(path_to_file):
                flash("Can't upload textfile, similar data already exists", category="error")
                selected_currency = session.get('selectedOption', 'ZWL')
                return render_template("general/upload-text-file.html", selected_currency=selected_currency,
                                       user=current_user)
            else:
                f.save(os.path.join(current_app.instance_path, 'text_file_uploads', secure_filename(f.filename)))
                path = os.path.join(current_app.instance_path, 'text_file_uploads', secure_filename(f.filename))
                upload_file(file=path)
                selected_currency = session.get('selectedOption', 'ZWL')
                return render_template("general/upload-text-file.html", selected_currency=selected_currency,
                                       user=current_user)
    else:
        user_data = User.query.filter_by(id=current_user.id).first()
        img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'
        selected_currency = session.get('selectedOption', 'ZWL')
        return render_template("general/upload-text-file.html", user=current_user, img_path=img_path,
                               selected_currency=selected_currency)


@views.route('/download-airtime', methods=['GET', 'POST'])
@login_required
def download():
    if request.method == "POST":
        try:
            if request.form.get('available'):
                number = request.form.get("print_number")
                selected_option = request.form.get('download_type')

                denomination = request.form.get("denomination")

                denominations = get_available_denominations()

                dt = datetime.now().strftime('%d_%b_%y')
                file_name = "airtime_printout_" + str(dt)

                if number != "":
                    if selected_option == "fpdf":
                        generate_pdf(file_name, number=int(number), denomination=float(denomination), file="fpdf")
                        download_file = (os.path.join(current_app.instance_path, 'file_downloads',
                                                      secure_filename(file_name)) + '.pdf')
                        return send_file(download_file,
                                         mimetype='text/csv',
                                         download_name=file_name + ".pdf")
                        user_data = User.query.filter_by(id=current_user.id).first()
                        img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'
                        selected_currency = session.get('selectedOption', 'ZWL')
                        return render_template("general/print-airtime.html", user=current_user,
                                               denominations=denominations, img_path=img_path,
                                               selected_currency=selected_currency)

                    if selected_option == "csv":
                        generate_pdf(file_name, number=int(number), denomination=float(denomination), file="csv")
                        download_file = (os.path.join(current_app.instance_path, 'file_downloads',
                                                      secure_filename(file_name)) + '.csv')
                        return send_file(download_file,
                                         mimetype='text/csv',
                                         download_name=file_name + ".csv")
                        user_data = User.query.filter_by(id=current_user.id).first()
                        img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'
                        selected_currency = session.get('selectedOption', 'ZWL')
                        return render_template("general/print-airtime.html", user=current_user,
                                               denominations=denominations, img_path=img_path,
                                               selected_currency=selected_currency)

                    if selected_option == "excel":
                        generate_pdf(file_name, number=int(number), denomination=float(denomination), file="excel")
                        download_file = (os.path.join(current_app.instance_path, 'file_downloads',
                                                      secure_filename(file_name)) + '.xlsx')
                        return send_file(download_file,
                                         mimetype='text/csv',
                                         download_name=file_name + ".xlsx")
                        selected_currency = session.get('selectedOption', 'ZWL')
                        return render_template("general/print-airtime.html", user=current_user,
                                               denominations=denominations, selected_currency=selected_currency)
                else:
                    denominations = get_available_denominations()
                    flash("Please enter number for the require vouchers to be printed")
                    selected_currency = session.get('selectedOption', 'ZWL')
                    return render_template("general/print-airtime.html", user=current_user,
                                           selected_currency=selected_currency, denominations=denominations)
            else:
                user_data = User.query.filter_by(id=current_user.id).first()
                img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'
                denominations = get_available_denominations()
                selected_currency = session.get('selectedOption', 'ZWL')
                return render_template("general/print-airtime.html", user=current_user, img_path=img_path,
                                       denominations=denominations, selected_currency=selected_currency)
        except IndexError as e:
            denominations = get_available_denominations(df=get_available_data())
            flash('Quantity of vouchers selected exceed available airtime in stock', category='error')
            user_data = User.query.filter_by(id=current_user.id).first()
            img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'
            selected_currency = session.get('selectedOption', 'ZWL')
            return render_template("general/print-airtime.html", user=current_user, img_path=img_path,
                                   denominations=denominations, selected_currency=selected_currency)
    else:

        airtime = get_available_value_counts()
        user_data = User.query.filter_by(id=current_user.id).first()
        img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'
        selected_currency = session.get('selectedOption', 'ZWL')
        return render_template('general/print-airtime.html', user=current_user,
                               status='none', airtime=airtime, img_path=img_path, selected_currency=selected_currency)


@views.route('/netone-pinless', methods=['GET', 'POST'])
@login_required
def netone_pinless():
    if request.method == 'GET':
        selected_currency = session.get('selectedOption', 'ZWL')

        if selected_currency == "ZWL":
            wallet_balance = float(get_wallet_balance())
            user_data = User.query.filter_by(id=current_user.id).first()
            img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'

            return render_template('general/pinless-airtime-netone.html', selected_currency=selected_currency,
                                   user=current_user, img_path=img_path, wallet_balance=wallet_balance)
        else:
            wallet_balance = float(get_wallet_balance_usd())
            user_data = User.query.filter_by(id=current_user.id).first()
            img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'

            return render_template('general/pinless-airtime-netone.html', selected_currency=selected_currency,
                                   user=current_user, img_path=img_path, wallet_balance=wallet_balance)
    else:
        phone_number = request.form.get('phone_number').strip()
        amount = float(request.form.get('amount'))

        wallet_balance = float(get_wallet_balance())

        if amount > wallet_balance:
            flash(f"Amount exceeds total of your float balance. Your wallet balance is {wallet_balance}",
                  category='error')
        elif phone_number[:3] != "071":
            flash(f"Please enter a netone phone number in the format starting with 071. {phone_number} is incorrect.",
                  category='error')
        elif len(phone_number) != 10:
            flash(
                'Incorrect format for mobile phone number, please follow this format 071X XXX XXX and make sure you '
                'meet a length of 10 for the number.', category='error')

        voice_api_request = voice_recharge(phone_number=phone_number, amount=amount)
        if voice_api_request == 200:
            flash(
                f"Transaction processed successfully!\nYou have successfully purchased voice for ZWL{amount} for {phone_number}",
                category='success')
        else:
            flash("Transaction failed!", category='error')
            user_data = User.query.filter_by(id=current_user.id).first()
            img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'
            selected_currency = session.get('selectedOption', 'ZWL')
        return render_template('general/pinless-airtime-netone.html', selected_currency=selected_currency,
                               user=current_user, img_path=img_path, wallet_balance=wallet_balance)


@views.route('/netone-bundles', methods=['GET', 'POST'])
@login_required
def netone_bundles():
    if request.method == 'GET':
        selected_currency = session.get('selectedOption', 'ZWL')

        if selected_currency == "ZWL":
            bundles = get_airtime_bundles()
            wallet_balance = float(get_wallet_balance())
            user_data = User.query.filter_by(id=current_user.id).first()
            img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'

            return render_template('general/bundles-netone.html', user=current_user, bundles=bundles,
                                   wallet_balance=wallet_balance, img_path=img_path,
                                   selected_currency=selected_currency)
        else:
            bundles = get_airtime_bundles_usd()
            wallet_balance = float(get_wallet_balance_usd())
            user_data = User.query.filter_by(id=current_user.id).first()
            img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'

            return render_template('general/bundles-netone.html', user=current_user, bundles=bundles,
                                   wallet_balance=wallet_balance, img_path=img_path,
                                   selected_currency=selected_currency)
    else:
        selected_currency = session.get('selectedOption', 'ZWL')
        if selected_currency == "ZWL":
            bundles = get_airtime_bundles()

            phone_number = request.form.get('phone_number').strip()
            pin_name = request.form.get('pin_name')
            bundle_name = request.form.get('bundle')

            name, amount = (bundle_name.split('~')[0]).rstrip(), (bundle_name.split('~')[1]).lstrip().replace("ZWL",
                                                                                                              "").strip()
            name = name.replace("  ", " ")
            code = [data[2] for data in bundles if data[0] == name][0]

            amount = float(amount)
            wallet_balance = float(get_wallet_balance())

            if amount > wallet_balance:
                flash(f"Amount exceeds total of your float balance. Your wallet balance is {wallet_balance}",
                      category='error')
            elif phone_number[:3] != "071":
                flash(
                    f"Please enter a netone phone number in the format starting with 071. {phone_number} is incorrect.",
                    category='error')
            elif len(phone_number) != 10:
                flash(
                    'Incorrect format for mobile phone number, please follow this format 071X XXX XXX and make sure you '
                    'meet a length of 10 for the number.', category='error')

            bundle_api_request = bundle_recharge(phone_number=phone_number, code=code)
            if bundle_api_request == 200:
                flash(
                    f"Transaction processed successfully!\nYou have successfully purchased {name} for ZWL{amount} for {phone_number}",
                    category='success')
            else:
                flash("Transaction failed!", category='error')
                user_data = User.query.filter_by(id=current_user.id).first()
                img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'
                selected_currency = session.get('selectedOption', 'ZWL')
            return render_template('general/bundles-netone.html', user=current_user, bundles=bundles,
                                   wallet_balance=wallet_balance, img_path=img_path,
                                   selected_currency=selected_currency)
        else:
            bundles = get_airtime_bundles_usd()

            phone_number = request.form.get('phone_number').strip()
            pin_name = request.form.get('pin_name')
            bundle_name = request.form.get('bundle')

            name, amount = (bundle_name.split('~')[0]).rstrip(), (bundle_name.split('~')[1]).lstrip().replace("USD",
                                                                                                              "").strip()
            name = name.replace("  ", " ")
            code = [data[2] for data in bundles if data[0] == name][0]

            amount = float(amount)
            wallet_balance = float(get_wallet_balance_usd())

            if amount > wallet_balance:
                flash(f"Amount exceeds total of your float balance. Your wallet balance is {wallet_balance}",
                      category='error')
            elif phone_number[:3] != "071":
                flash(
                    f"Please enter a netone phone number in the format starting with 071. {phone_number} is incorrect.",
                    category='error')
            elif len(phone_number) != 10:
                flash(
                    'Incorrect format for mobile phone number, please follow this format 071X XXX XXX and make sure you '
                    'meet a length of 10 for the number.', category='error')

            bundle_api_request = bundle_recharge(phone_number=phone_number, code=code)
            if bundle_api_request == 200:
                flash(
                    f"Transaction processed successfully!\nYou have successfully purchased {name} for ZWL{amount} for {phone_number}",
                    category='success')
            else:
                flash("Transaction failed!", category='error')
                user_data = User.query.filter_by(id=current_user.id).first()
                img_path = f'profiles/img/{user_data.username}/{user_data.profile_pic}'
                selected_currency = session.get('selectedOption', 'ZWL')
            return render_template('general/bundles-netone.html', user=current_user, bundles=bundles,
                                   wallet_balance=wallet_balance, img_path=img_path,
                                   selected_currency=selected_currency)


def get_time_of_day(time):
    if time < 12:
        return "Morning"
    elif time < 16:
        return "Afternoon"
    elif time < 19:
        return "Evening"
    else:
        return "Evening"


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Define the allowed file extensions for image uploads
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Define a function to check if a filename has an allowed extension
def allowed_images(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


@views.route('/get-selected-currency', methods=['POST'])
def get_selected_value():
    selected_option = request.json['selectedOption']
    session['selectedOption'] = selected_option
    return 'OK'


@views.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    try:
        if request.method == 'GET':
            user_data = User.query.filter_by(id=current_user.id).first()
            # session['user_id'] = current_user.id
            date_joined = user_data.date_created.strftime("%d-%b-%Y")
            # session['date_joined'] = date_joined
            now = datetime.now()

            time_of_day = get_time_of_day(now.hour)
            # Render the edit user form with the user data
            img_path = f'profiles/img/{user_data.username.lower()}/{user_data.profile_pic}'
            print("Image Path is ", img_path)
            # session['img_path'] = img_path
            # session['user_data'] = user_data
            selected_currency = session.get('selectedOption', 'ZWL')
            return render_template('general/profile.html', time_of_day=time_of_day, user=current_user,
                                   date_joined=date_joined, user_data=user_data, img_path=img_path,
                                   selected_currency=selected_currency)

        elif request.method == 'POST':
            # Get the uploaded file and check that it's an image
            user_data = User.query.filter_by(id=current_user.id).first()
            file = request.files.get('profile_pic')
            email = request.form.get('email')
            username = user_data.username.lower()
            mobile = request.form.get('mobile')
            old_password = request.form.get('oldpassword')
            new_password = request.form.get('newpassword')
            if old_password == check_password_hash(user_data.password, old_password):
                print(f"Old password is {check_password_hash(user_data.password, old_password)}")
                flash('Old Password is wrong!', category='error')
                return redirect('/login')
            else:
                if file and allowed_file(file.filename):
                    # Generate a secure filename and save the file to the upload directory
                    filename = secure_filename(file.filename)
                    filename = filename.replace("-", "_")
                    os.makedirs(
                        os.path.join(current_app.config['STATIC_FOLDER'], 'profiles', 'img',
                                     str(current_user.username.lower())),
                        exist_ok=True)
                    file.save(
                        os.path.join(current_app.config['STATIC_FOLDER'], 'profiles', 'img',
                                     str(current_user.username.lower()),
                                     filename))

                    # Update the user data in the database with the new profile picture filename
                    User.query.filter_by(id=current_user.id).update(
                        {'email': email, 'username': username, 'mobile': mobile, 'password': generate_password_hash(
                            new_password, method='sha256'),
                         'profile_pic': filename})
                    db.session.commit()
                    # Redirect to the user's profile page
                    return redirect(f'/profile/{user_id}')
                else:
                    filename = user_data.profile_pic

                    # Update the user data in the database with the new profile picture filename
                    User.query.filter_by(id=current_user.id).update(
                        {'email': email, 'username': username, 'mobile': mobile, 'password': generate_password_hash(
                            new_password, method='sha256'),
                         'profile_pic': filename})
                    db.session.commit()
                    # Redirect to the user's profile page
                    return redirect(f'/profile/{user_id}')

        else:
            # If the uploaded file is not an image, show an error message
            error_message = 'Invalid file format. Please upload a PNG, JPG, JPEG, or GIF file.'
            return render_template('general/profile.html', error_message=error_message)
    except Exception as e:
        print(e)
        return redirect('/login')
        # id = session.get('user_id')
        # user_data = session.get('user_data')
        # img_path = session.get('img_path')
        # date_joined = session.get('date_joined')
        #
        # now = datetime.now()
        # time_of_day = get_time_of_day(now.hour)
        # return redirect(
        #     url_for('views.profile', user_data=user_data, img_path=img_path, date_joined=date_joined))
