class ParserFailedException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class InvalidInputException(Exception): 
    def __init__(self, *args, **kwargs): 
        Exception.__init__(self, *args, **kwargs)
        
class EmptyDataframeException(Exception): 
    def __init__(self, *args, **kwargs): 
        Exception.__init__(self, *args, **kwargs)

class EmptyHTTPResponseException(Exception):
    def __init__(self, *args, **kwargs): 
        Exception.__init__(self, *args, **kwargs)