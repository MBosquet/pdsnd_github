import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
city_lst = ['chicago', 'washington', 'new york city']
month_lst = ['january', 'february', 'march', 'april', 'may', 'june']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input("\nFrom which city would you like to see data? \nPlease choose by typing: chicago, new york city or washington:").lower()
        if city in city_lst:

# get user input for month (all, january, february, ... , june)
            ask_month_day = input('Would you like to filter the data by month, day, both, or not at all?').lower()
            if ask_month_day == 'month':
                month = input('Please select a month: January to June or choose all:').lower()
                day = 'all'

            elif ask_month_day == 'day':
    # get user input for day of week (all, monday, tuesday, ... sunday)
                day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?').lower()
                month = 'all'

            elif ask_month_day == 'both':
                month = input('Please select a month: January to June or choose all:').lower()
                day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?').lower()

            else:
                month = 'all'
                day = 'all'

            print('-'*40)
            return city, month, day

        else:
            print('Oops, looks like we do not have data for this city. Please try again!')
            print()



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

    # loads data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe

        df = df[df['Day of Week'] == day.title()]

    return df



def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel in {}...\n'.format(city.title()))
    start_time = time.time()

    # display the most common month
    popular_month = month_lst[df['Month'].mode()[0] - 1].title()
    print('The most popular month is {}.'.format(popular_month))

    # display the most common day of week
    popular_dow = df['Day of Week'].mode()[0]
    print('The most popular day of the week is {}.'.format(popular_dow))

    # display the most common start hour
    popular_hour = df['Start Time'].dt.hour.mode()[0]
    print('The most popular start hour is {}h.'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip in {}...\n'.format(city.title()))
    start_time = time.time()

    # display most commonly used start station
    popular_start_stn = df['Start Station'].mode()[0]
    print('The most commonly used start station is {}.'.format(popular_start_stn))

    # display most commonly used end station
    popular_end_stn = df['End Station'].mode()[0]
    print('The most commonly used end station is {}.'.format(popular_end_stn))

    # display most frequent combination of start station and end station trip
    df['Combo'] = 'from ' + '"'+ df['Start Station']+'"' + ' to '+ '"'+ df ['End Station'] +'"'
    popular_combo = df['Combo'].mode()[0]

    print('\nThe most frequent combination of start and end station is {}.'.format(popular_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration in {}...\n'.format(city.title()))
    start_time = time.time()

    # display total travel time
    tot_travel_time = (df['Trip Duration'].sum()/(60*60*24)).round(1)
    tot_time_years = (tot_travel_time/(30*12)).round(1)
    print('The total travel time cyclists in {} have traveled with the bike share system has been around {} days or {} years.'.format(city.title(), tot_travel_time, tot_time_years))

    # display mean travel time
    mean_travel_time = (df['Trip Duration'].mean()/60).round(0)
    print('\nThe average travel time of the trips has been around {} min.'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats in {}...\n'.format(city.title()))
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('The bike share system differntiates the following user types in {}:'.format(city.title()))
    print(user_type)


    # Display counts of gender
    if city == 'washington':
        print('\nNo information on gender and birth year available for {}.'.format(city.title()))
    else:
# Display counts of gender
        gender = df['Gender'].value_counts()
        print('\nThe number of men and women that have used the system in {}:'.format(city.title()))
        print(gender)

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]

        print('\nThe oldest {} bike sharer was born in {}.'.format(city.title(), earliest_birth_year))
        print('The youngest {} bike sharer was born in {}.'.format(city.title(), recent_birth_year))
        print('The most common birth year for {} bike sharers is {}.'.format(city.title(), common_birth_year))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    def get_raw_data(df):
    n = 5
    while True:
        raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
        print(df.head(n))
        n = n + 5

        if raw_data.lower() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df, city)
        get_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
