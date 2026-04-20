---
title: "Magic methods and Syntactic sugar in Python"
date: 2016-06-02
categories:
  - "programming"
  - "python"
tags:
  - "programming"
  - "python"
---
<!--more-->
### Magic methods

_**M**_agic methods are special methods which can be defined (or already designed and available) to act on objects.

Magic methods start and end with underscores `"__"`, and are not implicitly called by the user even though they can be. Most magic methods are used as syntactic sugar by binding it to more clear/easy\_to\_understand keywords.

Python is mostly objects and method calls done on objects. Many available functions in Python are actually tied to magic methods_**.**_ Let's checkout a few examples.

_**Example 0:**_

```python
In [1]: my_var = "Hello!"

In [2]: print(my_var) Hello!

In [3]: my_var.__repr__() Out[3]: "'Hello!'"
```

As we can see, the `__repr__()` magic method can be called to print the object, ie.. it is bound to the `print()` keyword.

This is true for many other builtin keywords/operators as well.

_**Example 1:**_

```python
In [22]: my_var = "Hello, " In [23]: my_var1 = "How are you?"

In [24]: my_var + my_var1 Out[24]: 'Hello, How are you?'

In [25]: my_var.__add__(my_var1) Out[25]: 'Hello, How are you?'
```

Here, Python interprets the `+` sign as a mapping to the magic method `__add__()`, and calls it on the L-value (Left hand object value) `my_var`, with the R-value (Right hand object value) as the argument.

When a builtin function is called on an object, in many cases it is mapped to the magic method.

_**Example 2:**_

```python
In [69]: my_list_1 = ['a', 'b', 'c', 'd']

In [70]: 'a' in my_list_1 Out[70]: True

In [71]: my_list_1.__contains__("a") Out[71]: True
```

The `in` builtin is mapped to the `__contains__()`method.

The methods available for an object should mostly be dependent on the type of the object.

_**Example 3:**_

```python
In [59]: my_num = 1

In [60]: type(my_num) Out[60]: int

In [61]: my_num.__doc__ Out[61]: Out[61]: "int(x=0) -> int or long\\nint(x, base=10) -> int or long\\n\\nConvert a number or string to an integer, or return 0 if no arguments\\nare given. ....>>>

In [62]: help(my_num) class int(object) | int(x=0) -> int or long | int(x, base=10) -> int or long | | Convert a number or string to an integer, or return 0 if no arguments | are given. If x is floating point, the conversion truncates towards zero. | If x is outside the integer range, the function returns a long instead.

```

From the tests above, we can understand that the `help()` function is actually mapped to the `object.__doc__` magic method. It's the same doc string that __doc__ and help() uses.

**_NOTE: Due to the syntax conversion (`+` to `__add__(),and other conversions`), operators like `+` , `in`, etc.. are also called Syntactic sugar._**

### What is Syntactic sugar?

_**A**_ccording to [Wikipedia](https://en.wikipedia.org/wiki/Syntactic_sugar), Syntact sugar is:

> In [computer science](https://en.wikipedia.org/wiki/Computer_science "Computer science"), **syntactic sugar** is [syntax](https://en.wikipedia.org/wiki/Syntax_%28programming_languages%29 "Syntax (programming languages)") within a [programming language](https://en.wikipedia.org/wiki/Programming_language "Programming language") that is designed to make things easier to read or to express. It makes the language "sweeter" for human use: things can be expressed more clearly, more concisely, or in an alternative style that some may prefer.

Hence, _**magic methods**_ can be said to be _**Syntactic sugar.**_ But it's not just magic methods that are mapped to syntactic sugar methods, but higher order features such as [Decorators](https://arvimal.wordpress.com/2016/05/30/decorators-object-oriented-programming/) are as well.

_**Example 4:**_

```python
def my_decorator(my_function): def inner_decorator(): print("This happened before!") my_function() print("This happens after ") print("This happened at the end!") return inner_decorator

def my_decorated(): print("This happened!")

var = my_decorator(my_decorated)

if __name__ == '__main__': var()
```

The example above borrows from one of the examples in the post on [Decorators](https://arvimal.wordpress.com/2016/05/30/decorators-object-oriented-programming/).

Here, `my_decorator()` is a decorator and is used to decorate `my_decorated()`. But rather than calling the decorator function `my_decorator()` with the argument `my_decorated()`, the above code can be syntactically sugar-coated as below:

```python
def my_decorator(my_function): def inner_decorator(): print("This happened before!") my_function() print("This happens after ") print("This happened at the end!") return inner_decorator

@my_decorator def my_decorated(): print("This happened!")

if __name__ == '__main__': my_decorated()
```

Observing both code snippets, the decorator is syntactically sugar coated and called as:

**@my\_decorator**

instead of instantiating the decorator with the function to be decorated as an argument, ie..

**var = my\_decorator(my\_decorated)**

### A few syntax resolution methods:

1. 'name' in my\_list       ->      my\_list.__contains__('name')
2. len(my\_list)                  ->      my\_list.__len__()
3. print(my\_list)              ->      my\_list.__repr__()
4. my\_list == "value"     ->      my\_list.__eq__("value")
5. my\_list\[5\]                      ->      my\_list.__getitem__(5)
6. my\_list\[5:10\]                 ->     my\_list.__getslice__(5, 10)

**NOTE: This article is written from the notes created while learning magic methods. The following articles (along with several others) were referred as part of the process.**

1. **[A Guide to Python's Magic Methods](http://www.rafekettler.com/magicmethods.pdf), by Rafe Kettler**
2. **[Special method names](https://docs.python.org/3/reference/datamodel.html#special-method-names), The Official Python 3 documentation**
