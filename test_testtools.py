import unittest
import testtools

class TestTestTools(unittest.TestCase):
    def test_run_function_tests(self):
        # Partitions
        #     cases size
        #         == 1 [x] | > 1 [x]
        #     args length
        #         == 0 [x] | == 1 [x] | > 1 [x]
        #     kwargs in function
        #         == 0 [x] | == 1 [x] | > 1 [x]
        #     kwargs used
        #         == 0 x] | == 1 [x] | < kwargs in [x] | == kwargs in [x]
        #     tests pass
        #         == True [x] | == False [x]
        #     cases passed in failed test
        #         == 0 [x] | == 1 [x] | > 1 & < cases [x]
        # Coverage
        #     cases == 1 | args == 0 | kwargs in == 0 | tests don't pass |
        #         cases passed == 0
        #     cases > 1 | args == 1 | kwargs in == 1 | kwargs used == 0 |
        #         cases passed == 1
        #     args > 1 | kwargs used == 1 | cases > cases passed > 1
        #     kwargs in > 1 | kwargs used < kwargs in | tests pass
        #     kwargs used == kwargs in
        function = testtools.run_function_tests
        cases = (
            (lambda: True, [{}], [False]),

            (lambda a, b=2: (a + b) == (a * b),
             [{'args': [2]}, {'args': [3]}], [True, True]),

            (lambda a, b, c=2: (a + b) * c, [
                {'args': [1, 2], 'kwargs': {'c': 4}},
                {'args': [3, 3], 'kwargs': {'c': 1}},
                {'args': [2, 3], 'kwargs': {'c': 5}}],
             [12, 6, 16]),

            (lambda a='s', b='a', c='d': a+b+c, [
                {'kwargs': {'a': 'sa', 'b': 'aa'}},
                {'kwargs': {'c': 'dboyz'}},
                {'kwargs': {}}],
             ['saaad', 'sadboyz', 'sad']),

            (lambda a=5, b=3: (a%b) * b,
             [{'kwargs': {'a': 7, 'b': 2}}], [2]))

        message = testtools.function_message
        expected_group = (
            [(False, message % (False, True))],

            [(True, message % (True, True)),
             (False, message % (True, False))],

            [(True, message % (12, 12)),
             (True, message % (6, 6)),
             (False, message % (16, 25))],

            [(True, message % ('saaad', 'saaad')),
             (True, message % ('sadboyz', 'sadboyz')),
             (True, message % ('sad', 'sad'))],

            [(True, message % (2, 2))])

        for i, testcase in enumerate(cases):
            expected_values = expected_group[i]
            j = 0
            for actual, actual_message in function(*testcase):
                expected, expected_message = expected_values[j]
                self.assertTrue(expected == actual, message % (expected, actual))
                self.assertTrue(
                    expected_message == actual_message,
                    message % (expected_message, actual_message))
                j += 1

    def test_run_void_method_tests(self):
        # Partitions
        #     instances length
        #         == 1 [x] | > 1 [x]
        #     args length
        #         == 0 [x] | == 1 [x] | > 1 [x]
        #     kwargs in
        #         == 0 [x] | == 1 [x] | > 1 [x]
        #     kwargs used
        #         == 0 [x] | == 1 [x] | > 1 & < kwargs in [x] | == kwargs in [x]
        #     targets size
        #         == 1 [x] | > 1 [x]
        #     tests pass
        #         == true [x] | == false [x]
        #     targets met
        #         == 0 [x] | == 1 [x] | > 1 & < targets [x]
        # Coverage
        #     instances == 1 | args == 0 | kwargs in == 0 | targets == 1 |
        #         tests don't pass | targets met == 0
        #     instances > 1 | args == 1 | kwargs in == 1 | kwargs used == 0 |
        #         targets > 1 | 1 < targets met < targets
        #     args > 1 | kwargs used == 1 | targets met == 1
        #     kwargs in > 1 | 1 < kwargs used < kwargs in | tests pass
        #     kwargs used == kwargs in
        function = testtools.run_void_method_tests
        cases = (
            ([TestClass1()], 'increment', [{}], [{'i': 2}]),

            ([TestClass3('s', 3), TestClass3('init', 1, '_')], 'make_x',
              [{'args': [2]}, {'args': [2]}],
              [{'b': 3, 'c': '~', 'x': '~~~s~~~'},
               {'b': 2, 'c': '_', 'x': '__init__'}]),

            ([TestClass2(1), TestClass2(2), TestClass2(3)],
             'method1',
             [{'args': (3, 2), 'kwargs': {'c': 2}},
              {'args': (2, 3), 'kwargs': {'c': 3}},
              {'args': (4, 4), 'kwargs': {'c': 4}}],
             [{'a': 10, 'b': 3}, {'a': 10, 'b': 3}, {'a': 16, 'b': 4}]),

            ([TestClass4()], 'method1',
             [{'kwargs': {'a': 's', 'c': 'd'}}],
             [{'a': 'sbd'}]),

            ([TestClass4(c='e'), TestClass4(b='i', c='r')], 'method1',
             [{'kwargs': {'a': 'm', 'b': 'o', 'c': 'd'}},
              {'kwargs': {'a': 'f', 'b': 'a', 'c': 'r'}}],
             [{'a': 'mod'}, {'a': 'far'}])
        )

        message = testtools.method_message
        expected_group = (
            [{'i': (False, message % ('i', 2, 1))}],

            [{'b': (False, message % ('b', 3, 2)),
              'c': (True, message % ('c', '~', '~')),
              'x': (False, message % ('x', '~~~s~~~', '~~s~~'))},

             {'b': (True, message % ('b', 2, 2)),
              'c': (False, message % ('c', '_', '~')),
              'x': (False, message % ('x', '__init__', '~~init~~'))}],

            [{'a': (True, message % ('a', 10, 10)),
              'b': (False, message % ('b', 3, 2))},

             {'a': (False, message % ('a', 10, 15)),
              'b': (True, message % ('b', 3, 3))},

             {'a': (False, message % ('a', 16, 32)),
              'b': (True, message % ('b', 4, 4))}],

            [{'a': (True, message % ('a', 'sbd', 'sbd'))}],

            [{'a': (True, message % ('a', 'mod', 'mod'))},
             {'a': (True, message % ('a', 'far', 'far'))}])

        message = testtools.function_message
        for i, testcase in enumerate(cases):
            expected_values = expected_group[i]
            j = 0
            count, length = 0, len(expected_values[j])

            for actual, actual_message in function(*testcase):
                instance = expected_values[j]
                attribute = actual_message.split('"')[1]
                expected, expected_message = instance[attribute]
                self.assertTrue(
                    expected == actual,
                    message % (expected, actual))
                self.assertTrue(
                    expected_message == actual_message,
                    message % (expected_message, actual_message))

                count += 1
                if count == length:
                    count = 0
                    j += 1

    def test_get_instances(self):
        # Partitions
        #     arguments length
        #         == 1 [x] | > 1 [x]
        #     args length
        #         == 0 [x] | == 1 [x] | > 1 [x]
        #     kwargs in
        #         == 0 [x] | == 1 [x] | > 1 [x]
        #     kwargs used
        #         == 0 [x] | == 1 [x] | > 1 & < kwargs in [x] | == kwargs in [x]
        #     attributes size
        #         == 0 [x] | == 1 [x] | > 1 [x]
        # Coverage
        #     arguments == 1 | args == 0 | kwargs in == 0 | attributes == 0
        #     arguments > 1 | args == 1 | kwargs in == 1 | kwargs used == 0
        #     args > 1 | kwargs used == 1 | attributes == 1
        #     kwargs in > 1 | kwargs in > kwargs used > 1
        #     kwargs used == kwargs in | attributes > 1
        tc3_1 = TestClass3('c o o l', 3, c=' ~!~ ')
        tc3_1.b = 2

        function = testtools.get_instances
        cases = (
            (TestClass1, [{}], [{}]),
            (TestClass2, [{'args': [2]}, {'args': [3]}], [{}, {}]),
            (TestClass3,
             [{'args': ['c o o l', 3], 'kwargs': {'c': ' ~!~ '}}],
             [{'b': 2}]),
            (TestClass4,
             [{'kwargs': {'a': 'b', 'b': 'c'}},
              {'kwargs': {'b': 'c', 'c': 'd'}}],
             [{}, {}]),
            (TestClass4,
             [{'kwargs': {'a': 'b', 'b': 'a', 'c': 'd'}},
              {'kwargs': {'a': 'b', 'b': 'o', 'c': 'o'}}],
             [{'a': 's', 'c': 'd'}, {'a': 'h', 'b': 'b'}]))
        expected_group = (
            [TestClass1()],
            [TestClass2(2), TestClass2(3)],
            [tc3_1],
            [TestClass4(a='b', b='c'), TestClass4(b='c', c='d')],
            [TestClass4(a='s', b='a', c='d'), TestClass4(a='h', b='b', c='o')]
        )

        message = testtools.function_message
        for i, testcase in enumerate(cases):
            expected_values = expected_group[i]
            for j, actual in enumerate(function(*testcase)):
                expected = expected_values[j]
                self.assertTrue(
                    expected == actual,
                    message % (repr(expected), repr(actual)))

class TestClass1(object):
    def __init__(self):
        self.i = 0
    def increment(self):
        self.i += 1
    def __eq__(self, other):
        return self.i == other.i
    def __repr__(self):
        return 'TestClass1\ni: %s' % self.i

class TestClass2(object):
    def __init__(self, a, b=1):
        self.a = a
        self.b = a*b
    def method1(self, a, b, c=1):
        self.a = (a+b)*c
        self.b = b
    def __eq__(self, other):
        return self.a == other.a and self.b == other.b
    def __repr__(self):
        return 'TestClass2\na: {0.a}\nb: {0.b}'.format(self)

class TestClass3(object):
    def __init__(self, a, b, c='~'):
        self.a = a
        self.make_x(b, c)
    def make_x(self, b, c='~'):
        self.b = b
        self.c = c
        self.x = '{0}{1}{0}'.format(c*b, self.a)
    def __eq__(self, other):
        for attribute in ('a', 'b', 'c', 'x'):
            if getattr(self, attribute) != getattr(other, attribute):
                return False
        return True
    def __repr__(self):
        return 'TestClass3\na: {0.a}\nb: {0.b}\nc: {0.c}\nx: {0.x}'.format(self)

class TestClass4(object):
    def __init__(self, a='a', b='b', c='c'):
        self.a = a
        self.b = b
        self.c = c
    def method1(self, a='a', b='b', c='c'):
        self.a = a+b+c
    def __eq__(self, other):
        for attribute in ('a', 'b', 'c'):
            if getattr(self, attribute) != getattr(other, attribute):
                return False
        return True
    def __repr__(self):
        return 'TestClass4\na: {0.a}\nb: {0.b}\nc: {0.c}'.format(self)

if __name__ == '__main__':
    unittest.main()
