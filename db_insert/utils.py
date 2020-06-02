from datetime import datetime


def time_operation(function):
    def timed_operation(*args, **kwargs):
        ts = datetime.now()
        result = function(*args, **kwargs)
        te = datetime.now()

        if 'log_time' in kwargs:
            name = kwargs.get('log_name', function.__name__.upper())
            kwargs['log_time'][name] = str(te - ts)
        else:
            print(f"{function.__name__}: {str(te - ts)}")
        return result
    return timed_operation
