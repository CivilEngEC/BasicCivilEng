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
    """
   
    def __init__(self, value:float, unit:str, decimal:int=3):
        self.__parent = "CivilEngUnits" #Name of the parent class 
        self.name = "Unit" #Name of the physical quantity
        self.value = value
        self.unit = unit
        self.decimal = decimal
        self.units = {"m": 1,  #units and their conversion to the main unit
                    "km": 1000, 
                    "cm": 0.01, 
                    "mm": 0.001, 
                    "mi": 1609.34, 
                    "yd": 0.9144, 
                    "ft": 0.3048, 
                    "in": 0.0254}
    
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
        string = string.split()
        self.value = float(string[0].replace(",", ""))
        self.unit = string[1]
        return self
    
    def check_unit(self, unit:str):
        """Checks if the unit is supported by the object."""
        if unit in self.units:
            return True
        else:
            return False
    
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
    
    def check_relationship(self, other):
        """Checks if the object are related one another."""
        try:
            if self._CivilEngUnits__parent == other._CivilEngUnits__parent:
                return True
            else:
                return False
        except AttributeError:
            return False
    
    def get_units(self):
        """Returns the units dictionary."""
        return self.units
    
    def edit_units(self, unit:str, factor:float):
        """Adds  a new unit or edit a Existing one in the units dictionary."""
        self.units[unit] = factor

    def remove_unit(self, unit:str):
        """Removes a unit from the units dictionary."""
        if self.check_unit(unit):
            del self.units[unit]
        else:
            raise ValueError("The unit is not in the units dictionary")

    def set_units(self, units:dict):
        """Sets the units dictionary."""
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
            for i in range(len(aux)):
                aux[i] = aux[i].replace(".","/")
                aux[i] = "/"+aux[i]
                unit = unit + aux[i]
            self.unit = unit
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
        multiply_un = re.findall(r"\.\w+", unit)
        divide_un = re.findall(r"/\w+", unit)
        for i in range(len(multiply_un)):
            multiply_un[i] = multiply_un[i].replace(".", "")
        for i in range(len(divide_un)):
            divide_un[i] = divide_un[i].replace("/", "")
        
        mult_un ={}
        for i in multiply_un:
            key = re.search(r"[a-zA-Z]+", i).group()
            c = re.search(r"\d+", i)
            if c == None:
                c=1
            else:
                c = c.group()
            c = int(c)
            if not key in mult_un:
                mult_un[key] = sym.Symbol(key)**c
            else:
                mult_un[key] *= sym.Symbol(key)**c
        div_un ={}
        for i in divide_un:
            key = re.search(r"[a-zA-Z]+", i).group()
            c = re.search(r"\d+", i)
            if c == None:
                c=1
            else:
                c = c.group()
            c = int(c)
            if not key in div_un:
                div_un[key] = sym.Symbol(key)**c
            else:
                div_un[key] *= sym.Symbol(key)**c
        new = 1
        for key in mult_un:
            new *= mult_un[key]
        for key in div_un:
            new /= div_un[key]
        new = str(new)
        new = new.replace("**", "")
        new = new.replace("*", ".")
        self.unit = new
        return self.unit

    def simplify(self, unit:str, units:dict=None):
        """Simplifies the unit of the object and converts the value to the unit specified in the unit argument."""
        if units == None:
            units = self.units
        if not unit in units:
            raise ValueError("""The unit is not in he units dictionary, 
            please provide a unit dictonary that contain the unit""")
        self.simplify_un()
        self.remove_parenthesis_un()
        old_unit = self.unit
        old_unit = "." + old_unit
        multiply_un = re.findall(r"\.\w+", old_unit)
        divide_un = re.findall(r"/\w+", old_unit)
        for i in range(len(multiply_un)):
            aux = multiply_un[i]
            un = re.search(r"[a-zA-Z]+", aux).group()
            c = re.search(r"\d+", aux)
            if c == None:
                c=1
            else:
                c = c.group()
            c  = int(c)
            if un in units:
                self.value *= (units[un]/units[unit])**c
                if c == 1:
                    multiply_un[i] = "." + unit
                else:
                    multiply_un[i] = "." + unit + str(c)
            else:
                continue
        for i in range(len(divide_un)):
            aux = divide_un[i]
            un = re.search(r"[a-zA-Z]+", aux).group()
            c = re.search(r"\d+", aux)
            if c == None:
                c=1
            else:
                c = c.group()
            c  = int(c)
            if un in units:
                self.value /= (units[un]/units[unit])**c
                if c == 1:
                    divide_un[i] = "/" + unit
                else:
                    divide_un[i] = "/" + unit + str(c)
            else:
                continue
        new = ""
        for i in multiply_un:
            new += i
        for i in divide_un:
            new += i
        if new[0] == ".":
            new = new[1:]
        self.unit = new
        self.simplify_un()
        return self


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
    
    
   



    
    
    




    
    
    
