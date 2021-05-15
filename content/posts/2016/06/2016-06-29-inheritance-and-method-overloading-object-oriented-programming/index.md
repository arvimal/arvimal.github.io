---
title: "Inheritance and Method overloading - Object Oriented Programming"
date: 2016-06-29
categories:
  - "programming"
  - "python"
tags:
  - "abstract-methods"
  - "abstractmethod"
  - "builtins"
  - "inheritance"
  - "method-overloading"
---

_**I**_nheritance is a usual theme in Object Oriented Programming. Because of Inheritance, the functions/methods defined in parent classes can be called in Child classes which enables code reuse, and several other features. In this article, we try to understand some of those features that come up with Inheritance.

We've discussed [Abstract Methods](https://arvimal.wordpress.com/2016/06/14/abstract-base-classesmethods-object-oriented-programming/) in an earlier post, which is a feature part of Inheritance, and can be applied on child classes that inherits from a Parent class.

E the methods which are inherited can also be seen as another feature or possibility in Inheritance. In many cases, it's required to override or specialize the methods inherited from the Parent class. This is of course possible, and is called as 'Method Overloading'.

Consider the two classes and its methods defined below:

_**Example 0:**_

\[code language="python"\] import abc

class MyClass(object):

\_\_metaclass\_\_ = abc.ABCMeta

def \_\_init\_\_(self): pass

def my\_set\_method(self, value): self.value = value

def my\_get\_method(self): return self.value

@abc.abstractmethod def printdoc(self): return

class MyChildClass(MyClass):

def my\_set\_method(self, value): if not isinstance(value, int): value = 0 super(MyChildClass, self).my\_set\_method(self)

def printdoc(self): print("\\nDocumentation for MyChildClass()")

instance\_1 = MyChildClass() instance\_1.my\_set\_method(10) print(instance\_1.my\_get\_method()) instance\_1.printdoc() \[/code\]

 

We have two classes, the parent class being `MyClass` and the child class being `MyChildClass`.

`MyClass` has three methods defined.

- my\_set\_method()
- my\_get\_method()
- printdoc()

The `printdoc()` method is an [Abstract method](https://arvimal.wordpress.com/2016/06/14/abstract-base-classesmethods-object-oriented-programming/), and hence should be implemented in the Child class as a mandatory method.

The child class `MyChildClass` inherits from `MyClass` and has access to all it's methods.

Normally, we can just go ahead and use the methods defined in `MyClass` , in `MyChildClass`. But there can be situations when we want to improve or build upon the methods inherited. As said earlier, this is called _**Method Overloading.**_

`MyChildClass` extends the parent's `my_set_method()` function by it's own implementation. In this example, it does an additional check to understand if the input value is an `int` or not, and then calls the `my_set_method()` of it's parent class using `super`. Hence, this method in the child class extends the functionality prior calling method in the parent. A post on `super` is set for a later time.

Even though this is a trivial example, it helps to understand how the features inherited from other classes can be extended or improved upon via method overloading.

The `my_get_method()` is not overridden in the child class but still called from the instance, as `instance_1.my_get_method()`. We're using it as it is available via Inheritance. Since it's defined in the parent class, it works in the child class' instance when called, even if not overridden.

The `printdoc()` method is an abstract method and hence is mandatory to be implemented in the child class, and can be overridden with what we choose to do.

Inheritance is possible from python builtins, and can be overridden as well. Let's check out another example:

_**Example 1:**_

\[code language="python"\] class MyList(list):

def \_\_getitem\_\_(self, index): if index == 0: raise IndexError if index &gt; 0: index -= 1 return list.\_\_getitem\_\_(self, index)

def \_\_setitem\_\_(self, index, value): if index == 0: raise IndexError if index &gt; 0: index -= 1 list.\_\_setitem\_\_(self, index, value)

x = MyList(\['a', 'b', 'c'\]) print(x) print("-" \* 10)

x.append('d') print(x) print("-" \* 10)

x.\_\_setitem\_\_(4, 'e') print(x) print("-" \* 10)

print(x\[1\]) print(x.\_\_getitem\_\_(1)) print("-" \* 10)

print(x\[4\]) print(x.\_\_getitem\_\_(4)) \[/code\] This outputs:

\[code language="python"\] \['a', 'b', 'c'\] ---------- \['a', 'b', 'c', 'd'\] ---------- \['a', 'b', 'c', 'e'\] ---------- a a ---------- e e \[/code\]

### How does the code work?

The class `MyList()` inherits from the builtin `list`. Because of the inheritance, we can use list's available magic methods such as `__getitem__()` , `__setitem__()` etc..

**_NOTE: In order to see the available methods in `list`, use `dir(list)`._**

1. We create two functions/methods named \`\_\_getitem\_\_()\` and \`\_\_setitem\_\_()\` to override the inherited methods.
2. Within these functions/methods, we set our own conditions.
3. Wie later call the builtin methods directly within these functions, using
    1. list.\_\_getitem\_\_()
    2. list.\_\_setitem\_\_()
4. We create an instance named `x` from `MyList()`.
5. We understand that
    1. `x[1]` and `x.__getitem__(1)` are same.
    2. `x[4, 'e']` and `x.__setitem__(4, 'e')` are same.
    3. `x.append(f)` is same as `x.__setitem__(<n>, f)` where <n> is the element to the extreme right which the python interpreter iterates and find on its own.

Hence, in Inheritance, child classes can:

- Inherit from parent classes and use those methods.
    - Parent classes can either be user-defined classes or buitins like `list` , `dict` etc..
- Override (or Overload) an inherited method.
- Extend an inherited method in its own way.
- Implement an Abstract method the parent class requires.

### Reference:

1. [Python beyond the basics - Object Oriented Programming](http://shop.oreilly.com/product/0636920040057.do)
