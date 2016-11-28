"""Tools to help with running tests

Arguments is an ordered collection of dictionaries where each dictionary has
the optional keys: 'args' [()] and 'kwargs' [{}]. 'args' maps to an ordered
collection, 'kwargs' maps to a dictionary

Results is a tuple of a bool (result) and a string (message) result is true if
the test passed, false otherwise. message is briefly compares the actual
results to the expected
"""

function_message = 'expected: %s\nactual: %s'
method_message = '"%s" attribute\n' + function_message

def run_function_tests(function, cases, expected_values):
    """Run tests on a function

    Assumes function returns a value

    Assumes cases is an ordered collection of dictionaries as defined by
    arguments in the module documentation

    Assumes expected_values is an ordered collection of obects as the expected
    values of the function called with the arguments from cases at the same
    index

    Returns a tuple of a bool (result) and a string (message) as defined by
    results in the module documentation
    """
    message = function_message
    for i, testcase in enumerate(cases):
        expected = expected_values[i]
        actual = function(*testcase.get('args', ()), **testcase.get('kwargs', {}))
        yield actual == expected, message % (expected, actual)

def run_void_method_tests(instances, method_name, cases, targets):
    """Run tests on a void mutator method

    Assumes instances is a list of object instances of a class. Each instance
    has the method 'method_name'

    Assumes method_name is a string as the name of the method being tested.

    Assumes cases is an ordered collection of dictionaries as defined by
    arguments in the module documentation. must be same length as isntances.

    Assumes targets is a list of dictionaries that map strings (attribute)
    to objects to objects (expected) where each attribute is the name of an
    attribute mutated by this method and each expected is the expected value.
    must be same length as instances.

    Returns a tuple of a bool (result) and a string (message) as defined by
    results in the module documentation. Each individual attribute test has no
    local return order, but each attribute group returns in aggregate in the
    same order as targets.
    """
    message = method_message
    for i, testcase in enumerate(cases):
        instance = instances[i]
        method = getattr(instance, method_name)
        method(*testcase.get('args', ()), **testcase.get('kwargs', {}))

        for attribute, expected in targets[i].items():
            actual = getattr(instance, attribute)
            yield expected == actual, message % (attribute, expected, actual)

def get_instances(ClassName, arguments, attributes):
    """Get instances of a class with specific attributes

    Assumes ClassName is a class type

    Assumes arguments is an ordered collection of dictionaries as defined
    in the module documentation

    Assumes attributes is a list of dictionaries that maps strings (name)
    to objects (value). name is the name of an attribute in ClassName, and
    value is what the value of the attribute should be. must be same length
    as arguments.

    Returns a list of instances of ClassName such that each relevant attribute
    is as specified in attributes
    """
    instances = []
    for instance in arguments:
        args = instance.get('args', ())
        kwargs = instance.get('kwargs', {})
        instances.append(ClassName(*args, **kwargs))

    for i, instance in enumerate(instances):
        for name, value in attributes[i].items():
            setattr(instance, name, value)
    return instances
