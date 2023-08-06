# Ini File Uts
#
### Installation

```sh
pip install iniUts
```

## Usage
#
<!-- //==================================================== -->
## read
##### test.ini file
```ini
[Person]
name    = myname
age     = 31
amount  = 20.3
friends = friend1,friend2,friend3
dob     = 1991-12-23
```
##### python code
```py
from iniUts import IniUts

ini = IniUts('test.ini')
data = ini.read('Person','name')

print(result)
```
##### output
```py
"myname"
```

<!-- //==================================================== -->
## write
##### test.ini file
```ini
[PERSON]
name    = myname
```
##### python code
```py
from iniUts import IniUts

ini = IniUts('test.ini')
ini.write('PERSON','last_name','mylastname')

```
##### test.ini file
```ini
[PERSON]
name      = myname
last_name = mylastname
```
<!-- //==================================================== -->
## getKeys
##### test.ini file
```ini
[PERSON]
name      = myname
last_name = mylastname
```
##### python code
```py
from iniUts import IniUts

ini = IniUts('test.ini')
keys = ini.getKeys("PERSON")
print(keys)
```
##### output
```py
['name','last_name']
```

<!-- //==================================================== -->
## Section2Dict
##### test.ini file
```ini
[PERSON]
name    = myname
age     = 31
amount  = 20.3
friends = friend1,friend2,friend3
dob     = 1991-12-23
```
##### python code
```py
from iniUts import IniUts

ini = IniUts('test.ini')
ini.Section2Dict('PERSON')
print(Person)

```
##### output
```py
{
    "name"    = "myname"
    "age"     = "31"
    "amount"  = "20.3"
    "friends" = "friend1,friend2,friend3"
    "dob"     = "1991-12-23"
}

```
<!-- //==================================================== -->
## section2DataClass
##### test.ini file
```ini
[PERSON]
name    = myname
age     = 31
amount  = 20.3
friends = friend1,friend2,friend3
dob     = 1991-12-23
```
##### python code
```py
from iniUts import IniUts
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Person():
    name   : str
    age    : int
    amount : float
    friends: tuple = ','
    dob    : datetime = "%Y-%m-%d"

ini = IniUts('test.ini')
ini.Section2Dict("section2DataClass")

print(Person.name)
print(Person.age)
print(Person.amount)
print(Person.friends)
print(Person.dob)

```
##### output
```py
myname
31
20.3
("friend1","friend2","friend3")
datetime.datetime(1991, 12, 2, 0, 0)

```




