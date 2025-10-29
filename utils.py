from enum import Enum

class Kind(str, Enum):
    CienciasBasicas = "Ciencias Basicas"
    Electiva = "Electiva"
    Semillero = "Semillero"
    Progamacion = "Progamacion"
    Otro = "Otro"
