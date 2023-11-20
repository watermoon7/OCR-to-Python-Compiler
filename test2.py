a = 5
if a > 4:
    print("peepeepoopoo")

print("123456789")
if a > 1:
    print("a > 1")
    if a > 2:
        print("a > 2")
        if a > 3:
            print("a > 3")
        
    
elif a > 2:
    if a > 2:
        print("a > 2")
    
    if a > 2:
        print("a > 2")
        if a > 2:
            print("a > 2")
            if a > 1:
                print("a > 1")
                if a > 2:
                    print("a > 2")
                    if a > 2:
                        print("a > 2")
                    
                
            elif a > 2:
                if a > 2:
                    print("a > 2")
                
                if a > 2:
                    print("a > 2")
                    if a > 2:
                        print("a > 2")
                    
                    for i in range(1, 10):
                        print(i)
                        for o in range(1, 10):
                            print(o)
                            for j in range(1, 10):
                                print(j)
                                if a > 1:
                                    print("a > 1")
                                    if a > 2:
                                        print("a > 2")
                                        if a > 3:
                                            print("a > 3")
                                        
                                    
                                
                            
                        
                    
                
            
        
    



for i in range(1, 10):
    print(i)
    for o in range(1, 10):
        print(o)
        for j in range(1, 10):
            print(j)
        
    


x = 1
while x < 10:
    print(x)
    x = x + 1
    y = 1
    while y < 1:
        print(x * y)
        y = y + 1
    


def weird(x, y):
    def one():
        print(1)
        def two():
            print(2)
        
        two()
    
    one()
    return x + y


entry = input("Hello there how are you today?")
match entry:
    case "good":
        print("That is great to hear")
    case "bad":
        entry2 = int(input("what is your age?"))
        match entry2:
            case 1:
                print("your young")
            case 2:
                print("you're old")
            case _:
                print("well well well, looks like you need 10 beers")
        
    case _:
        print("well well well, looks like you need a beer")


p = 0
while not (p == 10):
    print("Hello world!")
    p = p + 1
    b = 0


print("Hello world")
