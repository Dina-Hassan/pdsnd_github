import time
import sys
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city would you like info about: Chicago, New York, or Washington? ').strip().lower()
        if city in CITY_DATA:
            break
        elif city == 'exit':
            sys.exit(0)
        else:
            print("Kindly enter a valid city or 'exit' for termination!")

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter the month you would like to filter the data by (January, February, ... , June) or 'All' for no filter. ").strip().lower()
        if month in MONTHS or month == 'all':
            break
        elif month == 'exit':
            sys.exit(0)
        else:
            print("Kindly enter a valid month or 'exit' for termination!")
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter the day of week you would like to filter the data by (Monday, Tuesday, ... , Sunday) or 'All' for no filter. ").strip().lower()
        if day in DAYS or day == 'all':
            break
        elif day == 'exit':
            sys.exit(0)
        else:
            print("Kindly enter a valid day or 'exit' for termination!")
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    popular_month = MONTHS[popular_month - 1].title()
    print('The most common month: ', popular_month)
    
    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of week: ', popular_day)
    
    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour is ', popular_hour," O'clock")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station: ', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station: ', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Start_End'] = df['Start Station'] + ' - ' + df['End Station']
    popular_trip = df['Start_End'].mode()[0]
    print('The most frequent combination of start station and end station trip: ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is ', total_travel_time, ' seconds.')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time is ', mean_travel_time, ' seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nCounts of each user type:\n')
    print(user_types)
    
    if(city == 'chicago' or city == 'new york'):
        # TO DO: Display counts of gender (only applicable to NYC and Chicago)
        gender_count = df['Gender'].value_counts()
        print('\nCounts of each gender:\n')
        print(gender_count)
        
        print('\n')

        # TO DO: Display earliest, most recent, and most common year of birth (only applicable to NYC and Chicago)
        min_year = df['Birth Year'].min()
        max_year = df['Birth Year'].max()
        popular_year = df['Birth Year'].mode()[0]
        print('The earliest year of birth is ', min_year)
        print('The most recent year of birth is ', max_year)
        print('The most common year of birth is ', popular_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def display_data(df):
    display = input('Do you want to see raw data? Yes/No ').strip().lower()
    i = 0
    while display == 'yes':
        print(df.iloc[i:i+5])
        display = input('Do you want to see more 5 lines of raw data? Yes/No ').strip().lower()
        i = i+5


def main():
    while True:
        city, month, day = get_filters()
        data_frame_1 = load_data(city, month, day)
        data_frame_2 = load_data(city, month, day)

        time_stats(data_frame_1)
        station_stats(data_frame_1)
        trip_duration_stats(data_frame_1)
        user_stats(data_frame_1, city)
        display_data(data_frame_2)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.strip().lower() != 'yes':
            break


if __name__ == "__main__":
	main()

