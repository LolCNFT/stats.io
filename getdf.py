import pandas as pd

import CheckCol
import streamlit as st


@st.cache
def getdf_eternl(file):
    df = pd.read_csv(file)

    if CheckCol.check('Koinly Date', df):
        return None
    elif CheckCol.check('ID', df):
        return None
    try:
        df["Received Amount"] = df["Received Amount"].str.replace(',', '.').astype(float)
        df["Sent Amount"] = df["Sent Amount"].str.replace(',', '.').astype(float)
        df["Fee Amount"] = df["Fee Amount"].str.replace(',', '.').astype(float)
    except Exception:
        pass
    lst = []
    for i in df["Description"]:
        lst.append(i)
    ls = []
    for j in lst:
        if str(j)[0:6] == 'reward':
            pal = 'Reward Epochs'
            ls.append(pal)
        elif str(j)[0:3] == 'nan':
            pal = 'No Description'
            ls.append(pal)
        elif len(str(j)) > 20:
            ls.append(str(j)[0:20])
        else:
            ls.append(str(j))
    df["Description"] = pd.Series(ls)
    try:
        df["Note"] = df["Note"].fillna('No Note')
    except Exception:
        df.insert(4, "Note", "None")
    try:
        df["Received Amount"] = df["Received Amount"].fillna(0)
        df["Sent Amount"] = df["Sent Amount"].fillna(0)
        df["Fee Amount"] = df["Fee Amount"].fillna(0)
        df["Label"] = df["Label"].fillna('No Label')
    except Exception as e:
        return e
    df["TxType"] = df["TxType"].fillna('No TxType')
    df["Total per Tx"] = df["Received Amount"] - df["Sent Amount"] - df["Fee Amount"]
    df["year"] = pd.to_datetime(df["Date"], infer_datetime_format=True).dt.year
    df["month"] = pd.to_datetime(df["Date"], infer_datetime_format=True).dt.month
    df["day"] = pd.to_datetime(df["Date"], infer_datetime_format=True).dt.day
    df['day-month'] = df["day"].astype(str) + '-' + df["month"].astype(str)
    df['days'] = pd.to_datetime(df["year"].astype(str) + '-' +
                                df["month"].astype(str) + '-' + df["day"].astype(str)).dt.date
    df.sort_values(by='Date')
    lst_wallet = []
    c = 0
    for f in df['Total per Tx']:
        c += float(f)
        lst_wallet.append(c)
    df['Wallet Holdings'] = pd.Series(lst_wallet)
    total = []
    for k in df["Total per Tx"]:
        total.append(abs(k))
    df["abs_total"] = pd.Series(total)
    return df


def getdf_daedalus(file):
    df = pd.read_csv(file, thousands=',', decimal='.')
    try:
        df.rename(columns={'Deposit amount (ADA)': 'Received Amount', "Sent amount (ADA)": "Sent Amount",
                           "Fee (ADA)": "Fee Amount", 'Date & time': 'Date',
                           'Type': 'TxType', 'TOTAL (ADA)': 'Total per Tx'}, inplace=True)
        df['Tokens (unformatted amounts)'] = df['Tokens (unformatted amounts)'].fillna('No Token')
        df.drop('Status', inplace=True, axis=1)
        df.drop('Addresses from', inplace=True, axis=1)
        df.drop('Addresses to', inplace=True, axis=1)
        df.drop('Withdrawals', inplace=True, axis=1)
    except Exception:
        st.warning('kkk')
    try:
        df["Received Amount"] = df["Received Amount"].str.replace(',', '.').astype(float)
        df["Sent Amount"] = df["Sent Amount"].str.replace(',', '.').astype(float)
        df["Fee Amount"] = df["Fee Amount"].str.replace(',', '.').astype(float)
        df["Total per Tx"] = df["Total per Tx"].str.replace(',', '.').astype(float)
    except Exception:
        pass
    try:
        df["Note"] = df["Note"].fillna('No Note')
        df["Description"] = df["Description"].fillna('No Description')
        df["Label"] = df["Label"].fillna('No Label')
    except Exception:
        df.insert(7, "Note", "None")
        df.insert(8, "Description", "None")
        df.insert(9, "Label", "None")
    try:
        df["Received Amount"] = df["Received Amount"].fillna(0)
        df["Sent Amount"] = df["Sent Amount"].fillna(0)
        df["Fee Amount"] = df["Fee Amount"].fillna(0)
        df["Total per Tx"] = df["Total per Tx"].fillna(0)
        df["TxType"] = df["TxType"].fillna('No TxType')
    except Exception:
        pass
    try:
        lst_str = []
        z = 0
        for j in df['Tokens (unformatted amounts)']:

            if str(j) == 'No Token':
                lst_str.append(str(df['TxType'][z]) + ' Funds')
            else:
                lst_str.append(str(df['TxType'][z]) + ' Token')
            z += 1
        df['TxType'] = pd.Series(lst_str)
        df.pop('Tokens (unformatted amounts)')
    except Exception:
        pass
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df["year"] = pd.to_datetime(df["Date"], infer_datetime_format=True).dt.year
    df["month"] = pd.to_datetime(df["Date"], infer_datetime_format=True).dt.month
    df["day"] = pd.to_datetime(df["Date"], infer_datetime_format=True).dt.day
    df['day-month'] = df["day"].astype(str) + '-' + df["month"].astype(str)
    df['days'] = pd.to_datetime(df["year"].astype(str) + '-' +
                                df["month"].astype(str) + '-' + df["day"].astype(str)).dt.date
    # lst_date = df['Date'].tolist()
    # df.pop('Date')
    # df.insert(0,'Date', lst_date)
    lst_wallet = []
    c = 0
    df.sort_values(by='Date', inplace=True)
    df = df.reset_index(drop=True)
    for f in df['Total per Tx']:
        c += float(f)
        lst_wallet.append(c)
    df['Wallet Holdings'] = pd.Series(lst_wallet)
    total = []
    for k in df["Total per Tx"]:
        total.append(abs(k))
    df["abs_total"] = pd.Series(total)
    lst_wallet2 = []
    for f in df['Total per Tx']:
        if float(f) > 0:
            lst_wallet2.append(f)
        else:
            lst_wallet2.append(0)
    df['Received Amount'] = pd.Series(lst_wallet2)
    return df


# file = './Transactions-Shit_Tickets-2022-04-27T152220.0400Z (2).csv'
# # file2 = './eternlio-Ledger-xpub1slq0fr3krwy-ml-universaldot.csv'
# # df=getdf_eternl(file2)
# df = getdf_daedalus(file)
# print(df.to_string())
