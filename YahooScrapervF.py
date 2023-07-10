import yahooquery
import pandas as pd
from yahooquery import Ticker
import matplotlib.pyplot as plt
from datetime import date, timedelta
import numpy as np


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

company = 'spy'
ticker = Ticker(company)

current_level = ticker.price[company]["regularMarketPrice"]

dailyMove = current_level * (3.5/100)


lowerBand = current_level - dailyMove
upperBand = current_level + dailyMove


mergedDf = pd.DataFrame(ticker.option_chain, columns=['strike', 'openInterest'])


print('DATE------------')
today = date.today()

expiration_date = str(today) #change this back to daily basis !!!!!



newMergedTable = mergedDf.loc[company, expiration_date]

newMergedTable = newMergedTable[newMergedTable['strike'] >= lowerBand]
newMergedTable = newMergedTable[newMergedTable['strike'] <= upperBand]


print('-------------------')
print(newMergedTable.iloc[1])
print('-------------------')
print(newMergedTable)


calls = newMergedTable[newMergedTable.index == 'calls']
puts = newMergedTable[newMergedTable.index == 'puts']

print(calls)
print('-------------------')
print(puts)

strikes = calls.iloc[:, 0].apply(lambda x: np.nan if pd.isnull(x) else x).values

intStrikes = strikes.astype(int)

openInterest1 = calls.iloc[:, 1].apply(lambda x: np.nan if pd.isnull(x) else x).values
openInterest2 = puts.iloc[:, 1].apply(lambda x: np.nan if pd.isnull(x) else x).values

openInterest2 = openInterest2 * -1

print('-------------------')
print(intStrikes)
print('-------------------')
print(openInterest1)
print('-------------------')
print(openInterest2)

finalTable = pd.DataFrame({'Strikes': intStrikes, 'Calls': openInterest1, 'Puts': openInterest2})
print(finalTable)

fig, ax = plt.subplots()

ax.bar(np.arange(len(intStrikes)), openInterest1, label='calls')
ax.bar(np.arange(len(intStrikes)) , openInterest2,  label='puts')

ax.set_xlabel('Strikes')
ax.set_ylabel('Open Interest')

ax.set_xticks(np.arange(len(intStrikes)))
ax.set_xticklabels(intStrikes)

plt.xticks(rotation=90)

plt.show()