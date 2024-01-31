# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 16:22:29 2024

@author: APUGNALIN
working version

CSS Project - Option 1: IMDB Data
As a researcher, you are tasked to do use ETL and EDA skills on a movie dataset to extract certain insights.
Using Pandas, use the "movie_dataset.csv" found in the "Week 1" section of Canvas.
Note, some column names have spaces which is not ideal. Some columns have missing values and it 
would be best to either fill or drop where appropriate those missing values to prevent a bias. Load and 
clean the data, make reasonable assumptions.

Q1: What is the highest rated movie in the dataset?
Q2: What is the average revenue of all movies in the dataset? (answer effected by method to deal with missing values)
Q3: What is the average revenue of movies from 2015 to 2017 in the dataset? (answer effected by method to deal with missing values)
Q4: How many movies were released in the year 2016?
Q5: How many movies were directed by Christopher Nolan?
Q6: How many movies in the dataset have a rating of at least 8.0?
Q7: What is the median rating of movies directed by Christopher Nolan?
Q8: Find the year with the highest average rating?
Q9: What is the percentage increase in number of movies made between 2006 and 2016?
Q10: Find the most common actor in all the movies? ("Actors" column has multiple actors names - 
    find a way to search for the most common actor in all the movies).
Q11: How many unique genres are there in the dataset?  ("Genre" column has multiple genres per movie -
    find a way to identify them individually).
Q12: Do a correlation of the numerical features, what insights can you deduce? Mention at least 5 insights.
    And what advice can you give directors to produce better movies?
Q13: Once you have completed the Quiz questions, create a GitHub repository and upload a single python file 
    called "css4p01.py" to it. Share the lurl ink for the your python file below. The code must show all 
    the code used to load, analyse and clean the data, as well how you answered the Quiz questions. 
    Make reasonable assumptions.

"""

import pandas as pd
df = pd.read_csv('movie_dataset.csv')
print("\n", df)

#print original column names 
column_headers = list(df.columns.values)
print("\nHeaders original:\n", column_headers)

#rename column names where necessary
df.rename(columns = {"Runtime (Minutes)": "Runtime", "Revenue (Millions)": "Revenue_millions"}, inplace=True)

#print renamed column names 
column_headers = list(df.columns.values)
print("\nHeaders after rename:\n", column_headers)

# get data types on df
print("\nafter renaming column headers:\n")
print("\n", df.info(), "\n")

# change Year fld from int64 to datetime64[ns]
df["Year"] = pd.to_datetime(df.Year, format = '%Y')

# change Runtime_ fld from int64 to timedelta64[ns] 
df["Runtime"] = pd.to_timedelta(df["Runtime"], unit='m')
# alternative: df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time

# get data types on df 
print("\nafter converting Year and Runtime fields to datetime:\n")
print(df.info())

#print no. of rows in df
rows_df = len(df)
print("\nno. of rows in df:\n", rows_df, "\n")

# print columns with/without NaN values
print(df.isnull().any())

# temporarily drop Revenue_millions that has NaN values so as not to affect the average
df_withoutmillionsnan = df.dropna(subset=["Revenue_millions"])
print("\ndf without Revenue_millions NaN:", df_withoutmillionsnan)

# # print columns with/without NaN values
print("\ncheck that df_withoutmillionsnan doesn't contain NaNs in Revenue_millions:\n", df_withoutmillionsnan.isnull().any(), "\n")

#print no. of rows in df when Revenue_millions excludes NaN
rows_df_millions_excl_nans = len(df_withoutmillionsnan)
print("\nno. of rows in df_withoutmillionsnan:\n", rows_df_millions_excl_nans, "\n")

# print no. of records being excluded from Revenue_millions calculations
print("no. of Revenue_millions records being excluded from calculations as NaN values: {0} ({1})%").format((rows_df - rows_df_millions_excl_nans), ((rows_df_millions_excl_nans / rows_df)*100))
