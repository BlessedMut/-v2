import os
from datetime import datetime

from flask import Blueprint, render_template, request, current_app, flash, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from website.airtime_statistics import get_montly_sales, get_buddie_sold, get_buddie_available, \
    get_available_value_counts, get_available_denominations
from website.api import get_wallet_balance, voice_recharge, get_airtime_bundles, bundle_recharge
from website.utils import upload_file, generate_pdf

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        return render_template("general/home.html", user=current_user)
    else:
        m_sales = get_montly_sales()
        wallet_balance = float(get_wallet_balance())
        sold, total = get_buddie_sold(), get_buddie_available() + get_buddie_sold()
        sold_percentage = round(((sold / total) * 100), 0)
        return render_template("general/home.html", user=current_user, sold=sold, total_buddie_sold=total,
                               sold_percentage=sold_percentage, wallet_balance=wallet_balance)


@views.route('/upload-text-file', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == "POST":
        # file_path = request.files['fileUpload']
        f = request.files['uploadedFile']

        path_to_file = os.path.join(current_app.instance_path, 'text_file_uploads', secure_filename(f.filename))

        print(len(f.filename))

        if len(f.filename) == 0:
            flash("Please upload a file to continue.", category="error")
            return render_template("general/upload-text-file.html", user=current_user)
        else:
            if os.path.exists(path_to_file):
                flash("Can't upload textfile, similar data already exists", category="error")
                return render_template("general/upload-text-file.html", user=current_user)
            else:
                f.save(os.path.join(current_app.instance_path, 'text_file_uploads', secure_filename(f.filename)))
                path = os.path.join(current_app.instance_path, 'text_file_uploads', secure_filename(f.filename))
                upload_file(file=path)
                return render_template("general/upload-text-file.html", user=current_user)
    else:
        return render_template("general/upload-text-file.html", user=current_user)


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
                        return render_template("general/print-airtime.html", user=current_user,
                                               denominations=denominations)

                    if selected_option == "csv":
                        generate_pdf(file_name, number=int(number), denomination=float(denomination), file="csv")
                        download_file = (os.path.join(current_app.instance_path, 'file_downloads',
                                                      secure_filename(file_name)) + '.csv')
                        return send_file(download_file,
                                         mimetype='text/csv',
                                         download_name=file_name + ".csv")
                        return render_template("general/print-airtime.html", user=current_user,
                                               denominations=denominations)

                    if selected_option == "excel":
                        generate_pdf(file_name, number=int(number), denomination=float(denomination), file="excel")
                        download_file = (os.path.join(current_app.instance_path, 'file_downloads',
                                                      secure_filename(file_name)) + '.xlsx')
                        return send_file(download_file,
                                         mimetype='text/csv',
                                         download_name=file_name + ".xlsx")
                        return render_template("general/print-airtime.html", user=current_user,
                                               denominations=denominations)
                else:
                    denominations = get_available_denominations()
                    flash("Please enter number for the require vouchers to be printed")
                    return render_template("general/print-airtime.html", user=current_user, denominations=denominations)
            else:
                denominations = get_available_denominations()
                return render_template("general/print-airtime.html", user=current_user, denominations=denominations, )
        except IndexError as e:
            denominations = get_available_denominations(df=get_available_data())
            flash('Quantity of vouchers selected exceed available airtime in stock', category='error')
            return render_template("general/print-airtime.html", user=current_user, denominations=denominations)
    else:

        airtime = get_available_value_counts()
        return render_template('general/print-airtime.html', user=current_user,
                               status='none', airtime=airtime)


@views.route('/netone-pinless', methods=['GET', 'POST'])
@login_required
def netone_pinless():
    if request.method == 'GET':
        wallet_balance = float(get_wallet_balance())

        return render_template('general/pinless-airtime-netone.html', user=current_user, wallet_balance=wallet_balance)
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
        return render_template('general/pinless-airtime-netone.html', user=current_user, wallet_balance=wallet_balance)


@views.route('/netone-bundles', methods=['GET', 'POST'])
@login_required
def netone_bundles():
    if request.method == 'GET':
        bundles = get_airtime_bundles()
        wallet_balance = float(get_wallet_balance())

        return render_template('general/bundles-netone.html', user=current_user, bundles=bundles, wallet_balance=wallet_balance)
    else:
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
            flash(f"Please enter a netone phone number in the format starting with 071. {phone_number} is incorrect.",
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
        return render_template('general/bundles-netone.html', user=current_user, bundles=bundles, wallet_balance=wallet_balance)
