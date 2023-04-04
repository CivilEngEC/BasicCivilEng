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
                            "Iluminance": iluminance}

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
                            "Iluminance": "lx"}
   
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

    
    
class Quantity:
    """This class will constitute a blueprint and parent class for Engineering quantities 
    -the value is the measure of the physical quantity
    -the unit use for measure the physical quantity
    -the decimal places that you want to show in the string representation of the object
    -the name of the physical quantity by default there are 12 physical quantities:
    ["Time", "Length", "Mass", "ElectricCurrent", "Temperature", "Luminus Intensity", "Angle"
    "Area", "Volume", "Force", "Pressure", "Energy", "Power", "ElectricCharge", "ElectricPotential",
    "LuminousFlux", "Iluminance"]
    By default the decimal places is 3 and the name is "Lenght" and the main units are SI units
    """
   
    def __init__(self, value:float, symbol:str, system_units:Units, decimal:int=3, name:str=""):
               
        #Check the type of the arguments
        if not isinstance(value, (int, float)):
            raise TypeError("The value must be a number")
        if not isinstance(symbol, str):
            raise TypeError("The unit must be a string")
        if not isinstance(decimal, int):
            raise TypeError("The decimal places must be an integer")
        if not isinstance(system_units, Units):
            raise TypeError("The units must be an instance of the class Units")
        if not isinstance(name, str):
            raise TypeError("The name of the physical quantity must be a string")
        
        self.name = name #Name of the physical quantity
        self.value = value
        self.symbol = symbol
        self.decimal = decimal
        self.system_units = system_units
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
                    result = self.__class__(value=value, symbol=self.symbol, name=self.name, 
                                            system_units=self.system_units, decimal=self.decimal)
                    result.set_factors(self.units)
                    return result
                else:   
                    raise TypeError(f"""The units of the object that you are trying to add don't match. The units that can be add are:
                    {self.units.keys()}""")
            else:
                value = self.value + other.value
                result = self.__class__(value=value, symbol=self.symbol, name=self.name, 
                                            system_units=self.system_units,decimal=self.decimal)
               
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
                    result = self.__class__(value=value, symbol=self.symbol, name=self.name, 
                                            system_units=self.system_units,decimal=self.decimal)
                    result.set_factors(self.units)
                    return result
                else:   
                    raise TypeError(f"""The units of the object that you are trying to substract don't match. The units that can be substract are:
                    {self.units.keys()}""")
            else:
                value = self.value - other.value
                result = self.__class__(value=value, symbol=self.symbol, name=self.name, 
                                            system_units=self.system_units,decimal=self.decimal)
                result.set_factors(self.units)
                return result
        else:
            raise TypeError(f"Can only substract {self.name} quantities")
        
    def __mul__(self, other):
        if self.is_related(other) or isinstance(other, (int, float)):
            try:
                result = self.__class__( value = self.value * other.value,
                                        symbol= self.symbol +"*"+ other.symbol,
                                        name = "",
                                        system_units=self.system_units,
                                        decimal=self.decimal)
                return result
            
            except AttributeError:
                result  = self.__class__( value = self.value * other, 
                                         symbol = self.symbol,
                                         name = "",
                                         system_units=self.system_units,
                                         decimal=self.decimal)
                
                return result
        else:
            raise TypeError("Can only multiply by similar or numbers like objects")
        
    def __truediv__(self, other):
        if self.is_related(other) or isinstance(other, (int, float)):
            try:
                other.symbol = other.symbol.replace("*", "?")
                other.symbol = other.symbol.replace("/", "*")
                other.symbol = other.symbol.replace("?", "/")
                result = self.__class__( value = self.value / other.value,
                                        symbol= self.symbol +"/"+ other.symbol,
                                        name = "",
                                        system_units=self.system_units,
                                        decimal=self.decimal)
                return result
            
            except AttributeError:
                result  = self.__class__( value = self.value / other, 
                                         symbol = self.symbol,
                                         name = "",
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
                                    name = "",
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
    
def from_string(string:str, units:Units, class_name=Quantity):
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
