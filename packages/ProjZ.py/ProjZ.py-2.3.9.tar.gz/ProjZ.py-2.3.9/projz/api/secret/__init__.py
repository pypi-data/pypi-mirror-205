from dill import loads
from types import ModuleType
from os import sep
from os import path
from base64 import b85decode

secret_functions = ModuleType("secret_functions")

with open(f"{path.dirname(__file__)}{sep}data.txt", "r") as file:
    exec(loads(b85decode(file.read())), secret_functions.__dict__)
