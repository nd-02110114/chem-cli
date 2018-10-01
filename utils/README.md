# Script for boring tasks

## enew
This script is a scf energy watcher for VASP and Quanutum Espresso  
**Usage**
```
// for Quantum Espresso
$ bin/enew/enew.py -e -p seraching_directory 

// for VASP
$ bin/enew/enew.py -v -p searching_directory

-h : help
-v : watch OUTCAR (For VASP)
-e : watch espresso.out (For Quantum Espresso)
-p : path which you want to find
```