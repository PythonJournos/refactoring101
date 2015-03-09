(Re)designing code
==================

Code smells
-----------

We begin with a single, linear script in the `elex1/ <https://github.com/PythonJournos/refactoring101/tree/master/elex1>`__ directory.
Below are a few reasons why this `code smells <http://en.wikipedia.org/wiki/Code_smell>`__ (some might say it
reeks):

-  It's hard to understand. You have to read the entire script before
   getting a full sense of what it does.
-  It's hard to debug when something goes wrong.
-  It's pretty much impossible to test, beyond eye-balling the output
   file.
-  None of the code is reusable by other programs.

Hacking-It-Out-As-You-Go
------------------------

Scripts like this are often born when a programmer dives immediately into implementing
his code. He sees the end goal -- "summarize election data" -- and gets right to it, hacking
his way through each step of the script until things "work".

The hack-it-out-as-you-go approach can certainly produce working code. But unless you're extremely disciplined,
this process can also yield spaghetti code -- a jumble of hard-to-decipher and error-prone logic that you fear changing.

So, how do we avoid spaghetti code? *By choosing to have lots of small problems instead of one big problem.*

Lots of small problems
----------------------

A key step in the art of designing code is hitting the breaks up front and spending a few minutes thinking 
through the problem at hand. Using this approach, you'll quickly discover that you don't really
have one big problem (*"summarize some election data"*) but a series of small problems:

* Download election data
* Parse election data
* Calculate candidate vote totals and determine winners
* Create a summary spreadsheet

Each of those smaller problems, in turn, can often be decomposed into a series of smaller steps, some of 
which don't become clear until you've started writing the code.

But it's critical at this phase to *NOT* start writing code!!! You will be tempted, but doing so will
switch your brain from "design mode" to the more myopic "code" mode (it's a thing).  Trust in your ability
to implement the code when the time is right (we promise, you'll figure it out), and instead grant yourself a
few minutes of freedom *to design the code*.

If you just can't resist implementing code as you design, then close your laptop
and go old school with pen and paper. A mind-map or flow-chart is a great way to hash out the
high-level design and flow of your program. Or if you're lucky enough to have a whiteboard,
use that to sketch out the initial steps of your program.

Some folks also like writing `pseudocode <http://en.wikipedia.org/wiki/Pseudocode>`__,
though beware the siren call's temptation to slip back into implementing "working" code 
(Python in particular makes this extremely easy).

    *Fun fact*: Jeremy and I are so enthusiastic about whiteboarding that we once sketched out a
    backyard goat roast on an office wall (said design was never implemented).

Shred this code (on paper)
--------------------------

In this tutorial, we already have some ready-baked `spaghetti code <https://github.com/PythonJournos/refactoring101/blob/master/elex1/election_results.py>`__ 
for you to slice and dice into smaller components.

We encourage you to print the code on paper -- yes, dead trees! -- and use a marker to group code bits
into separate functions. As you to try to make sense of the logic and data structures, it's a good idea to reference the 
`source data <https://docs.google.com/spreadsheet/pub?key=0AhhC0IWaObRqdGFkUW1kUmp2ZlZjUjdTYV9lNFJ5RHc&output=html>`__.

This exercise is intended to familiarize you with the data and the mechanics of the code, and get your 
creative juices flowing. As you read the code, think about which sections of logic are related (perhaps they 
process some piece of data, or apply a process to a bunch of data in a loop).

Use circles, brackets, arrows -- whatever marks on paper you need to group together such related bits of code.
Then, try to give them *meaningful names*. These names will become the functions that wrap these bits of logic.

`Naming things is hard <http://martinfowler.com/bliki/TwoHardThings.html>`__, and can become *really hard* if a function is trying to do too many things.
If you find yourself struggling to come up with a clear function name, ask yourself if breaking down the section of code into even smaller parts (
say two or three functions instead of one) would make it easier to assign a clear and meaningful name to each function.

Finally, spend some time thinking about how all these new bits of code will interact. Will one of the functions require an input that comes
from another function? This orchestration of code is typically handled in a function called `main <http://en.wikipedia.org/wiki/Entry_point>`__,
which serves as the entry point and quarterback for the entire script.

Keep in mind there's no "right" approach or solution here.  The overarching goal is to improve the *readability of the code*.

    Whether you resort to pseudocode, a whiteboard, or simple pen-on-paper, the point is to stop thinking
    about *how to implement the code* and instead focus on *how to design the program*.

Once the code design process is complete, try implementing the design.  Ask yourself how this process compared to prior efforts to 
write a script (or unravel someone else's code). Was it easier? Harder? Is the end product easier to read and understand?

In the next section, you'll see our pass at the same exercise, and learn how to further improve this script by organizing functions into
new source files.


Questions
---------

-  What are `unit
   tests <http://docs.python.org/2/library/unittest.html>`__?
-  Can you identify three sections of logic that could be unit tested?
-  What are
   `modules <http://docs.python.org/2/tutorial/modules.html>`__?
-  What are
   `packages <http://docs.python.org/2/tutorial/modules.html#packages>`__?

Exercises
---------

-  Slice up this code into a bunch of functions, where related bits of
   logic are grouped together. Do function names accurately reflect what they
   actually do? If not, how could you rename functions and/or re-organize the code
   to clarify the purpose of each function?
-  Compare your revised script to `our version <https://github.com/PythonJournos/refactoring101/blob/master/elex2/election_results.py>`__.
   What's similar? What's different? Explain 5 things you like or dislike about each and why.
-  Write a unit test for one or more functions extracted from this module.
