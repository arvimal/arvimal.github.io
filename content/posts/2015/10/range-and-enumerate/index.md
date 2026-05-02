---
title: range() and enumerate()
date: 2015-10-12
categories:
  - programming
  - python
tags:
  - enumerate
  - programming
  - python
  - range
---

<!--more-->

The usual way to iterate over a range of numbers or a list in python, is to use **range().**

***Example 0:***

```python
colors = ["yellow", "red", "blue", "white", "black"]

for i in range(len(colors)): print(i, colors[i])
```

This should output:

```bash
(0, 'yellow') (1, 'red') (2, 'blue') (3, 'white') (4, 'black')
```

**print()**, by default, returns a tuple. If we want to print it in a more presentable way, we’ll need to find the indice at which each value is, and print that as well. Re-write the code a bit, to achieve the desired output:

```python
colors = ["yellow", "red", "blue", "white", "black"]

for i in range(len(colors)): color = colors[i] print("%d: %s" % (i, color))
```

This should print:

```bash
0: yellow 1: red 2: blue 3: white 4: black
```

We can see that the above output starts with ‘0’ since python starts counting from ‘0’. To change that to ‘1’, we’ll need to tweak the **print()** statement.

```python
colors = ["yellow", "red", "blue", "white", "black"]

for i in range(len(colors)): color = colors[i] print("%d: %s" % (i + 1, color))
```

This should print:

```bash
1: yellow 2: red 3: blue 4: white 5: black
```

Even though the above code snippet isn’t that complex, a much better way exists to do this. This is where the builtin function **enumerate()** comes in.

**enumerate()** returns a tuple when passed an object which supports iteration, for example, a list. It also supports a second argument named '**start**' which default to 0, and can be changed depending on where to start the order. We’ll check what '**start**' is towards the end of this article.

```python
colors = ["yellow", "red", "blue", "white", "black"] print(list(enumerate(colors)))
```

This returns a list of a tuples.

```bash
[(0, 'yellow'), (1, 'red'), (2, 'blue'), (3, 'white'), (4, 'black')]
```

To get to what we desire, modify it as:

```python
for i, color in enumerate(colors): print('%d: %s' % (i, color))
```

This outputs:

```bash
0: yellow 1: red 2: blue 3: white 4: black
```

Remember that we talked about that **enumerate()** takes a second value named '**start**' which defaults to ‘0’? Let’s check how that’ll help here.

The above output starts with ‘**0**’. '**start'** can help to change that.

```python
for i, color in enumerate(colors, start=1): print('%d: %s' % (i, color))
```

This should change the output as:

```bash
1: yellow 2: red 3: blue 4: white 5: black
```
