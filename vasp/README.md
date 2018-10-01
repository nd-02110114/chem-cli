# Script for VASP

## potcar.py
This script is a automatic creater for POTCAR

**Usage**
```
$ bin/potcar.py -a H Cu S -p ....

-h : help
-a : atoms about which you want to create POTCAR (order is important) 
-o : output path (optional, default: current directory)
-p : pseudopotential directory path
```

## poscar.py
This script is a automatic creater for POTCAR from .gjf file  

**Usage**
```
$ bin/potcar.py -f -o -p ....

-h : help
-f : fix number (you can fix the atom, optional)
-o : output path (optional, default: current directory)
-p : path for .gjf file
```