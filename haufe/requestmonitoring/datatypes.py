from io import StringIO
import traceback


def importable_name(name):
    # A datatype that converts a Python dotted-path-name to an object
    try:
        components = name.split('.')
        start = components[0]
        g = globals()
        package = __import__(start, g, g)
        modulenames = [start]
        for component in components[1:]:
            modulenames.append(component)
            try:
                package = getattr(package, component)
            except AttributeError:
                n = '.'.join(modulenames)
                package = __import__(n, g, g, component)
        return package
    except ImportError:
        IO = StringIO()
        traceback.print_exc(file=IO)
        raise ValueError(
            'The object named by "%s" could not be imported\n%s' % (
                name, IO.getvalue()))


def python_dotted_path(name):
    # A datatype that ensures that a dotted path name can be resolved but
    # returns the name instead of the object
    ob = importable_name(name)  # NOQA - will fail in course
    return name
