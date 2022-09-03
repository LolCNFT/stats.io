import json

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import requests
import streamlit as st  # pip install streamlit

from fpdf import FPDF
import base64

import GetAPI
import Home
import Stats

st.set_page_config(page_title="Wallet Flow", page_icon=":bar_chart:", layout="wide")
with st.spinner('Loading...'):
    @st.cache
    def get_dataframe(address):
        type = 'addresses'
        search = address
        url = 'https://cardano-mainnet.tangocrypto.com/e22dc92d75c54bb1a95aee4778f3b1d7/v1/addresses/' + search
        headers = {'x-api-key': '5d137b67bbaa466f93f1d3def97cd368'}
        r = requests.get(url, headers=headers)
        resp = r.text
        res = json.loads(resp)
        stake = res['stake_address']
        stake2 = '{:.12}'.format(res['stake_address'])
        # # All add
        lst_add = []
        url = f'https://cardano-mainnet.tangocrypto.com/e22dc92d75c54bb1a95aee4778f3b1d7/v1/wallets/{stake}/addresses'
        headers = {'x-api-key': '5d137b67bbaa466f93f1d3def97cd368'}
        r = requests.get(url, headers=headers)
        resp = r.text
        res = json.loads(resp)
        lst = []
        cursor = res['cursor']
        for t in res['data']:
            lst_add.append(t)
        while cursor is not None:
            url = f'https://cardano-mainnet.tangocrypto.com/e22dc92d75c54bb1a95aee4778f3b1d7/v1/wallets/{stake}/addresses?cursor={cursor}'
            headers = {'x-api-key': '5d137b67bbaa466f93f1d3def97cd368'}
            r = requests.get(url, headers=headers)
            resp = r.text
            res = json.loads(resp)
            for t in res['data']:
                lst_add.append(t)
            cursor = res['cursor']
        print(len(lst_add))
        for k in lst_add:
            url = f'https://cardano-mainnet.tangocrypto.com/e22dc92d75c54bb1a95aee4778f3b1d7/v1/{type}/{k["address"]}/transactions'
            headers = {'x-api-key': '5d137b67bbaa466f93f1d3def97cd368'}
            r = requests.get(url, headers=headers)
            resp = r.text
            res = json.loads(resp)
            for j in res['data']:
                lst.append({'Time': j['block']['time'], 'hash': j['hash'], 'out_sum': j['out_sum'], 'fee': j['fee'],
                            'deposit': j['deposit']})

        df = pd.DataFrame.from_dict(lst)
        return [df, stake2]
    hide_st_style = '''
                    <style>
                    #MainMenu {visibility: hidden;}
                    header {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    '''
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.image("https://www.lolcnft.com/img/favicons/android-chrome-512x512.png", width=50)

    tab1, tab2, tab3 = st.tabs(["🏠 Home", "📈 Statistics", "📍 Info"])

    with st.sidebar:
        with tab1:
            st.header("🏠 Home")
            Home.Home()

        with tab2:
            st.header("📈 Statistics")
            Stats.Stats()
        with tab3:
            st.header("📍 Info")
