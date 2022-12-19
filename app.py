import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from time import time
from pathlib import Path,PurePath
import pytz

INSULIN_CSV = Path("data/insulin_data.csv")
POO_CSV = Path("data/poo_data.csv")
PEE_CSV = Path("data/pee_data.csv")
FOOD_CSV = Path("data/food_data.csv")
WATER_CSV = Path("data/water_data.csv")

EST = pytz.timezone('US/Eastern')
overview_tab,restroom_tab, feeding_tab, insulin_tab = st.tabs(["Overview","Restroom","Feeding","Insulin"])



if 'pee_df' not in st.session_state:
	if not PEE_CSV.is_file():
		st.session_state.pee_df = pd.read_csv("templates/pee_data.csv")
	else:
		st.session_state.pee_df = pd.read_csv(PEE_CSV)
st.session_state.pee_df['date'] = pd.to_datetime(st.session_state.pee_df['date'])
st.session_state.last_pee = st.session_state.pee_df.date[0] if len(st.session_state.pee_df.index) > 0 else None
st.session_state.last_pee_diff = f'{round(((datetime.now(EST) - st.session_state.pee_df.date[0]).total_seconds() / 3600),2)} Hours' if len(st.session_state.pee_df.index) > 0 else None

if 'poo_df' not in st.session_state:
	if not POO_CSV.is_file():
		st.session_state.poo_df = pd.read_csv("templates/poo_data.csv")
	else:
		st.session_state.poo_df = pd.read_csv(POO_CSV)
st.session_state.poo_df['date'] = pd.to_datetime(st.session_state.poo_df['date'])
st.session_state.last_poo = st.session_state.poo_df.date[0] if len(st.session_state.poo_df.index) > 0 else None
st.session_state.last_poo_diff = f'{round(((datetime.now(EST) - st.session_state.poo_df.date[0]).total_seconds() / 3600),2)} Hours' if len(st.session_state.poo_df.index) > 0 else None

if 'food_df' not in st.session_state:
	if not FOOD_CSV.is_file():
		st.session_state.food_df = pd.read_csv("templates/food_data.csv")
	else:
		st.session_state.food_df = pd.read_csv(FOOD_CSV)
st.session_state.food_df['date'] = pd.to_datetime(st.session_state.food_df['date'])
st.session_state.last_feeding = st.session_state.food_df.date[0] if len(st.session_state.food_df.index) > 0 else None
st.session_state.last_feeding_diff = f'{round(((datetime.now(EST) - st.session_state.food_df.date[0]).total_seconds() / 3600),2)} Hours' if len(st.session_state.food_df.index) > 0 else None

if 'water_df' not in st.session_state:
	if not WATER_CSV.is_file():
		st.session_state.water_df = pd.read_csv("templates/water_data.csv")
	else:
		st.session_state.water_df = pd.read_csv(WATER_CSV)
st.session_state.water_df['date'] = pd.to_datetime(st.session_state.water_df['date'])
st.session_state.last_watering = st.session_state.water_df.date[0] if len(st.session_state.water_df.index) > 0 else None
st.session_state.last_watering_diff = f'{round(((datetime.now(EST) - st.session_state.water_df.date[0]).total_seconds() / 3600),2)} Hours' if len(st.session_state.water_df.index) > 0 else None

if 'insulin_df' not in st.session_state:
	if not INSULIN_CSV.is_file():
		st.session_state.insulin_df = pd.read_csv("templates/insulin_data.csv")
	else:
		st.session_state.insulin_df = pd.read_csv(INSULIN_CSV)
st.session_state.insulin_df['date'] = pd.to_datetime(st.session_state.insulin_df['date'])
st.session_state.last_insulin = st.session_state.insulin_df.date[0] if len(st.session_state.insulin_df.index) > 0 else None
st.session_state.last_insulin_diff = f'{round(((datetime.now(EST) - st.session_state.insulin_df.date[0]).total_seconds() / 3600),2)} Hours' if len(st.session_state.insulin_df.index) > 0 else None


with overview_tab:
	st.header("Latest Events")
	with st.container():
		st.subheader("Dogpark Trips")
		col1,col2 = st.columns(2)
		with col1:
			st.metric("Latest Pee Run", st.session_state.last_pee.strftime("%Y-%m-%d, %H:%M") if st.session_state.last_pee is not None else None)
		with col2:
			st.metric("Time since latest pee", st.session_state.last_pee_diff)
	with st.container():
		col1,col2 = st.columns(2)
		with col1:
			st.metric("Latest Poo Run", st.session_state.last_poo.strftime("%Y-%m-%d, %H:%M") if st.session_state.last_poo is not None else None)
		with col2:
			st.metric("Time since latest poo", st.session_state.last_poo_diff)
	st.write("---------------------")
	with st.container():
		st.subheader("Feeding Events")
		col1,col2 = st.columns(2)
		with col1:
			st.metric("Latest Feeding", st.session_state.last_feeding.strftime("%Y-%m-%d, %H:%M") if st.session_state.last_feeding is not None else None)
		with col2:
			st.metric("Time since feeding", st.session_state.last_feeding_diff)
	with st.container():
		col1,col2 = st.columns(2)
		with col1:
			st.metric("Latest Water Change", st.session_state.last_watering.strftime("%Y-%m-%d, %H:%M") if st.session_state.last_watering is not None else None)
		with col2:
			st.metric("Time since last water change", st.session_state.last_watering_diff)
	st.write("---------------------")
	with st.container():
		st.subheader("Insulin Injections")
		col1,col2 = st.columns(2)
		with col1:
			st.metric("Latest Insulin Injection", st.session_state.last_insulin.strftime("%Y-%m-%d, %H:%M") if st.session_state.last_insulin is not None else None)
		with col2:
			st.metric("Time since last injection", st.session_state.last_insulin_diff)
	st.write("---------------------")
	



with restroom_tab:
	with st.container():
		col1,col2 = st.columns(2)
		with col1:
			st.header("Pee")
			pee_button = st.button("Record Pee")
			if pee_button:
				pee_date_time = datetime.now(EST)
				st.session_state.pee_df = st.session_state.pee_df.append({'date': pee_date_time}, ignore_index=True).sort_values(['date'],ascending = False,ignore_index=True)
				st.session_state.pee_df.to_csv(PEE_CSV,index = False)
				st.session_state.last_pee = st.session_state.pee_df.date[0]
				st.session_state.last_pee_diff = f'{round(((pee_date_time - st.session_state.last_pee).total_seconds() / 3600),2)} Hours'

		with col2:
			st.header("Poo")
			poo_button = st.button("Record Poo")
			poo_size = st.selectbox("Size",("tadpole","goldfish","guppy","tuna","salmon","baby shamu","shamu","mega shamu"))
			poo_type = st.selectbox("Type",("normal","runny","other"))
			if poo_button:
				poo_items = {
					"date": datetime.now(EST),
					"size": poo_size,
					"type": poo_type
				}
				st.session_state.poo_df = st.session_state.poo_df.append(poo_items, ignore_index=True).sort_values(['date'],ascending = False,ignore_index=True)
				st.session_state.poo_df.to_csv(POO_CSV,index = False)
				st.session_state.last_poo = st.session_state.poo_df.date[0]
				st.session_state.last_poo_diff = f'{round(((poo_items["date"] - st.session_state.last_poo).total_seconds() / 3600),2)} Hours'

	with st.container():
		col1,col2 = st.columns(2)
		with col1:
			st.subheader("Recent Pee Records")
			st.write(st.session_state.pee_df.head(10))
		with col2:
			st.subheader("Recent Poo Records")
			st.write(st.session_state.poo_df.head(10))


with feeding_tab:
	with st.container():
		col1,col2 = st.columns(2)
		with col1:
			st.subheader("Food")
			food_button = st.button("Record Feeding")
			food_cups = st.number_input("Food amount (cups)", min_value=0.0, max_value=5.0, value=0.5, step=0.1)
			if food_button:
				food_items = {
					"date": datetime.now(EST),
					"cups": food_cups
				}
				st.session_state.food_df = st.session_state.food_df.append(food_items, ignore_index=True).sort_values(['date'],ascending = False,ignore_index=True)
				st.session_state.food_df.to_csv(FOOD_CSV,index = False)
				st.session_state.last_feeding = st.session_state.food_df.date[0]
				st.session_state.last_feeding_diff = f'{round(((food_items["date"] - st.session_state.last_feeding).total_seconds() / 3600),2)} Hours'

		with col2:
			st.subheader("Water")
			water_button = st.button("Record Water Change")
			water_change_type = st.selectbox("Record Type?",("normal","measured"))
			if water_change_type == "measured":
				water_remaining_vol = st.number_input("Water remaining in bowl (mL)", min_value=0, max_value=1000, value=0, step=100)
				water_added_vol = st.number_input("Water added (mL)", min_value=0, max_value=1500, value=1000, step=100)
			elif water_change_type == "normal":
				water_remaining_vol = None
				water_added_vol = 1000
			if water_button:
				water_items = {
					"date": datetime.now(EST),
					"remaining ml": water_remaining_vol,
					"added ml": water_added_vol,
					"record type": water_change_type
				}
				st.session_state.water_df = st.session_state.water_df.append(water_items, ignore_index=True).sort_values(['date'],ascending = False,ignore_index=True)
				st.session_state.water_df.to_csv(WATER_CSV,index = False)
				st.session_state.last_watering = st.session_state.water_df.date[0]
				st.session_state.last_watering_diff = f'{round(((water_items["date"] - st.session_state.last_watering).total_seconds() / 3600),2)} Hours'
	
	with st.container():
		col1,col2 = st.columns(2)
		with col1:
			st.subheader("Recent Feedings")
			st.write(st.session_state.food_df.head(10))
		with col2:
			st.subheader("Recent Water Changes")
			st.write(st.session_state.water_df.head(10))


with insulin_tab:
	st.header("Insulin Injections")

	insulin_record = st.button("Record Insulin Injection")
	insulin_dose = st.number_input("Insulin Dose", min_value=0, max_value=100, value=5, step=1)
	insulin_brand = st.selectbox("Insulin Brand",["Novolin"])
	insulin_user = st.selectbox("Who administered it?",["AVH","JVH","DVH","RVH"])

	if insulin_record:
		# update dataframe state
		insulin_items = {
					"date": datetime.now(EST),
					"dose administered (units)": insulin_dose,
					"brand": insulin_brand,
					"user": insulin_user
				}
		st.session_state.insulin_df = st.session_state.insulin_df.append(insulin_items, ignore_index=True).sort_values(['date'],ascending = False,ignore_index=True)
		st.session_state.insulin_df.to_csv(INSULIN_CSV,index = False)
		st.session_state.last_insulin = st.session_state.insulin_df.date[0]
		st.session_state.last_insulin_diff = f'{round(((insulin_items["date"] - st.session_state.last_insulin).total_seconds() / 3600),2)} Hours'
	st.write("--------------")
	st.subheader("Recent Insulin Injection Records")
	st.write(st.session_state.insulin_df.head(10))


