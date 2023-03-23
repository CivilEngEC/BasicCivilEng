#BasicCivilEng.py

"""A module that will contain basic Civil Engineering Classes and Functions 
for developing free, open-source Software in python"""

import re
import numpy as np
import sympy as sym

class CivilEngUnits:
    """This class will constitute a blueprint and parent class for Units in Civil Engineering
    -the value is the measure of the physical quantity
    -the unit use for measure the physical quantity
    -the decimal places that you want to show in the string representation of the object
    -the name of the physical quantity
    By default the decimal places is 3 and the name is "Lenght" and the main units are SI units
    """
   
    def __init__(self, value:float, unit:str, decimal:int=3, name:str ="Length"):
        self.__parent = "CivilEngUnits" #Name of the parent class 
        
        #Check the type of the arguments
        if not isinstance(value, (int, float)):
            raise TypeError("The value must be a number")
        if not isinstance(unit, str):
            raise TypeError("The unit must be a string")
        if not isinstance(decimal, int):
            raise TypeError("The decimal places must be an integer")
        if not isinstance(name, str):
            raise TypeError("The name of the physical quantity must be a string")
        
        self.name = name #Name of the physical quantity
        self.value = value
        self.unit = unit
        self.decimal = decimal
        #Units and their conversion to the main unit
        Time = {"s": 1, "min": 60, "h": 3600, "d": 86400, "y": 31536000}
        
        Length = {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001, "dm":0.1,
                  "mi": 1609.34, "yd": 0.9144, "ft": 0.3048, "in": 0.0254}
        
        Area = {"m2": 1, "km2": 1000000, "cm2": 0.0001, "mm2": 0.000001, "dm2":0.01,
                "mi2": 2589988.11, "yd2": 0.836127, "ft2": 0.092903, "in2": 0.00064516,
                "ha": 10000, "acre": 4046.86, "a": 100}
        
        Volume = {"m3": 1, "km3": 1000000000, "cm3": 0.000001, "mm3": 0.000000001, "dm3":0.001,
                "mi3": 4168181825.44, "yd3": 0.764555, "ft3": 0.0283168, "in3": 0.0000163871,
                "l": 0.001, "ml": 0.000001, "hl": 0.01, "gal": 0.00378541, "qt": 0.000946353,
                "pt": 0.000473176, "cup": 0.000236588, "floz": 0.0000295735}

        Mass = {"kg": 1, "g": 0.001, "mg": 0.000001, "ton": 1000,
                "lb": 0.453592, "klb": 453.592, "oz": 0.0283495}
        
        force = {"N": 1, "kN": 1000, "MN": 1000000, "lbf": 4.44822, "kips": 4448.22, "kgf": 9.80665}
        
        pressure = {"Pa": 1, "kPa": 1000, "MPa": 1000000, "bar": 100000, "psi": 6894.76, "ksi": 6894760}
        
        Energy = {"J": 1, "kJ": 1000, "MJ": 1000000, "GJ": 1000000000, "Wh": 3600, "kWh": 3600000, 
                  "MWh": 3600000000, "Btu": 1055.06, "kcal": 4184}
        
        Power = {"W": 1, "kW": 1000, "MW": 1000000, "GW": 1000000000, "hp": 745.7, "cv": 735.5}

        ElectricCharge = {"C": 1, "mC": 0.001, "kC": 1000}

        ElectricPotential = {"V": 1, "mV": 0.001, "kV": 1000}
        
        ElectricCurrent = {"A": 1, "mA": 0.001, "kA": 1000}
        
        Temperature = {"K": 1, "oC": 1, "F": 1}
        
        ASubstance = {"mol": 1, "kmol": 1000}

        LIntensity = {"cd": 1, "kcd": 1000, "mcd": 0.001}

        LFlux = {"lm": 1, "klm": 1000, "mlm": 0.001}

        iluminance = {"lx": 1, "klx": 1000, "mlx": 0.001, "ft-cd": 10.7639}


        #The dictionary of the base units supported by the class

        self.base_units = {"Time": Time, 
                           "Length": Length,
                           "Area": Area,
                           "Volume": Volume,
                           "Mass": Mass,
                           "force": force, #"Mass*Length/Time**2"
                            "Pressure": pressure,  #"force/Area"
                            "Energy": Energy, #"force*Length"
                            "Power": Power , #"force*Length/Time"
                            "Electric charge": ElectricCharge, #"ElectricCurrent*Time"
                            "Electric potential": ElectricPotential, #"Energy/Electric charge"
                           "Electric current": ElectricCurrent, 
                           "Temperature": Temperature,
                           "Amount of substance": ASubstance,
                           "Luminous intensity": LIntensity,
                           "Luminous flux": LFlux, #"Luminous intensity*Solid angle"
                           "Iluminance": iluminance}  # "Luminous flux/Area"
        
        L = []
        for d in self.base_units:
            for k in self.base_units[d]:
                L.append(k)
        L = np.array(L)
        L,c  = np.unique(L, return_counts=True)
        if (c > 1).any() :
            raise ValueError("There are repeated units in the list of units")
        
        self.ListOfUnits = L #List of all the units supported by the class

        if not self.name in self.base_units:
            self.base_units[self.name] = {}
        self.units =  self.base_units[self.name]
        for k in self.units:
            self.ListOfUnits = np.delete(self.ListOfUnits, 
                                         np.where(self.ListOfUnits == k)) #Remove the units that are already in the dictionary
        
    
    #Magic Methods
    def __repr__(self):
        return f"{self.name}:({self.value}, '{self.unit}')"
    
    def __float__(self):
        return self.value * self.units[self.unit]
    
    def __int__(self):
        return int(self.value * self.units[self.unit])
    
    def __str__(self):
        return f"{round(self.value,self.decimal):,} {self.unit}"
    
    #Methods

    def from_string(self, string:str):
        """Creates a new object from a string with the value and the unit separated by a space"""
        if not isinstance(string, str):
            raise TypeError("The input must be a string")
        string = string.split()
        try:    
            self.value = float(string[0].replace(",", ""))
            self.unit = string[1]
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
    
    def check_unit(self, unit:str):
        """Checks if the unit is supported by the object.
        Returns True if the unit is supported and False if not."""
        
        if unit in self.units:
            return True
        else:
            return False
    
    def get_units(self):
        """Returns the units dictionary."""
        return self.units
    
    def edit_units(self, unit:str, factor:float):
        """Adds  a new unit or edit a Existing one in the units dictionary."""
        if not isinstance(unit, str):
            raise TypeError("The unit must be a string")
        if not isinstance(factor, (int, float)):
            raise TypeError("The factor must be a number")
        self.units[unit] = factor

    def remove_unit(self, unit:str):
        """Removes a unit from the units dictionary."""
        if not isinstance(unit, str):
            raise TypeError("The unit must be a string")
        if self.check_unit(unit):
            del self.units[unit]
        else:
            raise ValueError("The unit is not in the units dictionary")

    def set_units(self, units:dict):
        """Sets the units dictionary."""
        if not isinstance(units, dict):
            raise TypeError("The units must be a dictionary")
        for k in units:
            if not isinstance(units[k], (int, float)):
                raise TypeError("The factors in the units dictionary must be a number")
            if k in self.ListOfUnits:
                raise ValueError(f"The unit {k} is already in the ListofUnits, please use another symbol to represent it")
        self.units = units

    
    def remove_parenthesis_un(self):
        """Removes the parenthesis in the unit of the object."""
        unit = self.unit
        if "(" in unit and ")" in unit:
            s = re.compile(r"""/\((.+?)\) """ , re.X)
            aux = re.findall(s, unit)
            unit = re.sub(s, r"", unit)
            unit = unit.replace("(", "")
            unit = unit.replace(")", "")    
            def aux_f(aux):
                aux = aux.replace(".", "/")
                aux = "/"+aux
                return aux
            vaux_f = np.vectorize(aux_f)
            aux = np.array(aux)
            aux = vaux_f(aux)
            aux = "".join(aux)
            unit = unit + aux
        elif "(" in unit or ")" in unit: 
            raise ValueError("The unit is not valid")  
        return unit
    
    def simplify_un(self):
        """Performs an algebraic simplification the unit of the object."""
        #Pass the unit
        unit =  self.unit
        #Check if the unit has parenthesis
        unit = self.remove_parenthesis_un()
        if re.match(r"\w+", unit) == None:
            raise ValueError("The unit is not valid")
        if unit[0] != "1":
            unit = "." + unit
        mult_un = re.findall(r"\.\w+", unit)
        div_un = re.findall(r"/\w+", unit)
        def to_symbol(x):
            arg = re.search(r"[a-zA-Z]+", x).group()
            c = re.search(r"\d+", x)
            if c == None:
                c=1
            else:
                c = c.group()
            c = int(c)
            return sym.Symbol(arg)**c
        v_to_symbol = np.vectorize(to_symbol)
        new = 1
        if mult_un != []:
            mult_un = np.array(mult_un)
            mult_un = np.char.replace(mult_un,".", "")
            mult_un = v_to_symbol(mult_un)
            mult_un = np.prod(mult_un)
            new = new*mult_un
        if div_un != []:
            div_un = np.array(div_un)
            div_un = np.char.replace(div_un,"/", "")
            div_un = v_to_symbol(div_un)
            div_un = np.prod(div_un)
            new = new/div_un
        new = str(new)
        new = new.replace("**", "")
        new = new.replace("*", ".")
        self.unit = new
        return self.unit

    def simplify(self, unit:str, units:dict=None):
        """Simplifies the unit of the object and converts the value to the unit specified in the unit argument."""
        if units == None:
            units = self.units
        if not isinstance(unit, str):
            raise TypeError("The unit must be a string")
        if not isinstance(units, dict):
            raise TypeError("The units must be a dictionary")
        for k in units:
            if not isinstance(units[k], (int, float)):
                raise TypeError("The factors in the units dictionary must be a number")
        if not unit in units:
            raise ValueError(f"""The unit is not in the units dictionary, 
            please provide a unit dictonary that contain the unit {unit}""")
        
        self.simplify_un()
        self.remove_parenthesis_un()
        old_unit = self.unit
        if old_unit[0] != "1":
            old_unit = "." + old_unit
        mult_un = re.findall(r"\.\w+", old_unit)
        div_un = re.findall(r"/\w+", old_unit)
        def to_symbol(x, y):
            arg = re.search(r"[a-zA-Z]+", x).group()
            c = re.search(r"\d+", x)
            if c == None:
                c=1
            else:
                c = c.group()
            c = int(c)
            if arg in units:
                y = (units[arg]/units[unit])**c
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
            new = new*mult_un
            value *= mult_un_factor
        if div_un != []:
            div_un = np.array(div_un)
            div_un, div_un_factor = v_to_symbol(div_un, np.ones(len(div_un)))
            div_un = np.prod(div_un)
            div_un_factor = np.prod(div_un_factor)
            new = new/div_un
            value /= div_un_factor
        new = str(new)
        new = new.replace("**", "")
        new = new.replace("*", ".")
        self.unit = new
        self.simplify_un()
        self.value = value
        return self
    
    def convert(self, unit:str, factor:float=None):
        """Converts the value of the object to the unit specified in the unit argument."""

        if factor:
            self.value = self.value * factor
            self.unit = unit
            
        else:
            if self.check_unit(unit):
                self.value = self.value * self.units[self.unit] / self.units[unit]
                self.unit = unit
                
            else:
                raise ValueError("Unit not supported, please specify a conversion factor")


    #Basic operators

    def __add__(self, other):
        if type(self) == type(other):
            if self.unit != other.unit:
                if self.unit in self.units and other.unit in self.units:
                    a = self.value * self.units[self.unit]
                    b = other.value * self.units[other.unit]
                    c = a + b
                    c = c / self.units[self.unit]
                    return self.__class__(c, self.unit)
                else:   
                    raise TypeError(f"""The units of the object that you are trying to add 
                    don't match and the conversion is not supported. The units that are supported are: 
                    {self.units.keys()}""")
            else:
                return self.__class__(self.value + other.value, self.unit)
        else:
            raise TypeError(f"Can only add {self.name} quantities")

    def __sub__(self, other):
        if type(self) == type(other):
            if self.unit != other.unit:
                if self.unit in self.units and other.unit in self.units:
                    a = self.value * self.units[self.unit]
                    b = other.value * self.units[other.unit]
                    c = a - b
                    c = c / self.units[self.unit]
                    return self.__class__(c, self.unit)
                else:   
                    raise TypeError(f"""The unit that you are trying to substract is not supported 
                    the units that are supported are: {self.units.keys()}""")
            return self.__class__(self.value + other.value, self.unit)
        else:
            raise TypeError(f"Can only substract {self.name} quantities")
        
    def __mul__(self, other):
        if self.check_relationship(other) or type(other) == int or type(other) == float:
            try:
                return CivilEngUnits(self.value * other.value, self.unit +"."+ other.unit)
            except AttributeError:
                return self.__class__(self.value * other, self.unit)
        else:
            raise TypeError("Can only multiply by similar or numbers like objects")
        
    def __truediv__(self, other):
        if self.check_relationship(other) or type(other) == int or type(other) == float:
            try:
                return CivilEngUnits(self.value / other.value, f"{self.unit}/{other.unit}")
            except AttributeError:
                return self.__class__(self.value / other, self.unit)
        else:
            raise TypeError("Can only divide by numbers")
    
    def __pow__(self, other):
        if type(other) == int or type(other) == float:
            return self.__class__(self.value ** other, self.unit)
        else:
            raise TypeError("Can only raise to the power of numbers like objects")

    #Inplace operators

    def __iadd__(self, other):
        if type(other) == type(self):
            if self.unit != other.unit:
                if self.unit in self.units and other.unit in self.units:
                    a = self.value * self.units[self.unit]
                    b = other.value * self.units[other.unit]
                    c = a + b
                    c = c / self.units[self.unit]
                    self.value = c
                    self.unit = self.unit
                    return self
                else:   
                   raise TypeError(f"""The unit that you are trying to add is not supported 
                    the units that are supported are: {self.units.keys()}""")
            else:
                self.value = self.value + other.value
                self.unit = self.unit
                return self 
        else:
            raise TypeError(f"Can only add {self.name} quantities")
        
    def __isub__(self, other):
        if type(other) == type(self):
            if self.unit != other.unit:
                if self.unit in self.units and other.unit in self.units:
                    a = self.value * self.units[self.unit]
                    b = other.value * self.units[other.unit]
                    c = a - b
                    c = c / self.units[self.unit]
                    self.value = c
                    self.unit = self.unit
                    return self
                else:   
                    raise TypeError(f"""The unit that you are trying to substract is not supported 
                    the units that are supported are: {self.units.keys()}""")
            else:
                self.value = self.value - other.value
                self.unit = self.unit
                return self
        else:
            raise TypeError(f"Can only substract {self.name} quantities")
          
    def __imul__(self, other):
        if self.check_relationship(other) or type(other) == int or type(other) == float:
            try:
                self.value *= other.value
                self.unit = self.unit+ "." + other.unit
                return CivilEngUnits(self.value * other.value, self.unit)
            except AttributeError:
                self.value *= other
                return self 
        else:
            raise TypeError("Can only multiply by similar or numbers like objects")

    def __itruediv__(self, other):
        if self.check_relationship(other) or type(other) == int or type(other) == float:
            try:
                self.value /= other.value
                self.unit = f"{self.unit}/{other.unit}"
                return CivilEngUnits(self.value * other.value, self.unit)
            except AttributeError:
                self.value /= other
                return self 
        else:
            raise TypeError("Can only divide by similar or numbers like objects")
    
    #Comparison operators

    def __eq__(self, other):
        if type(other) == type(self):
            a = self.value * self.units[self.unit]
            b = other.value * self.units[other.unit]
            return a == b
        else:
            raise TypeError("Can only compare similar objects")
    def __ne__(self, other):
        if type(other) == type(self):
            a = self.value * self.units[self.unit]
            b = other.value * self.units[other.unit]
            return a != b
        else:
            raise TypeError("Can only compare similar objects")
        
    def __lt__(self, other):
        if type(other) == type(self):
            a = self.value * self.units[self.unit]
            b = other.value * self.units[other.unit]
            return a < b
        else:
            raise TypeError("Can only compare similar objects")
        
    def __le__(self, other):
        if type(other) == type(self):
            a = self.value * self.units[self.unit]
            b = other.value * self.units[other.unit]
            return a <= b
        else:
            raise TypeError("Can only compare similar objects")
        
    def __gt__(self, other):
        if type(other) == type(self):
            a = self.value * self.units[self.unit]
            b = other.value * self.units[other.unit]
            return a > b
        else:
            raise TypeError("Can only compare similar objects")
        
    def __ge__(self, other):
        if type(other) == type(self):
            a = self.value * self.units[self.unit]
            b = other.value * self.units[other.unit]
            return a >= b
        else:
            raise TypeError("Can only compare similar objects")    
    
    #Unary operators

    def __neg__(self):
        return self.__class__(-self.value, self.unit)
    def __pos__(self):
        return self.__class__(self.value, self.unit)
    def __abs__(self):
        return self.__class__(abs(self.value), self.unit)
    def __round__(self, n=0):
        return self.__class__(round(self.value, n), self.unit)
    def __floor__(self):
        return self.__class__(self.value // 1, self.unit)
    def __ceil__(self):
        return self.__class__(self.value // 1 + 1, self.unit)
    def __trunc__(self):
        return self.__class__(self.value // 1, self.unit)
    
    
   



    
    
    




    
    
    
