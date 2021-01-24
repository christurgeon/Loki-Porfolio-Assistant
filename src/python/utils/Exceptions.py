class ParserFailedException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class InvalidInputException(Exception): 
    def __init__(self, *args, **kwargs): 
        Exception.__init__(self, *args, **kwargs)