Decorators - Object Oriented Programming
########################################
:date: 2016-05-30 12:02
:author: arvimal
:category: Programming, Python
:tags: classmethod, decorators, Object Oriented Programming, programming, python, staticmethod
:slug: decorators-object-oriented-programming
:status: published

**D**\ ecorators are wrapper functions (or classes) that wrap and modify another function (or class), and change it's behavior as required. Decorators help to modify your code without actually modifying the working function/class itself.

There are several inbuilt Decorators in Python, such as ``@classmethod`` and ``@staticmethod``. Examples on these are due for another post.

Decorators are called to act upon a function or class, by mentioning the Decorator name just above the function/class.

Decorators are written such as it returns a function, rather than output something.

**Example 0:**

| [code language='python']
| @my_decorator
| def my_func():
| print("Hello")

| my_func()
| [/code]

In the above code snippet, when ``my_func()`` is called, the python interpreter calls the decorator function ``my_decorator``, executes it, and then passes the result to ``my_func()``.

The example above doesn't do anything worth, but the following example should help to get a better idea.

**NOTE:** The examples below are taken from the excellent talks done by Jillian Munson (in PyGotham 2014) and Mike Burns for `ThoughtBot <https://www.youtube.com/channel/UCUR1pFG_3XoZn3JNKjulqZg>`__. The URLs are at \ `[1] <https://www.youtube.com/watch?v=yW0cK3IxlHc>`__ and `[2] <https://www.youtube.com/watch?v=Slf1b3yUocc>`__. All credit goes to them.

**Example 1:**

| [code language="python"]
| def my_decorator(my_function):
| def inner_decorator():
| print("This happened before!")
| my_function()
| print("This happens after ")
| print("This happened at the end!")
| return inner_decorator

| @my_decorator
| def my_decorated():
| print("This happened!")

| if \__name_\_ == '__main__':
| my_decorated()
| [/code]

**
Components:**
~~~~~~~~~~~~~

#. A function named ``my_decorated()``.
#. A decorator function named ``my_decorator()``.
#. The decorator function \ ``my_decorator()`` has a function within itself named ``inner_decorator()``.
#. The decorator function \ ``my_decorator()``, returns the inner function ``inner_decorator()``.

   #. Every function should return a value, if not it defaults to \ **``None``.**
   #. ``my_decorator()`` decorator should return the ``inner_decorator()`` inner function, else the decorator cannot be used with the ``my_decorated()`` function.
   #. To understand this, test with 'return None' for the decorator function ``my_decorator()``.

#. The inner function ``inner_decorator()`` is the one that actually decorates (modifies) the function ``my_decorated()``.
#. The decorator function is called on the function ``my_decorated()`` using the format ``@my_decorator``.
#. The decorator function takes an argument, which can be named whatever the developer decides. When the decorator function is executed, the argument is replaced with the function name on which the decorator is executed. In our case, it would be ``my_decorated()``

**How does the code work?**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. The function ``my_decorated()`` is called.
#. The interpreter sees that the decorator ``@my_decorator`` is called wrt this function.
#. The interpreter searches for a function named ``my_decorator()``\ and executes it.
#. Since the decorator function returns the inner function ``inner_decorator()``, the python interpreter executes the inner function.
#. It goes through each steps, reaches ``my_function()`` , and gets it executed.
#. Once that function is executed, it goes back and continues with the execution of the decorator ``my_decorator()``.

**Output:**
~~~~~~~~~~~

| [code language="bash"]
| # python decorators-1.py
| This happened before! # Called from the decorator
| This happened! # Called from the function
| This happens after # Called from the decorator
| This happened at the end! # Called from the decorator
| [/code]

 

**Example 2:**

| [code language="python"]
| def double(my_func):
| def inner_func(a, b):
| return 2 \* my_func(a, b)
| return inner_func

| @double
| def adder(a, b):
| return a + b

| @double
| def subtractor(a, b):
| return a - b

| print(adder(10, 20))
| print(subtractor(6, 1))
| [/code]

.. _components-1:

**Components:
**
~~~~~~~~~~~~~

#. Two functions named ``adder()`` and ``subtractor()``.
#. A decorator function named ``double()``.
#. The decorator has an inner function named ``inner_func()`` which does the actual intended work.
#. The decorator returns the value of the inner function ``inner_func()``
#. Both the ``adder()`` and ``subtractor()``\ functions are decorated with the decorator \ ``double()``

.. _how-does-the-code-work-1:

**How does the code work?**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. We call the ``adder()`` and ``subtractor()`` functions with a print(), since the said functions don't print by default (due to the ``return`` statement).
#. The python interpreter sees the decorator ``@double`` and calls it.
#. Since the decorator returns the inner function ``inner_func()``, the interpreter executes it.
#. The decorator takes an argument ``my_func``, which is always the function on which the decorator is applied, ie.. in our case ``my_case == adder()``\ and ``my_case == subtractor()``.
#. The inner function within the decorator takes arguments, which are the arguments passed to the functions that are being decorated. ie.. Any arguments passed to ``adder()`` and ``subtractor()``\ are passed to ``inner_func()``.
#. The statement ``return 2 * my_func(a, b)`` returns the value of :

   #. 2 x ``adder(10, 20)``
   #. 2 x ``subtractor(6, 1)``

.. _output-1:

**Output:**
~~~~~~~~~~~

| [code language="bash"]
| # python decorators-2.py
| 60
| 10
| [/code]

Inbuilt decorators such as @staticmethod and @classmethod will be discussed in an upcoming post.

**NOTE: To see how decorators are syntactically sugar coated, read \ **\ `Magic methods and Syntactic sugar in Python <https://arvimal.wordpress.com/2016/06/02/magic-methods-in-python/>`__
