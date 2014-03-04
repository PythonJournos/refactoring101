# refactoring101

![Draw the rest of the owl](http://i2.kym-cdn.com/photos/images/original/000/572/090/77f.jpg)

## Inspiration

> "[Complexity kills][]." ~ *Ray Ozzie*

> "The art of simplicity is a puzzle of complexity." ~ *Douglas Horton*

> "...you're not refactoring; you're just [changing shit][]." ~ *Hamlet D'Arcy*

[Complexity kills]: http://ozzie.net/docs/dawn-of-a-new-day/
[changing shit]: http://hamletdarcy.blogspot.com/2009/06/forgotten-refactorings.html

## Overview

This repo contains code samples demonstrating how to transform a complex, linear script into a modular, 
easier-to-maintain package. The code was written as a reference for the *Python: Beyond the Basics* class 
at [NICAR 2014][], but can also work as a stand-alone tutorial (check out our [main documentation site](http://refactoring-101.readthedocs.org/en/latest/)).

The tutorial uses a small, [fake set of election results][] for demonstration purposes.

Project code evolves through four phases, each contained in a numbered *elex* directory. Below are descriptions of each phase, 
along with related questions and exercises that anticipate the next phase or set of skills.

The goal is to demonstrate how to use Python functions, modules, packages and classes to organize code more effectively. 
We also introduce unit testing as a strategy for writing programs that you can update with confidence. The overarching theme:
 **_As an application or program grows in size, writing readable code with tests can help tame complexity and keep you sane._**

Wondering how to use this tutorial or why the hell we called it *refactoring101*? The [FAQ][] has answers to 
these and sundry other questions. Also, check out the [Resources][] page for wisdom from our tribal elders.

[NICAR 2014]: http://ire.org/conferences/nicar-2014/
[fake set of election results]: https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=html
[FAQ]: https://github.com/PythonJournos/refactoring101/wiki/FAQ
[Resources]: https://github.com/PythonJournos/refactoring101/wiki/Resources
