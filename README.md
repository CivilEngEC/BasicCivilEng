# EngUnits.py
## Content
-[Introduction](#Introductio)  <br />
-[Installation](#Installation)  <br />
-[Documentation](#Documentation)  <br />
    -[CivilEngUnits](#CivilEngUnits) <br />

## Introduction
A module that will contain basic Civil Engineering Classes and Functions for developing free, open-source Software in python
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

```
> **Note** All requirements will be installed automatically while installing this module.
### List of all Classes and argument
| Class | Required Arguments | Optional Arguments |
| -- | -- | -- |
| `CivilEngUnits` | `value: float, unit: str`  | `decimal: int, name: str`  |

### Class CivilEngUnits
This class will constitute a blueprint and parent class for Units in Civil Engineering

#### Atributes
-`value(float)`: the magnitude measure of the physical quantity  <br />
-`symbol(str)`: the symbol use for represent the unit used for the measurement of the physical quantity  <br />
-`decimal(int)`: the number of significance decimal that will be use to represent as string  <br />
-`name(str)`: the name of the physical quantity that is messure by this class <br />
-`units(DataFrame)`: The DataFrame contain the symbols as index and the fields Name, Factor and Equation. <br />
-`dic_units(dict)`: Dictonary that contain the main physical quantities and its units DataFrame. <br />
-`all_units(list)`: List that contain all units. <br />
-`unit_system(dic)`: dic that contain all main units. <br />


#### Methods
-It allows all the basic arithmetic `+,-,*,/` while checking the unit consistency. It can only add or subtract similar units. It can multiply and divide by any given unit or numerical value..<br />
-It can compare measurement of the same physical quantity with the operators `==,>=,<=,>,>,<,!=`. <br />
| Method | Required Arguments | Optional Arguments | Operation | Return | 
| -- | -- | -- | -- | -- |
| `from_string()` | `string:str`  |  | It upddate the value and symbol of an object from a string with the value and the symbol separated by a space. | `CivilEngUnits` like object |
| `check_relationship()` | `other`  |  | It verifies if the object have the same parent Object.| `Bool` True if they are related by the same parent, False otherwise |
| `check_unit()` | `unit:str`  |  | It checks if the symbol use to represent the unit it is used already by other unit in the object | The name of the physical quantity that use unit with a similar simbol if the unit is already in used or False otherwise |
| `get_units()` |  |  | It return the `units` dictionary of the object | `units:dict` |
| `add_unit()` | `unit:str`, `factor:float`  | `name:str`, `equation:str`   | It add a new record to the `units` DataFrame, with|  |
| `remove_unit()` | `unit:str` |  | It remove the record of the given `unit` from the `units` DataFrame |  |
| `empty_units()` | |  | It creates an empty  `units` DataFrame | `units:DataFrame`  |
| `set_physical_quantity()` | `name:str`, `units:DataFrame`  |  | It asign the `units` DataFrame to `name` physical quantity in the `dic_units` dictionary  |  |
| `set_unit_system()` | `system_dic:dic` |  | It set the `unit_system()` DataFrame of the object |  |
| `set_units()` | `units:DataFrame` |  | It set the `units` DataFrame of the object and update the `dic_units` dictionary |  |
| `simplify_un()` | |  | It performs an algebraic simplification of the `symbol` of the object and update the object | `unit:str` |
| `simplify()` | `unit:str` |  `units:DataFrame=None` |  It performs an algebraic simplification of the `unit` of the object. And convert all the units of the same physical quantity to the given `unit` string in the argument. If a `units` DataFrame is provided, it uses this DataFrame to operate. Otherwise, it will use the `units` DataFrame the object provides. | `unit:str` |
| `simplify_all()` | |  | It performs an algebraic simplification of the `symbol` of the object and update the object, using the `unit_system()` | `unit:str` |
| `convert()` | `unit:str`  | `factor:str=None` | It converts the object to the unit specified in the unit argument. If a `factor` is provided, it will use as the conversion factor to perform the operation. Otherwise, it will try to mach to any of the given units inside `units` DataFrame the object.|  |









   
