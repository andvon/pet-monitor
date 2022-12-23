import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path,PurePath
import pendulum
import uuid

def load_data(record_file: PurePath):
	if record_file.is_file():
		with open(record_file,"r") as input_file:
			records = json.load(input_file)
	else:
		records = []
	return records

def report_latest_entry(label,session_name,idx):
	if st.session_state[session_name] and st.session_state[session_name][0][idx]:
		out_value = st.session_state[session_name][0][idx]
	else:
		out_value = None
	st.metric(label,out_value)
	return

PEE_JSON = Path("data/pee_records.json")
POO_JSON = Path("data/poo_records.json")
WATER_JSON = Path("data/water_records.json")
FOOD_JSON = Path("data/food_records.json")
INSULIN_JSON = Path("data/insulin_records.json")

if 'pee_info' not in st.session_state:
	st.session_state.pee_info = load_data(PEE_JSON)
	st.session_state.pee_additions = []

if 'poo_info' not in st.session_state:
	st.session_state.poo_info = load_data(POO_JSON)
	st.session_state.poo_additions = []
if 'water_info' not in st.session_state:
	st.session_state.water_info = load_data(WATER_JSON)
	st.session_state.water_additions = []
if 'food_info' not in st.session_state:
	st.session_state.food_info = load_data(FOOD_JSON)
	st.session_state.food_additions = []
if 'insulin_info' not in st.session_state:
	st.session_state.insulin_info = load_data(INSULIN_JSON)
	st.session_state.insulin_additions = []

# --- PEE --- #

def add_record(session_name,additions_name,records_file,contents = {}):
	current_time = pendulum.now("US/Eastern")
	contents["local_datetime"] = current_time.to_day_datetime_string()
	contents["iso8601_datetime"] = current_time.to_iso8601_string()
	contents["identifier"] = str(uuid.uuid1())
	
	st.session_state[session_name].insert(0,contents)
	st.session_state[additions_name].insert(0,contents)
	with open(records_file,"w") as output_file:
		json.dump(st.session_state[session_name],output_file,indent = 4)
	#st.success("Success!")
	return

def remove_record(session_name,additions_name,records_file):
	if not st.session_state[additions_name]:
		#st.write("Nothing to remove")
		return
	st.session_state[session_name].pop(0)
	st.session_state[additions_name].pop(0)
	with open(records_file,"w") as output_file:
		json.dump(st.session_state[session_name],output_file,indent = 4)
	#st.write("Removed!")
	return


def module_pee():
	pee_placeholder = st.empty()
	col1,col2 = st.columns(2)
	with st.container():
		with col1:
			pee_button = st.button(
				"Record Pee",
				on_click=add_record,
				kwargs = dict(
					session_name = "pee_info",
					additions_name = "pee_additions",
					records_file = PEE_JSON
					)
				)
		with col2:
			undo_pee_button = st.button(
				"Undo Pee",
				on_click=remove_record,
				kwargs = dict(
					session_name = "pee_info",
					additions_name = "pee_additions",
					records_file = PEE_JSON
					)
				)
		report_latest_entry("Pee Run","pee_info","local_datetime")
	return
	#st.write(st.session_state.pee_info)

# --- POO --- #

def module_poo():
	poo_size = st.selectbox("Size",("tadpole","goldfish","guppy","tuna","salmon","baby shamu","shamu","mega shamu"),key = "poo_size")
	poo_type = st.selectbox("Type",("normal","runny","other"),key = "poo_type")
	col1,col2 = st.columns(2)
	with st.container():
		with col1:
			poo_button = st.button(
				"Record Poo",
				on_click=add_record,
				kwargs = dict(
					session_name = "poo_info",
					additions_name = "poo_additions",
					records_file = POO_JSON,
					contents = dict(
						size = st.session_state["poo_size"],
						type = st.session_state["poo_type"]
					)
					)
				)
		with col2:
			undo_poo_button = st.button(
				"Undo Poo",
				on_click=remove_record,
				kwargs = dict(
					session_name = "poo_info",
					additions_name = "poo_additions",
					records_file = POO_JSON
					)
				)
		report_latest_entry("Poo Run","poo_info","local_datetime")
	return
	#st.write(st.session_state.pee_info)

# --- Water --- #

def module_water():
	report_latest_entry("Last Changed","water_info","local_datetime")
	st.checkbox("Is this measured?", value=False, key="measured_water_change")
	if st.session_state["measured_water_change"]:
		st.number_input("Water remaining in bowl (mL)", min_value=0, max_value=1000, value=0, step=100,key = "remaining_ml")
		st.number_input("Water added (mL)", min_value=0, max_value=1500, value=1000, step=100,key = "added_ml")
	col1,col2 = st.columns(2)
	with st.container():
		with col1:
			st.button(
				"Record Water Change",
				on_click=add_record,
				kwargs = dict(
					session_name = "water_info",
					additions_name = "water_additions",
					records_file = WATER_JSON,
					contents = dict(
						remaining_ml = st.session_state["remaining_ml"] if st.session_state["measured_water_change"] else None,
						added_ml = st.session_state["added_ml"] if st.session_state["measured_water_change"] else None
					)
					)
				)
		with col2:
			st.button(
				"Undo Water Change",
				on_click=remove_record,
				kwargs = dict(
					session_name = "water_info",
					additions_name = "water_additions",
					records_file = WATER_JSON
					)
				)
	return

# --- FOOD --- #

def module_food():
	report_latest_entry("Last Changed","food_info","local_datetime")
	st.number_input("Amount of food given (in cups)", min_value=0.0, max_value=2.0, value=0.5, step=0.1,key = "food_cups")
	col1,col2 = st.columns(2)
	with st.container():
		with col1:
			st.button(
				"Record Feeding Frenzy",
				on_click=add_record,
				kwargs = dict(
					session_name = "food_info",
					additions_name = "food_additions",
					records_file = FOOD_JSON,
					contents = dict(
						food_cups = st.session_state["food_cups"] if st.session_state["food_cups"] else None
					)
					)
				)
		with col2:
			st.button(
				"Undo Feeding Frenzy",
				on_click=remove_record,
				kwargs = dict(
					session_name = "food_info",
					additions_name = "food_additions",
					records_file = FOOD_JSON
					)
				)
	return

# --- INSULIN --- #

def module_insulin():
	report_latest_entry("Last Injection","insulin_info","local_datetime")
	st.subheader("Report new injection")
	st.number_input("Insulin Dose (Units)", min_value=0.0, max_value=100.0, value=5.0, step=0.5,key = "insulin_dose")
	st.selectbox("Insulin Brand",["Novolin"],key = "insulin_brand")
	st.selectbox("Who administered it?",["AVH","JVH","DVH","RVH"],key = "insulin_user")
	col1,col2 = st.columns(2)
	with st.container():
		with col1:
			st.button(
				"Record Injection",
				on_click=add_record,
				kwargs = dict(
					session_name = "insulin_info",
					additions_name = "insulin_additions",
					records_file = INSULIN_JSON,
					contents = dict(
						insulin_dose_units = st.session_state["insulin_dose"] if st.session_state["insulin_dose"] else None,
						insulin_brand = st.session_state["insulin_brand"] if st.session_state["insulin_brand"] else None,
						insulin_user = st.session_state["insulin_user"] if st.session_state["insulin_user"] else None,
					)
					)
				)
		with col2:
			st.button(
				"Undo Insulin Injection",
				on_click=remove_record,
				kwargs = dict(
					session_name = "insulin_info",
					additions_name = "insulin_additions",
					records_file = INSULIN_JSON
					)
				)
	return

# --- APP --- #

overview_tab,restroom_tab, feeding_tab, insulin_tab = st.tabs(["Overview","Restroom","Feeding","Insulin"])

with overview_tab:
	st.header("Latest Events")
	st.write("-----")
	st.header("Dogpark trips")
	report_latest_entry("Pee Run","pee_info","local_datetime")
	report_latest_entry("Poo Run","poo_info","local_datetime")
	st.write("-----")
	st.header("Food and Water")
	report_latest_entry("Feeding Frenzy","food_info","local_datetime")
	report_latest_entry("Water Change","water_info","local_datetime")
	st.write("-----")
	st.header("Insulin Injection")
	report_latest_entry("Insulin Injection","insulin_info","local_datetime")
	st.write("-----")

with restroom_tab:
	st.header("Pee Run")
	module_pee()
	st.write("-----")
	st.header("Poo Run")
	module_poo()

with feeding_tab:
	st.write("-----")
	st.header("Water")
	module_water()
	st.write("-----")
	st.header("Food")
	module_food()

with insulin_tab:
	st.write("-----")
	st.header("Insulin")
	module_insulin()

