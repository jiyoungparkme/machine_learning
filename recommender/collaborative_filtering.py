# CF
# use connection between user and product

import pandas as pd
rating = pd.read_csv("ratings.csv")
movie = pd.read_csv("movies.csv")
print(rating.shape)
print(movie.shape)
print(rating.head())
print(movie.head())

# combine rating and movie data
combined = pd.merge(rating, movie, on='movieId')
print(combined.head())
print(combined.columns)

pvt = combined.pivot_table(index="userId", columns='title',
                            values = 'rating')
pvt = pvt.fillna(0) # to simplify the analysis
print(pvt)

# find correlation between user and item
'''This will find user's preference based on ratings'''
item_corr = pvt.corr()
print(item_corr.head())

# Here is an exmaple 
title = "Wick"
for target in pvt.columns:
    if title in target:
        print(target)
'''Crow, The: Wicked Prayer (2005)
John Wick (2014)
John Wick: Chapter Two (2017)
Something Wicked This Way Comes (1983)
Wicked Blood (2014)
Wicked City (Yôjû toshi) (1987)
Wicker Man, The (1973)
Wicker Man, The (2006)
Wicker Park (2004)'''    

# If user saw John Wick (2014)
# Here are top 10 similar movies user would be like
interested = "John Wick (2014)"
item_corr.sort_values(by=interested, ascending=False)[interested].head(10)