---
title: "Accessor and Mutator methods - Python"
date: 2016-12-18
categories:
  - "programming"
  - "python"
tags:
  - "object-oriented-programming"
  - "python"
---

_**A**_ method defined within a class can either be an Accessor or a Mutator method.

An `Accessor` method returns the information about the object, but do not change the state or the object.

A `Mutator` method, also called an `Update` method, can change the state of the object.

Consider the following example:

\[code language="python"\] In \[10\]: a = \[1,2,3,4,5\]

In \[11\]: a.count(1) Out\[11\]: 1

In \[12\]: a.index(2) Out\[12\]: 1

In \[13\]: a Out\[13\]: \[1, 2, 3, 4, 5\]

In \[14\]: a.append(6)

In \[15\]: a Out\[15\]: \[1, 2, 3, 4, 5, 6\] \[/code\]

The methods `a.count()` and `a.index()` are both `Accessor` methods since it doesn't alter the object `a` in any sense, but only pulls the relevant information.

But `a.append()` is a mutator method, since it effectively changes the object (list `a`) to a new one.

In short, knowing the behavior of a method is helpful to understand how it alters the objects it acts upon.
