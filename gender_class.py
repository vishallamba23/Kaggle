# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 07:10:08 2016

@author: asus
"""
import os, numpy as np, csv
os.chdir('C:\\Users\\asus\Desktop\Titanic')

train = csv.reader(open('train.csv', 'r'))
header = next(train)

data = []

for row in train:
    data.append(row)

data = np.array(data)

fare_ceil = 40

data[data[:,9].astype(np.float) >= fare_ceil, 9] = fare_ceil - 1
fare_bracket = 10
number_of_fare_brackets = 4
number_of_classes = len(np.unique(data[:,2]))

#initializing survial array
survival_table = np.zeros([2,number_of_classes,number_of_fare_brackets],float)

for i in range(number_of_classes):
    for j in range(int(number_of_fare_brackets)):

        female_stats = data[ (data[0::,4] == "female") \
                                 & (data[:,2].astype(np.float) == i+1) \
                                 & (data[:,9].astype(np.float) >= j*fare_bracket) \
                                 & (data[:,9].astype(np.float) < (j+1)*fare_bracket), 1]

        male_stats = data[ (data[0::,4] != "female") \
                                 & (data[:,2].astype(np.float) == i+1) \
                                 & (data[:,9].astype(np.float) >= j*fare_bracket) \
                                 & (data[:,9].astype(np.float) < (j+1)*fare_bracket), 1]

        survival_table[0,i,j] = np.mean(female_stats.astype(np.float))
        survival_table[1,i,j] = np.mean(male_stats.astype(np.float))

survival_table[ survival_table != survival_table] = 0
survival_table[ survival_table < 0.5] = 0
survival_table[ survival_table >= 0.5] = 1


test = csv.reader(open('test.csv', 'r'))
header = next(test)

prediction_file = csv.writer(open("gender_class_model.csv", 'w'))
prediction_file.writerow(["PassengerId", "Survived"])

for row in test:
    for j in range(number_of_fare_brackets):
        try:
            row[8] = float(row[8])
        except:
            bin_fare = 3 - float(row[1])
            break
        if row[8] > fare_ceil:
            bin_fare = number_of_fare_brackets - 1
            break
        if row[8] >= j*fare_bracket \
            and row[8] < (j+1)*fare_bracket:
                bin_fare = j
                break
    if row[3] == 'female':
        prediction_file.writerow([row[0], "%d" % int(survival_table[0, float(row[1]) - 1, bin_fare])])
    else:
        prediction_file.writerow([row[0], "%d" % int(survival_table[1, float(row[1]) - 1, bin_fare])])




















