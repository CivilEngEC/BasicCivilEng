#EngUnits.py

"""A module that contain  and handle basic units for Engineering 
for developing free, open-source Software in python"""

import re
import numpy as np
import pandas as pd
import sympy as sym
import matplotlib.pyplot as plt
import datetime

def remove_parenthesis_un(unit:str):
        """Removes the parenthesis in the unit of the object."""
        if not isinstance(unit, str):
            raise TypeError("The unit must be a string")

        if "(" in unit and ")" in unit:
            #Clear the parenthesis from exponentials
            p = re.compile(r"""\^\(\-?\d+\.?\d*\)""" , re.X)
            for i in re.finditer(p, unit):
                t = i.group()
                q = t.replace("(","")
                q = q.replace(")","")
                unit = unit.replace(t,q)
            #Clear Parenthesis from division and multiplication   
            s = re.compile(r"""/\((.+?)\)""" , re.X)
            aux = re.findall(s, unit)
            unit = re.sub(s, r"", unit)
            unit = unit.replace("(", "")
            unit = unit.replace(")", "")  
            def aux_f(aux):
                aux = aux.replace("*", "?")
                aux = aux.replace("/", "*")
                aux = aux.replace("?", "/")
                aux = "/"+aux
                return aux
            vaux_f = np.vectorize(aux_f)
            aux = np.array(aux)
            if list(aux) != []:
                aux = vaux_f(aux)
                aux = "".join(aux)
                unit = unit + aux
        elif "(" in unit or ")" in unit: 
            raise ValueError("The unit is not valid")  
        return unit

def from_string(string:str, units, class_name):
    """Creates a new object from a string with the value and the unit separated by a space"""
    if not isinstance(string, str):
        raise TypeError("The input must be a string")
    if not isinstance(units, Units):
        raise TypeError("The unit must be an instance of the Units class")
    if not isinstance(class_name, type):
        raise TypeError("The class_name must be a class")
    if not issubclass(class_name, Quantity):
        raise TypeError("The class_name must be a subclass of Quantity")
    string = string.strip().replace(",", "")
    if re.match(r"^\d+\.?\d*\s\w+$", string) is None:
        raise ValueError("""The input string is not in the correct format. Examples of the correct format are '2 m', '2,000.00 m', '2000.00 m' """)
    string = string.split() 
    value = float(string[0])
    symbol = string[1]
    return class_name(value, symbol, units)

class Units:
    """This class will constitute a blueprint and parent class for Units of messurement in Engineering"""
    def __init__(self):
        #Units and their conversion to the main unit
        #time
        Time = [
            ("Second","s", 1/3600), 
            ("Minute","min", 1/60), 
            ("Hour","h", 1), 
            ("Day","day", 24),
            ("Week","week", 168),
            ("Month","month", 730), 
            ("Year","year", 8760)
            ]
        #length
        Length = [ 
            ("Milimeter","mm", 0.001),
            ("Centimeter","cm", 0.01),
            ("Inch","in", 0.0254),
            ("Decimeter","dm",0.1),
            ("Foot","ft", 0.3048),
            ("Yard","yd", 0.9144),
            ("Meter","m", 1), 
            ("Kilometer","km", 1000), 
            ("Mile","mi", 1609.34),
            ("Nautical Mile","nmi", 1852)
            ]
        #lenght*Lenght        
        Area = [
            ("Square milimeter","mm^2", 0.000001,"mm*mm"), 
            ("Square centimeter","cm^2", 0.0001,"cm*cm"), 
            ("Square inch","in^2", 0.00064516, "in*in"),
            ("Square foot","ft^2", 0.092903,"ft*ft"), 
            ("Square decimeter","dm^2",0.01,"dm*dm"),
            ("Square yard","yd^2", 0.836127,"yd*yd"),
            ("Square meter","m^2", 1,"m*m"),
            ("Are","a", 100,"100*m*m"), 
            ("Acre","ac", 4046.86,"43560*ft*ft"),
            ("Hectare","ha", 10000,"10000*m*m"),                 
            ("Square kilometer","km^2", 1000000,"km*km"), 
            ("Square mile","mi^2", 2589988.11,"mi*mi")
            ]
        #lenght*lenght*lenght   
        Volume = [
            ("Cubic milimeter","mm^3", 0.000000001,"mm*mm*mm"), 
            ("Cubic centimeter","cm^3", 0.000001,"cm*cm*cm"), 
            ("Mililiter","ml", 0.000001,"cm*cm*cm"),
            ("Cubic inch","in3", 0.0000163871,"in*in*in"),
            ("Fluid ounce","floz", 0.0000295735,"1.80469*in*in*in"),
            ("Cup","cup", 0.000236588,"14.4375*gal"),
            ("Pint","pt", 0.000473176,"28.875*gal"),
            ("Quart","qt", 0.000946353,"57.75*in*in*in"),    
            ("Liter","l", 0.001,"dm*dm*dm"),
            ("Cubic decimeter","dm^3",0.001,"dm*dm*dm"), 
            ("Gallon","gal", 0.00378541,"231*in*in*in"),
            ("Cubic foot","ft3", 0.0283168,"ft*ft*ft"),
            ("Cubic yard","yd3", 0.764555,"yd*yd*yd"),
            ("Cubic meter","m^3", 1,"m*m*m"),
            ("Cubic kilometer","km^3", 1000000000,"km*km*km"),
            ("Cubic mile","mi^3", 4168181825.44,"mi*mi*mi")
            ]
        #mass              
        Mass = [
            ("Miligram","mg", 0.000001),
            ("Gram","g", 0.001),
            ("Ounce","oz", 0.0283495),  
            ("Pound","lb", 0.453592), 
            ("Kilogram","kg", 1),
            ("Kilopound","klb", 453.592),  
            ("Metric Tonne","t", 1000),
            ]
        #mass*lenght/time^2
        Force = [
            ("Dyne","dyn", 0.00001, "g*cm/s^2"),
            ("Poundal","pdl", 0.138255, "lb*ft/s^2"),
            ("Newton","N", 1, "kg*m/s^2"),
            ("Force pound","lbf", 4.44822, "32.174*lb*ft/s^2"),
            ("Force kilogram","kgf", 9.80665,"9.80665*Kg*m/s^2"),
            ("Force Kilopound","kips", 4448.22,"32.174*klb*ft/s^2"), 
            ("Kilonewton","kN", 1000,"t*m/s^2"),
            ("Metric force Tonne","tf", 9806.65,"9.80665*t*m/s^2"),
            ("Meganewton","MN", 1000000,"1000*t*m/s^2")
            ]
        #Force/area
        Pressure = [
            ("Pascal","Pa", 1, "N/m^2"), 
            ("Pound per square inch", "psi", 6894.76,"lbf/in^2"), 
            ("Kilopascal","kPa", 1000,"kN/m^2"), 
            ("Bar","bar", 100000,"100*kN/m^2"),
            ("Atmosphere","atm", 101325,"101.325*kN/m^2"), 
            ("Megapascal","MPa", 1000000,"MN/m^2"), 
            ("Kilopound per square inch","ksi", 6894760,"kips/in^2"),
            ]
        #Force*lenght
        Energy = [
            ("Joule","J", 1,"N*m"), 
            ("Kilojoule","kJ", 100, "kN*m"), 
            ("Megajoule","MJ", 1000000, "MN*m"), 
            ("Gigajoule","GJ", 1000000000,"1000*MN*m"), 
            ("Watt hour","Wh", 3600,"3600*J"), 
            ("Kilowatt hour","kWh", 3600000,"3600*kJ"), 
            ("Megawatt hour","MWh", 3600000000,"3600*MJ"), 
            ("British thermal unit","Btu", 1055.06,"1055.06*J"), 
            ("Kilocalories","kcal", 4184,"4184*J"),
            ("Calories","cal", 4.184,"4.184*J"),
            ]
        
        Power = [
            ("Watt","W", 1, "J/s"), 
            ("Kilowatt","kW", 1000,"kJ/s"), 
            ("Megawatt","MW", 1000000,"MJ/s"), 
            ("Gigawatt","GW", 1000000000,"GJ/s"), 
            ("Horse power","hp", 745.7,"745.7*J/s"), 
            ("Steam horse power","cv", 735.5,"735.5*J/s")
            ]
        #ElectricCurren
        ElectricCurrent = [
            ("Ampere","A", 1), 
            ("Miliampere","mA", 0.001,), 
            ("Kiloampere","kA", 1000)
            ]
        #Electriccurr*time
        
        ElectricCharge = [
            ("Coulomb","C", 1,"A*s"), 
            ("Microcoulomb","mC", 0.001,"mA*s"), 
            ("Kilocoulomb","kC", 1000,"kA*s")
            ]

        ElectricPotential = [
            ("Voult","V", 1, "W/A"),
            ("kilovolt","kV", 1000, "kW/kA")
            ]
        #Temperature
        Temperature = [
            ("Kelvin","K", 1), 
            ("Celcius","oC", 1), 
            ("Farenheit","F", 1)
            ]
        #Luminosity
        LIntensity = [
            ("Candela","cd", 1), 
            ("Kilocandela","kcd", 1000), 
            ("Microcandela","mcd", 0.001)
            ]
        #Luminosity*solid angle
        LFlux = [
            ("Lumen","lm", 1), 
            ("Kilolumen","klm", 1000), 
            ("Microlumen","mlm", 0.001)
            ]
        #Luminosity*solid angle/area
        iluminance = [
            ("Lux","lx", 1, "lm/m^2"), 
            ("kiloLux","klx", 1000, "klm/m^2"), 
            ("MiliLoux","mlx", 0.001, "mlm/m^2"),
            ("footcandle","ft-cd", 10.7639, "lm/ft^2")
            ]
        #Angle Lenght/Length
        Angle = [
            ("Radian","rad", 1),
            ("Degree","deg", 0.0174533)
            ]
        #Currency
        Currency = [("US Dollar", "USD", 1,""),
                    ("Euro", "EUR", 1.12,""),
                    ("British Pound", "GBP", 1.29,""),
                    ("Russian Ruble", "RUB", 0.014,""),
                    ("Chinese Yuan", "CNY", 0.15,""),
                    ("Indian Rupee", "INR", 0.014,""),
                    ("Argentine Peso", "ARS", 0.011,""),
                    ("Brazilian Real", "BRL", 0.19,""),
                    ("Paraguayan Guarani", "PYG", 0.0014,""),
                    ("Uruguayan Peso", "UYU", 0.023,""),
                    ("Mexican Peso", "MXN", 0.052,"")
                    ]
    
        #Dictionary of base units
        self.dic_units = {"Time": Time,
                            "Length": Length,
                            "Mass": Mass,
                            "ElectricCurrent": ElectricCurrent,
                            "Temperature": Temperature,
                            "Luminus Intensity": LIntensity,
                            "Angle": Angle,
                            "Area": Area,
                            "Volume": Volume,
                            "Force": Force,
                            "Pressure": Pressure,
                            "Energy": Energy,
                            "Power": Power,
                            "ElectricCharge": ElectricCharge,
                            "ElectricPotential": ElectricPotential,
                            "LuminousFlux": LFlux,
                            "Iluminance": iluminance,
                            "Currency": Currency}

        columns = ["Name", "Symbol", "Factor", "Description"]
        
        def to_df(dic):
          for d in dic:
            if len(dic[d][0]) == 3:
                dic[d] = pd.DataFrame(dic[d], columns=columns[:3])
                dic[d][columns[-1]] = ""
                dic[d].set_index("Symbol", inplace=True)
            else:
                dic[d] = pd.DataFrame(dic[d], columns=columns)
                dic[d].set_index("Symbol", inplace=True)
          return dic
        
        to_df(self.dic_units)

        #List of all symbols units in the class
        L =[]
        #Check if there are repeated units symbols
        for d in self.dic_units:
            L = L + self.dic_units[d].index.tolist()
        self.all_units = L
        L = np.array(L)
        L,c = np.unique(L, return_counts=True)
        if np.any(c>1):
            raise ValueError("The are repeated symbols in the units database")
        
        self.unit_system = {"Time": "s",
                            "Length": "m",
                            "Mass": "kg",
                            "ElectricCurrent": "A",
                            "Temperature": "K",
                            "Luminus Intensity": "cd",
                            "Angle": "rad",
                            "Area": "m^2",
                            "Volume": "m^3",
                            "Force": "N",
                            "Pressure": "Pa",
                            "Energy": "J",
                            "Power": "W",
                            "ElectricCharge": "C",
                            "ElectricPotential": "V",
                            "LuminousFlux": "lm",
                            "Iluminance": "lx",
                            "Currency": "USD"}
   
    def find_unit(self, unit):
        """Checks if the unit is supported by the object.
        Returns name where the unit is allocated and False if not."""

        if unit in self.all_units:
            for d in self.dic_units:
                if unit in self.dic_units[d].index:
                    name = d
                    break
            return name
        else:
            return False
        
    def append(self, name:str, record:list):
        """Append a new unit to the units DataFrame.
        name must be a string with the name of the physical quantity.
        ther reord must be a list with the following structure:
        [name, symbol, factor, Description]"""
        if not isinstance(name, str):
            raise TypeError("The name must be a string")
        try:
            record = list(record)
        except:
            raise TypeError("The record must be a list like object")
        if len(record) != 4:
            raise ValueError("The record must have 4 elements")
        if not isinstance(record[0], str):
            raise TypeError("The name must be a string")
        if not isinstance(record[1], str):
            raise TypeError("The symbol must be a string")
        if not isinstance(record[2], (int, float)):
            raise TypeError("The factor must be a number")
        if self.find_unit(record[1]):
           raise ValueError(f"""The symbol {record[1]} is already used by the object for messure {self.find_unit(record[1])}, please use another symbol""")
        else:
            symbol = record[1]
            record = pd.DataFrame([record], columns=["Name", "Symbol", "Factor", "Description"])
            record =  record.set_index("Symbol")
            self.dic_units[name] =  pd.concat([self.dic_units[name], record])
            self.all_units.append(symbol)

    def remove(self, symbol:str):
        """Removes a unit from the unit DataFrame."""
        name =  self.find_unit(symbol)
        if name:
            self.dic_units[name].drop(symbol, inplace=True)
            self.all_units.remove(symbol)
        else:
            raise ValueError("The unit is not find inside the object")
        
    def empty(self, name:str):
        """Empty units DataFrame from the name physical quantity."""
        if not isinstance(name, str):
            raise TypeError("The name must be a string")
        if name in self.dic_units:
            for symbol in self.dic_units[name].index:
                self.all_units.remove(symbol)
            self.dic_units[name] = pd.DataFrame(columns=["Name", "Symbol", "Factor", "Description"])
        else:
            raise ValueError("The name of the physical quantity is not find inside the object")
    
    def set_units(self, units:pd.DataFrame, name:str):
        """Sets the units Dataframe of a given physical quantities.
        unit must be a DataFrame with the columns Name, Symbol, Factor and Description
        The factor  columnn must contain number values and at least one row must have the factor column = 1.
        The symbol column must contain string values."""
        
        if not isinstance(units, pd.DataFrame):
            raise TypeError("The units must be a dataframe")
        if not set(units.columns) == set(["Name", "Symbol", "Factor", "Description"]):
            raise ValueError("The units dataframe must have the columns Name, Symbol, Factor and Description")
        if not np.all(units["Symbol"].apply(lambda x: isinstance(x, str))):
            raise ValueError("The symbol column must contain string values")
        if not np.all(units["Factor"].apply(lambda x: isinstance(x, (int, float)))):
            raise ValueError("The factor column must contain number values")
        if not np.any(units["Factor"] == 1):
            raise ValueError("At least one unit has to have the factor 1")
        if not isinstance(name, str):
            raise TypeError("The name must be a string")
            
        #Check if there are repeated units symbols
     
        if name not in self.dic_units:
            for row in units.iterrows():
                if self.find_unit(row[1]["Symbol"]):
                    raise ValueError(f"""The symbol {row[1]["Symbol"]} is already used by the object for messure {self.find_unit(row[1]["Symbol"])}, please use another symbol""")
                else:
                   self.all_units.append(row[1]["Symbol"])
        else:
            if self.dic_units[name].index.tolist() == []:
                pass
            else:
                for x in self.dic_units[name].index:
                    self.all_units.remove(x)       
            for x in units["Symbol"].tolist():
                if self.find_unit(x):
                    raise ValueError(f"""The symbol {x} is already used by the object for messure {self.find_unit(x)}, please use another symbol""")
                else:
                    self.all_units.append(x)

        units = units.set_index("Symbol")
        self.dic_units[name] = units 
        self.unit_system[name] = units.loc[units["Factor"] == 1].index[0]

    def set_unit_system (self, system_dic:dict):
        """Set unit sytem for symplify all unit.
        The keys of the dictionary are the physical quantity name and the values are the symbol 
        of the main unit of the physical quantity."""
        if not isinstance(system_dic, dict):
            raise TypeError("The system dictionary must be a dictionary")
        
        for k in system_dic:
            if  k not in self.unit_system:
                raise ValueError(f"The key {k} is not recognized as a physical quantity, please add it using .set_units")
            if system_dic[k] not in self.dic_units[k].index:
                raise TypeError(f"The physical quantity {k} does not have the unit {system_dic[k]}")
            else:
                self.unit_system[k] = system_dic[k]  
        
    
    def simplify(self, unit:str):

        """ Perform an algebraic simplification of the unit using the unit system."""
        if not isinstance(unit, str):
            raise TypeError("The unit must be a string")
        
        def to_symbol(x, y):
                arg = re.search(r"[a-zA-Z]+", x).group()
                c = re.search(r"\-?\d+\.?\d*", x)
                if c == None:
                    c = 1
                else:
                    c = c.group()
                    c = float(c)
                    c = round(c, 3)
                if arg in units.index:
                    y = (units.loc[arg]["Factor"]/units.loc[main_unit]["Factor"])**c
                    arg = main_unit
                else:
                    y = 1
                return sym.Symbol(arg)**c, y
        v_to_symbol = np.vectorize(to_symbol)
        
        value = 1

        for name in self.dic_units:
            units = self.dic_units[name]
            main_unit = self.unit_system[name]
            old_unit = remove_parenthesis_un(unit)
            if old_unit[0] != "1":
                old_unit = "*" + old_unit
            mult_un = re.findall(r"\*(\w+\^?\-?\d*\.?\d*)", old_unit)
            div_un = re.findall(r"/(\w+\^?\-?\d*\.?\d*)", old_unit)
            new = 1
            if mult_un != []:
                mult_un = np.array(mult_un)
                mult_un, mult_un_factor = v_to_symbol(mult_un, np.ones(len(mult_un)))
                mult_un = np.prod(mult_un)
                mult_un_factor = np.prod(mult_un_factor)
                new *= mult_un
                value *= mult_un_factor
            if div_un != []:
                div_un = np.array(div_un)
                div_un, div_un_factor = v_to_symbol(div_un, np.ones(len(div_un)))
                div_un = np.prod(div_un)
                div_un_factor = np.prod(div_un_factor)
                new /= div_un
                value /= div_un_factor
            new = str(new)
            new = new.replace("**1.0*", "*")
            new = new.replace("**1.0/", "/") 
            if new[-5:] == "**1.0":
                new = new[:-5]
            new =  new.replace("**", "^")
            unit = new
           
        return unit, value
   
#Physical quantities class    
class Quantity:
    """This class will constitute a blueprint and parent class for Engineering quantities 
    -the value is the measure of the physical quantity
    -the symbol is the unit of the physical quantity
    -system_units is an instance of the class Units it is used as interpreter of the unit
    -decimal is the number of decimal places to be displayed
    -name is the name of the physical quantity
    """
   
    def __init__(self, value:float, symbol:str, system_units:Units, decimal:int=3):
               
        #Check the type of the arguments
        if not isinstance(value, (int, float)):
            raise TypeError("The value must be a number")
        if not isinstance(symbol, str):
            raise TypeError("The unit must be a string")
        if not isinstance(decimal, int):
            raise TypeError("The decimal places must be an integer")
        if not isinstance(system_units, Units):
            raise TypeError("The units must be an instance of the class Units")
        
        self.value = value
        self.symbol = symbol
        self.decimal = decimal
        self.system_units = system_units
        self.name = "" #Name of the physical quantity
        if symbol in self.system_units.all_units:
            self.name = self.system_units.find_unit(symbol)
        if self.name == "":
            self.units = {}
            self.main_unit = ""
        elif self.name in system_units.dic_units:
            self.units = system_units.dic_units[self.name]["Factor"].to_dict()
            self.main_unit = system_units.unit_system[self.name]
        else:
            raise ValueError(f"The name of the physical quantity is not supported by the Units object, please use .set_units() method to add the physical quantity to the Units object, the list name that are supported is {system_units.dic_units.keys()}")

    #Magic Methods
    def __repr__(self):
        return f"{self.name}:({self.value}, '{self.symbol}')"
    
    def __float__(self):
        return float(self.value)
    
    def __int__(self):
        return int(self.value)
    
    def __str__(self):
        return f"{round(self.value,self.decimal):,} {self.symbol}"
    
    #Methods
   
    def is_related(self, other):
        """Checks if the object are related one another."""
        try:
            if issubclass(type(other), Quantity):
                return True
            else:
                return False
        except:
            return False
    
    def get_units(self):
        """Returns the units Dataframe."""
        return self.units
    
    def update_units(self, units:Units):
        """Updates the units DataFrame."""
        if not isinstance(units, Units):
            raise TypeError("The units must be an instance of the class Units")
        else:
            new = self.__class__(value=self.value,
                                    symbol=self.symbol,
                                    system_units=units,
                                    decimal=self.decimal)
            return new
        
    def set_factors(self, factors:dict):
        """Sets the factors of the units Dictionary."""
        main_unit = False
        if not isinstance(factors, dict):
            raise TypeError("The factors must be a dictionary")
        for key, value in factors.items():
            if key in self.units.keys():
                self.units[key]= value
            else:
                raise ValueError(f"The key {key} is not in the units Dictionary")
        for key, value in self.units.items():
                if value == 1:
                    self.main_unit = key
                    main_unit = True
        if not main_unit:
            raise ValueError("The dictionary must have a main unit which factor is 1")
    
    def simplify(self):
        """Performs an algebraic simplification the unit of the object."""
        
        #Check if the unit has parenthesis 
        symbol, factor = self.system_units.simplify(self.symbol)
        value = self.value*factor
        new = self.__class__(value=value,
                             symbol=symbol,
                             system_units=self.system_units)
        return new
        

    def convert(self, new_unit:str, factor:float=False):
        """Converts the value of the object to the unit specified in the unit argument."""
        if not isinstance(new_unit, str):
            raise TypeError("The unit must be a string")
        if not isinstance(factor, (int, float, bool)):
            raise TypeError("The factor must be a number or False")
        
        if factor:
            value= self.value * factor
            symbol = new_unit    
        else:
            if self.system_units.find_unit(new_unit):
                factor = self.units[self.symbol]/ self.units[new_unit]
                value = self.value * factor
                symbol = new_unit
            else:
                raise ValueError("Unit not supported, please specify a conversion factor")
        new = self.__class__(value=value,
                             symbol=symbol,
                            system_units=self.system_units,
                            decimal=self.decimal)
        return new

    #Basic operators

    def __add__(self, other):
        """Adds two objects of the same class and returns a new object of the same class."""
        
        if self.is_related(other) and self.name == other.name:
            if self.symbol != other.symbol:
                if self.symbol in self.units.keys() and other.symbol in self.units.keys():
                    factor = self.units[other.symbol]/self.units[self.symbol]
                    value = self.value + other.value * factor
                    result = self.__class__(value=value,
                                            symbol=self.symbol, 
                                            system_units=self.system_units, 
                                            decimal=self.decimal)
                    result.set_factors(self.units)
                    return result
                else:   
                    raise TypeError(f"""The units of the object that you are trying to add don't match. The units that can be add are:
                    {self.units.keys()}""")
            else:
                value = self.value + other.value
                result = self.__class__(value=value, 
                                        symbol=self.symbol,
                                        system_units=self.system_units,
                                        decimal=self.decimal)
               
                result.set_factors(self.units)
                return result
        else:
            raise TypeError(f"Can only add {self.name} quantities")

    def __sub__(self, other):

        if self.is_related(other) and self.name == other.name:
            if self.symbol != other.symbol:
                if self.symbol in self.units.keys() and other.symbol in self.units.keys():
                    factor = self.units[other.symbol]/self.units[self.symbol]
                    value = self.value - other.value * factor
                    result = self.__class__(value=value, 
                                            symbol=self.symbol,
                                            system_units=self.system_units,
                                            decimal=self.decimal)
                    result.set_factors(self.units)
                    return result
                else:   
                    raise TypeError(f"""The units of the object that you are trying to substract don't match. The units that can be substract are:
                    {self.units.keys()}""")
            else:
                value = self.value - other.value
                result = self.__class__(value=value, 
                                        symbol=self.symbol, 
                                        system_units=self.system_units,
                                        decimal=self.decimal)
                result.set_factors(self.units)
                return result
        else:
            raise TypeError(f"Can only substract {self.name} quantities")
        
    def __mul__(self, other):
        if self.is_related(other) or isinstance(other, (int, float, np.ndarray, pd.Series, pd.DataFrame)):
            if self.is_related(other):
                result = Quantity( value = self.value * other.value,
                                        symbol= self.symbol +"*"+ other.symbol,
                                        system_units=self.system_units,
                                        decimal=self.decimal)
                return result
            
            elif isinstance(other, (int, float)):
                result = self.__class__( value = self.value * other,
                                        symbol= self.symbol,
                                        system_units=self.system_units,
                                        decimal=self.decimal)
                return result
            
            elif isinstance(other, (np.ndarray, pd.Series, pd.DataFrame)):
                    result = other*self
                    return result    
        else:
            raise TypeError("Can only multiply by similar, numbers like objects, or arrays of numbers like objects")
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def __truediv__(self, other):
        if self.is_related(other) or isinstance(other, (int, float)):
            if self.is_related(other):
                other.symbol = other.symbol.replace("*", "?")
                other.symbol = other.symbol.replace("/", "*")
                other.symbol = other.symbol.replace("?", "/")
                result = Quantity( value = self.value / other.value,
                                        symbol= self.symbol +"/"+ other.symbol,
                                        system_units=self.system_units,
                                        decimal=self.decimal)
                return result
            
            elif isinstance(other, (int, float)):
                result = self.__class__( value = self.value / other,
                                        symbol= self.symbol,
                                        system_units=self.system_units,
                                        decimal=self.decimal)
                return result
        else:
            raise TypeError("Can only divide by similar or numbers like objects")
    
    def __pow__(self, other):
        if isinstance(other, (int, float)):

            def to_symbol(x):
                arg = re.search(r"[a-zA-Z]+", x).group()
                c = re.search(r"\-?\d+\.?\d*", x)
                if c == None:
                    c = 1
                else:
                    c = c.group()
                    c = float(c)
                    c = round(c, 3)
                    y = 1
                return sym.Symbol(arg)**c
            v_to_symbol = np.vectorize(to_symbol)
            old_unit = remove_parenthesis_un(self.symbol)
            if old_unit[0] != "1":
                old_unit = "*" + old_unit
            mult_un = re.findall(r"\*(\w+\^?\-?\d*\.?\d*)", old_unit)
            div_un = re.findall(r"/(\w+\^?\-?\d*\.?\d*)", old_unit)
            new = 1
            if mult_un != []:
                mult_un = np.array(mult_un)
                mult_un = v_to_symbol(mult_un)
                mult_un = np.prod(mult_un)
                new *= mult_un
            if div_un != []:
                div_un = np.array(div_un)
                div_un = v_to_symbol(div_un)
                div_un = np.prod(div_un)
                new /= div_un
            new  = new**other
            new = sym.powdenest(new, force=True)
            print(new)
            new = str(new)
            new = new.replace("**1.0*", "*")
            new = new.replace("**1.0/", "/") 
            if new[-5:] == "**1.0":
                new = new[:-5]
            new =  new.replace("**", "^")
            unit = new
            result = self.__class__(value = self.value ** other, 
                                    symbol= unit,
                                    system_units=self.system_units,
                                    decimal=self.decimal)
            return result
        else:
            raise TypeError("Can only raise to the power of numbers like objects")

    #Inplace operators

    def __iadd__(self, other):
        if self.is_related(other) and self.name == other.name:
            if self.symbol != other.symbol:
                if self.symbol in self.units.keys() and other.symbol in self.units.keys():
                    factor = self.units[other.symbol]/self.units[self.symbol]
                    self.value = self.value + other.value * factor
                    self.symbol = self.symbol
                    return self
                else:   
                   raise TypeError(f"""The unit that you are trying to add is not supported the units that are supported are: {self.units.keys()}""")
            else:
                self.value = self.value + other.value
                self.symbol = self.symbol
                return self 
        else:
            raise TypeError(f"Can only add {self.name} quantities")
        
    def __isub__(self, other):
        if self.is_related(other) and self.name == other.name:
            if self.symbol != other.symbol:
                if self.symbol in self.units.keys() and other.symbol in self.units.keys():
                    factor = self.units[other.symbol]/self.units[self.symbol]
                    self.value = self.value - other.value * factor
                    self.symbol = self.symbol
                    return self
                else:   
                   raise TypeError(f"""The unit that you are trying to substract is not supported the units that are supported are: {self.units.index.to_list()}""")
            else:
                self.value = self.value - other.value
                self.symbol = self.symbol
                return self 
        else:
            raise TypeError(f"Can only substract {self.name} quantities")
          
    
    #Comparison operators

    def __eq__(self, other):
        if self.is_related(other):
            factor = self.units[other.symbol]/self.units[self.symbol]
            a = self.value 
            b = other.value * factor 
            return a == b
        else:
            raise TypeError("Can only compare similar objects")
    def __ne__(self, other):
        if self.is_related(other):
            factor = self.units[other.symbol]/self.units[self.symbol]
            a = self.value 
            b = other.value * factor 
            return a != b
        else:
            raise TypeError("Can only compare similar objects")
        
    def __lt__(self, other):
        if self.is_related(other):
            factor = self.units[other.symbol]/self.units[self.symbol]
            a = self.value 
            b = other.value * factor 
            return a < b
        else:
            raise TypeError("Can only compare similar objects")
        
    def __le__(self, other):
        if self.is_related(other):
            factor = self.units[other.symbol]/self.units[self.symbol]
            a = self.value 
            b = other.value * factor 
            return a <= b
        else:
            raise TypeError("Can only compare similar objects")
        
    def __gt__(self, other):
       if self.is_related(other):
            factor = self.units[other.symbol]/self.units[self.symbol]
            a = self.value 
            b = other.value * factor 
            return a > b
       else:
            raise TypeError("Can only compare similar objects")
        
    def __ge__(self, other):
       if self.is_related(other):
            factor = self.units[other.symbol]/self.units[self.symbol]
            a = self.value 
            b = other.value * factor 
            return a >= b
       else:
            raise TypeError("Can only compare similar objects")    
    
    #Unary operators

    def __neg__(self):
        self.value = -self.value
        return self
    def __pos__(self):
        self.value = +self.value
        return self
    def __abs__(self):
        self.value = abs(self.value)
        return self
    def __round__(self, n=0):
        self.value = round(self.value, n)
        return self
    def __floor__(self):
        self.value = self.value // 1
        return self
    def __ceil__(self):
        self.value = self.value // 1 + 1
        return self
    def __trunc__(self):
        self.value = self.value // 1
        return self
    
#Money class
class Money(Quantity):
    """Money class, inherits from Quantity class
    The money class should have in addition to all the atributes and methods of the Quantity 
    class the following:
        - A date attribute that stores the date of the transaction, the date should be a string in the 
        iso format this is YYYY-MM-DD
        - A year rate attribute that stores the interest rate of the transaction
        - A method that calculates the future value of the money
        - A method that calculates the present value of the money
        - and other financial methods that you think are relevant"""
    def __init__(self, value, symbol, system_units, date:str="", year_rate:float=0.0, decimal:int=2):
        super().__init__(value, symbol, system_units, decimal=2)
        if not isinstance(date, str):
            raise TypeError("Date should be a string")
        if date == "":
            self.date = datetime.date.today()
        else:
            try: 
                self.date = datetime.date.fromisoformat(date)
            except Exception as e:
                raise ValueError( str(e) + ". Date should be in the iso format YYYY-MM-DD")
        if not isinstance(year_rate, (float, int)):
            raise TypeError("Year rate should be a number")
        self.date = date
        self.year_rate = year_rate

    def time_value(self, n:int, rate:float=None):
        """Calculates the value of the money at the end of n periods
        n: number of payment periods, if it is positive it is the future value, 
        if it is negative it is the present/past value
        rate: interest rate"""
        if not isinstance(n, int) and n==0:
            if n == 0:
                raise ValueError("n should be different from 0")
            try:
                n = float(n)
                if round(n,0) ==  round(n,2):
                    n = int(n)
                else:
                    raise TypeError("n should be an integer like object")
            except:
                raise TypeError("n should be an integer")
        if rate == None:
            rate = self.year_rate
        if not isinstance(rate, (float, int)):
            raise TypeError("rate should be a number")
        value = self * (1 + rate)**n
        return value
    
    def show_values(self, n:int, rate=None, plot=True):
        """Calculates the value of the money at the end of n periods
        n: number of payment periods, if it is positive it is the future value, 
        if it is negative it is the present/past value
        rate: interest rate, if its variable you can pass it as a list or array, with the
        same lenght as the number of periods, when you pass a list or array the rate is
        assumed to be constant for each period and the lenght of the list or array should
        be equal to the number of periods, if you pass a number the rate is assumed to be
        constant for all the periods. It always go from the period 0 to the period n
        plot: if True it plots the values"""
        if not isinstance(n, int) and n==0:
            if n == 0:
                raise ValueError("n should be different from 0")
            try:
                n = float(n)
                if round(n,0) ==  round(n,2):
                    n = int(n)
                else:
                    raise TypeError("n should be an integer like object")
            except:
                raise TypeError("n should be an integer")
        if rate == None:
            rate = self.year_rate
        if not isinstance(rate, (float, int, list, np.ndarray)):
            raise TypeError("rate should be a number or a list/array of numbers")
        if isinstance(rate, (list, np.ndarray)):
            if len(rate) != abs(n):
                raise ValueError(f"rate should have the lenght equal to the number of periods {n}")
            rate = np.array(rate)
        else:
            rate = np.ones(abs(n)) * rate
        if n > 0:
            x = np.arange(0, n+1, 1)
            rate = np.insert(rate, 0, 0)
            y = self*np.cumprod(1 + rate)
            
        elif n < 0:
            x = np.arange(n, 1, 1)
            rate = np.insert(rate, 0, 0)
            y = self*np.cumprod(1/(1 + rate))
            rate = np.flip(rate)
            y = np.flip(y)

        if plot:
            plt.plot(x, y)
            plt.xlabel("Period")
            plt.ylabel("Value")
            plt.show()
        return pd.DataFrame({"Period":x, "Value":y, "Rate":rate}).set_index("Period")
    
    def date_value(self,date:str, year_rate:float=None):
        """Calculate the value of a money object at a specific date.
        the date is a string in the format YYYY-MM-DD."""
        if year_rate == None:
            year_rate = self.year_rate
        if not isinstance(year_rate, (float, int, list, np.ndarray)):
            raise TypeError("rate should be a number or a list/array of numbers")
        if not isinstance(date, str):
            raise TypeError("The date must be a string.")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            raise ValueError("The date must be in the format YYYY-MM-DD.")
        n = (datetime.date.fromisoformat(date) - self.date).days / 365
        n = round(n, 0)
        return self * (1 + year_rate) ** n
    
    def sinking_fund(self, n: int, rate: float, as_series:bool=False):
        """Calculate the sinking fund of a money object. It is used to determine a series of equal payments 
        or receipts at the end of each period that is equivalent to a stated or required future sum
        the rate is the value that will be add if rate is positive or substracted if negative at the end of each period, 
        the period is an integer usually are the number of years.
        -n: number of periods
        -rate: interest rate"""

        if not isinstance(rate, float):
            raise TypeError("The discount rate must be a number.")
        if not isinstance(n, int):
            try:
                n = float(n)
                if round(n,0) ==  round(n,2):
                    n = int(n)
                else:
                    raise TypeError("n should be an integer like object")
            except:
                raise TypeError("n should be an integer")
        if not isinstance(as_series, bool):
            raise TypeError("as_series must be a boolean.")
        factor = rate/((1 + rate)**n - 1)
        y = self * factor * np.ones(n)
        x = np.arange(1, n+1, 1)
        result = pd.Series(y, index=x)
        if as_series:
            return result
        else:
            return result.iloc[0]
    
    def capital_recovery(self, n: int, rate: float, as_series:bool=False):
        """Calculate the capital recovery of a money object. It is used to determine a series of equal payments 
        or receipts at the end of each period that is equivalent to a stated or required present sum
        the rate is the value that will be add if rate is positive or substracted if negative at the end of each period, 
        the period is an integer usually are the number of years.
        -n: number of periods
        -rate: interest rate"""

        if not isinstance(rate, float):
            raise TypeError("The discount rate must be a number.")
        if not isinstance(n, int):
            try:
                n = float(n)
                if round(n,0) ==  round(n,2):
                    n = int(n)
                else:
                    raise TypeError("n should be an integer like object")
            except:
                raise TypeError("n should be an integer")
        if not isinstance(as_series, bool):
            raise TypeError("as_series must be a boolean.")
        factor = (rate*(1+rate)**n)/((1 + rate)**n - 1)
        y = self * factor * np.ones(n)
        x = np.arange(1, n+1, 1)
        result = pd.Series(y, index=x)
        if as_series:
            return result
        else:
            return result.iloc[0]

    def sinked_fund(self, n:int, rate:float):
        """Calculate the sinked fund of a money object. 
        It is used to determine the future value of a series of equal payments or 
        receipts at the end of each period"""
        if not isinstance(rate, float):
            raise TypeError("The discount rate must be a number.")
        if not isinstance(n, int):
            try:
                n = float(n)
                if round(n,0) ==  round(n,2):
                    n = int(n)
                else:
                    raise TypeError("n should be an integer like object")
            except:
                raise TypeError("n should be an integer")
        factor = ((1 + rate)**n - 1)/rate
        return self * factor
    
    def recovered_capital(self, n:int, rate:float):
        """Calculate the recovered capital of a money object. 
        It is used to determine the present value of a series of equal payments or 
        receipts at the end of each period"""
        if not isinstance(rate, float):
            raise TypeError("The discount rate must be a number.")
        if not isinstance(n, int):
            try:
                n = float(n)
                if round(n,0) ==  round(n,2):
                    n = int(n)
                else:
                    raise TypeError("n should be an integer like object")
            except:
                raise TypeError("n should be an integer")
        factor = ((1 + rate)**n - 1)/(rate*(1 + rate)**n)
        return self * factor

#Cash Flow
def cash_flow(inflow, outflow, n:int, rate:float, plot:bool=True):
    """Calculate the cash flow of a money.
    It plots the cash flow, returns a dataframe with the cash flow and the net cash flow 
    and the net present value.
    Inflow and outflow can be a tuple (period, value) for representing single paymentes, 
    or pd.series in wich the index is the period and the values 
    are the sum of the money for each period, to represent multiple payments 
    A list of different pd.series and tuples to represent multiple different of payments.
    n: number of periods
    rate: interest rate"""
    if not isinstance(rate, float):
        raise TypeError("The discount rate must be a number.")

    if not isinstance(n, int):
            try:
                n = float(n)
                if round(n,0) ==  round(n,2):
                    n = int(n)
                else:
                    raise TypeError("n should be an integer like object")
            except:
                raise TypeError("n should be an integer")
    if not isinstance(plot, bool):
        raise TypeError("plot must be a boolean.")
    if not isinstance(inflow, (tuple, list, pd.Series)):
        raise TypeError("inflow should be a number a tuple, Series or a list of tuples or Series")
    if not isinstance(outflow , (tuple, list, pd.Series)):
        raise TypeError("outflow should be a number a tuple, Series or a list of tuples or Series")
    
    if isinstance(inflow, tuple):
        if not isinstance(inflow[0], (np.int64,int)):
            raise TypeError("The period must be an integer.")
        elif not isinstance(inflow[1], Money):
            raise TypeError("The value must be a Money object.")
        else:
            inflow = pd.Series(inflow[1], index=[inflow[0]])
    
    if isinstance(outflow, tuple):
        if not isinstance(outflow[0], (np.int64,int)):
            raise TypeError("The period must be an integer.")
        elif not isinstance(outflow[1], Money):
            raise TypeError("The value must be a Money object.")
        else:
            outflow = pd.Series(outflow[1], index=[outflow[0]])

    if isinstance(inflow, pd.Series):
        if not isinstance(inflow.index[0], (np.int64,int)):
            raise TypeError("The period must be an integer.")
        elif not isinstance(inflow.iloc[0], Money):
            raise TypeError("The value must be a Money object.")
    
    if isinstance(outflow, pd.Series):
        if not isinstance(outflow.index[0], (np.int64,int)):
            raise TypeError("The period must be an integer.")
        elif not isinstance(outflow.iloc[0], Money):
            raise TypeError("The value must be a Money object.")
    
    cero = Money(0, "USD", Units())
    
    if isinstance(inflow, list):
        for i in range(len(inflow)):
            if not isinstance(inflow[i], (tuple, pd.Series)):
                raise TypeError("inflow should be a list a tuple or Series")
            if isinstance(inflow[i], pd.Series):
                if not isinstance(inflow[i].index[0], (np.int64,int)):
                    raise TypeError("The period must be an integer.")
                if not isinstance(inflow[i].iloc[0], Money):
                    raise TypeError("The value must be a Money object.")
            if isinstance(inflow[i], tuple):
                if not isinstance(inflow[i][0], (np.int64,int)):
                    raise TypeError("The period must be an integer.")
                if not isinstance(inflow[i][1], Money):
                    raise TypeError("The value must be a Money object.")
                inflow[i] = pd.Series(inflow[i][1], index=[inflow[i][0]])
            if i == 0:
                x = inflow[i]

            else:
                x = x.add(inflow[i], fill_value=cero)
           
        inflow = x
    if isinstance(outflow, list):
        for i in range(len(outflow)):
            if not isinstance(outflow[i], (tuple, pd.Series)):
                raise TypeError("outflow should be a list a tuple or Series")
            elif isinstance(outflow[i], pd.Series):
                if not isinstance(outflow[i].index[0], (np.int64,int)):
                    raise TypeError("The period must be an integer.")
                if not isinstance(outflow[i].iloc[0], Money):
                    raise TypeError("The value must be a Money object.")
            if isinstance(outflow[i], tuple):
                if not isinstance(outflow[i][0], (np.int64,int)):
                     raise TypeError("The period must be an integer.")
                if not isinstance(outflow[i][1], Money):
                    raise TypeError("The value must be a Money object.")
                outflow[i] = pd.Series(outflow[i][1], index=[outflow[i][0]])
            if i == 0:
                x = outflow[i]
            else:
                x = x.add(outflow[i], fill_value=cero)
        outflow = x
    
    Cash_flow = inflow.add(-outflow, fill_value = cero)
    net_cash_flow = Cash_flow.copy()
    def discount(x,y):
        z = x*(1 + rate)**(-y)
        return z
    discount = np.vectorize(discount)
    net_cash_flow = discount(net_cash_flow, net_cash_flow.index)
    df_cash_flow = pd.DataFrame({'Inflow':inflow, 
                                'Outflow':outflow,
                                "Cash_Flow":Cash_flow, 
                                'Net_Cash_Flow':net_cash_flow, 
                                "Net_Value":net_cash_flow.cumsum()})
    df_cash_flow.index.name = 'Period'
    df_cash_flow = df_cash_flow.fillna(cero)
    if plot:
        """Plot the cash flow, the inflow will be represented by a green arrow,
        the outflow by a red arrow and the net cash flow by a black line"""
        max = df_cash_flow['Inflow'].max()
        if df_cash_flow['Outflow'].max() > max:
            max = df_cash_flow['Outflow'].max()
        if df_cash_flow['Net_Cash_Flow'].max() > max:
            max = df_cash_flow['Net_Cash_Flow'].max()
        max = float(max)
        fig, ax = plt.subplots()
        for i in range(len(df_cash_flow)):
            outfl = df_cash_flow.iloc[i]['Outflow']
            outfl = - float(outfl)
            infl = df_cash_flow.iloc[i]['Inflow']
            infl = float(infl)
            netfl = df_cash_flow.iloc[i]['Net_Cash_Flow']
            netfl = float(netfl)
            if outfl != 0:
                ax.arrow(i,0,0,-outfl, width=0.1, head_width=0.2, head_length=max/100, fc='r', ec='r')
            if infl != 0:
                ax.arrow(i,0,0,infl, width=0.1, head_width=0.2, head_length=max/100, fc='g', ec='g')
        
        ax.plot(df_cash_flow.index, df_cash_flow['Net_Value'], 'k--')
        ax.set_xlabel('Period')
        ax.set_ylabel('Money')
        ax.set_title('Cash Flow')
        plt.show()

    return df_cash_flow

def find_rate(inflow, outflow, n, i_start:float = 0.01, error =0.05, iteration=100):
    """This function is used to find the discount rate that makes the net present value of a cash flow zero
    Inflow and outflow can be a tuple (period, value) for representing single paymentes, 
    or pd.series in wich the index is the period and the values 
    are the sum of the money for each period, to represent multiple payments 
    A list of different pd.series and tuples to represent multiple different of payments.
    n: number of periods
    i_start: initial guess for the discount rate
    error: the admissible error for the net present value
    iteration: the maximum number of iterations"""
    if not isinstance(n, (np.int64,int)):
        raise TypeError("The number of periods must be an integer.")
    if not isinstance(i_start, (float, int)):
        raise TypeError("The initial guess for the discount rate must be a number.")
    end = False
    i = i_start
    step = 0
    #check if the absolute value of the net present value is less than the error
    def check_rate(i):
        cash_flow_df = cash_flow(inflow=inflow, outflow=outflow, n=n, rate=i, plot = False)
        net_value = cash_flow_df['Net_Value'].iloc[-1]
        net_value = float(net_value)
        if abs(net_value) < error:
            return True,i, net_value, cash_flow_df
        else:
            return False, i, net_value, cash_flow_df
    #check if step is less than the maximum number of iterations
    def check_step(step, iteration):
        if step < iteration:
            pass
        else:
            raise ValueError("The maximum number of iterations has been reached.")

    while not end:
        try:
            step += 1
            check_step(step, iteration)
            if not end and i == i_start:
                end, i, net_value, cash_flow_df = check_rate(i)
                i_before = i
                net_value_before = net_value
                i = i + 0.01
                end, i, net_value, cash_flow_df = check_rate(i)
            if not end and net_value_before == net_value:
                while net_value_before == net_value:
                    step += 1
                    i = i + 0.01
                    check_step(step, iteration)
                    end, i, net_value, cash_flow_df = check_rate(i)
            if not end:
                i_aux = i
                i =  i - net_value*(i - i_before)/(net_value - net_value_before)
                i_before = i_aux
                net_value_before = net_value
                end, i, net_value, cash_flow_df = check_rate(i)
            print(step,i)
            if end:
                return i, cash_flow_df
            
        except Exception as e:
            end = True
            raise e
