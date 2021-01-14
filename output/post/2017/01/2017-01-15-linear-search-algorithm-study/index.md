---
title: "Linear Search - Algorithm Study"
date: "2017-01-15"
categories: 
  - "data-structures-and-algorithms"
  - "programming"
  - "python"
---

## Introduction

_**L**_inear Search is an way to search a data set for an element of interest. It is one of the many search algorithms available and is also the most direct and simple of the lot.

Linear search looks for the element of interest in a dataset starting from the first element and moves on to the consecutive elements till it finds the one we're interested in. Due to this behaviour, it's not the fastest search algorithm around.

In the worst case, when the element of interest is the last (or near-last) in the data set, linear-search has to sift through till the end. Hence, in a worst-case scenario, the larger the data set is, the more the iterations it take to find the element of interest. Hence, the performance of Linear search takes a toll as the data set grows.

Linear search works on sorted and unsorted data sets equally, since it has to go through the elements one by one and so doesn't mind if the data is ordered or not.

## Performance

### 1\. Worst-case performance: O(n)

A worst-case analysis is done with the upper bound of the running time of the algorithm. ie.. the case when the maximum number of operations are executed.

The worst-case scenario for a linear search happens when the element-of-interest is not present in the dataset. A near worst-case scenario is when the element-of-interest is the last element of the dataset. In the first case, the search has to go through each element only to find that the element is not present in the dataset. In the second scenario, the search has to be done till the last element, which still takes `n` iterations.

In the worst-case, the performance is O(n), where  `n`  is the number of elements in the dataset.

### 2\. Best-case performance: O(1)

In the best-case, where the element-of-interest is the first element in the dataset, only one search/lookup is needed. Hence the performance is denoted as `O(1)`, for `n` elements.

### 3\. Average performance: O(n/2)

On an average, the performance can be denoted as `O(n/2)`.

### Observations:

- Linear Search iterates through every element in the dataset until it finds the match.
- In Linear Search, the number of iterations grows linearly if the data set grows in size.
- This algorithm is called  `Linear Search`  due to this linear increase in the complexity depending on the dataset.
- The best case scenario is when the first iteration finds the element.
- The Worst case is when the element of interest is not present in the dataset.
- A very near worse case is when the element of interest is the last one in the dataset.

## How does Linear Search work?

Linear search progresses as following:

1\. Takes in a dataset as well as an element of interest. 2. Checks if the first element is the element of interest. 3. If yes, returns the element. 4. If not, move to the next element in the dataset. 5. Iterate till the dataset is exhausted. 6. Return  `None` if the element of interest is not present in the dataset.

## Code

\[code language="python"\] def linear\_search(my\_list, item): """Linear search"""

low\_position = 0 high\_position = len(my\_list) - 1

while low\_position < high\_position:

if my\_list\[low\_position\] == item: print("Your search item {0} is at position {1}".format( item, low\_position)) return low\_position else: low\_position += 1

if \_\_name\_\_ == "\_\_main\_\_": my\_list = \[1, 2, 3, 4, 5, 6\] linear\_search(my\_list, 5) \[/code\]

 

### Reference:

1. [http://quiz.geeksforgeeks.org/linear-search/](http://quiz.geeksforgeeks.org/linear-search/)
2. [http://research.cs.queensu.ca/home/cisc121/2006s/webnotes/search.html](http://research.cs.queensu.ca/home/cisc121/2006s/webnotes/search.html)
