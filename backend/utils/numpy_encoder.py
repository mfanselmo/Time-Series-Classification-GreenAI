import numpy as np
from typing import Union

def transformer(obj):
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                        np.int16, np.int32, np.int64, np.uint8,
                        np.uint16, np.uint32, np.uint64)):

        return int(obj)

    elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
        return float(obj)

    elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
        return {'real': obj.real, 'imag': obj.imag}

    elif isinstance(obj, (np.ndarray,)):
        return obj.tolist()

    elif isinstance(obj, (np.bool_)):
        return bool(obj)

    elif isinstance(obj, (np.void)): 
        return None

    return obj

def NumpyEncoder(object: Union[list, dict]): 
    """ Converts dicts or arrays with numpy types to python """


    if isinstance(object, list):
        for i, value in enumerate(object):
            object[i] = NumpyEncoder(value)

    elif isinstance(object, dict):
        for key in object.keys():
            object[key] = NumpyEncoder(object[key])
    else:
        object = transformer(object)

    return object
