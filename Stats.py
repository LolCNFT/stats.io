import base64
import time

import streamlit as st
import pandas as pd
from fpdf import FPDF
import plotly.express as px  # pip install plotly-express

import CheckCol


def Stats():
    st.markdown('---')
    genre = st.radio(
        "What's your wallet?",
        ('Eternl', 'Daedalus'))
    uploaded_file = st.file_uploader('Upload Universal .csv', type='csv', key=12212)
    st.sidebar.header("Paste your address")
    add = st.sidebar.text_input("", value="", placeholder="Soon!", disabled=True)
    export_as_pdf = st.button("Export Report")

    def create_download_link(val, filename):
        b64 = base64.b64encode(val)  # val looks like b'...'
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

    if export_as_pdf:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10)

        html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

        st.markdown(html, unsafe_allow_html=True)
    st.markdown("---")

    @st.cache
    def read_csv_daedalus(file):
        df = pd.read_csv(file,thousands=',',decimal='.')
        try:
            df.rename(columns={'Deposit amount (ADA)': 'Received Amount', "Sent amount (ADA)": "Sent Amount",
                               "Fee (ADA)": "Fee Amount", 'Date & time': 'Date',
                               'Type': 'TxType'},inplace=True)
            df.drop('Status', inplace=True, axis=1)
            df.drop('Addresses from', inplace=True, axis=1)
            df.drop('Addresses to', inplace=True, axis=1)
            df.drop('Withdrawals', inplace=True, axis=1)
            df.drop('TOTAL (ADA)', inplace=True, axis=1)
        except Exception:
            st.warning('kkk')
        try:
            df["Received Amount"] = df["Received Amount"].str.replace(',', '.').astype(float)
            df["Sent Amount"] = df["Sent Amount"].str.replace(',', '.').astype(float)
            df["Fee Amount"] = df["Fee Amount"].str.replace(',', '.').astype(float)
        except Exception:
            pass
        try:
            df["Note"] = df["Note"].fillna('No Note')
            df["Description"] = df["Description"].fillna('No Description')
            df["Label"] = df["Label"].fillna('No Label')
        except Exception:
            df.insert(4, "Note", "None")
            df.insert(5, "Description", "None")
            df.insert(5, "Label", "None")
        try:
            df["Received Amount"] = df["Received Amount"].fillna(0)
            df["Sent Amount"] = df["Sent Amount"].fillna(0)
            df["Fee Amount"] = df["Fee Amount"].fillna(0)

        except Exception:
            pass
        try:
            s = 0
            for j in df['Tokens (unformatted amounts)']:
                s+=1
                if j is not None:
                    df["TxType"][s] = (df["TxType"][s].astype(str) + ' Tokens')
            df["TxType"] = df["TxType"].fillna('No TxType')
        except Exception:
            pass
        df["Total per Tx"] = df["Received Amount"] - df["Sent Amount"] - df["Fee Amount"]
        df["year"] = pd.to_datetime(df["Date"], infer_datetime_format=True).dt.year
        df["month"] = pd.to_datetime(df["Date"], infer_datetime_format=True).dt.month
        df["day"] = pd.to_datetime(df["Date"], infer_datetime_format=True).dt.day
        df['day-month'] = df["day"].astype(str) + '-' + df["month"].astype(str)
        df['days'] = pd.to_datetime(
            df["day"].astype(str) + '-' + df["month"].astype(str) + '-' + df["year"].astype(str)).dt.date
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

    def read_csv_eternl(file):
        df = pd.read_csv(file)

        if CheckCol.check('Koinly Date', df):
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
        except Exception:
            return st.error('We could not read columns: Received Amount, Sent Amount, Fee Amount, Label')
        df["TxType"] = df["TxType"].fillna('No TxType')
        df["Total per Tx"] = df["Received Amount"] - df["Sent Amount"] - df["Fee Amount"]
        df["year"] = pd.to_datetime(df["Date"], infer_datetime_format=True).dt.year
        df["month"] = pd.to_datetime(df["Date"], infer_datetime_format=True).dt.month
        df["day"] = pd.to_datetime(df["Date"], infer_datetime_format=True).dt.day
        df['day-month'] = df["day"].astype(str) + '-' + df["month"].astype(str)
        df['days'] = pd.to_datetime(
            df["day"].astype(str) + '-' + df["month"].astype(str) + '-' + df["year"].astype(str)).dt.date
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

    # address = st.sidebar.text_input("", value="", placeholder="add1q...")
    # if address != '':
    #     if address[0:4] == 'addr':
    #         listdf = GetAPI.LookforStake(address)
    #         stake_address = listdf
    #         stake2 = '{:.12}'.format(str(listdf))
    #         dataframe = GetAPI.GetTx(stake_address)
    #         st.write(stake2)
    #         st.write(dataframe)
    #         # st.write(stake2)
    #     elif address[0:5] == 'stake':
    #         dataframe = GetAPI.GetTx(address)
    #         st.write(dataframe)
    #     else:
    #         st.error("No recognizable address")
    if uploaded_file is not None:
        if genre == 'Eternl':
            dataframe = read_csv_eternl(uploaded_file)
        elif genre == 'Daedalus':
            dataframe = read_csv_daedalus(uploaded_file)

        if dataframe is None:
            st.warning('Upload a Universal CSV.')
        else:

            st.sidebar.header("Filter here:")
            year = st.sidebar.multiselect(
                "Select year:",
                options=sorted(dataframe["year"].unique()),
                default=sorted(dataframe["year"].unique())
            )
            month = st.sidebar.multiselect(
                "Select month:",
                options=sorted(dataframe["month"].unique()),
                default=sorted(dataframe["month"].unique())
            )
            day = st.sidebar.multiselect(
                "Select day:",
                options=sorted(dataframe["day"].unique()),
                default=sorted(dataframe["day"].unique())
            )
            description = st.sidebar.multiselect(
                "Select by Description:",
                options=dataframe["Description"].unique(),
                default=dataframe["Description"].unique()
            )
            note = st.sidebar.multiselect(
                "Select by Note:",
                options=dataframe["Note"].unique(),
                default=dataframe["Note"].unique()
            )
            label = st.sidebar.multiselect(
                "Select by Label:",
                options=dataframe["Label"].unique(),
                default=dataframe["Label"].unique()
            )
            tx = st.sidebar.multiselect(
                "Select by TxType:",
                options=dataframe["TxType"].unique(),
                default=dataframe["TxType"].unique()
            )

            df_selection = dataframe.query(
                "Note == @note & year == @year & month == @month & day == @day & TxType == @tx & Label == @label & "
                "Description == @description")
            st.dataframe(df_selection)

            total_in_wallet = float(df_selection["Total per Tx"].sum())
            total_income = int(df_selection["Received Amount"].sum())
            total_sent = int(df_selection["Sent Amount"].sum())
            fee_spent = int(df_selection["Fee Amount"].sum())
            volume = float(total_income + total_sent + fee_spent)
            tx_quantity = int(df_selection["Date"].size)
            total_abs = float(dataframe['abs_total'].sum())
            total_h = float(dataframe["Total per Tx"].sum())
            tx_total = int(dataframe["Date"].size)

    try:
        average_total = round(total_abs / tx_total, 2)
        average = round(volume / tx_quantity, 2)
        t = round(((total_in_wallet - total_h) / total_h) * 100, 2)
        q = round(((average - average_total) / average_total) * 100, 2)
        v = round(((volume - total_abs) / total_abs) * 100, 2)
    except Exception:
        total_in_wallet = 0
        total_income = 0
        total_sent = 0
        fee_spent = 0
        volume = 0
        tx_quantity = 0
        total_abs = 0
        total_h = 0
        tx_total = 0
        average = 0
        average_total = 0
        t = 0
        q = 0
        v = 0
    try:
        if total_in_wallet > 1000:
            total_in_wallet = str(round(float(df_selection["Total per Tx"].sum()) / 1000, 2)) + 'K ADA'
        else:
            total_in_wallet = str(round(float(df_selection["Total per Tx"].sum()), 2)) + ' ADA'

        if volume > 1000:
            volume = str(float((total_income + total_sent + fee_spent) / 1000)) + 'K ADA'
        else:
            volume = str(float((total_income + total_sent + fee_spent) / 1000)) + ' ADA'
        if average > 1000:
            average = str(average) + 'K ADA/Tx'
        else:
            average = str(average) + " ADA/Tx"
    except Exception:
        pass
    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total:")
        # st.subheader(f'{total_in_wallet:.2f} ADA')
        st.metric("", value=total_in_wallet, delta=f'{t}%')
    with middle_column:
        st.subheader("Volume:")
        # st.subheader(f'{volume:.2f}K ADA')
        st.metric("", value=volume, delta=f'{v}%')

    with right_column:
        st.subheader("Average:")
        # st.subheader(f'{average} ADA/Tx')
        st.metric("", value=average, delta=f'{q}%')
    st.markdown('---')
    if uploaded_file is not None:
        if dataframe is None:
            st.warning('Can\'t show graphs! Upload Universal CSV.')

        else:
            with st.spinner('Loading graphs...'):
                st.subheader("General Graphs")
                # time.sleep(2)
                sales_by_des = df_selection.groupby(by=["Description"]).sum()["Total per Tx"].abs()
                fig_by_des = px.pie(
                    sales_by_des, sales_by_des.index, "Total per Tx", title="<b>Volume by Categories<b>",
                    color_discrete_sequence=px.colors.sequential.Agsunset)
                full_widht = st.columns(1)
                fig_by_des.update_traces(textposition='inside', textinfo='percent')
                with st.container():
                    st.plotly_chart(fig_by_des, use_container_width=True)
                sales_by_tx = df_selection.groupby(by=["TxType"]).sum()["Total per Tx"].abs()
                fig_by_tx = px.pie(
                    sales_by_tx, sales_by_tx.index, "Total per Tx", title="<b>Volume by Tx Type<b>",
                    color_discrete_sequence=px.colors.sequential.Rainbow)
                fig_by_tx.update_traces(textposition='inside', textinfo='percent')
                full_widht = st.columns(1)
                with st.container():
                    st.plotly_chart(fig_by_tx, use_container_width=True)
                # Year
                sales_by_year = df_selection.groupby(by=["year"]).sum()[["Total per Tx"]]
                fig_year_sale = px.bar(
                    sales_by_year,
                    y="Total per Tx",
                    x=sales_by_year.index,
                    title="<b>Sum of Tx Yearly<b>",
                    color_discrete_sequence=["#84ba5b"] * len(sales_by_year),
                    template="plotly_white"
                )
                fig_year_sale.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    yaxis=(dict(showgrid=False)),
                    xaxis=dict(tickmode='linear')
                )

                # Sales by month
                sales_by_month = df_selection.groupby(by=["month"]).sum()[["Total per Tx"]]
                fig_month_sale = px.bar(
                    sales_by_month,
                    y="Total per Tx",
                    x=sales_by_month.index,
                    title="<b>Sum of Tx Monthly<b>",
                    color_discrete_sequence=["#34B1FF"] * len(sales_by_month),
                    template="plotly_white"
                )
                fig_month_sale.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    yaxis=(dict(showgrid=False)),
                    xaxis=dict(tickmode='linear')
                )
                # Sales by day
                sales_by_day = df_selection.groupby(by=["day"]).sum()[["Total per Tx"]]
                fig_day_sale = px.bar(
                    sales_by_day,
                    y="Total per Tx",
                    x=sales_by_day.index,
                    title="<b>Sum of Tx Daily<b>",
                    color_discrete_sequence=["#ff7cbc"] * len(sales_by_day),
                    template="plotly_white"
                )
                fig_day_sale.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    yaxis=(dict(showgrid=False)),
                    xaxis=dict(tickmode='array')
                )
                with st.container():
                    st.plotly_chart(fig_year_sale, use_container_width=True)
                    st.plotly_chart(fig_month_sale, use_container_width=True)
                    st.plotly_chart(fig_day_sale, use_container_width=True)
                # Daily for year
                sales_by_days = df_selection.groupby(by=["days"]).max(numeric_only=True)[["Wallet Holdings"]]
                fig_days_sales = px.line(
                    sales_by_days,
                    y="Wallet Holdings",
                    x=sales_by_days.index,
                    title="<b>History holdings<b>",
                    color_discrete_sequence=["#8A3FFC"] * len(sales_by_days),
                    template="simple_white"
                )
                fig_days_sales.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    yaxis=(dict(showgrid=False)),
                    xaxis=dict(tickmode='array')
                )
                full_widht = st.columns(1)
                with st.container():
                    st.plotly_chart(fig_days_sales, use_container_width=True)

                txs = df_selection.groupby(by=["days"]).sum()[["abs_total"]]
                fig_txs = px.histogram(txs, x=txs.index, y='abs_total',
                                       title='<b>Histogram of volume<b>',
                                       opacity=1,
                                       log_y=False,  # represent bars with log scale
                                       color_discrete_sequence=['#E1974C']  # color of histogram bars
                                       )
                fig_txs.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    yaxis=(dict(showgrid=False)),
                    xaxis=dict(tickmode='array')
                )
                full_widht = st.columns(1)
                with st.container():
                    st.plotly_chart(fig_txs, use_container_width=True)
                st.subheader('Comparative over years')

                # Comparative

                # wallet holdings
                #
                # sales_by_days2 = df_selection.groupby(by=['day-month', 'year']).sum()[["Wallet Holdings"]]
                #
                # st.write(sales_by_days2)
                # fig_w_holding = px.line(sales_by_days2, x='year', y='Wallet Holdings', color='year')
                # fig_w_holding.update_layout(
                #     plot_bgcolor="rgba(0,0,0,0)",
                #     yaxis=(dict(showgrid=False)),
                #     xaxis=dict(tickmode='array')
                # )
                # full_widht = st.columns(1)
                # with st.container():
                #     st.plotly_chart(fig_w_holding, use_container_width=True)
