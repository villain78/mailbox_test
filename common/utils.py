
import uuid
import hashlib


def gen_uuid():
    """Generate uuid."""
    return uuid.uuid1().hex


def hash_md5(data):
    """Encrypt the data with MD5."""
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
