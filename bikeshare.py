import time

import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TODO : get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city would you like to filter by?(new york city, chicago or washington )\n")
        city = city.lower()  # avoid case sensitive

        if city not in ("new york city", "chicago", "washington"):
            print("Wrong input! please try again")
            continue
        else:
            break

    # TODO: get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "Which month would you like to filter by? (January, February, March, April, May, June or type 'all' to get all)\n")
        month = month.lower()
        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print("Wrong input! please try again")
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "Please choose a day? (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' to get all)\n")
        day = day.lower()
        if day not in ("sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"):
            print("Wrong input! please try again")
            continue
        else:
            break

    print('-' * 40)
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
    df = pd.read_csv("{}.csv".format(city.replace(" ", "_")))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df.loc[df['month'] == month, :]
    if day != 'all':
        df = df.loc[df['day_of_week'] == day, :]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
              'november', 'december']
    # TO DO: display the most common month
    commonMonth = df["month"].mode()[0]
    print("Most Common Month:", months[commonMonth - 1])
    # TO DO: display the most common day of week
    commonDay = df["day_of_week"].mode()[0]
    print("Most Common day:", commonDay)
    # TO DO: display the most common start hour
    df['hour'] = df["Start Time"].dt.hour
    commonHour = df['hour'].mode()[0]
    print("Most Common Hour:", commonHour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    CommonlyStartStation = df["Start Station"].value_counts().idxmax()
    print("Most Commonly used start station:", CommonlyStartStation)

    # TO DO: display most commonly used end station
    CommonlyEndStation = df["End Station"].value_counts().idxmax()
    print("Most Commonly used end station:", CommonlyEndStation)
    # TO DO: display most frequent combination of start station and end station trip
    CombinationStation = df.groupby(["Start Station", "End Station"]).count()
    print('Most Commonly used combination of start station and end station trip:', CombinationStation)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    TotalTravelTime = sum(df['Trip Duration'])
    print("Total travel time:", TotalTravelTime / 86400, "Days")

    # TO DO: display mean travel time
    MeanTravelTime = df["Trip Duration"].mean()
    print("Mean travel time:", MeanTravelTime / 60, "Minutes")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    userTypes = df["User Type"].value_counts()
    print("User Types:", userTypes)
    # TO DO: Display counts of gender
    try:

        genderTypes = df["Gender"].value_counts()
        print("Gender Types:", genderTypes)
    except KeyError:
        print("We're sorry! There is no data of user genders for the choosen city")
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        EarliestBirth = df["Birth Year"].min()
        print("Earliest Birth Year:", EarliestBirth)
    except:
        print("We're sorry! There is no data of birth year for the choosen city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        row = 0
        raw_data = input('Would you like to see raw data? '
                         'Enter (y / n) : ').lower()
        while raw_data == 'y':
            print(df.iloc[row:row + 5].to_string())
            raw_data = input('Would you like to see more '
                             'raw data? Enter (y / n) : ').lower()
            row += 5

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
