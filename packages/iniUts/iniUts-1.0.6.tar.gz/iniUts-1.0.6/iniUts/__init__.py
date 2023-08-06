import configparser as cp
from dataclasses import dataclass
from dateUts import date
from datetime import datetime
import re


class IniUts():
    def __init__(self,_file):
        self.file = _file
        self.delimiters = {}
        self.dateFormats = {}


    def write(self,sec,key,value):
        config = cp.RawConfigParser()
        config.optionxform = str
        config.read(self.file)
        if not sec in config.sections():
            config[sec] = {}
            config[sec][key] = ""
            config.write(open(self.file, 'w'))
        config[sec][key] = value
        config.write(open(self.file, 'w'))
    
    def read(self,sec,key):
        config = cp.RawConfigParser()
        config.optionxform = str
        config.read(self.file)
        if not sec in config.sections():
            raise Exception("Section not found!")
        if not key in config[sec]:
            raise Exception("Key not found!")
        return config[sec][key]
    
    def getKeys(self,section):
        config = cp.RawConfigParser()
        config.read(self.file)
        if not section in config.sections():
            raise Exception("Section not found!")

        return [k for k in config[section]]
   
    def Section2Dict(self,section,empty_as_null=False):
        config = cp.RawConfigParser(allow_no_value=True)
        config.optionxform = str
        config.read(self.file)

        dc = dict(config[section])
        return dc if not empty_as_null else {x:(y or None) for x,y in dc.items()}
    
    def section2DataClass(self,section,dtClass,skip_missing=False,empty_as_null=False):
        dt = self.Section2Dict(section,empty_as_null=empty_as_null)
        for k, v in dt.items():
            if not k in dtClass.__annotations__:
                if not skip_missing:
                    raise Exception(f"please create the key '{k}' in data class object")
                else:
                    continue
            cls = dtClass.__annotations__[k]
            if cls == tuple:
                name =  f"{str(dtClass)}_{k}"
                if not name in self.delimiters:
                    isFormatDefined = k in [x for x in dir(dtClass) if not re.search("__.*__", x)]
                    delimiter = getattr(dtClass,k) if isFormatDefined else ','
                    self.delimiters[name]=delimiter
                    a = 2

                v = tuple(v.split(self.delimiters[name]))
            if cls == datetime:
                name =  f"{str(dtClass)}_{k}"
                if not name in self.dateFormats:
                    isFormatDefined = k in [x for x in dir(dtClass) if not re.search("__.*__", x)]
                    delimiter = getattr(dtClass,k) if isFormatDefined else '%Y-%m-%d'
                    self.dateFormats[name]=delimiter
                    a = 2

                v = datetime.strptime(v,self.dateFormats[name])
            else:
                v = cls(v)

            setattr(dtClass, k, v)
        
        MissingKeysFromClass = list(set(dtClass.__annotations__.keys())  - set(dt.keys()))
        if not skip_missing and MissingKeysFromClass:
            raise Exception(f"Cound not find '{MissingKeysFromClass}' keys at ini file")



@dataclass
class Person():
    NAME   : str
    age    : int
    amount : float
    friends: tuple = ','
    dob    : datetime = "%Y-%m-%d"


# ini = IniUts('test.ini')
# ini.Section2Dict('IPS2')
# # ini.section2DataClass('PERSON',Person)
# # ini.section2DataClass('PERSON',Person)
# # print(Person.NAME)

# a  =1






