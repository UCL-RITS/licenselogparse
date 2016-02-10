# licenselogparse
Tools for parsing FlexLM logs

Currently there is a single tool in this repository, maxlic.py.

##maxlic.py

Maxlic.py analyses a FlexLM license manager log file and then prints out the maximum usage of each product it detects, e.g.:

```none
$ ./maxlic.py -l logs/lm_intel.log 
Analysing logs/lm_intel.log
(INTEL).CCompL: 22
(INTEL).DbgL: 1
(INTEL).FCompL: 7
(INTEL).IB87C5F90: 22
```

By default it analyses logs/test.log in the current working directory but it supports these flags:

|-----|--------------|
| -h  | Prints flags |
| -l logfile | Analyse logfile |
| -d | Enable debug output |
