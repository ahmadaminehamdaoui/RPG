from math import sqrt, sin, cos, radians

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def normalize(self):
        if (self.x, self.y) == (0,0):
            return self
        else:
            length = sqrt(self.x**2 + self.y**2)
            x, y = self.x/length, self.y/length
            return Vector2(x, y)
    
    def rotateBy(self, degrees):
        angle = radians(degrees)
        return Vector2(self.x * cos(angle) - self.y * sin(angle), self.x * sin(angle) + self.y * cos(angle))
    
    def toTuple(self):
        return [self.x, self.y]

    def __add__(self, vec2):
        assert type(vec2) == Vector2, "Type Vector2 can only be added to : 'Vector2'"
        return Vector2(self.x+vec2.x, self.y+vec2.y)
    
    def __sub__(self, vec2):
        assert type(vec2) == Vector2, "Type Vector2 can only be substracted by : 'Vector2'"
        return Vector2(self.x-vec2.x, self.y-vec2.y)
    def __mul__(self, vec2):
        assert type(vec2) == int or type(vec2) == float, "Type Vector2 can only be multiplied by : 'int' and 'float'"
        return Vector2(self.x*vec2, self.y*vec2)
    
    def __rmul__(self, vec2):
        assert type(vec2) == int or type(vec2) == float, "Type Vector2 can only be multiplied by : 'int' and 'float'"
        return Vector2(self.x*vec2, self.y*vec2)

    def __eq__(self, vec2):
        return (self.x == vec2.x and self.y == self.y)

    def __repr__(self):
        return 'Vector2({},{})'.format(str(self.x),str(self.y))