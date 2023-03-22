# BasicCivilEng.py
## Content
-[Introduction](##Introductio)  <br />
-[Installation](##Installation)  <br />
-[Documentation](##Documentation)  <br />
    -[CivilEngUnits](###CivilEngUnits) <br />

## Introduction
A module that will contain basic Civil Engineering Classes and Functions for developing free, open-source Software in python
## Documentation
### Installation and usage
```
pip install BasicCivilEng
```

**Requirements**

```
"re",
"numpy",
"pandas",
"sympy",
"matplotlib"
```
> **Note** All requirements will be installed automatically while installing this module.
### List of all Classes and argument
| Class | Required Arguments | Optional Arguments |
| -- | -- | -- |
| `CivilEngUnits` | `value: float, unit: str`  | `decimal: int` |

### Class CivilEngUnits
This class will constitute a blueprint and parent class for Units in Civil Engineering

#### Atributes
-`value(float)`: the magnitude measure of the physical quantity  <br />
-`unit(str)`: the unit used for the measurement of the physical quantity  <br />
-`decimal(int)`: the number of significance decimal that will be use to represent as string  <br />
-`name(str)`: the name of the physical quantity that is messure by this class <br />
-`units(dict)`: The dictionary's keys are the symbols of the units that the class will support, and the values are the conversion factors of the unit. <br />

#### Methods
-It allows all the basic arithmetic `+,-,*,/` while checking the unit consistency. It can only add or subtract similar units. It can multiply and divide by any given unit or numerical value..<br />
-It can compare measurement of the same physical quantity with the operators `==,>=,<=,>,>,<,!=`. <br />
| Method | Required Arguments | Optional Arguments | Operation | Return | 
| -- | -- | -- | -- | -- |
| `from_string()` | `string:str`  |  | It creates a new object from a string with the value and the unit separated by a space. | `CivilEngUnits` like object |
| `check_unit()` | `unit:str`  |  | It checks if the unit is in the ´units´ dictionary and, thus, if it is supported | `Bool` like object |
| `convert()` | `unit:str`  | `factor:str=None` | It converts the object to the unit specified in the unit argument. If a `factor` is provided, it will use as the conversion factor to perform the operation. Otherwise, it will use the conversion that is located in the dictionary `units`.| `Bool` like object |
| `check_relationship()` | `other`  |  | It verifies if the object have the same parent Object.| `Bool` like object |
| `get_units()` |  |  | It return the `units` dictionary of the object | `units` dictionary |
| `edit_units()` | `unit:str`, `factor:float`  |  | It add a new `unit` with a new `factor` or it update a existing `unit` with a given `factor`|  |
| `remove_unit()` | `unit:str` |  | It remove the given `unit` from the `units` dictionary |  |
| `set_units()` | `units:dict` |  | It set the `units` dictionary of the object |  |
| `simplify_un()` | |  | It performs an algebraic simplification of the `unit` of the object | `unit:str` |
| `simplify()` | `unit:str` |  `units:dict=None` |  It performs an algebraic simplification of the `unit` of the object. And convert all the units of the same physical quantity to the given `unit` string in the argument. If a `units` dictionary is provided, it uses this dictionary to operate. Otherwise, it will use the `units` dictionary the object provides. | `unit:str` |








   
