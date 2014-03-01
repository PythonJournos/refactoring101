.. _OOdesign:

OO Design and Refactoring
=========================

Real World Objects
------------------

In this section, we create classes that model the real world of
elections. These classes are intended to serve as more intuitive
containers for data transformations and complex bits of logic currently
scattered across our application.

The goal is to `hide
complexity <http://en.wikipedia.org/wiki/Encapsulation_(object-oriented_programming)>`__
behind simple
`interfaces <http://en.wikipedia.org/wiki/Interface_(computing)>`__.

We perform these refactorings in a step-by-step fashion and attempt to
`write tests before the actual
code <http://en.wikipedia.org/wiki/Test-driven_development>`__.

So how do we start modeling our domain? We clearly have races and
candidates, which seem like natural...wait for it... "candidates" for
model classes. We also have county-level results associated with each
candidate.

Let's start by creating Candidate and Race classes with some simple
behavior. These classes will eventually be our workhorses, handling most
of the grunt work needed to produce the summary report. But let's start
with the basics.
