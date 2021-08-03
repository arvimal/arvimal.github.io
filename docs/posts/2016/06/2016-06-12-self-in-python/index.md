---
title: "`self` in Python - Object Oriented Programming"
date: 2016-06-12
categories: 
  - "programming"
  - "python"
---

_**T**_his article was long overdue and should have been published before many of the articles in this blog. Better late than never.

`self` in Python is usually used in an Object Oriented nomenclature, to denote the instance/object created from a Class.

In short, `self` is the instance itself.

Let's check the following example:

\[code language="python"\] class MyClass(object): def \_\_init\_\_(self, name): self.name = name print("Initiating the instance!")

def hello(self): print(self.name)

myclass = MyClass("Dan Inosanto")

\# Calling the \`hello\` method via the Instance \`myclass\` myclass.hello()

\# Calling the \`hello\` method vai the class. MyClass.hello(myclass) \[/code\]

The code snippet above is trivial and stupid, but I think it gets the idea across.

We have a class named `MyClass()` which takes a `name` value as an argument. It also prints the string "Initiating the instance".  The `name` value is something that has to be passed while creating an instance.

The function `hello()` just prints the `name` value that is passed while instantiating the class `MyClass()`.

We instantiate the class `MyClass()` as `myclass` and pass the string  _**Dan Inosanto**_ as an argument. Read about the great Inosanto [here](https://en.wikipedia.org/wiki/Dan_Inosanto).

Next, we call the `hello()` method through the instance. ie..

\[code language="python"\] myclass.hello() \[/code\]

This should print the name we passed while instantiating `MyClass()` as `myclass` , which should be pretty obvious.

The second and last instruction is doing the same thing, but in a different way.

\[code language="python"\] MyClass.hello(myclass) \[/code\] Here, we call the class `MyClass()` directly as well as it's method `hello()`. Let's check out what both prints:

\[code language="bash"\] # python /tmp/test.py

Initiating the instance! Dan Inosanto Dan Inosanto \[/code\]

As we can see, both prints the same output. This means that :

**myclass.hello(self) == MyClass.hello(myclass)**

In general, we can say that:

**<instance-name>.<method>(self) == <Class>.<method>(<instance-name>)**

ie.. The keyword `self` actually represents the instance being instantiated from the Class. Hence `self` can be seen as Syntactic sugar.
