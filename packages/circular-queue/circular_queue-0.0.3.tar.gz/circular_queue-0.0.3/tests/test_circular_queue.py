from unittest import TestCase
from src.circular_queue import CircularQueue


class TestCircularQueue(TestCase):

    def setUp(self):
        self.queue = ('AMMT', 'BBBV', 'JBSS', 'AMMT', 'MGLU')

    def test_should_raise_value_error_when_trying_to_pass_an_initial_element_that_is_not_in_queue(self):
        initial_element = 'XXXXX'
        self.assertRaises(ValueError, CircularQueue, self.queue, initial_element)

    def test_should_return_first_element_in_queue_when_calling_get_next_element_method(self):
        myqueue = CircularQueue(self.queue)
        next = myqueue.get_next_element()
        self.assertEqual(next, self.queue[0])

    def test_should_return_third_element_in_queue_when_calling_get_next_element_method(self):
        initial_element = 'BBBV'
        myqueue = CircularQueue(self.queue, initial_element)
        next = myqueue.get_next_element()
        self.assertEqual(next, self.queue[2])

    def test_should_return_first_element_in_queue_when_calling_get_next_element_method_at_the_end_of_the_queue(self):
        initial_element = 'MGLU'
        myqueue = CircularQueue(self.queue, initial_element)
        next = myqueue.get_next_element()
        self.assertEqual(next, self.queue[0])

    def test_should_return_first_element_in_queue_when_calling_get_previous_element_method_at_the_second_element_in_the_queue(self):
        initial_element = 'BBBV'
        myqueue = CircularQueue(self.queue, initial_element)
        next = myqueue.get_previous_element()
        self.assertEqual(next, self.queue[0])

    def test_should_return_last_element_in_queue_when_calling_get_previous_element_method_at_the_begginig_of_the_queue(self):
        initial_element = 'AMMT'
        myqueue = CircularQueue(self.queue, initial_element)
        next = myqueue.get_previous_element()
        self.assertEqual(next, self.queue[-1])

    def test_should_return_next_three_elements_when_calling_get_batch_method(self):
        initial_element = 'AMMT'
        myqueue = CircularQueue(self.queue, initial_element)
        mybatch = myqueue.get_batch(2)
        self.assertEqual(['BBBV', 'JBSS'], mybatch)

    def test_should_return_previous_three_elements_when_calling_get_batch_method_with_rotation_left(self):
        initial_element = 'AMMT'
        myqueue = CircularQueue(self.queue, initial_element)
        mybatch = myqueue.get_batch(2, rotation='left')
        self.assertEqual(['MGLU', 'AMMT'], mybatch)

    def test_should_return_attribute_error_when_calling_get_batch_method_with_invalid_rotation(self):
        initial_element = 'AMMT'
        myqueue = CircularQueue(self.queue, initial_element)
        self.assertRaises(AttributeError, myqueue.get_batch, 2, rotation='center')

    def test_should_return_next_when_get_next_element_function_after_a_get_batch_function(self):
        initial_element = 'AMMT'
        myqueue = CircularQueue(self.queue, initial_element)
        myqueue.get_batch(3)
        next_element = myqueue.get_next_element()
        self.assertEqual('MGLU', next_element)

