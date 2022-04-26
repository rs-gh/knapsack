from collections import namedtuple


HeapNode = namedtuple("HeapNode", ["assignment", "assignment_depth", "value"])


class Heap:
    def __init__(self):
        self.heap = []
        self.heap_size = 0
    
    @staticmethod
    def left_child(n):
        return 2*n + 1
    
    @staticmethod
    def right_child(n):
        return 2*n + 2
    
    @staticmethod
    def parent(n):
        return int((n-1)/2)
    
    @staticmethod
    def is_leaf(n, heap_size):
        return Heap.left_child(n) >= heap_size
    
    @staticmethod
    def has_right(n, heap_size):
        return Heap.right_child(n) < heap_size
    
    def is_empty(self):
        return self.heap_size == 0

    def swap(self, x, y):
        temp = self.heap[x]
        self.heap[x] = self.heap[y]
        self.heap[y] = temp

    def add_to_heap(self, node):
        self.heap_size += 1
        self.heap.append(node)
        i = self.heap_size - 1
        # float up
        while i > 0 and self.heap[i].value > self.heap[Heap.parent(i)].value:
            self.swap(i, Heap.parent(i))
            i = Heap.parent(i)
    
    def heapify(self, i):
        if Heap.is_leaf(i, self.heap_size):
            return
        child = None
        left = Heap.left_child(i)
        if not Heap.has_right(i, self.heap_size):
            if self.heap[i].value < self.heap[left].value:
                child = left
        else:
            right = Heap.right_child(i)
            if self.heap[i].value < self.heap[left].value or self.heap[i].value < self.heap[right].value:
                child = left if self.heap[left].value > self.heap[right].value else right
        if child is not None:
            self.swap(i, child)
            self.heapify(child)

    def get_heap_max(self):
        heap_max = self.heap[0]
        self.swap(0, self.heap_size-1)
        self.heap = self.heap[:-1]
        self.heap_size -= 1
        self.heapify(0)
        return heap_max