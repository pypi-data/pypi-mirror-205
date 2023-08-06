from numpy import ndarray
import torch.tensor
import dill
import inspect

from . import files


"""
IDEA: serialize function and data to bytes string - which we then save to image metadata
Then you dont need another file, just slap it on the og image
Need a way to write and read metadata
hmac sign the original bytes so that we can verify???

"""

class archive(object):
    """
    plotarchive.archive is the main function to save your code


    """
    def __init__(self, filename=None):

        if filename is None:
            self.filename = 'myplot.plotarchive'
        else:
            self.filename = filename

    def __call__(self, func):
        def wrapper(*args, **kwargs):

            python_files = files.create_file_dict()

            args_name = inspect.getfullargspec(func)[0]
            args_dict = dict(zip(args_name, args))

            for i, arg in enumerate(args):
                if not isinstance(arg, (int, float, bool, bytes, str, list, tuple, dict, ndarray, torch.tensor)):
                    raise TypeError(f'Unrecognized argument type for {args_name[i]}:{type(arg)}')

            data = {'args': args_dict, 'files': python_files, 'func': func}
            dill.dump(data, open(self.filename, 'wb'))

            return func(*args, **kwargs)
        return wrapper


