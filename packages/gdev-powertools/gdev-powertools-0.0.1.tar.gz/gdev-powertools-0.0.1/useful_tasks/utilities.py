# -*- coding: utf-8 -*-
"""
Nombre del archivo: utilities.py
Creado por juansanz@gmail.com en Jue Abr 27 04:21:26 2023

"""


class Utilities:
    # constructor
    def __init__(self, message: str, code: int):
        """Este método se invoca al crear el objeto de la clase"""
        self.message = message
        self.code = code

    # toString
    def __str__(self):
        return "Utilities@{:#x}: Error {}".format(id(self), self.code)
