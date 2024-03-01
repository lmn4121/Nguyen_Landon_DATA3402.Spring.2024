import math

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1,y2):
            x= int(slope * y)
            self.set_pixel(x,y, **kargs)

    def inverse_line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        b = int((y2-y1)/(len(list(range(y1,y2)))))+1
        a=int(y2-y1)
        for y in range(y1,y2):
            x= int(slope * y)
            self.set_pixel(x,y+a, **kargs)
            a-=b
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))

    def __repr__(self):
        return 'Canvas('+repr(self.width)+','+repr(self.length)+')'

class shape():
    shapes=list()
    def __init__(self,name="",**kwargs):
        shape.shapes.append(self)
        shape.name=name
        self.kwargs=kwargs
    def area(self):
        raise NotImplementedError
    def perimeter(self):
        raise NotImplementedError
    def overlap(self, s):
        ret=list()
        s_points=s.generate_points()
        for p in range(len(s_points)):
            x,y=s_points[p]
            ret.append(not self.in_bound(x,y))
        return not all(ret)
    def paint(self):
        raise NotImplementedError

class rectangle(shape):
    def __init__(self,l,w,x,y,**kwargs):
        shape.__init__(self,**kwargs)
        self.__length=l
        self.__width=w
        self.__x=x
        self.__y=y

    def get_length(self):
        return self.__length
    def get_width(self):
        return self.__width
    def get_x(self):
        return self.__x
    def get_y(self):
        return self.__y
    
    def area(self):
        return self.__length*self.__width
    def perimeter(self):
        return 2*self.__length+2*self.__width

    ## Check (x,y) in object

    def in_bound(self,x,y):
        x2,y2=self.__x+self.__length, self.__y+self.__width
        return all([(x>self.__x and x<x2) and (y>self.__y and y<y2)])

    def generate_points(self, n=16):
        n=16 if n>16 else n
        ret=[(self.__x, self.__y), (self.__x+self.__length, self.__y), (self.__x,self.__y+self.__width), (self.__x+self.__length, self.__y+self.__width)]
        n-=4
        per_side=math.floor(n/4)
        for n in range(1,per_side+1):ret.append((self.__x + n*(self.__length/(per_side+1)), self.__y))
        for n in range(1,per_side+1):ret.append((self.__x + n*(self.__length/(per_side+1)), self.__y+self.__width))
        for n in range(1,per_side+1):ret.append((self.__x, self.__y + n*(self.__width/(per_side+1))))
        for n in range(1,per_side+1):ret.append((self.__x+self.__length, self.__y + n*(self.__width/(per_side+1))))
        return ret

    def paint(self, canvas):
        canvas.v_line(self.__x, self.__y, self.__width, **self.kwargs)
        canvas.v_line(self.__x, self.__y + self.__length, self.__width, **self.kwargs)
        canvas.h_line(self.__x, self.__y, self.__length, **self.kwargs)
        canvas.h_line(self.__x + self.__width, self.__y, self.__length, **self.kwargs)

    def __repr__(self):
        return 'paint.rectangle('+repr(self.__length)+','+repr(self.__width)+','+repr(self.__x)+','+repr(self.__y)+')'

class triangle(shape):
    def __init__(self,a,b,c,x,y,**kwargs):
        shape.__init__(self,**kwargs)
        self.__a=a
        self.__b=b
        self.__c=c
        self.__x=x
        self.__y=y

    def get_a(self):
        return self.__a
    def get_b(self):
        return self.__b
    def get_c(self):
        return self.__c
    def get_x(self):
        return self.__x
    def get_y(self):
        return self.__y

    def area(self):
        s=self.perimeter()/2
        return math.sqrt(s*(s-self.__a)*(s-self.__b)*(s-self.__c))
    def perimeter(self):
        return self.__a+self.__b+self.__c

    ## Check if (x,y) is inside the object

    def __angleC(self):
        return math.acos((self.__a**2+self.__b**2-self.__c**2)/(2*self.__a*self.__b))
    def __endpoint(self):
        theta=self.__angleC()
        return (self.__b*math.cos(theta)+self.__x), (self.__b*math.sin(theta)+self.__y)
    def __slopeBC(self):
        x2,y2=self.__endpoint()
        return (y2-self.__y)/(x2-self.__x), (y2-self.__y)/(x2-(self.__x+self.__a))
    def in_bound(self,x,y):
        vx,vy=self.__endpoint()
        mb,mc=self.__slopeBC()
        x1,x2=((y-(vy-(mb*vx)))/mb),((y-(vy-(mc*vx)))/mc)
        return all([(y>=self.__y and y<=vy),(x>=x1 and x<=x2)])

    def generate_points(self, n=16):
        n=16 if n>16 else n
        ret=[(self.__x,self.__y), (self.__endpoint()), (self.__x+self.__a, self.__y)]
        n-=3
        per_side=math.floor(n/3)
        theta_b=self.__angleC()
        theta_c=math.acos((self.__a**2+self.__c**2-self.__b**2)/(2*self.__a*self.__c))
        for x in range(1,per_side+1): ret.append((self.__x+self.__a/(per_side+1)*x, self.__y))
        for x in range(1,per_side+1): ret.append((self.__b/(per_side+1)*x*math.cos(theta_b)+self.__x, self.__b/(per_side+1)*math.sin(theta_b)+self.__y))
        for x in range(1,per_side+1): ret.append((self.__c/(per_side+1)*x*math.cos(theta_c-math.pi)+(self.__x+self.__a), self.__c/(per_side+1)*math.sin(theta_c)+self.__y))
        return ret

    def paint(self,canvas):
        x2,y2=self.__endpoint()
        canvas.h_line(self.__x, self.__y, self.__a,**self.kwargs)
        canvas.line(self.__x,self.__y,int(x2),int(y2), **self.kwargs)
        canvas.inverse_line(self.__x,self.__y,int(x2),int(y2), **self.kwargs)

    def __repr__(self):
        return 'paint.triangle('+repr(self.__a)+','+repr(self.__b)+','+repr(self.__c)+','+repr(self.__x)+','+repr(self.__y)+')'

class circle(shape):
    def __init__(self,r,x,y,**kwargs):
        shape.__init__(self,**kwargs)
        self.__radius=r
        self.__x=x
        self.__y=y

    def get_radius(self):
        return self.__radius
    def get_x(self):
        return self.__x
    def get_y(self):
        return self.__y

    def area(self):
        return 3.14*self.__radius**2
    def perimeter(self):
        return 2*3.14*self.__radius

    # Check (x,y) in object

    def in_bound(self,x,y):
        return self.__radius>math.sqrt((x-self.__x)**2+(y-self.__y)**2)

    def generate_points(self,n=16):
        n=16 if n>16 else n
        ret=list()
        for count in range(n): ret.append((self.__radius*math.cos(2*math.pi/n*count)+self.__x, self.__radius*math.sin(2*math.pi/n*count)+self.__y))
        return ret

    def paint(self, canvas):
        canvas.h_line(self.__x, self.__y, self.__radius)
        canvas.h_line(self.__x, self.__y-self.__radius, self.__radius)
        for n in range(self.__radius):
            canvas.h_line(self.__x+n, self.__y, self.__radius-n+1, **self.kwargs)
            canvas.h_line(self.__x+n, self.__y-self.__radius+n, self.__radius-n+1, **self.kwargs)
        for n in range(self.__radius):
            canvas.h_line(self.__x-n, self.__y, self.__radius-n+1, **self.kwargs)
            canvas.h_line(self.__x-n, self.__y-self.__radius+n, self.__radius-n+1, **self.kwargs)

    def __repr__(self):
        return 'paint.circle('+repr(self.__radius)+','+repr(self.__x)+','+repr(self.__y)+')'

class CompoundShape(shape):
    def __init__(self, shapes):
        self.shapes = shapes

    def paint(self, canvas):
        for s in self.shapes:
            s.paint(canvas)
