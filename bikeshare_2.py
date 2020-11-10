import time
import pandas as pd
import numpy as np

months = ["january", "february", "march", "april", "may", "june"]
weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

CITY_DATA = { "chicago": "chicago.csv",
              "new york city": "new_york_city.csv",
              "washington": "washington.csv" }

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("Hello! Let\"s explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("What City you want to take a look at (chicago, new york city, washington)?: ")
            city = city.lower()
            x = CITY_DATA[city]
            break
        except KeyError:
            print("We could not find the city in our Database, pleas choose Chigago, New York City or Washington")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("What specific month do you want to see between January and June (all, january, february, ... , june)? :")
        month = month.lower()
        if month in months or month == "all":
            break
        else:
            print("This month format does not match our requirements. Please enter the month in text form e.g. january, february etc. and only one at a time.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("What day of the week do you want to see (all, monday, tuesday, ... sunday)? :")
        day = day.lower()
        if day in weekdays or day == "all":
            break
        else:
            print("This day format does not match our requirements. Please enter the day in text form e.g. monday, tuesday etc. and only one at a time.")

    print("-"*40)
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

    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name
    df["hour"] = df["Start Time"].dt.hour

    if month != "all":
        month = months.index(month) + 1
        df = df[df["month"] == month]

    if day != "all":
        df = df[df["day_of_week"] == day.title()]

    return df

def time_stats(df):

    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    print("The most common month to use the bikes is", df["month"].mode()[0], "\n")

    # display the most common day of week

    print("The most common day to use the bikes is", df["day_of_week"].mode()[0], "\n")

    # display the most common start hour
    print("The most common hour to start a bike trip is", df["hour"].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start Station is : ",df["Start Station"].mode()[0], "\n")

    # display most commonly used end station
    print("The most commonly used end Station is : ",df["End Station"].mode()[0], "\n")

    # display most frequent combination of start station and end station trip
    station_start, station_end = df.groupby(["Start Station","End Station"]).size().idxmax()
    print("The most connection is between", station_start, "and", station_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    print("The total time of all trips added is:", df["Trip Duration"].sum(), "seconds or ", df["Trip Duration"].sum()/60, "minutes.", "\n")

    # display mean travel time
    print("The average travel time is:", df["Trip Duration"].mean(), "seconds or ", df["Trip Duration"].mean()/60, "minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def user_stats(df, city):
    """ Displays statistics on bikeshare users. """

    print("\nCalculating User Stats...\n \n")
    start_time = time.time()

    # Display counts of user types
    print("User Types:\n" + str(df['User Type'].value_counts()), "\n")

    # Display counts of gender
    if city != "washington":
        print("Gender Split:\n" + str(df["Gender"].value_counts()),"\n")
    else:
        print("There are no information on the gender of our users in Washington!\n")

    # Display earliest, most recent, and most common year of birth
    if city != "washington":
        print("The oldest customer is born in:", int(df["Birth Year"].min()))
        print("\nThe youngest customer is born in:", int(df["Birth Year"].max()))
        print("\nThe most common year of birth is:", int(df["Birth Year"].mode()[0]))
    else:
        print("\nThere are no information on the year of birth of our users in Washington!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        counter = 0

        while True:
            if counter == 0:
                 while True:
                        raw_data = input("\nWould you like to view the raw Data(Yes/No)? ")
                        raw_data = raw_data.lower()
                        if raw_data in ["yes", "no"]:
                            break
                        else:
                            print("Please answer Yes or No")
            else:
                while True:
                        raw_data = input("\nWould you like to view more raw Data(Yes/No)? ")
                        raw_data = raw_data.lower()
                        if raw_data in ["yes", "no"]:
                            break
                        else:
                            print("Please answer Yes or No")
            if raw_data == "yes":
                print(df.iloc[counter:counter+5])
                counter += 5
            else:
                break

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
	main()
