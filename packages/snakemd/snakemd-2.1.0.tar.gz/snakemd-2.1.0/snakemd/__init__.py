from .document import *


def new_doc() -> Document:
    """
    Creates a new SnakeMD document. This is a convenience function
    that allows you to create a new markdown document without having
    to import the :class:`Document` class. This is useful for anyone who
    wants to take advantage of the procedural interface of SnakeMD.
    For those looking for a bit more control, each element class
    will need to be imported as needed.
    
    .. doctest:: document
        
        >>> doc = snakemd.new_doc()

    :return: 
        a new Document object
    """
    return Document()
