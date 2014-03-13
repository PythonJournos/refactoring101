refactoring101
==============

Inspiration
-----------

    "`Complexity kills <http://ozzie.net/docs/dawn-of-a-new-day/>`__." ~
    *Ray Ozzie*

    "The art of simplicity is a puzzle of complexity." ~ *Douglas
    Horton*

    "...you're not refactoring; you're just `changing
    shit <http://hamletdarcy.blogspot.com/2009/06/forgotten-refactorings.html>`__."
    ~ *Hamlet D'Arcy*


Overview
--------

So you've written a few scripts that get the job done. The machine
does your bidding, but the initial euphoria has worn off.

Bugs are cropping up. Data quirks are creeping in. Duplicate code is spreading like a
virus across projects, or worse, inside the same project. Programs aren't `failing gracefully <http://en.wikipedia.org/wiki/Graceful_exit>`__.

There *must* be a better way, but the path forward is not clear.

If you're like us and have had that itchy feeling, this tutorial is for you.

After you've mastered the basics of writing code, you need to understand how to *design* programs.
The goal of this tutorial is to bridge that gap. We'll demonstrate how to use Python language
features -- functions, modules, packages and classes -- to organize code more effectively. We also
introduce unit testing as a strategy for writing programs that you can update with confidence.

The overarching theme: **As a program grows in size, writing readable code with tests can help tame
complexity and keep you sane.**


How To Use This Tutorial
------------------------

The `Github repo <https://github.com/PythonJournos/refactoring101>`__ contains code samples demonstrating how to transform a
complex, linear script into a modular, easier-to-maintain package. The code was written as a reference for the
*Python: Beyond the Basics* class at `NICAR 2014 <http://ire.org/conferences/nicar-2014/>`__, but can also
work as a stand-alone tutorial.

We use a small, `fake set of election
results <https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=html>`__
for demonstration purposes. Project code evolves through four phases, each contained in a numbered
*elex* directory in the `code repo <https://github.com/PythonJournos/refactoring101>`__.

**Each section ends with questions and/or exercises. These are the most important part of the tutorial.**
You're supposed to wrestle with these questions and exercises. Tinker with the code; break the code; write alternative versions of the code.
Then email me (it's not Jeremy's fault) and explain why the code sucks.
Then read your own code from six months ago ;)


Questions and Resources
-----------------------

Still have questions? Check out the :ref:`FAQ`, as well the :ref:`Resources` page for wisdom from tribal elders.


Table of Contents
-----
.. toctree::
   :maxdepth: 1

   phase1
   phase2
   phase3
   phase4/overview
   phase4/candidates
   phase4/races
   phase4/swapout
   whats_next
   faq
   resources
