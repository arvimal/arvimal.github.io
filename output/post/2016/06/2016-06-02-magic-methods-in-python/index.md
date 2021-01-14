---
title: "Magic methods and Syntactic sugar in Python"
date: "2016-06-02"
categories: 
  - "programming"
  - "python"
tags: 
  - "programming"
  - "python"
---

### Magic methods

_**M**_agic methods are special methods which can be defined (or already designed and available) to act on objects.

Magic methods start and end with underscores `"__"`, and are not implicitly called by the user even though they can be. Most magic methods are used as syntactic sugar by binding it to more clear/easy\_to\_understand keywords.

Python is mostly objects and method calls done on objects. Many available functions in Python are actually tied to magic methods_**.**_ Let's checkout a few examples.

_**Example 0:**_

\[code language="python"\] In \[1\]: my\_var = "Hello!"

In \[2\]: print(my\_var) Hello!

In \[3\]: my\_var.\_\_repr\_\_() Out\[3\]: "'Hello!'" \[/code\] As we can see, the `__repr__()` magic method can be called to print the object, ie.. it is bound to the `print()` keyword.

This is true for many other builtin keywords/operators as well.

_**Example 1:**_

\[code language="python"\] In \[22\]: my\_var = "Hello, " In \[23\]: my\_var1 = "How are you?"

In \[24\]: my\_var + my\_var1 Out\[24\]: 'Hello, How are you?'

In \[25\]: my\_var.\_\_add\_\_(my\_var1) Out\[25\]: 'Hello, How are you?' \[/code\] Here, Python interprets the `+` sign as a mapping to the magic method `__add__()`, and calls it on the L-value (Left hand object value) `my_var`, with the R-value (Right hand object value) as the argument.

When a builtin function is called on an object, in many cases it is mapped to the magic method.

_**Example 2:**_

\[code language="python"\] In \[69\]: my\_list\_1 = \['a', 'b', 'c', 'd'\]

In \[70\]: 'a' in my\_list\_1 Out\[70\]: True

In \[71\]: my\_list\_1.\_\_contains\_\_("a") Out\[71\]: True \[/code\]

The `in` builtin is mapped to the `__contains__()`method.

The methods available for an object should mostly be dependent on the type of the object.

_**Example 3:**_

\[code language="python" wraplines="true"\] In \[59\]: my\_num = 1

In \[60\]: type(my\_num) Out\[60\]: int

In \[61\]: my\_num.\_\_doc\_\_ Out\[61\]: Out\[61\]: "int(x=0) -> int or long\\nint(x, base=10) -> int or long\\n\\nConvert a number or string to an integer, or return 0 if no arguments\\nare given. ....>>>

In \[62\]: help(my\_num) class int(object) | int(x=0) -> int or long | int(x, base=10) -> int or long | | Convert a number or string to an integer, or return 0 if no arguments | are given. If x is floating point, the conversion truncates towards zero. | If x is outside the integer range, the function returns a long instead.

\[/code\]

From the tests above, we can understand that the `help()` function is actually mapped to the `object.__doc__` magic method. It's the same doc string that \_\_doc\_\_ and help() uses.

**_NOTE: Due to the syntax conversion (`+` to `__add__(),and other conversions`), operators like `+` , `in`, etc.. are also called Syntactic sugar._**

### What is Syntactic sugar?

_**A**_ccording to [Wikipedia](https://en.wikipedia.org/wiki/Syntactic_sugar), Syntact sugar is:

> In [computer science](https://en.wikipedia.org/wiki/Computer_science "Computer science"), **syntactic sugar** is [syntax](https://en.wikipedia.org/wiki/Syntax_%28programming_languages%29 "Syntax (programming languages)") within a [programming language](https://en.wikipedia.org/wiki/Programming_language "Programming language") that is designed to make things easier to read or to express. It makes the language "sweeter" for human use: things can be expressed more clearly, more concisely, or in an alternative style that some may prefer.

Hence, _**magic methods**_ can be said to be _**Syntactic sugar.**_ But it's not just magic methods that are mapped to syntactic sugar methods, but higher order features such as [Decorators](https://arvimal.wordpress.com/2016/05/30/decorators-object-oriented-programming/) are as well.

_**Example 4:**_ 

\[code language="python"\] def my\_decorator(my\_function): def inner\_decorator(): print("This happened before!") my\_function() print("This happens after ") print("This happened at the end!") return inner\_decorator

def my\_decorated(): print("This happened!")

var = my\_decorator(my\_decorated)

if \_\_name\_\_ == '\_\_main\_\_': var() \[/code\] The example above borrows from one of the examples in the post on [Decorators](https://arvimal.wordpress.com/2016/05/30/decorators-object-oriented-programming/).

Here, `my_decorator()` is a decorator and is used to decorate `my_decorated()`. But rather than calling the decorator function `my_decorator()` with the argument `my_decorated()`, the above code can be syntactically sugar-coated as below:

\[code language="python"\] def my\_decorator(my\_function): def inner\_decorator(): print("This happened before!") my\_function() print("This happens after ") print("This happened at the end!") return inner\_decorator

@my\_decorator def my\_decorated(): print("This happened!")

if \_\_name\_\_ == '\_\_main\_\_': my\_decorated() \[/code\] Observing both code snippets, the decorator is syntactically sugar coated and called as:

**@my\_decorator**

instead of instantiating the decorator with the function to be decorated as an argument, ie..

**var = my\_decorator(my\_decorated)**

### A few syntax resolution methods:

1. 'name' in my\_list       ->      my\_list.\_\_contains\_\_('name')
2. len(my\_list)                  ->      my\_list.\_\_len\_\_()
3. print(my\_list)              ->      my\_list.\_\_repr\_\_()
4. my\_list == "value"     ->      my\_list.\_\_eq\_\_("value")
5. my\_list\[5\]                      ->      my\_list.\_\_getitem\_\_(5)
6. my\_list\[5:10\]                 ->     my\_list.\_\_getslice\_\_(5, 10)

**NOTE: This article is written from the notes created while learning magic methods. The following articles (along with several others) were referred as part of the process.**

1. **[A Guide to Python's Magic Methods](http://www.rafekettler.com/magicmethods.pdf), by Rafe Kettler**
2. **[Special method names](https://docs.python.org/3/reference/datamodel.html#special-method-names), The Official Python 3 documentation**
