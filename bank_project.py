'''
Project made for fun and some practice

all csv files were downloaded from the web
import a csv with many names
import a csv with pesel numbers
import a function which converts the pesel number into a date

perform some df manipulations

create class Person with information about every person
it contains full name, address, date of birth (which is converted from the PESEL number), PESEL number
create class Account which inherits the Person class
the class contains the account balance for each person and methods to insert and withdraw money

there is a time series index which represents the birth date of each person

use groupby and perform some computations
get the maximum balance
plot some information

'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pesel_converter
#import names, addresses csv
df = pd.read_csv('data.csv', index_col=False ,header=None, names=['name', 'surname', 'address', 'city', 'state', 'postcode'])

#setting a seed for easier computations
np.random.seed(5)

#creating a new column with the account random balance of each person
df['balance'] = [np.random.randint(0, 1000000) for i in range(len(df))]
#dropping the postcode column
df = df.drop(['postcode'], axis=1)
#concatenating address and city column
df.address = df.address+' '+df.city

#importing 2nd df
pesel_info = pd.read_csv('pesel.csv', index_col=False, header = None, names=['pesel'], dtype={0: object})

#converting each pesel to date
pesel_info['date'] = pesel_info['pesel'].apply(lambda p: pesel_converter.pesel_to_date(p))
#concatenating these two dataframes into one
df = pd.concat([df, pesel_info], axis=1)
#setting index to datetime
df.index = pd.to_datetime(df['date'])
df = df.drop(['date'], axis=1)

#dropping the one missing entry
df = df.dropna()

class Bank():
    def __init__(self, company_name, company_address, nip):
        self.company_name = company_name
        self.company_address = company_address
        self.nip = nip #zabezpieczyc przy wpisywaniu zeby skladal sie tylko z liczb calkowytych

class Person():
    def __init__(self, name, surname, address, pesel, birth_date):
        self.person_name = name
        self.surname = surname
        self.person_address = address
        self.birth_date = birth_date
        self.pesel = pesel

class Account(Person):
    def __init__(self, balance, i):
        super().__init__(df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2], df.iloc[i, 4], str(df.index[i])[:10])
        self.balance = balance
    def withdraw(self, amount):
        try:
            if self.balance - amount > 0: #check if balance is not below 0
                self.balance -= amount
                print('''Withdraw successful,
remaining balance is {} euro\n'''.format(self.balance))
            else:
                print('''Unable to withdraw money, not enough funds
the balance is: {} euro
tried to withdraw {} euro\n'''.format(self.balance, amount))
        except ValueError:
            print('Amount to withdraw must be a number\n')
        except Exception:
            print('Unknown error occurred\n')

    def deposit(self, amount):
        try:
            self.balance += amount
            print('''Deposit successful,
the balance is {} euro\n'''.format(self.balance))
        except ValueError:
            print('Amount to deposit must be a number\n')
        except Exception:
            print('Unknown error occurred\n')


class BasicAcc(Account):
    account_type = 'Basic account'

class ExtendedAcc(Account): #may go under the limit, may take a credit
    account_type = 'Extended account'
    #def credit(self, amount): #take a credit (balance may go below zero but has to be fulfilled in the time of 2 years)

#creating a list of accounts(instances)
objs = [Account(df['balance'][i], i) for i in range(len(df))]

#chacing if functions work properly
objs[1].withdraw(2000)
objs[2].withdraw('20a')
objs[1].withdraw(20000)
objs[3].deposit(1000)


print('\nMaximal balances in each state:\n',df.groupby('state')['balance'].max())
print('The maximal balance is: {} euro,\n and it belongs to {} {}'.format(df.balance.max(),  df.name[df.balance == df.balance.max()].values[0], df.surname[df.balance == df.balance.max()].values[0]))


#computating the mean balance for each state
print('\nAverage balances for each state:\n', df.groupby('state')['balance'].mean())

#make a scatter of the balances for each state
xticks = [i for i in range(len(df))]
plt.scatter(xticks, df['balance'])
plt.xticks(xticks,df.state)
plt.title('Balances')
plt.show()

