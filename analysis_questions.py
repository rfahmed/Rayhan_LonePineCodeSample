# Name: Rayhan Ahmed
# Date: 1/5/22
# Lone Pine Code Sample
import pandas as pd


def driver(filename):
    """
    function: driver
    params: filename (location of data in question)
    use: answers the 4 set questions from the specifications in the assignment document
    """
    current_sample = pd.read_csv(f'cached_data/{filename}', compression='gzip', error_bad_lines=False)

    # Grab answers to our specific questions:
    state_popularity_answer = state_popularity(current_sample, 'CO', 'Make', 1)
    year_popularity_answer = year_popularity(current_sample, 2010, 'Color', 3)
    city_population_answer = city_population(current_sample, 2000000)
    yoy_growth_answer_2019 = yoy_growth(current_sample, 2019, 2020, 'Make')
    yoy_growth_answer_2020 = yoy_growth(current_sample, 2020, 2021, 'Make')

    # Pretty print our answers:
    pretty_print(state_popularity_answer, year_popularity_answer, city_population_answer,
                 yoy_growth_answer_2019, yoy_growth_answer_2020)


def pretty_print(state_popularity_answer, year_popularity_answer, city_population_answer,
                 yoy_growth_answer_2019, yoy_growth_answer_2020):
    """
    function: pretty_print
    params: state_popularity_answer, (to format most popular car maker in CO)
            year_popularity_answer, (to format top 3 colors in 2010)
            city_population_answer, (to format the percent of cars in cities over 2MM)
            yoy_growth_answer_2019, and yoy_growth_answer_2020 (to calculate YoY growth)
    use: formats answers provided in the driver function
    """
    # Answer question 1:
    print('\n Q1: What car make in the sample is the most popular in Colorado?')
    print(
        f'In Colorado the most popular car make is {state_popularity_answer.index[0][0]} with {state_popularity_answer[0]}'
        f' used car registrations')

    # Answer question 2:
    print('\n Q2: What were the three most popular car colors in the sample in 2010?')
    print('The 3 most popular car colors in 2010 were: ')
    print(year_popularity_answer.index[0][0], year_popularity_answer.index[1][0], 'and',
          year_popularity_answer.index[2][0],
          'with', year_popularity_answer[0], year_popularity_answer[1], 'and', year_popularity_answer[2],
          'cars respectively.')

    # Answer question 3:
    print('\n Q3: What percentage of cars in the sample are in cities with populations above 2MM?')
    print(f"The percentage of cars that are in cities above 2MM in population is {round(city_population_answer, 3)}%.")

    # Answer question 4:
    print('\n Q4: Which car maker saw the greatest year-over-year (YOY) growth in registrations between 2019 and '
          '2020?  Between 2020 and 2021?')
    print(
        f'{yoy_growth_answer_2019.name} had the greatest YOY growth between 2019 and 2020 at '
        f'{round(yoy_growth_answer_2019[0], 3)}%.')
    print(
        f'{yoy_growth_answer_2020.name} had the greatest YOY growth between 2020 and 2021 at '
        f'{round(yoy_growth_answer_2020[0], 3)}%.')


def state_popularity(current_sample, state, value, topk=None):
    """
    function: state_popularity
    params: current_sample, (dataframe from top level file)
            state, (Select which state to examine in our analysis)
            value, (Specify which column in our data to analyze (ex. Make, Model, Year, Color, Registration Date))
            topk (Specify the top n records to return, default = None)
    use: Returns the top K values in a given state for a specified identifier.
    note: can be adapted to work with a list of states easily by passing a list of state codes and altering the
          condition to check if our given state code matches any in the list we took in.
    """
    # First check our state code by converting the address object to a string (.str) and checking the substring
    # from the 8th to last to 6th to last positions (this will always be the state code as zip codes are always 5 long):
    prune_our_state = current_sample['Address'].str[-8:-6] == state

    # Cut out all values not matching our state:
    sample_with_state = current_sample.loc[prune_our_state]

    # Tabulate the values in our specified column 'value' within our state:
    most_popular = sample_with_state[[value]].value_counts()

    # return either the topk if it is set, or the top value by default:
    if topk is not None:
        return most_popular.iloc[0:topk]
    else:
        return most_popular.iloc[0]


def year_popularity(current_sample, year, value, topk=None):
    """
    function: year_popularity
    params: current_sample, (dataframe from top level file)
            year, (Select which year to examine in our analysis)
            value, (Specify which column in our data to analyze (ex. Make, Model, Year, Color, Registration Date))
            topk (Specify the top n records to return, default = None)
    use: Returns the top K values in a given year for a specified identifier.
    note: can be adapted to work with a range of years easily by passing a start/end year and altering the
          condition to check if our given year is between them.
    """
    # Cut out all values not matching our condition that the year is our target year:
    sample_with_year = current_sample.loc[current_sample['Year'] == year]

    # Tabulate the values in our specified column 'value' within our year:
    most_popular = sample_with_year[[value]].value_counts()

    # return either the topk if it is set, or the top value by default:
    if topk is not None:
        return most_popular.iloc[0:topk]
    else:
        return most_popular.iloc[0]


def city_population(current_sample, population_target):
    """
    function: city_population
    params: current_sample, (dataframe from top level file)
            population_target (Select cities with a population above this target)
    use: Returns the percentage of cars in cities with a population above population_target.
    note: can be adapted to work with a specific city by adding a param for city_name and matching it to pop_data.
    """
    # To start get our initial number of cars:
    total_cars = len(current_sample.index)

    # Read in and format our population data (taken from the US census in 2021):
    pop_data = pd.read_csv('cityPopulationData.csv', usecols=['name', 'usps', 'pop2021'])
    pop_data['name'] = pop_data['name'] + ' ' + pop_data['usps']  # format name string as City State in one column
    pop_data = pop_data.drop('usps', 1)  # Drop the extraneous state code column (they are now merged into 'name')
    pop_data = pop_data.loc[pop_data['pop2021'] >= population_target]  # filter by cities greater than the target

    # Only keep entries in our data that are in one of our target cities:
    # Here we can use a lambda function to only keep the section of our address string after the comma (our city/state):
    current_sample['Address'] = current_sample['Address'].apply(lambda x: str(x.split(',')[1][1:-6]))
    # Get our target cities (in our population range) as a list:
    pop_list = pop_data['name'].tolist()

    # Match our city/state string to our set of targets:
    sample_in_population_range = current_sample.loc[current_sample['Address'].isin(pop_list)]
    # Number of cars in our new sample:
    total_cars_in_population_range = len(sample_in_population_range.index)

    percent_of_overall = total_cars_in_population_range / total_cars * 100  # Simple percent calculation
    return percent_of_overall


def yoy_growth(current_sample, year1, year2, value, topk=None):
    """
    function: yoy_growth
    params: current_sample, (dataframe from top level file)
            year1, (start year)
            year2, (end year)
            value, (Specify which column in our data to analyze (ex. Make, Model, Year, Color, Registration Date))
            topk (Specify the top n records to return, default = None)
    use: Returns the growth between two given years for car makers.
    note: can be adapted to work with any timeframe (months, days) by changing the condition to dt.month or dt.day.
    """
    # Make our date strings datetime objects in pandas:
    current_sample['Registration Date'] = pd.to_datetime(current_sample['Registration Date'])
    # Cut to the Make and Registration Date columns:
    current_sample = current_sample[[value, 'Registration Date']]
    current_sample = current_sample.sort_values(by=['Make', 'Registration Date']) # Helpful for visualization
    # Initialize counts:
    year_1_counts = None
    year_2_counts = None
    # Iterate through years and grab value counts for year1 and year2:
    for year, df_year in current_sample.groupby(current_sample['Registration Date'].dt.year):
        # Send our value counts to a dataframe and specify the year:
        if year == year1:
            year_1_counts = df_year[value].value_counts().to_frame(name=f'Registrations_{year1}')
        if year == year2:
            year_2_counts = df_year[value].value_counts().to_frame(name=f'Registrations_{year2}')

    # Join our two years of value counts to one df:
    joined_years = pd.concat([year_1_counts, year_2_counts], axis=1)
    # Get difference between the years:
    joined_years['Delta'] = joined_years[f'Registrations_{year2}'] - joined_years[f'Registrations_{year1}']
    # Calculate a percent change:
    joined_years['Growth'] = joined_years['Delta'] / joined_years[f'Registrations_{year1}'] * 100
    # Sort to return top values:
    joined_years.sort_values('Growth', ascending=False, inplace=True)
    all_growth = joined_years[['Growth']]
    # return either the topk if it is set, or the top value by default:
    if topk is not None:
        return all_growth.iloc[0:topk]
    else:
        return all_growth.iloc[0]
