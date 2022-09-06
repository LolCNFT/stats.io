import json

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import requests
import streamlit as st  # pip install streamlit

from fpdf import FPDF
import base64

import GetAPI
import Home
import Info
import Stats

st.set_page_config(page_title="Wallet Flow", page_icon=":bar_chart:", layout="wide")
with st.spinner('Loading...'):
    # @st.cache
    # def get_dataframe(address):
    #     type = 'addresses'
    #     search = address
    #     url = 'https://cardano-mainnet.tangocrypto.com/e22dc92d75c54bb1a95aee4778f3b1d7/v1/addresses/' + search
    #     headers = {'x-api-key': ''}
    #     r = requests.get(url, headers=headers)
    #     resp = r.text
    #     res = json.loads(resp)
    #     stake = res['stake_address']
    #     stake2 = '{:.12}'.format(res['stake_address'])
    #     # # All add
    #     lst_add = []
    #     url = f'https://cardano-mainnet.tangocrypto.com/e22dc92d75c54bb1a95aee4778f3b1d7/v1/wallets/{stake}/addresses'
    #     headers = {'x-api-key': ''}
    #     r = requests.get(url, headers=headers)
    #     resp = r.text
    #     res = json.loads(resp)
    #     lst = []
    #     cursor = res['cursor']
    #     for t in res['data']:
    #         lst_add.append(t)
    #     while cursor is not None:
    #         url = f'https://cardano-mainnet.tangocrypto.com/e22dc92d75c54bb1a95aee4778f3b1d7/v1/wallets/{stake}/addresses?cursor={cursor}'
    #         headers = {'x-api-key': ''}
    #         r = requests.get(url, headers=headers)
    #         resp = r.text
    #         res = json.loads(resp)
    #         for t in res['data']:
    #             lst_add.append(t)
    #         cursor = res['cursor']
    #     print(len(lst_add))
    #     for k in lst_add:
    #         url = f'https://cardano-mainnet.tangocrypto.com/e22dc92d75c54bb1a95aee4778f3b1d7/v1/{type}/{k["address"]}/transactions'
    #         headers = {'x-api-key': ''}
    #         r = requests.get(url, headers=headers)
    #         resp = r.text
    #         res = json.loads(resp)
    #         for j in res['data']:
    #             lst.append({'Time': j['block']['time'], 'hash': j['hash'], 'out_sum': j['out_sum'], 'fee': j['fee'],
    #                         'deposit': j['deposit']})
    #
    #     df = pd.DataFrame.from_dict(lst)
    #     return [df, stake2]
    hide_st_style = '''
                    <style>
                    #MainMenu {visibility: hidden;}
                    header {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    '''
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.image("https://www.lolcnft.com/img/favicons/android-chrome-512x512.png", width=50)
    st.subheader('BETA')
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
            Info.info()


footer = """<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}
.css-1r6slb0{
background-color:#262626;
padding: 1em;
border-radius:10px;
}
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
display: flex;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: black;
text-align: center;
}
.lol{color:rgb(255, 0, 242);}.lol:hover{size:1rem;color:#ff0 !important;}.lol:visited{color:rgb(206, 4, 4);}.hero2{line-height:1;display:inline-block;z-index:2;letter-spacing:4px;filter:drop-shadow(0 1px 3px)}.layers{position:relative}.layers::after,.layers::before{content:attr(data-text);position:absolute;width:110%;z-index:-1}.layers::before{top:10px;left:15px;color:#23ff1c}.layers::after{top:5px;left:-10px;color:#4aeaff}.glitch span{animation:paths 5s step-end infinite}.glitch::before{animation:paths 5s step-end infinite,opacity 5s step-end infinite,font 8s step-end infinite,movement 10s step-end infinite}.glitch::after{animation:paths 5s step-end infinite,opacity 5s step-end infinite,font 7s step-end infinite,movement 8s step-end infinite}.single-path{clip-path:polygon(0% 12%,53% 12%,53% 26%,25% 26%,25% 86%,31% 86%,31% 0%,53% 0%,53% 84%,92% 84%,92% 82%,70% 82%,70% 29%,78% 29%,78% 65%,69% 65%,69% 66%,77% 66%,77% 45%,85% 45%,85% 26%,97% 26%,97% 28%,84% 28%,84% 34%,54% 34%,54% 89%,30% 89%,30% 58%,83% 58%,83% 5%,68% 5%,68% 36%,62% 36%,62% 1%,12% 1%,12% 34%,60% 34%,60% 57%,98% 57%,98% 83%,1% 83%,1% 53%,91% 53%,91% 84%,8% 84%,8% 83%,4% 83%)}.paths{animation:paths 5s step-end infinite}@keyframes paths{0%{clip-path:polygon(0% 43%,83% 43%,83% 22%,23% 22%,23% 24%,91% 24%,91% 26%,18% 26%,18% 83%,29% 83%,29% 17%,41% 17%,41% 39%,18% 39%,18% 82%,54% 82%,54% 88%,19% 88%,19% 4%,39% 4%,39% 14%,76% 14%,76% 52%,23% 52%,23% 35%,19% 35%,19% 8%,36% 8%,36% 31%,73% 31%,73% 16%,1% 16%,1% 56%,50% 56%,50% 8%)}5%{clip-path:polygon(0% 29%,44% 29%,44% 83%,94% 83%,94% 56%,11% 56%,11% 64%,94% 64%,94% 70%,88% 70%,88% 32%,18% 32%,18% 96%,10% 96%,10% 62%,9% 62%,9% 84%,68% 84%,68% 50%,52% 50%,52% 55%,35% 55%,35% 87%,25% 87%,25% 39%,15% 39%,15% 88%,52% 88%)}30%{clip-path:polygon(0% 53%,93% 53%,93% 62%,68% 62%,68% 37%,97% 37%,97% 89%,13% 89%,13% 45%,51% 45%,51% 88%,17% 88%,17% 54%,81% 54%,81% 75%,79% 75%,79% 76%,38% 76%,38% 28%,61% 28%,61% 12%,55% 12%,55% 62%,68% 62%,68% 51%,0% 51%,0% 92%,63% 92%,63% 4%,65% 4%)}45%{clip-path:polygon(0% 33%,2% 33%,2% 69%,58% 69%,58% 94%,55% 94%,55% 25%,33% 25%,33% 85%,16% 85%,16% 19%,5% 19%,5% 20%,79% 20%,79% 96%,93% 96%,93% 50%,5% 50%,5% 74%,55% 74%,55% 57%,96% 57%,96% 59%,87% 59%,87% 65%,82% 65%,82% 39%,63% 39%,63% 92%,4% 92%,4% 36%,24% 36%,24% 70%,1% 70%,1% 43%,15% 43%,15% 28%,23% 28%,23% 71%,90% 71%,90% 86%,97% 86%,97% 1%,60% 1%,60% 67%,71% 67%,71% 91%,17% 91%,17% 14%,39% 14%,39% 30%,58% 30%,58% 11%,52% 11%,52% 83%,68% 83%)}76%{clip-path:polygon(0% 26%,15% 26%,15% 73%,72% 73%,72% 70%,77% 70%,77% 75%,8% 75%,8% 42%,4% 42%,4% 61%,17% 61%,17% 12%,26% 12%,26% 63%,73% 63%,73% 43%,90% 43%,90% 67%,50% 67%,50% 41%,42% 41%,42% 46%,50% 46%,50% 84%,96% 84%,96% 78%,49% 78%,49% 25%,63% 25%,63% 14%)}90%{clip-path:polygon(0% 41%,13% 41%,13% 6%,87% 6%,87% 93%,10% 93%,10% 13%,89% 13%,89% 6%,3% 6%,3% 8%,16% 8%,16% 79%,0% 79%,0% 99%,92% 99%,92% 90%,5% 90%,5% 60%,0% 60%,0% 48%,89% 48%,89% 13%,80% 13%,80% 43%,95% 43%,95% 19%,80% 19%,80% 85%,38% 85%,38% 62%)}1%,33%,47%,7%,78%,93%{clip-path:none}}.movement{position:relative;animation:movement 8s step-end infinite}@keyframes movement{0%{top:0;left:-20px}15%{top:10px;left:10px}60%{top:5px;left:-10px}75%{top:-5px;left:20px}100%{top:10px;left:5px}}.opacity{animation:opacity 5s step-end infinite}@keyframes opacity{0%{opacity:.5}5%{opacity:.7}30%{opacity:.5}45%{opacity:.6}76%{opacity:.5}90%{opacity:.8}1%,33%,47%,7%,78%,93%{opacity:0}}
.pre-sign{
    z-index: 100;
  color: rgb(0, 255, 136);
  background-color: rgba(0, 0, 0, 0);
  padding: 2rem; 
  width: max-content; 
  font-size: 1.2rem; 
  text-indent: .5rem;
  margin-top: 0rem;
  width: 100%;

}

</style>
<div class="footer">
<h6 class="pre-sign">Created by <a class="lol hero2 glitch layers" style='text-decoration:none;' data-text="LolCNFT" href="https://www.lolcnft.com/" target="_blank"><span>LolCNFT</span></a></h6>
</div>
"""
st.markdown('---')
st.markdown(footer, unsafe_allow_html=True)
# <p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://www.lolcnft.com/" target="_blank">LolCNFT</a></p>
# report_text = st.text_input("Report Text")

# export_as_pdf = st.button("Export Report")
