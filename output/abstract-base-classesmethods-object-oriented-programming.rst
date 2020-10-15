Abstract Base Classes/Methods - Object Oriented Programming
###########################################################
:date: 2016-06-14 11:56
:author: arvimal
:category: Programming, Python
:tags: abstract base class, abstract methods, abstractmethod, Object Oriented Programming, programming, python
:slug: abstract-base-classesmethods-object-oriented-programming
:status: published

**A**\ bstract classes, in short, are classes that are supposed to be inherited or subclassed, rather than instantiated.

Through Abstract Classes, we can enforce a blueprint on the subclasses that inherit the Abstract Class. This means that Abstract classes can be used to define a set of methods that **must** be implemented by it subclasses.

Abstract classes are used when working on large projects where classes have to be inherited, and need to strictly follow certain blueprints.

Python supports Abstract Classes via the module ``abc`` from version 2.6. Using the ``abc`` module, its pretty straight forward to implement an Abstract Class.

**Example 0:**

| [code language="python"]
| import abc

| class My_ABC_Class(object):
| \__metaclass_\_ = abc.ABCMeta

| @abc.abstractmethod
| def set_val(self, val):
| return

| @abc.abstractmethod
| def get_val(self):
| return

# Abstract Base Class defined above ^^^

# Custom class inheriting from the above Abstract Base Class, below

class MyClass(My_ABC_Class):

| def set_val(self, input):
| self.val = input

| def get_val(self):
| print("\nCalling the get_val() method")
| print("I'm part of the Abstract Methods defined in My_ABC_Class()")
| return self.val

| def hello(self):
| print("\nCalling the hello() method")
| print("I'm \*not\* part of the Abstract Methods defined in My_ABC_Class()")

my_class = MyClass()

| my_class.set_val(10)
| print(my_class.get_val())
| my_class.hello()
| [/code]
| In the code above, ``set_val()`` and ``get_val()`` are both abstract methods defined in the Abstract Class ``My_ABC_Class()``. Hence it should be implemented in the child class inheriting from ``My_ABC_Class()``.

In the child class ``MyClass()`` , we have to strictly define the abstract classes defined in the Parent class. But the child class is free to implement other methods of their own. The ``hello()`` method is one such.

This will print :

| [code language="bash"]
| # python abstractclasses-1.py

| Calling the get_val() method
| I'm part of the Abstract Methods defined in My_ABC_Class()
| 10

| Calling the hello() method
| I'm \*not\* part of the Abstract Methods defined in My_ABC_Class()
| [/code]
| The code gets executed properly even if the  ``hello()`` method is not an abstract method.

Let's check what happens if we don't implement a method marked as an abstract method, in the child class.

**Example 1:**

| [code language="python"]
| import abc

| class My_ABC_Class(object):
| \__metaclass_\_ = abc.ABCMeta

| @abc.abstractmethod
| def set_val(self, val):
| return

| @abc.abstractmethod
| def get_val(self):
| return

# Abstract Base Class defined above ^^^

# Custom class inheriting from the above Abstract Base Class, below

class MyClass(My_ABC_Class):

| def set_val(self, input):
| self.val = input

| def hello(self):
| print("\nCalling the hello() method")
| print("I'm \*not\* part of the Abstract Methods defined in My_ABC_Class()")

my_class = MyClass()

| my_class.set_val(10)
| print(my_class.get_val())
| my_class.hello()
| [/code]
| **Example 1 **\ is the same as \ **Example 0** except we don't have the ``get_val()`` method defined in the child class.

This means that we're breaking the rule of abstraction. Let's see what happens:

| [code language="bash"]
| # python abstractclasses-2.py
| Traceback (most recent call last):
| File "abstractclasses-2.py", line 50, in
| my_class = MyClass()
| TypeError: Can't instantiate abstract class MyClass with abstract methods get_val
| [/code]

The traceback clearly states that the child class ``MyClass()`` cannot be instantiated since it does not implement the Abstract methods defined in it's Parent class.

We mentioned that an Abstract class is supposed to be inherited rather than instantiated. What happens if we try instantiating an Abstract class?

Let's use the same example, this time we're instantiating the Abstract class though.

**Example 2:**

| [code language="python"]
| import abc

| class My_ABC_Class(object):
| \__metaclass_\_ = abc.ABCMeta

| @abc.abstractmethod
| def set_val(self, val):
| return

| @abc.abstractmethod
| def get_val(self):
| return

# Abstract Base Class defined above ^^^

# Custom class inheriting from the above Abstract Base Class, below

class MyClass(My_ABC_Class):

| def set_val(self, input):
| self.val = input

| def hello(self):
| print("\nCalling the hello() method")
| print("I'm \*not\* part of the Abstract Methods defined in My_ABC_Class()")

my_class = My_ABC_Class()    # <- Instantiating the Abstract Class

| my_class.set_val(10)
| print(my_class.get_val())
| my_class.hello()
| [/code]
| What does this output?

| [code language="bash"]
| # python abstractclasses-3.py
| Traceback (most recent call last):
| File "abstractclasses-3.py", line 54, in <module>
| my_class = My_ABC_Class()
| TypeError: Can't instantiate abstract class My_ABC_Class with abstract methods get_val, set_val
| [/code]
| As expected, the Python interpreter says that it can't instantiate the abstract class My_ABC_Class.

**Takeaway: **
~~~~~~~~~~~~~~

#. An Abstract Class is supposed to be inherited, not instantiated.
#. The Abstraction nomenclature is applied on the methods within a Class.
#. The abstraction is enforced on methods which are marked with the decorator ``@abstractmethod`` or ``@abc.abstractmethod``, depending on how you imported the module, ``from abc import abstractmethod`` or ``import abc``.
#. It is not mandatory to have all the methods defined as abstract methods, in an Abstract Class.
#. Subclasses/Child classes are enforced to define the methods which are marked with ``@abstractmethod`` in the Parent class.
#. Subclasses are free to create methods of their own, other than the abstract methods enforced by the Parent class.

Reference:
~~~~~~~~~~

#. https://pymotw.com/2/abc/
#. `Python beyond the basics - Object Oriented Programming <http://shop.oreilly.com/product/0636920040057.do>`__
