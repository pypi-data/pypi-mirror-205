# -*- coding: utf-8 -*-
"""
Nombre del archivo: make_response.py
Creado por juansanz@gmail.com en Jue Abr 27 04:27:11 2023

"""


class MakeResponse:
    # constructor
    def __init__(self, parameter):
        """Este método se invoca al crear el objeto de la clase"""
        self.parameter = parameter

    # destructor
    def __del__(self):
        print("Objeto eliminado")

    # toString
    def __str__(self):
        return "MakeResponse@{:#x}: {}".format(id(self), self.parameter)
