import pandas as pd
import numpy as np


class money():
    tax_dict = {}
    tax_dict['pre_tax'] = 0
    tax_dict['post_tax'] = 0.2

    def __init__(self, principal, time, percent = 0.1015, bracket = 0.2, annual_investment = 0):
        self.principal = principal
        self.time = time
        self.percent = percent
        self.bracket = bracket
        self.annual_investment = annual_investment

    def investment_growth(self):
        '''A function designed to estimate how much money currently in the market can be expected to grow. Variables as follows:
        principal - the amount in the markets
        time - the amount of time it is allowed to grow
        percent - expected annual growth; by default this is set to the historical average return for the S&P 500 cited here: https://www.investopedia.com/ask/answers/042415/what-average-annual-return-sp-500.asp
        bracket - expected tax on any capital gains, set by default to the maximum cited here: https://www.investopedia.com/terms/c/capital_gains_tax.asp'''
        

        grows_to = self.principal * ((1 + self.percent) ** self.time) #SAME COMPOUNDING GROWTH
        cap_gain = grows_to - self.principal #HOW MUCH WAS INVESTMENT PROFIT?
        taxed = cap_gain * self.bracket #WHAT DO YOU PAY IN TAX?
        takehome = grows_to - taxed #LEAVING YOU WITH
        acct = {"takehome": round(takehome, 2), "taxed": round(taxed, 2), "cap_gain": round(cap_gain, 2)} #CONSOLIDATE TO DICT
        return acct
    
    def recurring_investment(self):
        '''The iterative ancestor of investment_growth().pre_tax - it sums a list of values defined by the pre_tax function with recurring investment amount as principal,
          one example for each year 0 to time input.'''
        
        every_val = [] #EMPTY LIST FOR EACH YEAR
        for i in range(self.time):

            #EACH YEAR SUBTRACT i FROM TIME FOR NUMBER OF YEARS REMAINING FOR GROWTH, APPEND GROWTH OUTPUT
            every_val.append(money(self.annual_investment, self.time - i, self.percent, 0).investment_growth()['takehome'])
        total_amount = sum(every_val) 
        total_invested = self.annual_investment * self.time #TOTAL PRINCIPAL
        cap_gain = total_amount - total_invested #HOW MUCH OF FINAL WAS GROWTH
        taxed = cap_gain * self.bracket #AMOUNT TAXED
        takehome = total_amount - taxed #LEAVING YOU WITH
        acct = {"takehome": round(takehome, 2), "taxed": round(taxed, 2), "cap_gain": round(cap_gain, 2), "pretax": total_amount} #CONSOLIDATE
        return acct
    
    @classmethod
    def pre_tax_initial(cls, principal, time, percent):
        return money(principal, time, percent, money.tax_dict['pre_tax']).investment_growth()
    
    @classmethod
    def post_tax_initial(cls, principal, time, percent):
        return money(principal, time, percent, money.tax_dict['post_tax']).investment_growth()
    
    @classmethod
    def pre_tax_recur(cls, annual_investment, time, percent):
        return money(0, time, percent, money.tax_dict['pre_tax'], annual_investment).recurring_investment()
    
    @classmethod
    def post_tax_recur(cls, annual_investment, time, percent):
        return money(0, time, percent, money.tax_dict['post_tax'], annual_investment).recurring_investment()

    