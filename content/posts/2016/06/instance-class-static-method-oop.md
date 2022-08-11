---
title: "Instance, Class, and Static methods - Object Oriented Programming"
date: 2016-06-12
categories:
  - "programming"
  - "python"
---
<!--more-->
_**F**_unctions defined under a class are also called `methods`. Most of the methods are accessed through an instance of the class.

There are three types of methods:

1. Instance methods
2. Static methods
3. Class methods

Both Static methods and Class methods can be called using the `@staticmethod` and `@classmethod` syntactic sugar respectively.

### Instance methods

_**I**_nstance methods are also called **_Bound methods_** since the instance is bound to the class via `self`. Read a simple explanation on `self` [here](https://arvimal.wordpress.com/2016/06/12/self-in-python/).

Almost all methods are Instance methods since they are accessed through instances.

For example:

\[code language="python"\] class MyClass(object):

def set\_val(self, val): self.value = val

def get\_val(self): print(self.value) return self.value

a = MyClass() b = MyClass()

a.set\_val(10) b.set\_val(100)

a.get\_val() b.get\_val() \[/code\] The above code snippet shows manipulating the two methods  `set_val()` and `get_val()` . These are done through the instances `a` and `b`. Hence these methods are called **Instance methods**.

**NOTE: Instance methods have `self` as their first argument. `self` is the instance itself.**

All methods defined under a class are usually called via the instance instantiated from the class. But there are methods which can work without instantiating an instance.

Class methods and Static methods don't require an instance, and hence don't need `self` as their first argument.

### Static methods

Static methods are functions/methods which doesn't need a binding to a class or an instance.

1. Static methods, as well as Class methods, don't require an instance to be called.
2. Static methods doesn't need  `self` or `cls` as the first argument since it's not bound to an instance or class.
3. Static methods are normal functions, but within a class.
4. Static methods are defined with the keyword `@staticmethod` above the function/method.
5. Static methods are usually used to work on Class Attributes.

\============================= **A note on class attributes**

Attributes set explicitly under a class (not under a function) are called Class Attributes.

For example:

\[code language="python"\] class MyClass(object): value = 10

def my\_func(self): pass \[/code\] In the code snippet above, `value = 10` is an attribute defined under the class `MyClass()` and not under any functions/methods. Hence, it's called a Class attribute. =============================

Let's check out an example on static methods and class attributes:

\[code language="python"\] class MyClass(object): # A class attribute count = 0

def \_\_init\_\_(self, name): print("An instance is created!") self.name = name MyClass.count += 1

\# Our class method @staticmethod def status(): print("The total number of instances are ", MyClass.count)

print(MyClass.count)

my\_func\_1 = MyClass("MyClass 1") my\_func\_2 = MyClass("MyClass 2") my\_func\_3 = MyClass("MyClass 3")

MyClass.status() print(MyClass.count) \[/code\] This prints the following:

\[code language="bash"\] # python statismethod.py

0 An instance is created! An instance is created! An instance is created!

The total number of instances are 3 3 \[/code\]

**How does the code work?**

1. The example above has a class  `MyClass()` with a class attribute `count = 0`.
2. An \_\_init\_\_ magic method accepts a `name` variable.
3. The \_\_init\_\_ method also increments the count in the `count` counter at each instantiation.
4. We define a staticmethod `status()` which just prints the number of the instances being created. The work done in this method is not necessarily associated with the class or any functions, hence its defined as a staticmethod.
5. We print the initial value of the counter `count` via the class, as `MyClass.count`. This will print `0`since the counter is called before any instances are created.
6. We create three instances from the class  `MyClass`
7. We can check the number of instances created through the `status()` method and the `count` counter.

Another example:

\[code language="python"\] class Car(object):

def sound(): print("vroom!") \[/code\]

The code above shows a method which is common to all the Car instances, and is not limited to a specific instance of Car. Hence, this can be called as a staticmethod since it's not necessarily bound to a Class or Instance to be called.

\[code language="python"\] class Car(object):

@staticmethod def sound(): print("vroom!") \[/code\]

### Class methods

We can define functions/methods specific to classes. These are called Class methods.

The speciality of a class methods is that an instance is not required to access a class method. It can be called directly via the Class name.

Class methods are used when it's not necessary to instantiate a class to access a method.

**NOTE: A method can be set as a Class method using the decorator @classmethod.**

Example:

\[code language="python"\] class MyClass(object): value = 10

@classmethod def my\_func(cls): print("Hello") \[/code\]

**NOTE: Class methods have `cls` as their first argument, instead of `self`.**

Example:

\[code language="python"\] class MyClass(object): count = 0

def \_\_init\_\_(self, val): self.val = val MyClass.count += 1

def set\_val(self, newval): self.val = newval

def get\_val(self): return self.val

@classmethod def get\_count(cls): return cls.count

object\_1 = MyClass(10) print("\\nValue of object : %s" % object\_1.get\_val()) print(MyClass.get\_count())

object\_2 = MyClass(20) print("\\nValue of object : %s" % object\_2.get\_val()) print(MyClass.get\_count())

object\_3 = MyClass(40) print("\\nValue of object : %s" % object\_3.get\_val()) print(MyClass.get\_count()) \[/code\] Here, we use a `get_count()` function to get the number of times the counter was incremented. The counter is incremented each time an instance is created.

Since the counter is not really tied with the instance but only counts the number of instance, we set it as a classmethod, and calls it each time using `MyClass.get_count()`when an instance is created. The output looks as following:

\[code language="bash"\] # python classmethod.py

Value of object : 10 1

Value of object : 20 2

Value of object : 40 3 \[/code\]

 

_**Courtsey**_: This was written as part of studying class and static methods. Several articles/videos have helped including but not limited to the following:

1. [https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/](https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/)
2. [Python beyond the basics - Object Oriented Programming](http://shop.oreilly.com/product/0636920040057.do) - O'Reilly Learning Paths
