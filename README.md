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
Sum: $2 m + 3 yd = 4.7432$ 
   
