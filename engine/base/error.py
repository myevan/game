class Error(Exception):
    def __init__(self, name):
        Exception.__init__(self, name)
        self.name = name

    def __str__(self):
        return f"{self.__class__.__name__}<{self.name}>"

    @property
    def category(self):
        return f"{self.__class__.__name__}<{self.name}>"