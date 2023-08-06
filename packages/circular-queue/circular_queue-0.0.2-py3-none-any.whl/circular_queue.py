class CircularQueue:
    def __init__(self, queue, initial_element=None):
        self.queue = queue
        self.initial_element = initial_element
        self._check_if_initial_element_was_provided()
        self._check_initial_element_is_valid()
        self.pointer = queue.index(self.initial_element)
        self.len = len(queue)

    def _check_if_initial_element_was_provided(self):
        if self.initial_element:
            pass
        else:
            self.initial_element = self.queue[-1]

    def _check_initial_element_is_valid(self):
        if self.initial_element in self.queue:
            pass
        else:
            raise ValueError("Initial element is not in the queue.")

    def get_next_element(self):
        if self.pointer == (self.len - 1):
            next_element = self.queue[0]
            self.pointer = 0
            return next_element
        else:
            next_element = self.queue[self.pointer + 1]
            self.pointer += 1
            return next_element

    def get_previous_element(self):
        if self.pointer == 0:
            previous_element = self.queue[self.len - 1]
            self.pointer = self.len - 1
            return previous_element
        else:
            previous_element = self.queue[self.pointer - 1]
            self.pointer -= 1
            return previous_element

    def get_batch(self, batch_size, rotation='right'):
        retrieved_elements = []
        for i in range(0, batch_size):
            if rotation == 'right':
                element = self.get_next_element()
                retrieved_elements.append(element)
            elif rotation == 'left':
                element = self.get_previous_element()
                retrieved_elements.append(element)
            else:
                raise AttributeError('An invalid rotation was provided. Please use left or right rotation.')
        return retrieved_elements
