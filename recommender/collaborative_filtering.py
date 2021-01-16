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

### item based recommender
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

# If user saw John Wick (2014) with high rating
# Here are top 10 similar movies user would be like
interested = "John Wick (2014)"
print(item_corr.sort_values(by=interested, ascending=False)[interested].head(10))
# User might like these movies 
'''John Wick (2014)
            1.000000
Mad Max: Fury Road (2015)
            0.617796
Snowpiercer (2013)
            0.604255
Fast Five (Fast and the Furious 5, The) (2011)    0.557030
Rogue One: A Star Wars Story (2016)   
            0.545675
John Wick: Chapter Two (2017)
            0.540651
Dredd (2012)
            0.540043
This Is the End (2013)
            0.538012
Deadpool (2016)
            0.533856
Suicide Squad (2016)
            0.530213'''

### user based recommender
# use same pivot but tranpose it
user_corr = pvt.T.corr()
print(user_corr.head())

# select a user
user = 200
print(user_corr.sort_values(by=user, ascending=False)[user])
'''userId
200    1.000000
68     0.431156
480    0.414132
219    0.413150
381    0.401098
         ...   
85     0.000313
571    0.000140
3     -0.006402
138   -0.008014
397   -0.008785'''
# 68 user has most similar preferencee with user 200

# recommendation for user 200 
interested = ['title', 'rating']
c_200 = combined.loc[combined['userId'] == 200][interested]
c_68 = combined.loc[combined['userId'] == 68][interested]

c_200_set = set(c_200['title'])
c_68_set = set(c_68['title'])

# movie list that user 68 saw but user 200 didn't see
diff_68_200 = c_68.difference(c_200_set)
print(diff_68_200)

# sort the list according to rating
recommend = c_68.loc[c_68['title'].isin(diff_68_200)].sort_values(
    by='rating', ascending=False)
print(recommend.head())