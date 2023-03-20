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
pip install beamframe
```

**Requirements**

```
"numpy",
"pandas",
"matplotlib"
```
> **Note** All requirements will be installed automatically while installing this module.
### List of all Classes and argument
| class | required arguments | optional arguments |
| -- | -- | -- |
| `CivilEngUnits` | `value: float, unit: str`  | `decimal: int` |

### Class CivilEngUnits
This class will constitude a blueprint and parent class for Units in Civil Engineering

#### Arguments
-value(float): the magnitude of the physical quantity  <br />
-unit(str): the unit of messurement of the physical quantity  <br />
-decimal(int): the number of significance decimal that will be use to represent as string  <br />

#### Methods
-It allow all the basic arithmetic `+,-,*,/` while operation checking the unit consitency. It can only add or substract similar units. It can multiply and divide by any given unit or numerical value.<br />
-It can compare similar messurement unit with the operators `==,>=,<=,>,>,<,!=`. <br />
-`simplify_un()`: Performs an algebraic simplification the unit of the object.<br />
-`get_units()`: returns the dictionary used for the conversition of the similar messurement units.<br />
-`set_units()`: set the dictionary used for the conversion of the similar messurement units.<br />
-`remove_unit()`: Removes a unit from the units dictionary `units`.<br />
-`dit_units()`: Adds  a new `unit` or edit a existing one in the ´units´ dictionary.<br />
-`check_relationship()`: check if the object is a `CivilEngUnits` object or a child.<br /> 
-`from_string(string=str)`: Creates a new object from a string with the value and the unit separated by a space <br />
-`check_unit(unit=str)`: Checks if the `unit` is supported by the object. <br />
-`convert(unit:str, conversion:float)`: Converts the value of the object to the unit specified in the unit argument, conversion is an optional argument needed if
the unit enter isn´t in the dictionary `units`.





   
