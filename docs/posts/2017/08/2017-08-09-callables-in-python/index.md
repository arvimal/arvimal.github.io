---
title: "Callables in Python"
date: 2017-08-09
categories:
  - "programming"
  - "python"
tags:
  - "callable"
  - "python"
  - "python-objects"
---

## Introduction

A `callable` is an object in Python that can be called / executed when called with parantheses `( )`. Classes and functions are callable.

Callables can be a class, a function, or an instance of a class. 

In simple terms, a class/function/instance/builtin is callable if it gets executed when called with parantheses `()`.

#### Example 1:

```python3
In [1]: help() 
Welcome to Python 3.6's help utility! 
-- content omitted -- -------- 

In [2]: int() 
Out[2]: 0

In [3]: 
callable(int) 
Out [3]: True

In [4]: callable(help) 
Out [4]: True

In [5]: def hello():
          print("Howdy!!")

In [6]: hello() 
Out [6]: Howdy!!

In [7]: callable(hello) 
Out [7]: True 
```

In _**Example 1**_, we can see that builtins like `help()`, a pre-defined type such as `int()`, and a custom function `hello()` are all callable. These can be executed while being called with parantheses.

## The \_\_call\_\_() method

The `callable()` builtin helps to determine if an object is callable or not. Internally, it translates to the magic method `__call__()`.

In short:

`my_object(*args)` translates to `my_object.__call__(*args)`

All classes and functions are callable, as well as _instances of classes_ with the `__call__` magic method. An instance of a class/function is usually not callable (even though the class/function itself is), unless the class carries a `__call__` magic method.

ie. An instance is callable only if the class it is instantiated from contains the `__call__` magic method.

- The inbuilt documentation on `callable` states:

```python3
In [1]: print(callable.__doc__) 
Return whether the object is callable (i.e., some kind of function).
```` 

Note that classes are callable, as are instances of classes with a \_\_call\_\_() method. \[/code\]

#### Example 2:

```python3
In [5]: def hello():
 ...:     print("Howdy!!")

In [6]: hello() 
Out [6]: Howdy!!

In [7]: hello.__call__() 
Out [7]: Howdy!!

In [8]: callable(hello) 
Out [8]: True 
```

 _**Example 2**_ shows that a function when called with the parantheses (including any required arguments) is equivalent to calling the `__call__()` magic method. ie.. calling a function/class with parantheses translates to calling the `__call__()` magic method.

_**NOTE:**_ Read more on [Magic methods in Python](https://arvimal.blog/2016/06/02/magic-methods-in-python/)

#### Example 3: Non-callable Instances

\[code language="bash"\]

In \[1\]: type(1) Out\[1\]: int

In \[2\]: callable(1) Out\[2\]: False

In \[3\]: x = 1

In \[4\]: type(x) Out\[4\]: int

In \[5\]: callable(int) Out\[5\]: True

In \[6\]: callable(x) Out\[6\]: False \[/code\] _**Example 3**_ above shows that even though the `int` class is callable, the instances created from the `int` class are not.

Remember that instances will only be callable if the class from which it was instantiated contains a `__call__` method. Inspecting the methods of `class int` reveals that it does not have a `__call__` method.

**NOTE**: You can view the methods of the `int` class using `help(int)` or `dir(int)`.

**Example 4: Another example with Classes**

\[code language="bash"\]

In \[52\]: class tell: ...: def \_\_call\_\_(self): ...: pass

In \[53\]: telling = tell()

In \[54\]: callable(tell) Out\[54\]: True

In \[55\]: callable(telling) Out\[55\]: True

\--------

In \[56\]: class test: ...: pass

In \[57\]: testing = test()

In \[58\]: callable(test) Out\[58\]: True

In \[59\]: callable(testing) Out\[59\]: False \[/code\] Since all classes are by default callable, both the classes `tell` and `test` in _**Example 4**_ are callable. But the instances of these classes necessarily need not be so. Since the class `tell` has the magic method `__call__`, the instance `telling` is callable. But the instance `testing` instantiated from the class `test` is not since the class does not have the magic method. Another set of examples.

#### Example 5: Non-callable instance of a class

\[code language="bash"\]

In \[1\]: class new: ...: def foo(self): ...: print("Hello")

In \[2\]: n = new()

In \[3\]: n() ------------------ TypeError Traceback (most recent call last) in module() ----> 1 n()

TypeError: 'new' object is not callable \[/code\]

#### Example 6: Callable instance of the same class

\[code language="bash"\] In \[4\]: class new: ...: def \_\_call\_\_(self): ...: print("I'm callable!")

In \[5\]: n = new()

In \[6\]: n Out\[6\]: \_\_main\_\_.new at 0x7f7a614b1f98

In \[7\]: n() I'm callable! \[/code\] _**Example 5**_ and _**Example 6**_ shows how a class is itself callable, but unless it carries a `__call__()` method, the instances spawned out of it are not so.

 

### References:

1. [http://docs.python.org/3/library/functions.html#callable](http://docs.python.org/3/library/functions.html#callable)
2. [http://eli.thegreenplace.net/2012/03/23/python-internals-how-callables-work/](http://eli.thegreenplace.net/2012/03/23/python-internals-how-callables-work/)
3. [https://docs.python.org/3/reference/datamodel.html#object.\_\_call\_\_](https://docs.python.org/3/reference/datamodel.html#object.__call__)
