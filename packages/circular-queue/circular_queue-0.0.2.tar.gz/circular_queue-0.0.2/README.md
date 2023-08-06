# Circular Queue
### A pythonic implementation of the beloved data structure
Circular Queue is an object that can be used whenever you need to connect the head of an iterable to its tail. 
It can be easily connected to a database in order to persist your queue rotation.  
##### Installation
```
pip install circular-queue
```
##### How to use
After cloning the repo, you can import the **CircularQueue** class to your project:
```python3
from CircularQueue.circular_queue import CircularQueue
```
You can instantiate the **CircularQueue** object passing a **queue** an a **pointer** as arguments:
```python3
mylist = ['Banana', 'Star Fruit', 'Apple', 'Orange', 'Avocado']
pointer = 'Apple'
myqueue = CircularQueue(mylist, pointer)
```
Now you have two methods at your disposal: **get_next_element** and **get_previous_element**:
```python3
myqueue.get_next_element()
>>> 'Orange'
myqueue.get_next_element()
>>> 'Avocado'
myqueue.get_next_element()
>>> 'Banana'
myqueue.get_previous_element()
>>> 'Avocado'
```
If you need to get a batch of elements you can use the get_batch method like so:
```python3
mylist = ['Banana', 'Star Fruit', 'Apple', 'Orange', 'Avocado']
pointer = 'Banana'
batch_size = 3
myqueue = CircularQueue(mylist, pointer)
myqueue.get_batch(batch_size)
>>> ['Star Fruit', 'Apple', 'Orange']
````
You can also get batch elements in queue rotating to the left:
```python3
myqueue.get_batch(batch_size, rotation='left')
>>> ['Orange', 'Apple', 'Star Fruit']
```