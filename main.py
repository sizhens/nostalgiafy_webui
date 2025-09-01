import streamlit as st
from datetime import datetime
import json
import requests
import random
import csv
import pandas as pd

prime_age_start = int(11)
prime_age_end = int(15)
current_year = int(datetime.now().year)
max_age = int(current_year - 1958)

st.write(" # Welcome to Nostalgiafy!")
st.write("To begin, select your age below.\n")
age = st.slider('Please select your age!', prime_age_end, max_age)
st.write(f"Due to the age of our database, and the current year, the max age allowable is: {max_age}")
st.write("We apologize for any inconvenience and congratulate you on your wizened years!")
st.write(f"The current year is: {current_year}")

number_of_songs_per_year = st.slider('Please select how many songs you would like per year.', 0, 10)

prime_age_diff_counter = (prime_age_end - prime_age_start)
prime_age_range = prime_age_end - prime_age_start
nostalgia_years_diff = age - prime_age_start
nostalgia_years_start = int(current_year) - nostalgia_years_diff

def main_functions_activate():
    st.write(f"Your nostalgia years are: {years_list}")
    st.write("Here is your final list of songs!\n")
    list_printer(final_list, years_list)


def nostalgia_years_generator():
    nostalgia_years_list = []
    for prime_years_counters in range(prime_age_range):
        if nostalgia_years_list == []:
            nostalgia_years_list.append(int(nostalgia_years_start))
        else:
            nostalgia_years_list.append(
                nostalgia_years_start + prime_years_counters
            )
    return nostalgia_years_list

years_list = nostalgia_years_generator()

valid_dates_db = requests.get('https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/valid_dates.json') # This is a database of valid dates for Billboard entries

random_numbers = (random.sample(range(100), int(f"{number_of_songs_per_year}")))

def dates_finder(year):
    loaded_data = valid_dates_db.json()
    valid_dates_in_year = []
    for dates in loaded_data:
        if dates.startswith(f"{year}"):
            valid_dates_in_year.append(dates)
    last_date = max(valid_dates_in_year)
    return last_date

selected_date = []

def song_selector(random_numbers, selected_date):
    song_list_for_given_year = []
    chart_req = requests.get(f'https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/date/{selected_date}.json')
    chart_data = chart_req.json()
    song_rank_list = chart_data.get("data")
    for random_number in random_numbers:
        song_selection = song_rank_list[random_number]['song']
        song_artist = song_rank_list[random_number]['artist']
        song_list_for_given_year.append(f"\"{song_selection}\" by {song_artist}")
    return (song_list_for_given_year)

def dates_maker(years_list):
    board_dates_list = []
    for year in years_list:
        new_date = dates_finder(year)
        board_dates_list.append(new_date)
    return board_dates_list

specific_dates_for_hot_100 = dates_maker(years_list)

def final_list_compiler(specific_dates_for_hot_100):
    final_list = []
    for dates in specific_dates_for_hot_100:
        selected_date = dates
        final_entries = song_selector(random_numbers, selected_date)
        final_list.append(final_entries)
    return final_list

final_list = final_list_compiler(specific_dates_for_hot_100)

def list_printer(final_list, years_list):
    for x in range(prime_age_diff_counter):
        st.write(f"\n### Songs from {years_list[x]}\n")
        for y in range(number_of_songs_per_year):
            st.write(f"##### {final_list[x][y]}\n")

filename = "song_list.txt"

cast_list = str(final_list)

st.write("Are you ready to go?")
if st.button("Fire!", 'firing_pin'):
    main_functions_activate()
    st.download_button(
        label="Download TXT",
        data=cast_list,
        file_name="data.txt",
        mime="text",
    )
else:
    st.write("You haven't fired yet!")

