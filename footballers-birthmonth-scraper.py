# converted Jupyter Notebook to Python script to scrape and clean data
from os import name
import pandas as pd

# scrapes tables from Goal article and returns .csv file


def scraper():
    source = pd.read_html(
        'https://www.goal.com/en-us/news/footballers-birthdays-messi-ronaldo-every-top-players-date/tfyes3k66ze81gozdgi8j5bna')

    # returns list
    # dataframes from January to December in list index 1-12
    # some tables have different column names for the first column i.e Player or Player name so need to change them before concatenating the dataframes
    columnNames = ['Player', 'Club', 'Nationality', 'Birthday']
    sourceDfs = source[1:13]
    for df in sourceDfs:
        df.columns = columnNames

    df = pd.concat(sourceDfs)

    # convert Birthday column to datetime
    # one value is Jun instead of June so that is fixed
    # 1900 is just a dummy year as the original dataset did not have years, only month & day

    df['Birthday'] = df['Birthday'].replace({'Jun ': 'June '}, regex=True)
    df['Birthday'] = pd.to_datetime(df['Birthday'], format='%B %d')

    # filter out the managers i.e. ones with manager string in Club column.
    # e.g. Sir Alex Ferguson is still in the dataset, he is mostly known for his managerial career but he was also a player

    df = df[~df.Club.str.contains('manager')]

    # reset index

    df = df.reset_index(drop=True)

    # print(df)

    # save to csv without index
    df.to_csv('footballers-birthmonths.csv', index=False)


if __name__ == "__main__":
    scraper()
