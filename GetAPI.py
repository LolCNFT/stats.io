import json
import time

import pandas as pd
import requests
import streamlit as st


def LookforStake(address):
    with st.spinner('Looking for stake address'):
        try:
            url = 'https://cardano-mainnet.tangocrypto.com/e22dc92d75c54bb1a95aee4778f3b1d7/v1/addresses/' + address
            headers = {'x-api-key': '5d137b67bbaa466f93f1d3def97cd368'}
            r = requests.get(url, headers=headers)
        except Exception as e:
            st.warning(f'Could not get stake {e}')
        resp = r.text
        res = json.loads(resp)
        stake = res['stake_address']

    return stake


def GetTx(stake_address):
    with st.spinner('Getting all your addresses'):
        lst_add = []
        try:
            url = f'https://cardano-mainnet.tangocrypto.com/e22dc92d75c54bb1a95aee4778f3b1d7/v1/wallets/{stake_address}/addresses'
            headers = {'x-api-key': '5d137b67bbaa466f93f1d3def97cd368'}
            r = requests.get(url, headers=headers)

        except Exception as e:
            st.warning(f'No connection made {e}')
        resp = r.text
        res = json.loads(resp)
        lst = []
        cursor = res['cursor']
        for t in res['data']:
            lst_add.append(t)
    with st.spinner('Wow! You got lot of addresses!'):
        while cursor is not None:
            #     print(cursor)

            try:
                url = f'https://cardano-mainnet.tangocrypto.com/e22dc92d75c54bb1a95aee4778f3b1d7/v1/wallets/{stake_address}/addresses?cursor={cursor}'
                headers = {'x-api-key': '5d137b67bbaa466f93f1d3def97cd368'}
                r = requests.get(url, headers=headers)

            except Exception as e:
                st.warning(f'No connection getting address {e}')
            resp = r.text
            res = json.loads(resp)
            for t in res['data']:
                lst_add.append(t)
            cursor = res['cursor']
    with st.spinner('Now your transactions! Nearly there! Be patience!'):
        for k in lst_add:
            try:
                url = f'https://cardano-mainnet.tangocrypto.com/e22dc92d75c54bb1a95aee4778f3b1d7/v1/addresses/{k["address"]}/transactions'
                headers = {'x-api-key': '5d137b67bbaa466f93f1d3def97cd368'}
                r = requests.get(url, headers=headers)
            except Exception as e:
                st.warning(f'No connection getting transactions {e}')
            resp = r.text
            res = json.loads(resp)
            for j in res['data']:
                lst.append({'Time': j['block']['time'], 'hash': j['hash'], 'out_sum': j['out_sum'], 'fee': j['fee'],
                            'deposit': j['deposit']})
        df = pd.DataFrame.from_dict(lst)
    return df
