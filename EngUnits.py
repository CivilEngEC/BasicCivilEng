#EngUnits.py

"""A module that contain  and handle basic units for Engineering 
for developing free, open-source Software in python"""

import re
import numpy as np
import pandas as pd
import sympy as sym

class CivilEngUnits:
    """This class will constitute a blueprint and parent class for Units in Civil Engineering
    -the value is the measure of the physical quantity
    -the unit use for measure the physical quantity
    -the decimal places that you want to show in the string representation of the object
    -the name of the physical quantity by default there are 12 physical quantities:
    ["Time", "Length", "Mass", "ElectricCurrent", "Temperature", "Luminus Intensity", "Angle"
    "Area", "Volume", "Force", "Pressure", "Energy", "Power", "ElectricCharge", "ElectricPotential",
    "LuminousFlux", "Iluminance"]
    By default the decimal places is 3 and the name is "Lenght" and the main units are SI units
    """
   
    def __init__(self, value:float, symbol:str, decimal:int=3, name:str="Length"):
        
        self.__parent = "CivilEngUnits" #Name of the parent class 
        
        #Check the type of the arguments
        if not isinstance(value, (int, float)):
            raise TypeError("The value must be a number")
        if not isinstance(symbol, str):
            raise TypeError("The unit must be a string")
        if not isinstance(decimal, int):
            raise TypeError("The decimal places must be an integer")
        if not isinstance(name, str):
            raise TypeError("The name of the physical quantity must be a string")
        
        self.name = name #Name of the physical quantity
        self.value = value
        self.symbol = symbol
        self.decimal = decimal
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

        columns = ["Name", "Symbol", "Factor", "Equation"]
        

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
        
        self.default_units = to_df(self.dic_units)

        #List of all symbols units in the class
        L =[]
        #Check if there are repeated units symbols
        for d in self.dic_units:
            L = L + self.dic_units[d].index.tolist()
        L = np.array(L)
        L,c = np.unique(L, return_counts=True)
        if np.any(c>1):
            raise ValueError("The are repeated symbols in the units database")
        self.all_units = L
        #Set the units dataframe
        if  self.name not in self.default_units:
            self.dic_units[self.name] = pd.DataFrame(columns=columns)
            self.dic_units[self.name] = self.dic_units[self.name].set_index("Symbol")
            self.units = self.dic_units[self.name]
        else:
            self.units = self.dic_units[self.name]
        #Set the default units system
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

    def from_string(self, string:str):
        """Creates a new object from a string with the value and the unit separated by a space"""
        if not isinstance(string, str):
            raise TypeError("The input must be a string")
        string = string.split()
        try:    
            self.value = float(string[0].replace(",", ""))
            self.symbol = string[1]
            return self
        except:
            raise ValueError("""The input string is not in the correct format. 
                             An example of the correct formtat is '2 m'""")
    
    def check_relationship(self, other):
        """Checks if the object are related one another."""
        
        try:
            if self._CivilEngUnits__parent == other._CivilEngUnits__parent:
                return True
            else:
                return False
        except AttributeError:
            return False
    
    def check_unit(self, unit:str=None):
        """Checks if the unit is supported by the object.
        Returns name where the unit is allocated and False if not."""
        if unit is None:
            unit = self.symbol
      
        if unit in self.all_units:

            for d in self.dic_units:
                if unit in self.default_units[d].index:
                    name = d
                    break
            return name
        else:
            return False
    
    def get_units(self):
        """Returns the units Dataframe."""
        return self.units
    
    def add_unit(self, symbol:str, factor:float, name:str="", equation:str=""):
        """Adds a new unit to the units DataFrame."""
        if not isinstance(symbol, str):
            raise TypeError("The unit must be a string")
        if not isinstance(factor, (int, float)):
            raise TypeError("The factor must be a number")
        if self.check_unit(symbol):
           raise ValueError(f"""The symbol is already used by the object for messure {self.check_unit()}, please use another symbol""")
        else:
            self.dic_units[self.name].loc[symbol] = [name, factor, equation]

    def remove_unit(self, symbol:str):
        """Removes a unit from the unit DataFrame."""
        if not isinstance(symbol, str):
            raise TypeError("The unit must be a string")
        if symbol in self.units.index:
           self.units.drop(symbol, inplace=True)
        else:
            raise ValueError("The unit is not in the unit DataFrame")

    def set_physical_quantity(self, name:str, units:pd.DataFrame):
        
        """Sets the physical quantity name of the object."""
        if not isinstance(units, pd.DataFrame):
            raise TypeError("The units must be a dataframe")
        if not set(units.columns) == set(["Name", "Symbol", "Factor", "Equation"]):
            raise ValueError("The units dataframe must have the columns Name, Symbol, Factor and Equation")
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
                if self.check_unit(row[1]["Symbol"]):
                    raise ValueError(f"""The symbol {row[1]["Symbol"]} is already used by the object for messure {self.check_unit(row[1]["Symbol"])}, please use another symbol""")
                else:
                    continue
        units = units.set_index("Symbol")
        self.dic_units[name] = units 
    
    
    
    def set_units(self, units:pd.DataFrame, name:str):
        """Sets the units Dataframe.
        unit must be a DataFrame with the columns Name, Symbol, Factor and Equation
        The factor  columnn must contain number values and at least one row must have the factor column = 1.
        The symbol column must contain string values."""
        
        if not isinstance(units, pd.DataFrame):
            raise TypeError("The units must be a dataframe")
        if not set(units.columns) == set(["Name", "Symbol", "Factor", "Equation"]):
            raise ValueError("The units dataframe must have the columns Name, Symbol, Factor and Equation")
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
                if self.check_unit(row[1]["Symbol"]):
                    raise ValueError(f"""The symbol {row[1]["Symbol"]} is already used by the object for messure {self.check_unit(row[1]["Symbol"])}, please use another symbol""")
                else:
                    continue
        units = units.set_index("Symbol")
        self.dic_units[name] = units 
        self.units = units
        self.name = name

    
    def remove_parenthesis_un(self):
        """Removes the parenthesis in the unit of the object."""
        unit = self.symbol
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
            self.symbol = unit
        elif "(" in unit or ")" in unit: 
            raise ValueError("The unit is not valid")  
        return unit
    
    def simplify_un(self):
        """Performs an algebraic simplification the unit of the object."""
        #Check if the unit has parenthesis 
        self.remove_parenthesis_un()
        #Pass the unit
        unit =  self.symbol
        if re.match(r"\w+", unit) == None:
            raise ValueError("The unit is not valid")
        if unit[0] != "1":
            unit = "*" + unit
        #Find the units
        mult_un = re.findall(r"\*(\w+\^?\-?\d*\.?\d*)", unit)
        div_un = re.findall(r"/(\w+\^?\-?\d*\.?\d*)", unit)
        def to_symbol(x):
            arg = re.search(r"[a-zA-Z]+", x).group()
            c = re.search(r"\-?\d+\.?\d*", x)
            if c == None:
                c = 1
            else:
                c = c.group()
                c = float(c)
                c = round(c, 2)
            return sym.Symbol(arg)**c
        v_to_symbol = np.vectorize(to_symbol)
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
        new = str(new)
        new = new.replace("**1.0*", "*")
        new = new.replace("**1.0/", "/") 
        if new[-5:] == "**1.0":
            new = new[:-5]
        new =  new.replace("**", "^")
        self.symbol = new
        return self.symbol
    
    def simplify(self, unit:str, units=None):
        """Simplifies the unit of the object and converts the value to the unit specified in the unit argument.
        if a units dataframe is provide it will use it to convert the value, 
        otherwise it will use the units dataframe of the object."""

        if isinstance(units, type(None)):
            units = self.units
        else:
            units.set_index("Symbol", inplace=True)
        if not isinstance(unit, str):
            raise TypeError("The unit must be a string")
        if not isinstance(units, pd.DataFrame):
            raise TypeError("The units must be a dataframe")
        if  unit not in units.index:
            raise ValueError(f"""The unit {unit} is not in the units dataframe. The units of the datframe are {units.index}""")
        
        self.simplify_un()
        self.remove_parenthesis_un()
        old_unit = self.symbol
        if old_unit[0] != "1":
            old_unit = "*" + old_unit
        mult_un = re.findall(r"\*(\w+\^?\-?\d*\.?\d*)", old_unit)
        div_un = re.findall(r"/(\w+\^?\-?\d*\.?\d*)", old_unit)
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
                y = (units.loc[arg]["Factor"]/units.loc[unit]["Factor"])**c
                arg = unit
            else:
                y = 1
            return sym.Symbol(arg)**c, y
        v_to_symbol = np.vectorize(to_symbol)
        value = self.value
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
        self.symbol = new
        self.value = value
        return self
    
    def set_unit_system (self, system_dic:dict):
        """Set unit sytem for symplify all unit.
        The keys of the dictionary are the physical quantity name and the values are the symbol 
        of the main unit of the physical quantity."""
        if not isinstance(system_dic, dict):
            raise TypeError("The system dictionary must be a dictionary")
        
        for k in system_dic:
            if  k not in self.dic_units:
                raise ValueError(f"The key {k} is not recognized as a physical quantity, please add it using .set_physical_quantity")
            if system_dic[k] in self.dic_units[k].index:
                raise TypeError(f"The physical quantity {k} does not have the unit {system_dic[k]}")  
        self.unit_system = system_dic
       
    
    def simplify_all(self, system_dic:dict=None):
        """Simplifies the units of an object using the units dictionary of a system messurement units.
        By default the system is the SI, but you can use your own system with system_dic.
        The keys of the dictionary must be the physical quantity and the values must be the main unit
        of the physical quantity."""
        if system_dic == None:
            system_dic = self.unit_system
        else:
            self.set_unit_system(system_dic)
        for k in system_dic:
            if k  == "Temperature":
                continue
            self.simplify(system_dic[k], self.dic_units[k].reset_index())
        return self

    
    def convert(self, unit:str, factor:float=None):
        """Converts the value of the object to the unit specified in the unit argument."""
        if factor:
            self.value = self.value * factor
            self.symbol = unit
            
        else:
            if self.check_unit(unit):
                factor = self.units.loc[self.symbol]["Factor"] / self.units.loc[unit]["Factor"]
                self.value = self.value * factor
                self.unit = unit
                
            else:
                raise ValueError("Unit not supported, please specify a conversion factor")


    #Basic operators

    def __add__(self, other):
        """Adds two objects of the same class and returns a new object of the same class."""
        
        if self.check_relationship(other) and self.name == other.name:
            if self.symbol != other.symbol:
                if self.symbol in self.units.index and other.symbol in self.units.index:
                    factor = self.units.loc[other.symbol]["Factor"]/self.units.loc[self.symbol]["Factor"]
                    value = self.value + other.value * factor
                    result = self.__class__(value=value, symbol=self.symbol, name=self.name)
                    result.set_units(self.units.reset_index(), self.name)
                    return result
                else:   
                    raise TypeError(f"""The units of the object that you are trying to add don't match. The units that can be add are:
                    {self.units.index.to_list()}""")
            else:
                result = self.__class__(self.value + other.value, self.symbol, name=self.name)
                result.set_units(self.units.reset_index(), self.name)
                return result
        else:
            raise TypeError(f"Can only add {self.name} quantities")

    def __sub__(self, other):

        if self.check_relationship(other) and self.name == other.name:
            if self.symbol != other.symbol:
                if self.symbol in self.units.index and other.symbol in self.units.index:
                    factor = self.units.loc[other.symbol]["Factor"]/self.units.loc[self.symbol]["Factor"]
                    value = self.value - other.value * factor
                    result = self.__class__(value=value, symbol=self.symbol, name=self.name)
                    result.set_units(self.units.reset_index(), self.name)
                    return result
                else:   
                    raise TypeError(f"""The units of the object that you are trying to substract don't match. The units that can be substract are
                      {self.units.index.to_list()}""")
            else:
                result = self.__class__(self.value - other.value, self.symbol, name=self.name)
                result.set_units(self.units.reset_index(), self.name)
                return result
        else:
            raise TypeError(f"Can only substract {self.name} quantities")
        
    def __mul__(self, other):
        if self.check_relationship(other) or isinstance(other, (int, float)):
            try:
                result = self.__class__(self.value * other.value, self.symbol +"*"+ other.symbol)
                return result
            except AttributeError:
                result  = self.__class__(self.value * other, self.symbol)
                return result.set_units(self.units.reset_index(), self.name)
        else:
            raise TypeError("Can only multiply by similar or numbers like objects")
        
    def __truediv__(self, other):
        if self.check_relationship(other) or isinstance(other, (int, float)):
            try:
                other.symbol = other.symbol.replace("*", "?")
                other.symbol = other.symbol.replace("/", "*")
                other.symbol = other.symbol.replace("?", "/")
                result = self.__class__(self.value / other.value, self.symbol +"/"+ other.symbol)
                return result
            except AttributeError:
                result  = self.__class__(self.value / other, self.symbol)
                return result.set_units(self.units.reset_index(), self.name)
        else:
            raise TypeError("Can only divide by similar or numbers like objects")
    
    def __pow__(self, other):
        if type(other) == int or type(other) == float:
            unit = self.symbol
            p = re.compile(r"""\^\(?\-?\d+\.?\d*\)?""" , re.X)
            for i in re.finditer(p, unit):
                t = i.group()
                q = re.search(r"\-?\d+\.?\d*", t).group()
                c = float(q)
                unit = unit.replace(q, f"{c*other}")
            result = self.__class__(self.value ** other, unit)
            return result
        else:
            raise TypeError("Can only raise to the power of numbers like objects")

    #Inplace operators

    def __iadd__(self, other):
        if self.check_relationship(other) and self.name == other.name:
            if self.symbol != other.symbol:
                if self.symbol in self.units.index and other.symbol in self.units.index:
                    factor = self.units.loc[other.symbol]["Factor"]/self.units.loc[self.symbol]["Factor"]
                    self.value = self.value + other.value * factor
                    self.symbol = self.symbol
                    return self
                else:   
                   raise TypeError(f"""The unit that you are trying to add is not supported the units that are supported are: {self.units.index.to_list()}""")
            else:
                self.value = self.value + other.value
                self.symbol = self.symbol
                return self 
        else:
            raise TypeError(f"Can only add {self.name} quantities")
        
    def __isub__(self, other):
        if self.check_relationship(other) and self.name == other.name:
            if self.symbol != other.symbol:
                if self.symbol in self.units.index and other.symbol in self.units.index:
                    factor = self.units.loc[other.symbol]["Factor"]/self.units.loc[self.symbol]["Factor"]
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
          
    def __imul__(self, other):
        if self.check_relationship(other) or isinstance(other, (int, float)):
            try:
                self.value *= other.value
                self.symbol = self.symbol+ "*" + other.symbol
            except AttributeError:
                self.value *= other
            return self
        else:
            raise TypeError("Can only multiply by similar or numbers like objects")

    def __itruediv__(self, other):
        if self.check_relationship(other) or isinstance(other, (int, float)):
            try:
                other.symbol = other.symbol.replace("*", "?")
                other.symbol = other.symbol.replace("/", "*")
                other.symbol = other.symbol.replace("?", "/")
                self.value /= other.value
                self.symbol = self.symbol + "/" + other.symbol
            except AttributeError:
                self.value /= other
            return self
        else:
            raise TypeError("Can only divide by similar or numbers like objects")
    
    #Comparison operators

    def __eq__(self, other):
        if self.check_relationship(other):
            a = self.value * self.units.loc[self.symbol]["Factor"]
            b = other.value * self.units.loc[other.symbol]["Factor"]
            return a == b
        else:
            raise TypeError("Can only compare similar objects")
    def __ne__(self, other):
        if self.check_relationship(other):
            a = self.value * self.units.loc[self.symbol]["Factor"]
            b = other.value * self.units.loc[other.symbol]["Factor"]
            return a != b
        else:
            raise TypeError("Can only compare similar objects")
        
    def __lt__(self, other):
        if self.check_relationship(other):
            a = self.value * self.units.loc[self.symbol]["Factor"]
            b = other.value * self.units.loc[other.symbol]["Factor"]
            return a < b
        else:
            raise TypeError("Can only compare similar objects")
        
    def __le__(self, other):
        if self.check_relationship(other):
            a = self.value * self.units.loc[self.symbol]["Factor"]
            b = other.value * self.units.loc[other.symbol]["Factor"]
            return a <= b
        else:
            raise TypeError("Can only compare similar objects")
        
    def __gt__(self, other):
       if self.check_relationship(other):
            a = self.value * self.units.loc[self.symbol]["Factor"]
            b = other.value * self.units.loc[other.symbol]["Factor"]
            return a > b
       else:
            raise TypeError("Can only compare similar objects")
        
    def __ge__(self, other):
       if self.check_relationship(other):
            a = self.value * self.units.loc[self.symbol]["Factor"]
            b = other.value * self.units.loc[other.symbol]["Factor"]
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
    

            
            
            






    
    
    
