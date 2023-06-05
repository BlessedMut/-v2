from datetime import datetime

import requests

from website import db
from website.models import PinlessRecharges, DataBundles


def get_agent_reference():
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    return ts


base_url = "https://pinlessevd.netone.co.zw/api/v1"
x_access_code = 'acecorpinvestments@gmail.com'
x_access_pass = 'acecorp01'


def get_wallet_balance():
    headers = {'User-Agent': 'Mozilla/5.0', 'x-access-code': x_access_code, 'x-access-password': x_access_pass,
               'x-agent-reference': str(get_agent_reference())}
    session = requests.Session()

    wallet_balance_request = session.get((base_url + "/agents/wallet-balance"), headers=headers)
    wallet_bal = wallet_balance_request.json()
    wallet_balance = wallet_bal['WalletBalance']
    return round(wallet_balance, 2)


def get_wallet_balance_usd():
    headers = {'User-Agent': 'Mozilla/5.0', 'x-access-code': x_access_code, 'x-access-password': x_access_pass,
               'x-agent-reference': str(get_agent_reference())}
    session = requests.Session()

    wallet_balance_request = session.get((base_url + "/agents/wallet-balance-usd"), headers=headers)
    wallet_bal = wallet_balance_request.json()
    wallet_balance = wallet_bal['WalletBalance']
    return round(wallet_balance, 2)


def voice_recharge(phone_number, amount):
    headers = {'User-Agent': 'Mozilla/5.0', 'x-access-code': x_access_code, 'x-access-password': x_access_pass,
               'x-agent-reference': str(get_agent_reference())}

    session = requests.Session()

    voice_request = session.post((base_url + "/agents/recharge-pinless"), headers=headers,
                                 json={'amount': amount, 'targetMobile': phone_number})
    voice_api = voice_request.json()
    print(voice_api)
    if voice_request.status_code == 200:
        transaction = PinlessRecharges(reply_code=voice_api['ReplyCode'], reply_message=voice_api['ReplyMsg'],
                                       wallet_balance=voice_api['WalletBalance'], amount=voice_api['Amount'],
                                       discount=voice_api['Discount'], initial_balance=voice_api['InitialBalance'],
                                       final_balance=voice_api['FinalBalance'], validity_window=voice_api['Window'],
                                       data=voice_api['Data'], sms=voice_api['SMS'],
                                       agent_reference=voice_api['AgentReference'],
                                       recharge_id=voice_api['RechargeID'])
        db.session.add(transaction)
        db.session.commit()
        print("Successfully saved data to db...")
        return voice_request.status_code
    else:
        print("Failed to save data to db...")

        print(f"Code: {voice_request.status_code}")
        return voice_request.status_code


def bundle_recharge(phone_number, code):
    headers = {'User-Agent': 'Mozilla/5.0', 'x-access-code': x_access_code, 'x-access-password': x_access_pass,
               'x-agent-reference': str(get_agent_reference())}

    session = requests.Session()

    bundle_request = session.post((base_url + "/agents/recharge-data"), headers=headers,
                                  json={'productcode': code, 'targetMobile': phone_number})
    bundle_api = bundle_request.json()
    print(bundle_api)
    if bundle_request.status_code == 200:
        transaction = DataBundles(reply_code=bundle_api['ReplyCode'], reply_message=bundle_api['ReplyMsg'],
                                  wallet_balance=bundle_api['WalletBalance'], amount=bundle_api['Amount'],
                                  discount=bundle_api['Discount'], initial_balance=bundle_api['InitialBalance'],
                                  final_balance=bundle_api['FinalBalance'], validity_window=bundle_api['Window'],
                                  data=bundle_api['Data'], sms=bundle_api['SMS'],
                                  agent_reference=bundle_api['AgentReference'],
                                  recharge_id=bundle_api['RechargeID'])
        db.session.add(transaction)
        db.session.commit()
        print("Successfully saved data to db...")
        return bundle_request.status_code
    else:
        print("Failed to save data to db...")

        print(f"Code: {bundle_request.status_code}")
        return bundle_request.status_code


def get_airtime_bundles():
    headers = {'User-Agent': 'Mozilla/5.0', 'x-access-code': x_access_code, 'x-access-password': x_access_pass,
               'x-agent-reference': str(get_agent_reference())}

    session = requests.Session()

    data_bundles_request = session.get((base_url + "/agents/get-data-bundles"), headers=headers).json()

    data_bundles = data_bundles_request['Bundles']

    data = []
    for entry in data_bundles:
        data.append((entry['Name'], str(entry['Amount']), entry['ProductCode']))

    data = (list(tuple(" ".join(i.split()) for i in a) for a in data))

    return data


def get_airtime_bundles_usd():
    headers = {'User-Agent': 'Mozilla/5.0', 'x-access-code': x_access_code, 'x-access-password': x_access_pass,
               'x-agent-reference': str(get_agent_reference())}

    session = requests.Session()

    data_bundles_request = session.get((base_url + "/agents/get-data-bundles-usd"), headers=headers).json()

    data_bundles = data_bundles_request['Bundles']

    data = []
    for entry in data_bundles:
        data.append((entry['Name'], str(entry['Amount']), entry['ProductCode']))

    data = (list(tuple(" ".join(i.split()) for i in a) for a in data))
    return data
