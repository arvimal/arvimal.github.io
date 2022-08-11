# Selection Sort - Algorithm Study

<!--more-->
**Selection Sort** is a sorting algorithm used to sort a data set either in incremental or decremental order.

It goes through the entire elements one by one and hence it's not a very efficient algorithm to work on large data sets.

## 1. How does Selection sort work?

Selection sort starts with an unsorted data set. With each iteration, it builds up a sub dataset with the sorted data.

By the end of the sorting process, the sub dataset contains the entire elements in a sorted order.

1. Iterate through the data set one element at a time.
2. Find the biggest element in the data set (Append it to another if needed)
3. Reduce the sample space by the biggest element just found. The new data set becomes `n - 1` compared to the previous iteration.
4. Start over the iteration again, on the reduced sample space.
5. Continue till we have a sorted data set, either incremental or decremental

## 2. How does the data sample change in each iteration?

Consider the data set **[10, 4, 9, 3, 6, 19, 8]**

>Data set            -   **[10, 4, 9, 3, 6, 19, 8]**

* After Iteration 1   -   **[10, 4, 9, 3, 6, 8]** - **[19]**
* After Iteration 2   -   **[4, 9, 3, 6, 8]** - **[10, 19]**
* After Iteration 3   -   **[4, 3, 6, 8]** - **[9, 10, 19]**
* After Iteration 4   -   **[4, 3, 6]** - **[8, 9, 10, 19]**
* After Iteration 5   -   **[4, 3]** - **[6, 8, 9, 10, 19]**
* After Iteration 6   -   **[3]** - **[4, 6, 8, 9, 10, 19]**
* After Iteration 7   -   **[3, 4, 6, 8, 9, 10, 19]**

Let's check what the Selection Sort algorithm has to go through in each iteration.

* Iter 1  - **[10, 4, 9, 3, 6, 8]**
* Iter 2  - **[4, 9, 3, 6, 8]**
* Iter 3  - **[4, 3, 6, 8]**
* Iter 4  - **[4, 3, 6]**
* Iter 5  - **[4, 3]**
* Iter 6  - **[3]**

>Sorted Dataset - **[3, 4, 6, 8, 9, 10, 19]**

## 3. Performance / Time Complexity

* Selection Sort has to go through all the elements in the data set, no matter what.
* Hence, the **Worst case**, **Best case** and **Average Time Complexity** would be *O(n^2)*.

Since `Selection Sort` takes in `n` elements while starting, and goes through the data set `n` times (each step reducing the data set size by 1 member), the iterations would be:

```bash
n + [ (n - 1) + (n - 2) + (n - 3) + (n - 4) + ... + 2 + 1 ]
```

We are more interested in the worse-case scenario. In a very large data set, an `n - 1`, `n - 2` etc.. won't make a difference.

Hence we can re-write the above iterations as:

```bash
n + [n + n + n + n ..... n]
```

Or also as:

```bash
n * n = (n^2)
```

## 4. Code

```python
def find_smallest(my_list): 
    smallest = my_list[0] 
    smallest_index = 0

for i in range(1, len(my_list)):
    if my_list[i] < smallest: 
      smallest = my_list[i] 
      smallest_index = i 
    return smallest_index

def selection_sort(my_list): 
    new_list = [] 
    for i in range(len(my_list)): 
        smallest = find_smallest(my_list) 
        new_list.append(my_list.pop(smallest)) 
    return new_list[code]
```

## 5. Observations

1. Selection Sort is an algorithm to sort a data set, but it is not particularly fast.
2. It takes `n` iterations in each step to find the biggest element in that iteration.
3. The next iteration has to run on a data set of `n - 1` elements compared to the previous iteration.
4. For `n` elements in a sample space, Selection Sort takes `n x n` iterations to sort the data set.

## 6. References

1. [https://en.wikipedia.org/wiki/Selection_sort](https://en.wikipedia.org/wiki/Selection_sort)
2. [http://bigocheatsheet.com](http://bigocheatsheet.com)
3. [https://github.com/egonschiele/grokking_algorithms](https://github.com/egonschiele/grokking_algorithms)

