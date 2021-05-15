---
title: "Inheritance and super() - Object Oriented Programming"
date: 2016-07-01
categories:
  - "programming"
  - "python"
tags:
  - "inheritance"
  - "object-oriented-programming"
  - "python"
  - "super"
---

_**s**_uper() is a feature through which inherited methods can be accessed, which has been overridden in a class. It can also help with the MRO lookup order in case of multiple inheritance. This may not be obvious first, but a few examples should help to drive the point home.

Inheritance and method overloading was discussed in a previous [post](https://arvimal.wordpress.com/2016/06/29/inheritance-and-method-overloading-object-oriented-programming/), where we saw how inherited methods can be overloaded or enhanced in the child classes.

In many scenarios, it's needed to overload an inherited method, but also call the actual method defined in the Parent class.

Let's start off with a simple example based on Inheritance, and build from there.

_**Example 0:**_

\[code language="python"\] class MyClass(object):

def func(self): print("I'm being called from the Parent class!")

class ChildClass(MyClass): pass

my\_instance\_1 = ChildClass() my\_instance\_1.func() \[/code\] This outputs:

\[code language="python"\] In \[18\]: %run /tmp/super-1.py I'm being called from the Parent class \[/code\] In _**Example 0**_, we have two classes, `MyClass` and `ChildClass`. The latter inherits from the former, and the parent class `MyClass` has a method named `func` defined.

Since `ChildClass` inherits from `MyClass`, the child class has access to the methods defined in the parent class. An instance is created `my_instance_2`, for `ChildClass.`

Calling `my_instance_1.func()` will print the statement from the Parent class, due to the inheritance.

Building up on the first example:

_**Example 1:**_

\[code language="python"\] class MyClass(object):

def func(self): print("I'm being called from the Parent class")

class ChildClass(MyClass):

def func(self): print("I'm being called from the Child class")

my\_instance\_1 = MyClass() my\_instance\_2 = ChildClass()

my\_instance\_1.func() my\_instance\_2.func() \[/code\] This outputs:

\[code language="python"\] In \[19\]: %run /tmp/super-1.py I'm being called from the Parent class I'm being called from the Child class \[/code\] This example has a slight difference, both the child class as well as the parent class have the same method defined, ie.. `func`. In this scenario, the parent class' method is overridden by the child class method.

ie.. if we call the `func()` method from the instance of `ChildClass`, it need not go a fetch the method from its Parent class, since it's already defined locally.

**NOTE: This is due to the Method Resolution Order, discussed in an earlier [post](https://arvimal.wordpress.com/2016/05/30/method-resolution-order-object-oriented-programming/).**

But what if there is a scenario that warranties the need for specifically calling methods defined in the Parent class, from the instance of a child class?

ie.. How to call the methods defined in the Parent class, through the instance of the Child class, even if the Parent class method is overloaded in the Child class?

In such a case, the inbuilt function `super()` can be used. Let's add to the previous example.

_**Example 2:**_

\[code language="python"\] class MyClass(object):

def func(self): print("I'm being called from the Parent class")

class ChildClass(MyClass):

def func(self): print("I'm actually being called from the Child class") print("But...") # Calling the \`func()\` method from the Parent class. super(ChildClass, self).func()

my\_instance\_2 = ChildClass() my\_instance\_2.func() \[/code\] This outputs:

\[code language="python"\] In \[21\]: %run /tmp/super-1.py I'm actually being called from the Child class But... I'm being called from the Parent class \[/code\]

### How is the code structured?

1. We have two classes `MyClass` and `ChildClass`.
2. The latter is inheriting from the former.
3. Both classes have a method named `func`
4. The child class `ChildClass` is instantiated as `my_instance_2`
5. The `func` method is called from the instance.

### How does the code work?

1. When the `func` method is called, the interpreter searches it using the Method Resolution Order, and find the method defined in the class `ChildClass`.
2. Since it finds the method in the child class, it executes it, and prints the string "I'm actually being called from the Child class", as well "But..."
3. The next statement is `super` which calls the method `func` defined in the parent class of `ChildClass`
4. Since the control is now passed onto the `func` method in the Parent class via `super`, the corresponding `print()` statement is printed to stdout.

Example 2 can also be re-written as :

\[code language="python"\] class MyClass(object):

def func(self): print("I'm being called from the Parent class")

class ChildClass(MyClass):

def func(self): print("I'm actually being called from the Child class") print("But...") # Calling the \`func()\` method from the Parent class. # super(ChildClass, self).func() MyClass.func(self) # Call the method directly via Parent class

my\_instance\_2 = ChildClass() my\_instance\_2.func() \[/code\]

 

_**NOTE:**_ _The example above uses the Parent class directly to access it's method. Even though it works, it is not the best way to do it since the code is tied to the Parent class name. If the Parent class name changes, the child/sub class code has to be changed as well._

Let's see another example for  `super()` . This is from our previous article on [Inheritance and method overloading](https://arvimal.wordpress.com/2016/06/29/inheritance-and-method-overloading-object-oriented-programming/).

_**Example 3:**_

\[code language="python"\] import abc

class MyClass(object):

\_\_metaclass\_\_ = abc.ABCMeta

def my\_set\_val(self, value): self.value = value

def my\_get\_val(self): return self.value

@abc.abstractmethod def print\_doc(self): return

class MyChildClass(MyClass):

def my\_set\_val(self, value): if not isinstance(value, int): value = 0 super(MyChildClass, self).my\_set\_val(self)

def print\_doc(self): print("Documentation for MyChild Class")

my\_instance = MyChildClass() my\_instance.my\_set\_val(100) print(my\_instance.my\_get\_val()) print(my\_instance.print\_doc()) \[/code\] The code is already discussed [here](https://arvimal.wordpress.com/2016/06/29/inheritance-and-method-overloading-object-oriented-programming/). The `my_set_val` method is defined in both the child class as well as the parent class.

We overload the `my_set_val` method defined in the parent class, in the child class. But after enhancing/overloading it, we call the `my_set_val` method specifically from the Parent class using `super()` and thus enhance it.

### Takeaway:

1. super() helps to specifically call the Parent class method which has been overridden in the child class, from the child class.
2. The super() in-built function can be used to call/refer the Parent class without explicitly naming them. This helps in situations where the Parent class name may change. Hence, super() helps in avoiding strong ties with class names and increases maintainability.
3. super() helps the most when there are multiple inheritance happening, and the MRO ends up being complex. In case you need to call a method from a specific parent class, use super().
4. There are multiple ways to call a method from a Parent class.
    1. <Parent-Class>.<method>
    2. super(<ChildClass>, self).<method>
    3. super().<method>

### References:

1. https://docs.python.org/2/library/functions.html#super
2. https://rhettinger.wordpress.com/2011/05/26/super-considered-super/
3. https://stackoverflow.com/questions/222877/how-to-use-super-in-python
