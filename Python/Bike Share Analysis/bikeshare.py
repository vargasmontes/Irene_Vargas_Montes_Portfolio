import time
from sys import exit
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

dict_weekday = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6, "all": "all"}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Welcome to the US Bikeshare Data Portal.')

    # get user input for city
    city = input("What city would you like to look at? ").lower().strip()
    if city not in ["chicago", "new york city", "washington"]:
        city = input("Sorry, we do not have information on that city. Please select one of the available options: Chicago, New York City or Washington: ").lower().strip()

    # get user input for month
    month = input("\nWhat month are you interested in? You can also select 'All' if you would like to compare the whole year: ").lower().strip()
    if month not in ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december", "all"]:
        month = input("Please type the whole month (e.g. 'January'): ").lower().strip()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nAnd what day of the week? You can also select 'All' if you would like to compare the whole week: ").lower().strip()
    if day not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
        day = input("Please type the whole name for the day of the week (e.g. 'Monday'): ").lower().strip()

    # checks that all the inputs are valid. If something fails, stops the program.
    tryagain = False
    if city not in ["chicago", "new york city", "washington"]:
        print("Sorry, we are having trouble with the city you chose. Please try again and select one of the available options: Chicago, New York City or Washington.")
        tryagain = True
    if month not in ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december", "all"]:
        print("Sorry, we are having trouble with the month you chose. Please try again and type the whole month (e.g. 'January') or 'All'.")
        tryagain = True
    if day not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
        print("Sorry, we are having trouble with the day of the week you chose. Please try again and type the whole name of the day of the week (e.g. 'Monday') or 'All'.")
        tryagain = True

        if tryagain == True:
            exit()

    day = dict_weekday[day]

    print("\n", '-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (int) day - day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    file = pd.read_csv(CITY_DATA[city], parse_dates = True)
    
    # formats the start time column to create another column for the month and the weekday
    file['Start Time'] = pd.to_datetime(file['Start Time'], format='%Y-%m-%d %H:%M:%S')
    file["Month"] = file["Start Time"].dt.strftime('%B')
    file["Weekday"] = file["Start Time"].dt.weekday
    

    # Checks if the month is available in the raw data. 
    # If there's not, asks again for the user input, giving them options. 
    month_available = list(file["Month"].unique())

    # Checks if the user added any filters or proceeded with 'all' and 'all'
    if month != "all":
        if month not in [m.lower() for m in month_available]:
            print("\nSorry, we do not have the data for the month you requested. Please select one of the following options: {}. ".format(", ".join(month_available)))
            month = input().lower().strip()
            print("\n", '-'*40)

        file = file[file["Month"] == month.capitalize()]
    
    if day != "all":
        file = file[file["Weekday"] == day]
    
    return file

start_time = time.time()
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nAbout the Most Frequent Times of Travel:\n')

    # display the most common month
    trips_per_month = df["Month"].value_counts()
    if len(trips_per_month) > 1:
        print("The month with more users active was {}.".format(trips_per_month.index[0].capitalize()))

    # display the most common day of week
    trips_per_weekday = df["Weekday"].value_counts()
    most_common_day = [key for key, val in dict_weekday.items() if val == trips_per_weekday.index[0]][0].capitalize()
    if len(trips_per_weekday) > 1:
        print("The most common day to use the service was {}.".format(most_common_day))

    # display the most common start hour and the most common end hour IF it's different from start
    trips_per_hour = df["Start Time"].dt.strftime('%I %p').value_counts()
    start_hour = trips_per_hour.index[0]

    df['End Time'] = pd.to_datetime(df['End Time'], format='%Y-%m-%d %H:%M:%S')
    end_per_hour = df["End Time"].dt.strftime('%I %p').value_counts()
    end_hour = end_per_hour.index[0]
    
    if end_hour != start_hour:
        print("Most users started their journey at {} and ended it at {}.\n".format(start_hour, end_hour))
    else:
        print("Most users started their journey at {}.\n".format(start_hour))

    print('-'*40)
time_frequent_times = time.time() - start_time

start_time = time.time()
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nAbout the Most Popular Stations and Trips:\n')

    # display the most and the least used start station 
    start_station = df["Start Station"].value_counts()
    most_start = start_station.index[0]
    most_start_trips = start_station.values[0]
    least_start = start_station.index[-1]
    least_start_trips = start_station.values[-1]

    print(f"The most common start station was '{most_start}' with {most_start_trips} trips, while the least used start station was '{least_start}' with {least_start_trips}.")

    # display the most and the least used end station 
    end_station = df["End Station"].value_counts()
    most_end = end_station.index[0]
    most_end_trips = end_station.values[0]
    least_end = end_station.index[-1]
    least_end_trips = end_station.values[-1]

    print(f"The most common end station was '{most_end}' with {most_end_trips} trips, while the least used end station was '{least_end}' with {least_end_trips}.")

    # display most frequent combination of start station and end station trip
    cross_stations = pd.crosstab(df["Start Station"], df["End Station"])
    cross_stations["max"] = cross_stations.max()
    cross_stations["end"] = cross_stations.idxmax()
    cross_stations = cross_stations.reset_index()
    cross_stations["combination"] = cross_stations["Start Station"].str.cat(cross_stations['end'], sep=" to ", na_rep='')
    cross_stations_max_trips = cross_stations["max"].idxmax()
    cross_stations_max = cross_stations.loc[cross_stations_max_trips, 'combination']

    print(f"The most frequent combination was from {cross_stations_max} with a total {cross_stations_max_trips} trips.\n")

    print('-'*40)
time_stations = time.time() - start_time

start_time = time.time()
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nAbout Trip Duration:\n')

    # display total travel time
    total_trip = df["Trip Duration"].sum()
    total_months = int(total_trip // (86400 * 30)) 
    total_d = int(total_trip % (86400 * 30) // 86400)
    total_h = int(total_trip % 86400 // 3600)
    total_m = int(total_trip % 3600 // 60)
    total_s = int(total_trip % 3600 % 60)
    print("The total trip duration was {} months, {} days, {} hours, {} minutes and {} seconds.".format(total_months, total_d, total_h, total_m, total_s))

    # display mean travel time
    mean_trip = int(df["Trip Duration"].mean())
    mean_m = str(mean_trip % 3600 // 60)
    mean_s = str(mean_trip % 3600 % 60)
    print("The mean trip duration was {} minutes and {} seconds.".format(mean_m, mean_s))

    # display max travel time
    max_trip = int(df["Trip Duration"].max())
    max_m = str(max_trip % 3600 // 60)
    max_s = str(max_trip % 3600 % 60)
    print("The longest trip was {} minutes and {} seconds.".format(max_m, max_s))

    # display min travel time
    min_trip = int(df["Trip Duration"].min())
    min_m = str(min_trip % 3600 // 60)
    min_s = str(min_trip % 3600 % 60)
    print("The shortest trip was {} minutes and {} seconds.\n".format(min_m, min_s))

    print('-'*40)
time_trip_duration = time.time() - start_time

start_time = time.time()
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nAbout our Users:\n')

    total_users = len(df.index)
    print("Out of the total {} travellers:".format(total_users))

    # Display counts of user types
    try: #if dependents
        subscribers = int(df["User Type"].value_counts()["Subscriber"])
        subscribers_per = round((subscribers / total_users) * 100, 2)
        customers = int(df["User Type"].value_counts()["Customer"])
        customers_per = round((customers / total_users) * 100, 2)
        dependents = int(df["User Type"].value_counts()["Dependent"])
        dependents_per = round((dependents / total_users) * 100, 2)

        print(f"· {subscribers:,} ({subscribers_per}%) were subscribers; {customers:,} ({customers_per}%) were customers and {dependents:,} ({dependents_per}%) were dependents.")
    
    except: #without
        subscribers = int(df["User Type"].value_counts()["Subscriber"])
        subscribers_per = round((subscribers / total_users) * 100, 2)
        customers = int(df["User Type"].value_counts()["Customer"])
        customers_per = round((customers / total_users) * 100, 2)

        print(f"· {subscribers:,} ({subscribers_per}%) were subscribers and {customers:,} ({customers_per}%) were customers.")

    # Display counts of gender if they exist in the raw data
    if "Gender" in df.columns:
        females = int(df["Gender"].value_counts()["Female"])
        females_per = round((females / total_users) * 100, 2)
        males = int(df["Gender"].value_counts()["Male"])
        males_per = round((males / total_users) * 100, 2)
        other_gender = round(100 - females_per - males_per, 2)
        
        print(f"· {females:,} ({females_per}%) were female; {males:,} ({males_per}%) were male. We did not record the gender of the other {other_gender}%.")

    # Display earliest, most recent, and most common year of birth if they exist
    if "Birth Year" in df.columns:
        oldest = int(df["Birth Year"].min())
        youngest = int(df["Birth Year"].max())
        common = int(df["Birth Year"].value_counts().index[0])
        
        print("The oldest person who travelled was born in {} and the youngest in {}. The most common birth year was {}.".format(oldest, youngest, common))

    print("\n", '-'*40)
time_user_stats = time.time() - start_time

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data = input("\nThis is the end of the analysis of the data. Would your like to see the raw data? Enter Yes or No: ").lower()
        start = 0
        end = 5
        while raw_data == "yes":
            print(df.iloc[start:end])
            raw_data = input("\nWould you like to see more?").lower()
            start += 5
            end += 5

        timing = input("\nWould you like to see how long this Python process took? Enter Yes or No: ")
        if timing.lower() == "yes":
            total_timing = time_frequent_times + time_stations + time_trip_duration + time_user_stats
            print(f"\nThe total time this took was {total_timing:.10f} seconds.")
            print(f"\nIn order, each section took the following time: {time_frequent_times:.10f}, {time_stations:.10f}, {time_trip_duration:.10f} and {time_user_stats:.10f} seconds.")

        restart = input('\nWould you like to restart? Enter Yes or No: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
