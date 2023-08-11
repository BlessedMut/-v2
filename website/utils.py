import os

import matplotlib
from flask import flash, current_app
from sqlalchemy.exc import ObjectNotExecutableError
from werkzeug.utils import secure_filename

matplotlib.use('Agg')
import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://postgres:Support1999@localhost:5432/zimtopup', pool_recycle=3600)


def append_data(df):
    id = "id"
    airtime_available = "airtime_available"

    sql_get_max_id = f'select max({id}) as id from {airtime_available}'

    s_id = pd.read_sql(sql_get_max_id, engine)

    last_index = s_id['id'].values[0]

    try:
        if last_index == None:
            new_index = []
            for i in range(1, len(df) + 1):
                new_index.append(i)
        else:
            new_index = []
            for i in range(int(s_id['id'].values[0]) + 1, int(s_id['id'].values[0]) + len(df) + 1):
                new_index.append(i)

        df['id'] = new_index
        df.set_index('id', inplace=True)
    except Exception as e:
        print(e)

    return df


def generate_pdf(output_name, number, denomination, file):
    available_airtime = pd.read_sql_table('airtime_available', con=engine)
    available_airtime.index.names = ['id']

    available_airtime['voucher_key'] = available_airtime['voucher_key'].astype('str')
    available_airtime['batch_number'] = available_airtime['batch_number'].astype('str')
    available_airtime['serial_number'] = available_airtime['serial_number'].astype('str')

    if file == "csv":
        f_data = available_airtime.loc[available_airtime.denomination == denomination]
        data = f_data.iloc[:number]

        # Extract indexes for teh filtered data so that we skip them when we select dataframe for left data
        indexes = data.index

        available_airtime = available_airtime.loc[~(available_airtime.index.isin(indexes))]

        data['expiry_date'] = data['expiry_date'].apply(pd.to_datetime, infer_datetime_format=True)
        airtime_sold = append_data(data)
        airtime_sold.to_sql(name='airtime_sold', con=engine, if_exists='append', index=False)
        airtime_left = append_data(available_airtime)
        airtime_left.to_sql(name='airtime_available', con=engine, if_exists='replace', index=True)

        try:
            with engine.connect() as con:
                con.execute('ALTER TABLE airtime_available ADD PRIMARY KEY (id);')
        except ObjectNotExecutableError:
            pass

        path_to_save = os.path.join(current_app.instance_path, 'file_downloads',
                                    secure_filename(output_name) + ".csv")

        airtime_sold.voucher_key = airtime_sold.voucher_key.apply('="{}"'.format)
        airtime_sold.batch_number = airtime_sold.batch_number.apply('="{}"'.format)
        airtime_sold.serial_number = airtime_sold.serial_number.apply('="{}"'.format)

        airtime_sold.to_csv(path_to_save, index=False)
    if file == "excel":
        f_data = available_airtime.loc[available_airtime.denomination == denomination]
        data = f_data.iloc[:number]

        # Extract indexes for teh filtered data so that we skip them when we select dataframe for left data
        indexes = data.index

        available_airtime = available_airtime.loc[~(available_airtime.index.isin(indexes))]

        data['expiry_date'] = data['expiry_date'].apply(pd.to_datetime, infer_datetime_format=True)

        airtime_sold = append_data(data)
        airtime_sold.to_sql(name='airtime_sold', con=engine, if_exists='append', index=False)
        airtime_left = append_data(available_airtime)
        airtime_left.to_sql(name='airtime_available', con=engine, if_exists='replace', index=True)

        try:
            with engine.connect() as con:
                con.execute('ALTER TABLE airtime_available ADD PRIMARY KEY (id);')
        except ObjectNotExecutableError:
            pass

        path_to_save = os.path.join(current_app.instance_path, 'file_downloads',
                                    secure_filename(output_name) + ".xlsx")

        airtime_sold.to_excel(path_to_save, index=False)
    if file == "fpdf":
        f_data = available_airtime.loc[available_airtime.denomination == denomination]
        data = f_data.iloc[:number]

        # Extract indexes for teh filtered data so that we skip them when we select dataframe for left data
        indexes = data.index

        available_airtime = available_airtime.loc[~(available_airtime.index.isin(indexes))]

        data['expiry_date'] = data['expiry_date'].apply(pd.to_datetime, infer_datetime_format=True)
        airtime_sold = append_data(data)
        airtime_sold.to_sql(name='airtime_sold', con=engine, if_exists='append', index=False)
        airtime_left = append_data(available_airtime)
        airtime_left.to_sql(name='airtime_available', con=engine, if_exists='replace', index=True)

        try:
            with engine.connect() as con:
                con.execute('ALTER TABLE airtime_available ADD PRIMARY KEY (id);')
        except ObjectNotExecutableError:
            pass

        path_to_save = os.path.join(current_app.instance_path, 'file_downloads',
                                    secure_filename(output_name) + ".pdf")

        fig, ax = plt.subplots(figsize=(12, 4))
        ax.axis('tight')
        ax.axis('off')

        the_table = ax.table(cellText=airtime_sold.values, colLabels=airtime_sold.columns, loc='center')

        pdf = matplotlib.backends.backend_pdf.PdfPages(path_to_save)

        pdf.savefig(fig, bbox_inches='tight')
        pdf.close()


def pull_data():
    available_airtime = pd.read_sql_table('airtime_available', con=engine)
    history_airtime = pd.read_sql_table('airtime_sold', con=engine)

    return available_airtime.to_dict(), history_airtime.to_dict()


def upload_file(file):
    try:
        converters = {'voucher_key': str,
                      'batch_number': str,
                      'serial_number': str}

        ### Read File Data
        data = pd.read_csv(file, sep='|',
                           names=['voucher_key', 'serial_number', 'batch_number', 'denomination', 'expiry_date', 'vic'],
                           converters=converters)
        data['expiry_date'] = data['expiry_date'].apply(pd.to_datetime, infer_datetime_format=True)
        data.index.names = ['id']

        print(data)

        ### File Exporting
        data = append_data(data)

        data.to_sql(name='airtime_available', con=engine, if_exists='append', index=True)

        flash('Data was uploaded Successfully', category='success')
        return data
    except Exception as e:
        print(e)
        flash('Data was upload failed', category='error')
