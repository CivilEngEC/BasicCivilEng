# EngUnits.py
## Content
-[Introduction](#Introductio)  <br />
-[Installation](#Installation)  <br />
-[Documentation](#Documentation)  <br />
    -[CivilEngUnits](#CivilEngUnits) <br />

## Introduction
A module that will contain basic Engineering Classes and Functions for developing free, open-source Software in python
## Documentation
### Installation and usage
```

```

**Requirements**

```
"re",
"numpy",
"pandas",
"sympy",
"matplotlib",
"datetime"

```
> **Note** 
### List of all Classes and argument
| Class | Required Arguments | Optional Arguments |
| -- | -- | -- |
| `Units` | ``  | ``  |
| `Quantity` | `value:number, symbol:string, system_units:Units`  | ` decimal:interger`  |
| `Money` | `value:number, symbol:string, system_units:Units`  | ` decimal:interger, date:string, year_rate:float`  |

### Class Units
This class will be the master for handle unit, it will contain all the physical quantanties and units of messurement that the software can interpret and read

#### Atributes
-`dic_units(dic)`: It is a dictionary of dataframe. Its keys are the physical quantities names and its values are the Dataframe. Each DataFrame contains the symbol unit of messurement as its index and the columns Name, Factor, Description. The column Name hold the name of the unit of messurement, the column factor the number for convert into the main unit of messurement, and description an string  <br />
-`all_units`: A list that contain all the symbols support by the class  <br />
-`unit_system(dic)`: dic that contain all main units. Its key are the physical quantities, its values are the symbol <br />
#### Methods
| Method | Required Arguments | Optional Arguments | Operation | Return | 
| -- | -- | -- | -- | -- |
| `find_unit` | `unit:str`  |  | Checks if the unit is supported by the object. | Name of the physical quantity where the unit is allocated and False if not. |
| `append` | `name:str`, `record:list`  |  | Append a new unit to the units DataFrame of the physical quantity name. Name must be a string and the name of a physical quantity. The reord must be a list with the following structure: [name, symbol, factor, Description] |  |
| `remove` | `symbol:str` |  | Removes a unit with the symbol pass from the Units class|  |
| `empty` | `name:str` |  | Empty units DataFrame from the name physical quantity.|  |
| `set_units` | `units:DataFrame`,`name:str` |  | Sets the units Dataframe of a given physical quantities. unit must be a DataFrame with the columns Name, Symbol, Factor and Description. The factor  columnn must contain number values and at least one row must have the factor column = 1.The symbol column must contain string values.|  |
| `set_unit_system ` | `system_dic:dict` |  | Set unit sytem for symplify all unit.The keys of the dictionary are the physical quantity name and the values are the symbol of the main unit of the physical quantity|  |
| `simplify` | `unit:str` |  | Perform an algebraic simplification of the unit using the unit system.|  |

### Class Quantity
This class will handle the quatities that must have a value, unit and a unit system

#### Atributes
-`value(number)`: It is the messure value  with a given unit of messurement <br />
-`symbol(string)`: Itis the symbol of the given unit use for messure the value  <br />
-`system_units(Units)`: It the class that help to handle, operate and interpret the unit of messurement  <br />
-`decimal (interger)`: Number of decimal that will be use for represent the object as string. <br />
-`name (string)`: name of the physical quantity that messure the given unit <br />
-`unit (dictionary)`: it have the symbol of the units as keys and the values of factors as value <br />
-`main_unit (string)`: the main unit of the quantity <br />

#### Methods
-It allows all the basic arithmetic `+,-,*,/` while checking the unit consistency. It can only add or subtract similar units. It can multiply and divide by any given unit or numerical value..<br />
-It can compare measurement of the same physical quantity with the operators `==,>=,<=,>,>,<,!=`. <br />
| Method | Required Arguments | Optional Arguments | Operation | Return | 
| -- | -- | -- | -- | -- |
| `is_related` | `other:object`  |  | Checks if the object are related one another | True if the object is a subclass of `Quantity` |
| `update_units` | `units:Units`  |  | Update the Units interpreter object | A copy of the Quantity object with the new units interpreter |
| `set_factors` | `units:Units`  |  |Sets the factors of the units Dictionary | Update the units dictionary and the main_unit |
| `simplify` |  |  | Perform an algebraic simplification of the unit using the unit system.|  |
| `convert` | `new_unit:str` | `factor:number` | Convert the quantity to the given new unit using the factor if provided or using the conversion factor that the system_unit holds.| new Quantity  |








   
