# Binary Search - Algorithm Study

<!--more-->
## Introduction

**_B_**inary Search is a search method used to find an object in a data set. This is much faster compared to the Linear Search algorithm we saw in a [previous post](https://arvimal.wordpress.com/2017/01/15/linear-search-algorithm-study/).

This algorithm works on the `Divide and Conquer` principle. Binary Search gets its speed by essentially dividing the list/array in half in each iteration, thus reducing the dataset size for the next iteration.

Imagine searching for an element in a rather large dataset. Searching for an element one by one using `Linear Search` would take `n` iterations. In a worst case scenario, if the element being searched is not present in the dataset or is at the end of the dataset, the time taken to find the object/element would be proportional to the size of the dataset.

The element of interest is returned if it is present in the dataset, else a NULL/None value is.

#### Note:

- Binary search will only work effectively on a _**Sorted**_ collection.
- The code implementation will need minor changes depending on how the dataset is sorted, ie.. either in an increasing order or in a decreasing order.

## Performance

### 1\. Worst-case performance: log(n)

As discussed in the post on, `Linear Search` a worst-case analysis is done with the upper bound of the running time of the algorithm. ie.. the case when the maximum number of operations are needed/executed to find/search the element of interest in the dataset.

Of course, the worst-case scenario for any search algorithms is when the element of interest is not present in the dataset. The maximum number of searches has to be done in such a case, and it still ends up with no fruitful result. A similar but less worse case is when the element is found in the final (or somewhere near the last) iteration.

Due to the divide-and-conquer method, the maximum number of iterations needed for a dataset of `n` elements is, `log(n)` where the log base is `2.`

Hence, for a data set of 10240 elements, Binary Search takes a maximum of `13` iterations.

\[code language="python"\] In \[1\]: import math

In \[2\]: math.log(10240, 2) Out\[2\]: 13.321928094887364 \[/code\] For a data set of 50,000 elements, Binary Search takes `16` iterations in the worst case scenario while a Linear Search may take 50,000 iterations in a similar case.

\[code language="python"\] In \[1\]: import math

In \[2\]: math.log(50000, 2) Out\[2\]: 15.609640474436812 \[/code\] ie.. the Worst case for Binary search takes `log(n)` iterations to find the element.

### 2\. Best-case performance: O(1)

The best case scenario is when the element of interest is found in the first iteration itself. Hence the best-case would be where the search finishes in one iteration.

ie.. The best-case scenario would be `O(1)`.

## **How does Binary Search work?**

Imagine a sorted dataset of `100` numbers and we're searching for  `98` is in the list. A simple search would start from index `0` , moves to the element at index `1`, progresses element by element until the one in interest is found. Since we're searching for `98`, it'll take `n` iterations depending on the number of elements between the first element in the dataset and `98`.

Binary Search uses the following method, provided the dataset is sorted.

1. Find the length of the data set.
2. Find the lowest (index `0`), highest (index `n`), and the middle index of the dataset.
3. Find the subsequent elements residing in the first, last, and middle index.
4. Check if the element of interest is the middle element.
5. If not, check if the element-of-interest is higher or lower than the middle element.
6. If it is higher, assuming the dataset is sorted in an increasing order, move the lower index to one **above** the middle index.
7. if it is lower, move the highest index to one **below** the middle index.
8. Check if the element of interest is the middle element in the new/shorter dataset.
9. Continue till the element of interest is found.

\[caption id="attachment\_2310" align="alignnone" width="1280"\]![binary_search_depiction-svg](images/binary_search_depiction-svg.png) Binary Search - Source: Wikipedia\[/caption\]

The figure above shows how Binary Search works on a dataset of 16 elements, to find the element `7`.

- Index `0` , Index `16`, and the middle index are noted.
- Subsequent values/elements at these indices are found out as well.
- Check if the element of interest `7` is equal to, lower, or higher than the middle element `14` at index `8`.
- Since it's lower and the dataset is sorted in an increasing order, the search moves to the left of the middle index, ie.. from index `0` to index `7`.
- \----
- The lower index is now `0`, the higher index is now `7`, and the middle index is now `3`, the element in the middle index is `6`.
- Check if the element of interest `7` is lower or higher than the middle element `6` at index `3`.
- Since it's higher and the dataset is sorted in an increasing order, the search moves to the right of the middle index, ie.. from index `4` to index 7.
- \----
- So on and so forth.. till we arrive at the element of interest, ie.. `7`.

As noted earlier, the data set is divided into half in each iteration. A numeric representation on how Binary search progress can be seen as:

_100 elements -> 50 elements -> 25 elements -> 12 elements -> 6 elements - 3 elements -> 1 element_

## Code

### Example 1 : (Data set sorted in Increasing order)

\[code language="python"\] def binary\_search(my\_list, item): low\_position = 0 high\_position = len(my\_list) - 1

while low\_position = high\_position: mid\_position = (low\_position + high\_position) // 2 mid\_element = my\_list\[mid\_position\]

if mid\_element == item: print("\\nYour search item {0} is at index {1}".format( item, mid\_position)) return mid\_element

elif mid\_element <= item: high\_position = mid\_position - 1

else: low\_position = mid\_position + 1 return None

if \_\_name\_\_ == "\_\_main\_\_": my\_list = \[1, 2, 3, 4, 5, 6\] binary\_search(my\_list, 3) \[/code\]

### Example 2 : (Same as above, with statements on how the search progresses)

\[code language="python"\] def binary\_search(my\_list, item):

\# Find and set the low and high positions of the data set # Note that these are not the values, but just positions. low\_position = 0 high\_position = len(my\_list) - 1

\# Calculate the Complexity import math complexity = math.ceil(math.log(len(my\_list), 2))

\# Print some info on the dataset print("\\nDataset size : {0} elements".format(len(my\_list))) print("Element of interest : {0}".format(item)) print("Maximum number of iterations to find {0} : {1}\\n".format( item, complexity))

while low\_position <= high\_position:

\# Find the middle position from the low and high positions mid\_position = (low\_position + high\_position) // 2

\# Find the element residing in the middle position of the data set. mid\_element = my\_list\[mid\_position\]

print("Element at min index : {0}".format(my\_list\[low\_position\])) print("Element at max index : {1}".format(high\_position, my\_list\[high\_position\])) print("Element at mid index {0} : {1}".format(mid\_position, mid\_element))

if mid\_element == item: print("\\nYour search item {0} is at index {1}".format( item, mid\_position)) return mid\_element

elif mid\_element > item: high\_position = mid\_position - 1 print("{0} in the left subset, omitting the right subset\\n".format(item))

else: low\_position = mid\_position + 1 print("{0} in the right subset, omitting the left subset\\n".format(item))

print("Element of interest not in dataset\\n") return None

if \_\_name\_\_ == "\_\_main\_\_": my\_list = \[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13\] binary\_search(my\_list, 13) \[/code\]

### Observations:

1. Binary Search needs a Sorted dataset to work, either increasing or decreasing.
2. It finds the element of interest in logarithmic time, hence is also known as, `Logarithmic Search`.
3. Binary Search searches through a dataset of `n` elements in `log(n)` iterations, in the worst case scenario.

### NOTE:

All the examples used in this blog are available at  [https://github.com/arvimal/DataStructures-and-Algorithms-in-Python](https://github.com/arvimal/DataStructures-and-Algorithms-in-Python), with more detailed notes.

### References:

1. [https://en.wikipedia.org/wiki/Binary\_search\_algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm)
2. [http://quiz.geeksforgeeks.org/binary-search/](http://quiz.geeksforgeeks.org/binary-search/)
3. [https://www.hackerearth.com/practice/algorithms/searching/binary-search/tutorial/](https://www.hackerearth.com/practice/algorithms/searching/binary-search/tutorial/)
4. [http://research.cs.queensu.ca/home/cisc121/2006s/webnotes/search.html](http://research.cs.queensu.ca/home/cisc121/2006s/webnotes/search.html)

