# Could just use eval, but this is more fun :)
import functools


@functools.total_ordering
class NestedList:
    def __init__(self, expression_string):
        self.current_node = None
        self.root = None
        self.expression = list(expression_string)
        self.initialize_tree()

    def eval(self):
        return self.root.get_as_object()

    def initialize_tree(self):
        while True:
            if len(self.expression) == 0:
                break

            chunk = self.pop_next_chunk()
            if chunk == "[":
                new_node = ListNode(self.current_node)
                if self.current_node is not None:
                    self.current_node.add_sub_list(new_node)
                else:
                    self.root = new_node
                self.current_node = new_node
            if chunk == "]":
                self.back_up()
            if isinstance(chunk, int):
                new_value = ValueNode(chunk)
                self.current_node.add_value(new_value)

    def back_up(self):
        self.current_node = self.current_node.parent

    def pop_next_chunk(self):
        digit_chunk = ""
        while True:
            character = self.expression.pop(0)
            if character == ',':
                continue
            if not character.isdigit():
                return character
            else:
                digit_chunk = digit_chunk + character
                if len(self.expression) == 0 or not self.expression[0].isdigit():
                    return int(digit_chunk)

    def __eq__(self, other):
        return self.root == other.root

    def __lt__(self, other):
        return self.root < other.root


@functools.total_ordering
class ValueNode:
    def __init__(self, value):
        self.value = value

    def get_as_object(self):
        return self.value

    def __lt__(self, other):
        if isinstance(other, ValueNode):
            return self.value < other.value
        elif isinstance(other, ListNode):
            temp_list = ListNode(None)
            temp_list.add_value(self)
            return temp_list < other
        else:
            raise NotImplementedError

    def __eq__(self, other):
        if isinstance(other, ValueNode):
            return self.value == other.value
        elif isinstance(other, ListNode):
            temp_list = ListNode(None)
            temp_list.add_value(self)
            return other == temp_list
        else:
            raise NotImplementedError


@functools.total_ordering
class ListNode:
    def __init__(self, parent):
        self.children = []  # Note: the children are ordered
        self.parent = parent

    def add_sub_list(self, sub_list):
        self.children.append(sub_list)

    def add_value(self, value):
        self.children.append(value)

    def get_as_object(self):
        return [child.get_as_object() for child in self.children]

    def __len__(self):
        return len(self.children)

    def __eq__(self, other):
        if isinstance(other, ListNode):
            if self.__len__() != len(other):
                return False

            for i in range(self.__len__()):
                if self.children[i] != other.children[i]:
                    return False
            return True
        elif isinstance(other, ValueNode):
            temp_list = ListNode(None)
            temp_list.add_value(other)
            return self == temp_list
        else:
            raise NotImplementedError

    def __lt__(self, other):
        if self == other:
            return False
        if isinstance(other, ListNode):
            min_length = min(self.__len__(), len(other))

            for i in range(min_length):
                if self.children[i] < other.children[i]:
                    return True
                if self.children[i] > other.children[i]:
                    return False
            return min_length == self.__len__()
        elif isinstance(other, ValueNode):
            temp_list = ListNode(None)
            temp_list.add_value(other)
            return self < temp_list
        else:
            raise NotImplementedError
