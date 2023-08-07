class Notation:

    def __init__(self, annotation={}):
        self.__dict__ = annotation

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[name] = value

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return f'{self.__class__.__name__}(annotation={self.__dict__})'

    def __contains__(self, key):
        return key in self.__dict__

    def __call__(self, *args, **kwargs):
        def decorator(fn):
            self.__dict__[fn] = {**{index:arg for index, arg in enumerate(args)}, **kwargs}
            return fn
        return decorator