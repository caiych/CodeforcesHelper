CodeforcesHelper
================

A script get the HTML of given problem, generate a directory and a test script

# Usage

Download the *CF* and put it into your system path.

run *CF <problem id>* to generate a directory under current path. 
e.g. *CF 353C* or *CF 353/C*

run *./test <filename>* to test a source code or something executable.
e.g. *./test main.cc* or *./test a.out*

# Features

* Automatically parse the HTML of a given problem ID in a problem set(gym).
* Generate a testscript.
* Compile and test a source code ( only C++ is available so far ).





# TODO

* may configure the test script
* support some other language
* is the testscript goes into system directory is better?
