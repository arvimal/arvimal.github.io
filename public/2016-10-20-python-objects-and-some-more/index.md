# Python, Objects, and some more..


_**E**_verything in Python is an object, what does that mean? This post tries to discuss some very basic concepts.

What does the following assignment do?

\[code language="python"\]

a = 1 \[/code\] Of course, anyone dabbled in code knows this. The statement above creates a container \`a\` and stores the value \`1\` in it.

But it seem that's not exactly what's happening, at least from Python's view-point.

When `a = 1` is entered or executed by the python interpreter, the following happens in the backend, seemingly unknown to the user.

- The Python interpreter evaluates the literal `1` and tries to understand what data type can be assigned for it.
    - There are several in-built data types such as `str`, `float`, `bool`, `list`, `dict`, `set` etc..
    - Builtin types are **classes** implemented in the python core.
    - For a full list of types and explanation, read the python help at `python`\-> `help()`\-> `topics` -> `TYPES`
    - Read the help sections for builtin types, eg.. `help(int)`, `help(list)` etc..
- The interpreter finds the appropriate builtin type for the literal. Since the literal `1` fits the type `int`, the interpreter creates an instance from `class int()` in memory.
    - This instance is called an `object` since it's just a `blob` with some metadata.
    - This object has a memory address, a value, a name in one or more namespace, some metadata etc..
    - `type(a)` helps in understanding the instance type.
    - In short, an assignment statement simply creates an instance in memory from a pre-defined class.
- The interpreter reads the LHS (Left hand side) of the statement `a = 1`, and creates the name `a` in the current namespace.
    - The name in the namespace is a reference to the object in memory.
    - Through this reference, we can access the data portion as well as the attributes of that object.
    - A single object can have multiple names (references).
- The name `a` created in the current namespace is linked to the corresponding object in memory.

When a name that's already defined is entered at the python prompt, the interpreter reads the namespace, finds the name (reference), goes to the memory location it's referring to, and pull the value of the object, and prints it on-screen.

#### Every object has the following features:

- A single value, available in its data section.

\[code language="python"\] In \[1\]: a = 1

In \[2\]: a Out\[2\]: 1 \[/code\]

- A single type, since the object is an instance of a pre-defined type class such as `int` , `float` etc..

\[code language="python"\] In \[3\]: type(a) Out\[3\]: int \[/code\]

- Attributes either inherited from the parent type class or defined by the user.

\[code language="python"\] In \[10\]: dir(a) Out\[10\]: \['\_\_abs\_\_', '\_\_add\_\_', '\_\_and\_\_', '\_\_bool\_\_', '\_\_ceil\_\_', '\_\_class\_\_', '\_\_delattr\_\_', '\_\_dir\_\_', '\_\_divmod\_\_', '\_\_doc\_\_', '\_\_eq\_\_', '\_\_float\_\_', ...\[content omitted\] '\_\_setattr\_\_', '\_\_sizeof\_\_', '\_\_str\_\_', '\_\_sub\_\_', '\_\_subclasshook\_\_', '\_\_truediv\_\_', '\_\_trunc\_\_', '\_\_xor\_\_', 'bit\_length', 'conjugate', 'denominator', 'from\_bytes', 'imag', 'numerator', 'real', 'to\_bytes'\] \[/code\]

- One or more base classes. All [new-stlye classes](https://www.python.org/doc/newstyle/) in Python ultimately inherits from the `object` class.

\[code language="python"\] In \[4\]: type(a) Out\[4\]: int

In \[5\]: int.mro() Out\[5\]: \[int, object\] \[/code\]

* * *

**NOTE:** `a` is an instance of the `int` class, and `int` inturn inherits from the `object` class. Read more on [Method Resolution Order](https://arvimal.wordpress.com/2016/05/30/method-resolution-order-object-oriented-programming/).

* * *

- A unique ID representing the object.

\[code language="python"\] In \[6\]: id(a) Out\[6\]: 140090033476640 \[/code\]

- Zero, One, or more names.
    - Use `dir()` to check the current namespace.
    - Use `dir(<object-name>)` to refer the indirect namespace.

* * *

Several other builtins are available in the default namespace without defining them specifically, possible due to the inclusion of the `builtin` module available under the reference `__builtin__` in the current namespace.

For a full list of the pre-defined variables, refer `dir(__builtins__)`, `help(__builtin__)` or `help(builtins)` after an `import builtins`.

#### A few questions and observations:

**Q1.** How can an assignment have zero names in the namespace?

**Ans**: An assignment such as `a = 1` creates an object in memory and creates a corresponding name (`a` in our case) in the namespace. `a` acts as a reference to the object in memory.

But, simply entering `1` at the python prompt creates an object in memory which is an instance of a type class, without creating the reference in the namespace.

Objects which don't have a reference from the current namespace are usually garbage-collected due to lack of references. Hence, an object which doesn't have a reference (a name), or had multiple references (more than one names) but had them deleted (for example, `del()` gets garbage-collected by python.

If the assignment `1` happens to be at a python prompt, it echoes the literal back after creating the object and reference since the prompt is essentially a `REPL` (Read Eval Print loop)

**Q2.** Can an object have more than one name references?

**Ans:** It's perfectly fine to have more than one reference to a single object. The example below should explain things very well.

\[code language="python"\] In \[1\]: a = 5000

In \[2\]: id(a) Out\[2\]: 140441367080400

In \[3\]: b = a

In \[4\]: b Out\[4\]: 5000

In \[5\]: id(b) Out\[5\]: 140441367080400

In \[6\]: c = 5000

In \[7\]: id(c) Out\[7\]: 140441367080432

In \[8\]: a is b Out\[8\]: True

In \[9\]: a == b Out\[9\]: True

In \[10\]: a is c Out\[10\]: False

In \[11\]: a == c Out\[11\]: True \[/code\]

The example shown above creates an object with value `5000` and assign it a name `a` in the current namespace. We checked the identifier of the object using `id(a)` and found out it to be `140441367080400`.

As the next step, we created another name in the namespace, ie.. `b` which takes in whatever `a` points to. Hence, `b` would default to `5000` and it will have the same identifier as `a`.

_This shows that an object in memory can have multiple references in a namespace._

Another object of value `5000` is created with a name `c` , but we can see that the identifier differs from what `id(a)` and `id(b)` is. This shows that `c` points to an entirely different object in memory.

To test if `a` is exactly the same object as `b`, use the keyword `is`. Meanwhile, if you want to test if two objects contain the same value, use the equality `==` symbol.

