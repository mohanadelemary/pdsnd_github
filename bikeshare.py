import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """Asks user to specify a city, month, and day to analyze."""
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city with input validation
    while True:
        city = input('Which city would you like to explore today? Type one of these choices (chicago, new york city, washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please try again.")

    # Get user input for month
    month = input("Which month would you like to explore today? Type 'all' to skip or type in the month name (between January to June): ").lower()

    # Get user input for day of week
    day = input("Which weekday would you like to explore today? Type 'all' to skip or type in the weekday (Monday to Sunday): ").lower()

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable."""
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert 'Start Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Create 'month' and 'day_of_week' columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    
    # Filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day of week
    if day != 'all':
        dows = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        dow_index = dows.index(day)
        df = df[df['day_of_week'] == dow_index]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most common month
    pop_month = df['month'].mode()[0]
    print('Most Popular Month: ', pop_month)

    # Most common day of week
    pop_dow = df['day_of_week'].mode()[0]
    print('Most Popular Day of Week: ', pop_dow)

    # Most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station
    pop_ss = df['Start Station'].mode()[0]
    print('Most Popular Start Station: ', pop_ss)

    # Most commonly used end station
    pop_es = df['End Station'].mode()[0]
    print('Most Popular End Station: ', pop_es)

    # Most frequent combination of start and end stations
    value_counts = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Counts')
    sorted_counts = value_counts.sort_values(by='Counts', ascending=False)
    most_frequent = sorted_counts.head(1)  # Get the top combination
    print("Most Frequent Combination of Start and End Stations: ")
    print(most_frequent)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_time = df['Trip Duration'].sum()
    print('Total Travel Time: ', total_time)

    # Mean travel time
    avg_time = df['Trip Duration'].mean()
    print('Average Travel Time: ', avg_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Count of user types
    ut_count = df['User Type'].value_counts()
    print('Count of Users Per Type: ')
    print(ut_count)

    # Count of gender (check for gender column existence)
    if 'Gender' in df.columns:
        g_count = df['Gender'].value_counts()
        print('Count of Users Per Gender: ')
        print(g_count)

    # Earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        b_min = int(df['Birth Year'].min())
        b_max = int(df['Birth Year'].max())
        b_common = int(df['Birth Year'].mode()[0])

        print('Earliest Birth Year: ', b_min)
        print('Most Recent Birth Year: ', b_max)
        print('Most Common Birth Year: ', b_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

# New function to display 5 rows at a time
def display_data(df):
    """Ask user if they want to see 5 rows of data, continue showing more rows if desired."""
    ind = 0
    while True:
        display_request = input('Do you want to check the first 5 rows of the dataset related to the chosen city? (Type yes or no): ').lower()
        if display_request == 'yes':
            print(df[ind:ind+5])
            ind += 5
            while ind < len(df):
                more_data = input('Do you want to check another 5 rows of the dataset? (Type yes or no): ').lower()
                if more_data == 'yes':
                    print(df[ind:ind+5])
                    ind += 5
                else:
                    break
        break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)  # Call the new function to display 5 rows of data

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
