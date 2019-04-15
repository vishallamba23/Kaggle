"""The genderclass model program converted to pandas"""
import pandas as pd
import numpy as np
import os

def AddBinFare(frame, fare_bracket_size=10, number_of_fares=4):
  """Bin the ticket fare and add a new column BinFare"""
  frame['BinFare'] = ((frame.Fare//fare_bracket_size)
                      .clip_upper(number_of_fares-1)
                      # Use class as substitute if no fare was given
                      .fillna(3-frame.Pclass)
                      .astype(np.int))

#in order to analyse the price collumn I need to bin up that data
#here are my binning parameters the problem we face is some of the fares are very large
#So we can either have a lot of bins with nothing in them or we can just absorb some
#information and just say anythng over 30 is just in the last bin so we add a ceiling
fare_ceiling = 40
fare_bracket_size = 10
number_of_fares = fare_ceiling // fare_bracket_size
number_of_classes = 3 #There were 1st, 2nd and 3rd classes on board

data = pd.read_csv('train.csv',skipinitialspace=1,index_col=[0])
AddBinFare(data,
           fare_bracket_size=fare_bracket_size,
           number_of_fares=number_of_fares)

# This reference table will show we the proportion of survivors as a function of
# Gender, class and ticket fare.
# I can now find the stats of all the women and men on board
index_list=[]
survival_list=[]
genderNames = ['female','male']
for sexIdx in range(2):
  for classIdx in range(number_of_classes):
    for fareIdx in range(number_of_fares):
      index_list += [(sexIdx,classIdx,fareIdx)]
      survival_probability = (data.Survived[(data.Sex == genderNames[sexIdx])
                                            & (data.Pclass-1==classIdx)
                                            & (data.BinFare == fareIdx)]
                              .mean())
      survival_list += [survival_probability]

# Turn into a series and transform probabilities into a binary survive label.
survival_index = pd.MultiIndex.from_tuples(index_list,
                                           names = ['Gender','Class','PriceBracket'])
survival_table = (pd.Series(survival_list,
                            index=survival_index, name='Survival')

                  # Replace nans with zeros and turn binary by assume <0.5 don't survive.
                  .fillna(0) > 0.5).astype(np.int)

print survival_table.values

# Read the test file
test = pd.read_csv('test.csv',index_col=[0])

# Calculate the bin fare
AddBinFare(test, fare_bracket_size=fare_bracket_size, number_of_fares=number_of_fares)

print test[['Fare','Pclass','BinFare']].head(10)

# Add survival table based on looking up the survival value of Sex,Pclass, and BinFare
test['Survived'] = (test[['Sex','Pclass','BinFare']]
                    .apply(lambda s: survival_table[(s[0]=='male', s[1]-1, s[2])],
                           axis=1)
)

# Output csv's for submission
test[['Survived']].to_csv('genderclassmodel-pandas.csv')
