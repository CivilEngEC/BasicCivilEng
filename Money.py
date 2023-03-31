#Money
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from EngUnits import CivilEngUnits

#Money class
class Money(CivilEngUnits):
    """Money class, this class is used to represent money objects,
    value is a float and represent the value of the money object at the date of the object,
    symbol is a string and represent the symbol of the currency object,
    date is a string in the format YYYY-MM-DD and represent the date of the money object,
    year_rate is a float and represent the anual interest of the money object.
    decimal is an integer and represent the number of decimal places of the money object,
    """
    
    def __init__(self, value: float, symbol: str, date:str="", year_rate:float = 0.0,
                 decimal: int = 2, name: str = "Currency"):
        super().__init__(value, symbol, decimal, name)
        self.value = value
        self.symbol = symbol
        self.decimal = decimal
        self.name = name
        units = pd.DataFrame(data= [["US Dollar","USD",1,"" ],
                              ["Euro","EUR",1.18,"" ],
                              ["British Pound","GBP",1.31,"" ],
                              ["Japanese Yen","JPY",0.0091,"" ],
                              ["Chinese Yuan","CNY",0.15,"" ],
                              ["Indian Rupee","INR",0.014,"" ],
                              ["Russian Ruble","RUB",0.014,"" ],
                              ["Paraguayan Guarani","PYG",0.00014,"" ]],
                              columns=["Name","Symbol","Factor","Description"])
        
        
        self.set_units(name=self.name, units=units)
        if date == "":
            self.date = datetime.date.today()
        else:
            self.date = datetime.date.fromisoformat(date)
        self.year_rate = year_rate #anual interest


    def future_value(self, rate: float, period: int):
        """Calculate the future value of a money object.
        the rate is the value that will be add if rate is positive or substracted if negative at the end of each period, 
        the period is an integer usually are the number of years."""
        if not isinstance(rate, float):
            raise TypeError("The discount rate must be a number.")
        if not isinstance(period, int):
            raise TypeError("The number of years must be an integer.")
        return self.value * (1 + rate) ** period
    
    def present_value(self, rate: float, period: int):
        """Calculate the present value of a money object.
        the rate is the value that will be add if rate is positive or substracted if negative at the end of each period, 
        the period is an integer usually are the number of years."""
        if not isinstance(rate, float):
            raise TypeError("The discount rate must be a number.")
        if not isinstance(period, int):
            raise TypeError("The number of years must be an integer.")
        return self.value / ((1 + rate) ** period)
    
    def predict_values(self, rate: float, period: int):
        """Predict the values of a money object.
        the discount rate is number, the period is an integer usually are the number of years."""
        if not isinstance(rate, float):
            raise TypeError("The discount rate must be a number.")
        if not isinstance(period, int):
            raise TypeError("The number of years must be an integer.")
        x =  np.arange(0, period+1, 1)
        y = self.value * (1 + rate) ** x
        return np.array([x, y])
    
    def predict_values_df(self, rate: float, period: int):
        """Predict the values of a money object.
        the discount rate is number, the period is an integer usually are the number of years."""
        if not isinstance(rate, float):
            raise TypeError("The discount rate must be a number.")
        if not isinstance(period, int):
            raise TypeError("The number of years must be an integer.")
        return pd.DataFrame(self.predict_values(rate, period).T, columns=["Period", "Value"])
    
    def show_values(self, rate: float, period: int):
        """Show the values of a money object.
        the discount rate is number, the period is an integer usually are the number of years."""
        if not isinstance(rate, float):
            raise TypeError("The discount rate must be a number.")
        if not isinstance(period, int):
            raise TypeError("The number of years must be an integer.")
        df = self.predict_values_df(rate, period)
        plt.plot(df["Period"], df["Value"])
        plt.xlabel("Period")
        plt.ylabel("Value")
        plt.show()
        return df
    
    def date_value(self,date:str):
        """Calculate the value of a money object at a specific date.
        the date is a string in the format YYYY-MM-DD."""
        if not isinstance(date, str):
            raise TypeError("The date must be a string.")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            raise ValueError("The date must be in the format YYYY-MM-DD.")
        x = (datetime.date.fromisoformat(date) - self.date).days / 365
        x = round(x, 0)
        return self.value * (1 + self.year_rate) ** x

        