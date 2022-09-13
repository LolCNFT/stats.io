import streamlit as st


def info():
    st.markdown('---')
    st.title('NO info is kept or stored!')
    st.write('All info is read in cache, send to make all maths and give it back, it\'s deleted once you refresh or leave the page!')
    st.write('Click "LolCNFT" below to head to the website and contact me!')
    st.header('General Graphs')
    st.subheader('Volume by Categories')
    st.write('This pie chart show how much % you moved over the selected period of time. This categories are taken '
             'from the Transaction messages anyone can send. Normally Eternl has this feature.')
    st.subheader('Volume by TxType')
    st.write('The Transaction Type shows what was about your Tx, if it was included with Tokens or if it\'s an '
             'internal transfer, among others')
    st.subheader('Sum of Tx Yearly')
    st.write('This takes all Tx and make a sum, the result would be how much ADA you ended the year with.')
    st.subheader('Sum of Tx Monthly')
    st.write('Takes the sum of all the Tx and display them month by month.')
    st.warning('Be aware that this also include the years, you are seeing the sum by year too.')
    st.subheader('Sum of Tx Monthly')
    st.write('Takes the sum of all the Tx and display them day by day.')
    st.warning('Be aware that this also include the years and months, you are seeing the sum each one!')
    st.subheader('History holdings')
    st.write('All life of your wallet displayed on how much ADA you were holding in time!')
    st.subheader('Histogram of volume')
    st.write('This histogram shows you how much volume you moved in all the wallet\'s life!')
    st.markdown('---')
    st.header('Comparative over years')
    st.write('Soon...')
