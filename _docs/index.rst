refactoring101
==============

.. figure:: http://i2.kym-cdn.com/photos/images/original/000/572/090/77f.jpg
   :alt: Draw the rest of the owl

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

So you have a few scripts under your belt that get the job done. But the initial 
euphoria of making the machine do your bidding is wearing off...

Bugs are cropping up. Data mistakes are creeping in. You're copying code between projects, 
or worse, inside the same project. Your programs aren't `failing gracefully <http://en.wikipedia.org/wiki/Graceful_exit>`__.

You realize there's a better way. You see how all these really smart people write elegant
code to handle the same problems, but you're bewildered at how to do the same.

If you're like us and have had that itchy feeling, this tutorial is for you.

After you've mastered the basics of writing code, you need to understand how to *design* programs. 
The goal of this tutorial is to bridge that gap. We'll demonstrate how to use Python language
features -- functions, modules,
packages and classes -- to organize code more effectively. We also
introduce unit testing as a strategy for writing programs that you can
update with confidence. The overarching theme: **As a program grows in size, writing readable code with tests can help tame
complexity and keep you sane.**

The `Github repo <https://github.com/PythonJournos/refactoring101>`__ contains code samples demonstrating how to transform a
complex, linear script into a modular, easier-to-maintain package. The
code was written as a reference for the *Python: Beyond the Basics* class
at `NICAR 2014 <http://ire.org/conferences/nicar-2014/>`__, but can also
work as a stand-alone tutorial.

The tutorial uses a small, `fake set of election
results <https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=html>`__
for demonstration purposes.

Project code evolves through four phases, each contained in a numbered
*elex* directory. Below are descriptions of each phase, along with
related questions and exercises that anticipate the next phase or set of
skills.

Wondering how to use this tutorial or why the hell we called it
*refactoring101*? The :ref:`FAQ` has answers to these and sundry other questions. 
Also, check out the :ref:`Resources` page for wisdom from our tribal elders.

Table of Contents
-----
.. toctree::
   :maxdepth: 2

   phase1
   phase2
   phase3
   phase4
   whats_next
   faq
   resources

