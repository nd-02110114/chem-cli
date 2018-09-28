# Convert Tool between Gaussian and VASP input file

This tool is made by forking [vtool](https://github.com/wsunccake/vtool)

## v2g 
v2g.py is converted tool  
supports VASP input (POSCAR, CONTCAR) to tranform to Gaussian input (.gjf or.com)  
  
**Usage**
```
$ bin/v2g.py -i POSCAR -o xxx.gjf

-h : help
-i : input file, ie POSCAR
-o : output file, ie xxx.gjf, xxx.com

```

## g2v
g2v.py is converted tool  
supports Gaussian input (.gjf or.com) to tranform to the VASP input (POSCAR)  
  
**Usage**
```
$ bin/g2v.py -i xxx.gjf [-o POSCAR]

-h : help
-i : input file, ie xxx.gjf, xxx.com
-o : output file, ie POSCAR
```

