# Data Structures - Arrays

<!--more-->
Arrays are a commonly used data structure, and is one of the first a DS student looks into.

It is created as a collection of memory addresses which are contiguous in memory. These memory locations store data of a specific type depending on the array's type.

**Advantages:**

- Arrays are easier to create since the size and type is mentioned at the creation time.
- Arrays have constant access/lookup time since the lookup is done by accessing the memory location as an offset from the base/first element. Hence the complexity will be O(1).
- Arrays are contiguous in memory, ie.. a 10 cell array can start at perhaps 0x0001 and end at 0x0010.

**Disadvantages:**

- The size of an array has to be defined at the time of its creation. This make the size static, and hence cannot be resized later.
- An array can only accomodate a specific data type. The type of data an array can store has to be defined at creation time. Hence, if an array is set to store integers, it can only store integers in each memory location.
- Since the size of an array is set at the time of creation, allocating an array may fail depending on the size of the array and the available memory on the machine.
- Inserting an element into an array can be expensive depending on the location. To insert an element at a particular position, for example 'n', the element already has to be moved to 'n + 1', the element at 'n + 1' to 'n + 2' etc.. Hence, if the position to which the element is written to is at the starting of the array, the operation will be expensive. But if the position is at the starting, it won't be.

**What is the lookup time in an array?**

The elements in an array are continuguous to each other. The address of an element is looked up as an \`offset\` of the primary or base element. Hence, the lookup of any element in the array is constant and can be denoted by O(1).

**Arrays in Python**

Python doesn't have a direct implementation of an Array. The one that closely resembles an array in python is a \`list\`.

The major differences between an array and a list are:

- The size of lists are not static. It can be grown or shrinked using the \`append\` and \`remove\` methods. Arrays are static in size.
- lists can accomodate multiple data types, while arrays cannot.

\[code language="python"\] In \[1\]: mylist = \[\]

In \[2\]: type(mylist) Out\[2\]: list

In \[3\]: mylist.append("string")

In \[4\]: mylist.append(1000)

In \[5\]: mylist Out\[5\]: \['string', 1000\] \[/code\]

**Time complexity of Arrays**

- Indexing    - O(1)
- Insertion/Deletion at beginning - O(n) (If the array has space to shift the elements)
- Insertion/Deletion at the end - O(1) (If the array has space at the end)
- Deletion at the end - O(1) (Since it doesn't have to move any elements and reorder)
- Insertion at the middle - O(n) (Since it requires to move the elements to the right and reorder)
- Deletion at the middle - O(n) (Since it requires to delete the element and move the ones from the right to the left)

**The 'array' module**

Python comes with a module named 'array' which emulates the behavior of arrays.

\[code language="python"\] In \[24\]: import array

In \[25\]: myarray = array.array('i', \[1,2,3,4\])

In \[26\]: myarray Out\[26\]: array('i', \[1, 2, 3, 4\]) \[/code\]

