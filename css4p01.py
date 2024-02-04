# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 16:22:29 2024 - Sun Feb 02 17:42:00 2024

@author: APUGNALIN

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

TO DO: 
fix Q10 
remove 0 days from  Runtime fld
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
print("\noriginal data types:\n")
print("\n", df.info(), "\n")

# change Year fld from int64 to datetime64[ns]
df["Year"] = pd.to_datetime(df.Year, format = '%Y')

# change Runtime_ fld from int64 to timedelta64[ns] 
df["Runtime"] = pd.to_timedelta(df["Runtime"], unit='m')
# alternative: df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time

# get data types on df 
print("\nafter converting Year and Runtime fields to datetime:\n")
print(df.info())

# # _________________________________________________________________________________________
# Q1: what is the highest rated movie?

highest_rate = df["Rating"].max()
highest_rated_movie = df[df["Rating"] == highest_rate]
# determine title of highest rated movie
highest_rated_movie_title = df.loc[df["Rating"]==highest_rate, ["Title"]].squeeze()
# determine the genre of the highest rated movie
highest_rated_movie_genre = df.loc[df["Rating"]==highest_rate, ["Genre"]].squeeze()
print(f"\nA1: the highest rated movie is {highest_rated_movie_title} ({highest_rated_movie_genre})")

#_________________________________________________________________________________________
# Q2: What is the average revenue of all movies in the dataset? [NaNs were replaced with the average]

# print columns with/without NaN values
# print("\nidentify which fields have NaN values:")
# print(df.isnull().any())

# temporarily drop Revenue_millions that has NaN values so as not to affect the average
df_withoutmillionsnan = df.dropna(subset=["Revenue_millions"])

# # print columns with/without NaN values
# print("\ncheck that new extract of df called df_withoutmillionsnan doesn't contain NaNs in Revenue_millions:\n", df_withoutmillionsnan.isnull().any(), "\n")

# # calculating average of Revenue_millions when NaNs excluded
avg_rev_mills_without_nan = df_withoutmillionsnan["Revenue_millions"].mean()
df["Revenue_millions"] = df["Revenue_millions"].fillna(avg_rev_mills_without_nan)

#calculating NaNs in df to be equal to the average of the Revenue (millions) when NaNs are excluded
avg_rev_mills = df["Revenue_millions"].mean()
print(f"A2: average movie revenue (Millions): US$ {avg_rev_mills.round(2)}")

# ___________________________________________________________________________________________
# Q3: What is the average revenue of movies from 2015 to 2017 in the dataset? II

# calculating average of Revenue_millions when NaNs excluded during a certain time period 

# filter for time period
strtyr_av = '2015/01/01'
endyr_av = '2017/01/01'
df_strtyr_endyr_av = df_withoutmillionsnan[(df_withoutmillionsnan["Year"] >= strtyr_av) & (df_withoutmillionsnan["Year"] <= endyr_av)]

# generate average of Revenue (millions) for the time period
avg_rev_mills_strtyr_endyr = df_strtyr_endyr_av["Revenue_millions"].mean()

#populate NaNs in Revenue (millions) fld in original table as average for the time period
df["Revenue_millions"] = df["Revenue_millions"].fillna(avg_rev_mills_strtyr_endyr)

print(f"A3: average movie revenue (Millions) {strtyr_av} to {endyr_av}: US$ {avg_rev_mills_strtyr_endyr.round(2)}")

# #___________________________________________________________________________________________
# # Q4: How many movies were released in the year 2016?

# filter by year
yr = '2016'
df_yr = df[df["Year"] >= yr]

# generate number of movies released that year
num_movie_count_yr = len(df_yr.index)
print(f"A4: number of movies released in {yr}: {num_movie_count_yr}")

# ________________________________________________________________________________________________
# Q5: How many movies were directed by Christopher Nolan?

# filter by director name
dirnm = 'Christopher Nolan'
df_dirnm = df[df["Director"]==dirnm]

# generate number of movies directed by this person
num_dirnm = len(df_dirnm.index)
print(f"A5: number of movies directed by {dirnm}: {num_dirnm}")

#___________________________________________________________________________________________________
# Q6: How many movies in the dataset have a rating of at least 8.0?

# filter by rating
rating = 8.0
df_rating = df[df["Rating"]>=rating]

# generate number of movies with this rating
num_rating = len(df_rating.index)
print(f"A6: number of movies with a rating of >={rating}: {num_rating}")

#_________________________________________________________________________________________________
# Q7: What is the median rating of movies directed by Christopher Nolan?

# filter by director name
dirnm = 'Christopher Nolan'
df_dirnm = df[df["Director"]==dirnm]
df_rating = df[df["Rating"]>=rating]
med_rating = df_rating["Rating"].median()
print(f"A7: median rating of movies directed by {dirnm}: {med_rating}")

# ____________________________________________________________________________________________________
# Q8: Find the year with the highest average rating?

# generate list of years
list_yrs = []
for yr in df["Year"]:
    if not yr in list_yrs:
        list_yrs.append(yr)
 
# calculate average rating per year
dict_av_rating_yr = {}
for yr in list_yrs:
    df_yr = df[df["Year"]==yr]
    av_rating_yr = (df_yr["Rating"].mean()).round(2)
    dict_av_rating_yr[yr] = av_rating_yr
    s = pd.Series(dict_av_rating_yr)
    max_av_rating_yr = (max(s.index)).strftime('%Y')
    
print(f"A8: the year with the highest average movie rating: {max_av_rating_yr}")

# #____________________________________________________________________________________________________
# Q9: What is the percentage increase in number of movies made between 2006 and 2016?


# filter by start year
strtyr_perc = '2006'
df_strt_yr_perc = df[df["Year"] == strtyr_perc]

# filter by end year
endyr_perc = '2016'
df_end_yr_perc = df[df["Year"] == endyr_perc]

# calculate % difference between number of movies made in start year and in end year
num_strt_yr_perc = len(df_strt_yr_perc.index)
num_end_yr_perc = len(df_end_yr_perc.index)
diff_yr_perc = ((num_end_yr_perc - num_strt_yr_perc)/100)

print(f"A9: the percentage increase in number of movies made between {strtyr_perc} and {endyr_perc}: {diff_yr_perc}%")

# __________________________________________________________________________________________________
# Q10: Find the most common actor in all the movies? ("Actors" column has multiple actors names - 
#    find a way to search for the most common actor in all the movies).

# split the actors names where more than one in field
s_act = df["Actors"].str.split(',').explode().value_counts()

# determine most common actor in all the movies 
most_com_actor = pd.Series(s_act.index).head(1)
print(f"A10: the most common actor in all the movies was: {most_com_actor}")

#_______________________________________________________________________________________________
# Q11: How many unique genres are there in the dataset?  ("Genre" column has multiple genres per movie -
#    find a way to identify them individually).        

# split the genres where more than one in field
s_genre = df["Genre"].str.split(',').explode().value_counts()

# determine how many genres of movies there are
num_genres = len(pd.Series(s_genre.index))
print(f"A11: the number of unique movie genres was: {num_genres}")

#______________________________________________________________________________________________________
# Q12: Do a correlation of the numerical features, what insights can you deduce? Mention at least 5 insights.
#    And what advice can you give directors to produce better movies?

"""
Background reading:
    - star power + director an indicator of success: https://journals.sagepub.com/doi/full/10.1177/0276237416628904
    - no. of votes representing audience engagement as an indicator of success: https://www.linkedin.com/advice/1/how-do-you-measure-films-success-skills-film-production#:~:text=Another%20way%20to%20measure%20a,its%20cultural%20and%20social%20relevance.
    - "the metascore is a weighted average of many reviews coming from reputed critics" - https://www.freecodecamp.org/news/whose-reviews-should-you-trust-imdb-rotten-tomatoes-metacritic-or-fandango-7d1010c6cf19/
"""

# # generated Profile Report in ArcGIS Pro Notebook
# # cloned environment in ArcGIS Pro and installed pandas_profiling package (ydata-profiling wouldn't install)
# https://pypi.org/project/pandas-profiling/3.1.0/

# import pandas as pd
# from pandas_profiling import ProfileReport
# df = pd.read_csv("D:/css2024/css_2024_project_imdb/movie_dataset.csv", index_col=0)
# profile = ProfileReport(df, title="Profiling Report movie dataset")
# profile.to_file('Profile Report movie dataset.html')  # to export it if it dosen’t display

# # Summarize dataset: 100%|██████████| 57/57 [00:05<00:00, 10.36it/s, Completed]                                     ﻿
# # Generate report structure: 100%|██████████| 1/1 [00:02<00:00,  2.81s/it]﻿
# # Render HTML: 100%|██████████| 1/1 [00:02<00:00,  2.03s/it]﻿
# # Export report to file: 100%|██████████| 1/1 [00:00<00:00, 14.75it/s]

# # profile report
# # https://tylerthetech.com/how-to-view-html-on-github/
    
import webbrowser

url = "https://raw.githack.com/ampugcct/css4p01/main/Profile%20Report%20movie%20dataset.html"
webbrowser.open_new(url)
print("""A12: please refer to the Profile Report that has opened in your browser.  
      
Five insights derived from the Profile Report below:
1. Rating is highly overall correlated [positively] with Votes: there is usually more audience engagement when the movie is a success
2. Metascore is highly overall correlated [positively] with Rating: the public and the critics tend to be in agreement in terms of rating
3. Revenue (Millions) is highly overall correlated [positively] with Votes: the more audience engagement there is with a movie, the more revenue it tends to have generated
4. Year is highly overall correlated [negatively] with Votes: the year did not impact how many votes were received
5. The movies that generated the most Revenue (millions) (+R600 million) were +120 Runtime (minutes)""")

print("""\nAdvice for directors to produce better movies:
1. Have a + 120 Runtime (minutes) as people want to feel as though they got their money's worth.
2. Feature a popular star, such as Christian Bale. The highest rated movie is The Dark Knight and he was the most common actor in all movies over the period.
3. Make a high quality movie.  The public clearly appreciate this as they tend to concur with the movie critics in their Ratings.
4. The most popular genre combination was Action-Drama-Crime so creating a movie with these elements is likely to draw the crowds.""")

