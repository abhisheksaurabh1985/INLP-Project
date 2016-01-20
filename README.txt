INSTRUCTIONS FOR RUNNING THE CODE:

* run_program.py

Execute run_program.py for running the script that performs the whole process.
In this file, in line 14 the variable filename has the path to the file with
the queries to test. The final XML output is stored in the output folder. In
this folder, finalOutput.xml is the last evaluated query list. It can also
be found the XML stored for test and train.

* scorer.py

The scorer.py script gets called after the execution of run_program.py,
giving results after running the code. If otherwise a score wants to be
performed from a given file, in line 123 and 124 the files for golden set
and evaluation set can be changed giving a filepath.
