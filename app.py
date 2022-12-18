import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from time import time
from pathlib import Path

INJECTION_CSV = Path("data/insulin_injections.csv")

if not INJECTION_CSV.is_file():
	st.session_state.df = pd.DataFrame(
		{
			"date": [],
			"dose administered (units)": []
		})
	INJECTION_CSV.parent.mkdir(parents = True,exist_ok = True)

if 'df' not in st.session_state:
	st.session_state.df = pd.read_csv(INJECTION_CSV)

st.session_state.df['date'] = pd.to_datetime(st.session_state.df['date'])
st.session_state.df = st.session_state.df.sort_values('date',ascending = False,ignore_index=True)

with st.container():
   st.write("Insulin Tracker")
   insulin_record = st.button("Record Insulin Injection")
   insulin_dose = st.number_input("Insulin Dose", min_value=0, max_value=100, value=5, step=1)

if insulin_record:
	# update dataframe state
	date_time = datetime.now()
	st.session_state.df = st.session_state.df.append({'date': date_time,'dose administered (units)': insulin_dose}, ignore_index=True).sort_values(['date'],ascending = False,ignore_index=True)
	st.session_state.df.to_csv(INJECTION_CSV,index = False)

if len(st.session_state.df.index) > 0:
	latest_dose = st.session_state.df.date[0]
	time_diff_dose = datetime.now() - latest_dose
	
else:
	latest_dose = None

st.metric("Latest injection", latest_dose.strftime("%Y-%m-%d, %H:%M:%S"), delta=None, delta_color="normal", help=None, label_visibility="visible")
st.metric("Time since last injection", f"{(time_diff_dose.total_seconds() / 3600):.2f} Hours", delta=None, delta_color="normal", help=None, label_visibility="visible")
	

st.dataframe(st.session_state.df)


