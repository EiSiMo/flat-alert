import hashlib
import pickle

def hash_any_object(var):
    byte_stream = pickle.dumps(var)
    return hashlib.sha256(byte_stream).hexdigest()