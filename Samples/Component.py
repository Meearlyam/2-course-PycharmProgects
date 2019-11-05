def my_try_decorator(any_function):
    def decorated_function():
        print('I am a text before function call')
        any_function()
        print('And I am a text after function call')
    return decorated_function


@my_try_decorator
def my_function():
    print('I do nothing, ooopsy')


my_function()


@my_try_decorator
def new_function():
    print('And now I print this text. Lets see what will happen')


new_function()
