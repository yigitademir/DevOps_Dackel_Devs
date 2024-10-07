# define ordinary function
def ordinary():
    print("I am ordinary")


# define a decorater function
def make_pretty(func):
    # define the inner function
    def inner():
        # add some additional behavior to decorated function
        print("I got decorated")

        # call original function
        func()
    # return the inner function
    return inner


# decorate the ordinary function
decorated_func = make_pretty(ordinary)

# call the decorated function
decorated_func()
