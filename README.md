# BasicCivilEng.py
## Content
-[Introduction](##Introductio)  <br />
-[Installation](##Installation)  <br />
-[Documentation](##Documentation)  <br />
    -[CivilEngUnits](###CivilEngUnits) <br />

## Introduction
Module that will contain basic Civil Engineering Classes and Functions for developing free open source Software in python
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
This class will constitude a blueprint and parent class for Units in Civil Engineering

#### Atributes
-`value(float)`: the magnitude of the physical quantity  <br />
-`unit(str)`: the unit of messurement of the physical quantity  <br />
-`decimal(int)`: the number of significance decimal that will be use to represent as string  <br />
-`name(str)`: the name of the physical quantity that is messure by this class <br />
-`units(dict)`: the key of the dictionary are the symbols of the units that the class will support and value are the convesion factor <br />

#### Methods
-It allow all the basic arithmetic `+,-,*,/` while operation checking the unit consitency. It can only add or substract similar units. It can multiply and divide by any given unit or numerical value.<br />
-It can compare similar messurement unit with the operators `==,>=,<=,>,>,<,!=`. <br />
| Method | Required Arguments | Optional Arguments | Operation | Return | 
| -- | -- | -- | -- | -- |
| `from_string()` | `string:str`  |  | Creates a new object from a string with the value and the unit separated by a space | `CivilEngUnits` like object |
| `check_unit()` | `unit:str`  |  | Checks if the unit is in the units dictionary and thus if is supported | `Bool` like object |
| `convert()` | `unit:str`  | `factor:str=None` | Converts the object to the unit specified in the unit argument. <br />
If `factor` is provide it will use the it as the conversion factor to perform the operation otherwise it will use the conversion that are located in the dictionary units| `Bool` like object |




   
