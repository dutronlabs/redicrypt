from Crypto.Cipher import AES
import random
import string
import redis
import os


def initialize_encryption(key_path, ivr_path):
    """ This function (re)generates the keys we'll use for encryption and stores them on the file system."""
    # We are using w+ here because during initialization, we are absolutely going to want to truncate it
    # and write a new key.
    with open(key_path, "w+") as key:
        key.write(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16)))
    # with CFB, the IV must be at least length of 16
    with open(ivr_path, "w+") as ivr:
        ivr.write(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16)))


def get_hash(key_path, ivr_path):
    """ This is a utility function to grab the values needed to produce the AES key"""
    with open(key_path, "r+") as key_file:
        key = key_file.read()
    with open(ivr_path, "r+") as ivr_file:
        ivr = ivr_file.read()
    return AES.new(key, AES.MODE_CFB, ivr)


def setencrypted(name, value, key_path=None, ivr_path=None, overredis=None):
    """ This sets a value encrypted in redis """
    aes = get_hash(key_path, ivr_path)
    ciphertext = aes.encrypt(value)
    r = overredis if overredis is not None else loadconfiguration()
    r.set(name, ciphertext)


def getencrypted(name, key_path=None, ivr_path=None, overredis=None):
    """ This gets a value that is encrypted in redis."""
    r = overredis if overredis is not None else loadconfiguration()
    cipher = r.get(name)
    aes = get_hash(key_path, ivr_path)
    return aes.decrypt(cipher)


def loadconfiguration(override=None):
    try:
        if override is not None:
            return redis.StrictRedis(host=override)
        else:
            url = os.environ['REDIS_ENDPOINT']
            return redis.StrictRedis(host=url)
    except Exception, e:
        raise e
