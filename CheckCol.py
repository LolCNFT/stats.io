import pandas as pd
import streamlit


def check(col, df):
    if col in df:
        return True
    else:
        return False
