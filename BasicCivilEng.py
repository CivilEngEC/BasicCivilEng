class CivilEngUnits:
    """This class will constitude a blueprint and parent class for messurement in Civil Engineering
    -the value messure of the physical quantity
    -the unit of the physical quantity
    -the decimal places that you want to show in the string representation of the object
    """
   
    def __init__(self, value:float, unit:str, decimal=3):
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
    
    def convert(self, unit:str, conversion=None):
        """Converts the value of the object to the unit specified in the unit argument."""

        if self.check_unit(unit):
            self.value = self.value * self.units[self.unit] / self.units[unit]
            self.unit = unit
            return self
        else:
            if conversion:
                self.units[unit] = conversion
                self.value = self.value * self.units[self.unit] / self.units[unit]
                self.unit = unit
                return self
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
    
    def edit_units(self, unit=str, value=float):
        """Adds  a new unit or edit a Existing one in the units dictionary."""
        self.units[unit] = value

    def remove_unit(self, unit=str):
        """Removes a unit from the units dictionary."""
        del self.units[unit]

    def get_units(self):
        """Returns the units dictionary."""
        return self.units
    
    def set_units(self, units=dict):
        """Sets the units dictionary."""
        self.units = units
    
    def simplify_un(self):
        """Performs an algebraic simplification the unit of the object."""
        #Pass the unit
        unit =  self.unit
        #Find the first unit
        try:
            first_un = re.search(r"\w+", unit)[0]
        except:
            raise ValueError("Unit not supported")
        #Find the units that are multiplied  
        multiply_un = re.findall(r"\.\w+", unit)
        #Find the units that are divided
        divide_un = re.findall(r"/\w+", unit)
        #Find the number of time that the each unit is multiplied
        mult_un  = {}
        for i in multiply_un:
            key = re.search(r"[a-zA-Z]+", i)[0]
            try:
                c = re.search(r"\d+", i)[0]
                c = int(c)
            except:
                c = 1
            if key in mult_un:
                mult_un[key] += c
            else:
                mult_un[key] = c
        #Find the number of time that the each unit is divided
        div_un = {}
        for i in divide_un:
            key = re.search(r"[a-zA-Z]+", i)[0]
            try:
                c = re.search(r"\d+", i)[0]
                c = int(c)
            except:
                c = 1
            if key in div_un:
                div_un[key] += c
            else:
                div_un[key] = c
        
        keys = set(mult_un.keys()).union(set(div_un.keys()))
        
        if first_un != "1":
            key = re.search(r"[a-zA-Z]+", first_un)[0]
            try:
                aux  = re.search(r"\d+", first_un)[0]
                aux = int(aux)
            except:
                aux = 1
            if key in div_un:
                if aux >= div_un[key]:
                    aux -= div_un[key]
                    del div_un[key]
                    if aux == 0:
                        first_un = "1"
                else:
                    div_un[key] -= aux
                    first_un = "1"

            elif key in mult_un:
                mult_un[key] += aux
            else:
                mult_un[key] = aux

        for key in keys:
            if key in mult_un and key in div_un:
                if mult_un[key] > div_un[key]:
                    mult_un[key] -= div_un[key]
                    del div_un[key]
                elif mult_un[key] < div_un[key]:
                    div_un[key] -= mult_un[key]
                    del mult_un[key]
                else:
                    del mult_un[key]
                    del div_un[key]
        
        new_unit = ""
        if first_un == "1" and len(mult_un) == 0:
            new_unit += first_un
        elif first_un == "1" and len(mult_un) > 0:
            key = list(mult_un.keys())[0]
            c = mult_un[key]
            if c == 1:
                new_unit += key
            else:
                new_unit += key + str(c)
            del mult_un[key]
        else:
            
            new_unit += first_un
        
        for key in mult_un:
            c = mult_un[key]
            if c == 1:
                new_unit += "." + key
            else:
                new_unit += "."+ key + str(c)
        
        for key in div_un:
            c = div_un[key]
            if c == 1:
                new_unit += "/"+ key
            else:
                new_unit +="/"+ key + str(c)
        self.unit = new_unit
        return self.unit       

    
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
    
   



    
    
    




    
    
    
