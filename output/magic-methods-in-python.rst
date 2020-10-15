Magic methods and Syntactic sugar in Python
###########################################
:date: 2016-06-02 12:12
:author: arvimal
:category: Programming, Python
:tags: programming, python
:slug: magic-methods-in-python
:status: published

Magic methods
~~~~~~~~~~~~~

**M**\ agic methods are special methods which can be defined (or already designed and available) to act on objects.

Magic methods start and end with underscores ``"__"``, and are not implicitly called by the user even though they can be. Most magic methods are used as syntactic sugar by binding it to more clear/easy_to_understand keywords.

Python is mostly objects and method calls done on objects. Many available functions in Python are actually tied to magic methods\ **. **\ Let's checkout a few examples.

**Example 0:**

| [code language="python"]
| In [1]: my_var = "Hello!"

| In [2]: print(my_var)
| Hello!

| In [3]: my_var.__repr__()
| Out[3]: "'Hello!'"
| [/code]
| As we can see, the ``__repr__()`` magic method can be called to print the object, ie.. it is bound to the ``print()`` keyword.

This is true for many other builtin keywords/operators as well.

**Example 1:**

| [code language="python"]
| In [22]: my_var = "Hello, "
| In [23]: my_var1 = "How are you?"

| In [24]: my_var + my_var1
| Out[24]: 'Hello, How are you?'

| In [25]: my_var.__add__(my_var1)
| Out[25]: 'Hello, How are you?'
| [/code]
| Here, Python interprets the ``+`` sign as a mapping to the magic method ``__add__()``, and calls it on the L-value (Left hand object value) ``my_var``, with the R-value (Right hand object value) as the argument.

When a builtin function is called on an object, in many cases it is mapped to the magic method.

**Example 2:**

| [code language="python"]
| In [69]: my_list_1 = ['a', 'b', 'c', 'd']

| In [70]: 'a' in my_list_1
| Out[70]: True

| In [71]: my_list_1.__contains__("a")
| Out[71]: True
| [/code]

The ``in`` builtin is mapped to the ``__contains__()``\ method.

The methods available for an object should mostly be dependent on the type of the object.

**Example 3:**

| [code language="python" wraplines="true"]
| In [59]: my_num = 1

| In [60]: type(my_num)
| Out[60]: int

| In [61]: my_num.__doc_\_
| Out[61]: Out[61]: "int(x=0) -> int or long\nint(x, base=10) -> int or long\n\nConvert a number or string to an integer, or return 0 if no arguments\nare given. ....>>>

| In [62]: help(my_num)
| class int(object)
| \| int(x=0) -> int or long
| \| int(x, base=10) -> int or long
| \|
| \| Convert a number or string to an integer, or return 0 if no arguments
| \| are given. If x is floating point, the conversion truncates towards zero.
| \| If x is outside the integer range, the function returns a long instead.

[/code]

From the tests above, we can understand that the ``help()`` function is actually mapped to the ``object.__doc__`` magic method. It's the same doc string that \__doc_\_ and help() uses.

**NOTE: Due to the syntax conversion (``+`` to ``__add__(),and other conversions``), operators like ``+`` , ``in``, etc.. are also called Syntactic sugar.**

What is Syntactic sugar?
~~~~~~~~~~~~~~~~~~~~~~~~

**A**\ ccording to \ `Wikipedia <https://en.wikipedia.org/wiki/Syntactic_sugar>`__, Syntact sugar is:

   In `computer science <https://en.wikipedia.org/wiki/Computer_science>`__, **syntactic sugar** is `syntax <https://en.wikipedia.org/wiki/Syntax_%28programming_languages%29>`__ within a `programming language <https://en.wikipedia.org/wiki/Programming_language>`__ that is designed to make things easier to read or to express. It makes the language "sweeter" for human use: things can be expressed more clearly, more concisely, or in an alternative style that some may prefer.

Hence, \ **magic methods** can be said to be \ **Syntactic sugar. **\ But it's not just magic methods that are mapped to syntactic sugar methods, but higher order features such as \ `Decorators <https://arvimal.wordpress.com/2016/05/30/decorators-object-oriented-programming/>`__ are as well.

**Example 4: **

| [code language="python"]
| def my_decorator(my_function):
| def inner_decorator():
| print("This happened before!")
| my_function()
| print("This happens after ")
| print("This happened at the end!")
| return inner_decorator

| def my_decorated():
| print("This happened!")

var = my_decorator(my_decorated)

| if \__name_\_ == '__main__':
| var()
| [/code]
| The example above borrows from one of the examples in the post on \ `Decorators <https://arvimal.wordpress.com/2016/05/30/decorators-object-oriented-programming/>`__.

Here, ``my_decorator()`` is a decorator and is used to decorate ``my_decorated()``. But rather than calling the decorator function \ ``my_decorator()`` with the argument ``my_decorated()``, the above code can be syntactically sugar-coated as below:

| [code language="python"]
| def my_decorator(my_function):
| def inner_decorator():
| print("This happened before!")
| my_function()
| print("This happens after ")
| print("This happened at the end!")
| return inner_decorator

| @my_decorator
| def my_decorated():
| print("This happened!")

| if \__name_\_ == '__main__':
| my_decorated()
| [/code]
| Observing both code snippets, the decorator is syntactically sugar coated and called as:

**@my_decorator**

instead of instantiating the decorator with the function to be decorated as an argument, ie..

**var = my_decorator(my_decorated)**

A few syntax resolution methods:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. 'name' in my_list       ->      my_list.__contains__('name')
#. len(my_list)                  ->      my_list.__len__()
#. print(my_list)              ->      my_list.__repr__()
#. my_list == "value"     ->      my_list.__eq__("value")
#. my_list[5]                      ->      my_list.__getitem__(5)
#. my_list[5:10]                 ->     my_list.__getslice__(5, 10)

**NOTE: This article is written from the notes created while learning magic methods. The following articles (along with several others) were referred as part of the process.**

#. `A Guide to Python's Magic Methods <http://www.rafekettler.com/magicmethods.pdf>`__\ **, by Rafe Kettler**
#. `Special method names <https://docs.python.org/3/reference/datamodel.html#special-method-names>`__\ **, The Official Python 3 documentation**
