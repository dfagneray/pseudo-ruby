class Shape:
    def __init__(self, a:int,name:str):
        self.a = a
        self.__name = name
    def area(self):
    	return self.a


s = Shape(0,"s")

