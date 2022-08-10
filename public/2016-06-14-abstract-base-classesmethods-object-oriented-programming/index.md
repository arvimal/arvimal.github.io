# Abstract Base Classes/Methods - Object Oriented Programming


_**A**_bstract classes, in short, are classes that are supposed to be inherited or subclassed, rather than instantiated.

Through Abstract Classes, we can enforce a blueprint on the subclasses that inherit the Abstract Class. This means that Abstract classes can be used to define a set of methods that **must** be implemented by it subclasses.

Abstract classes are used when working on large projects where classes have to be inherited, and need to strictly follow certain blueprints.

Python supports Abstract Classes via the module `abc` from version 2.6. Using the `abc` module, its pretty straight forward to implement an Abstract Class.

_**Example 0:**_

\[code language="python"\] import abc

class My\_ABC\_Class(object): \_\_metaclass\_\_ = abc.ABCMeta

@abc.abstractmethod def set\_val(self, val): return

@abc.abstractmethod def get\_val(self): return

\# Abstract Base Class defined above ^^^

\# Custom class inheriting from the above Abstract Base Class, below

class MyClass(My\_ABC\_Class):

def set\_val(self, input): self.val = input

def get\_val(self): print("\\nCalling the get\_val() method") print("I'm part of the Abstract Methods defined in My\_ABC\_Class()") return self.val

def hello(self): print("\\nCalling the hello() method") print("I'm \*not\* part of the Abstract Methods defined in My\_ABC\_Class()")

my\_class = MyClass()

my\_class.set\_val(10) print(my\_class.get\_val()) my\_class.hello() \[/code\] In the code above, `set_val()` and `get_val()` are both abstract methods defined in the Abstract Class `My_ABC_Class()`. Hence it should be implemented in the child class inheriting from `My_ABC_Class()`.

In the child class `MyClass()` , we have to strictly define the abstract classes defined in the Parent class. But the child class is free to implement other methods of their own. The `hello()` method is one such.

This will print :

\[code language="bash"\] # python abstractclasses-1.py

Calling the get\_val() method I'm part of the Abstract Methods defined in My\_ABC\_Class() 10

Calling the hello() method I'm \*not\* part of the Abstract Methods defined in My\_ABC\_Class() \[/code\] The code gets executed properly even if the  `hello()` method is not an abstract method.

Let's check what happens if we don't implement a method marked as an abstract method, in the child class.

_**Example 1:**_

\[code language="python"\] import abc

class My\_ABC\_Class(object): \_\_metaclass\_\_ = abc.ABCMeta

@abc.abstractmethod def set\_val(self, val): return

@abc.abstractmethod def get\_val(self): return

\# Abstract Base Class defined above ^^^

\# Custom class inheriting from the above Abstract Base Class, below

class MyClass(My\_ABC\_Class):

def set\_val(self, input): self.val = input

def hello(self): print("\\nCalling the hello() method") print("I'm \*not\* part of the Abstract Methods defined in My\_ABC\_Class()")

my\_class = MyClass()

my\_class.set\_val(10) print(my\_class.get\_val()) my\_class.hello() \[/code\] _**Example 1**_ is the same as _**Example 0**_ except we don't have the `get_val()` method defined in the child class.

This means that we're breaking the rule of abstraction. Let's see what happens:

\[code language="bash"\] # python abstractclasses-2.py Traceback (most recent call last): File "abstractclasses-2.py", line 50, in my\_class = MyClass() TypeError: Can't instantiate abstract class MyClass with abstract methods get\_val \[/code\]

The traceback clearly states that the child class `MyClass()` cannot be instantiated since it does not implement the Abstract methods defined in it's Parent class.

We mentioned that an Abstract class is supposed to be inherited rather than instantiated. What happens if we try instantiating an Abstract class?

Let's use the same example, this time we're instantiating the Abstract class though.

_**Example 2:**_

\[code language="python"\] import abc

class My\_ABC\_Class(object): \_\_metaclass\_\_ = abc.ABCMeta

@abc.abstractmethod def set\_val(self, val): return

@abc.abstractmethod def get\_val(self): return

\# Abstract Base Class defined above ^^^

\# Custom class inheriting from the above Abstract Base Class, below

class MyClass(My\_ABC\_Class):

def set\_val(self, input): self.val = input

def hello(self): print("\\nCalling the hello() method") print("I'm \*not\* part of the Abstract Methods defined in My\_ABC\_Class()")

my\_class = My\_ABC\_Class()    # <- Instantiating the Abstract Class

my\_class.set\_val(10) print(my\_class.get\_val()) my\_class.hello() \[/code\] What does this output?

\[code language="bash"\] # python abstractclasses-3.py Traceback (most recent call last): File "abstractclasses-3.py", line 54, in <module> my\_class = My\_ABC\_Class() TypeError: Can't instantiate abstract class My\_ABC\_Class with abstract methods get\_val, set\_val \[/code\] As expected, the Python interpreter says that it can't instantiate the abstract class My\_ABC\_Class.

### **Takeaway:**

1. An Abstract Class is supposed to be inherited, not instantiated.
2. The Abstraction nomenclature is applied on the methods within a Class.
3. The abstraction is enforced on methods which are marked with the decorator `@abstractmethod` or `@abc.abstractmethod`, depending on how you imported the module, `from abc import abstractmethod` or `import abc`.
4. It is not mandatory to have all the methods defined as abstract methods, in an Abstract Class.
5. Subclasses/Child classes are enforced to define the methods which are marked with `@abstractmethod` in the Parent class.
6. Subclasses are free to create methods of their own, other than the abstract methods enforced by the Parent class.

### Reference:

1. [https://pymotw.com/2/abc/](https://pymotw.com/2/abc/)
2. [Python beyond the basics - Object Oriented Programming](http://shop.oreilly.com/product/0636920040057.do)

