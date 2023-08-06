""" 
Modulo para carpetas 
"""
import os


def message() -> str:
    """ 
    Esta funcion imprime un mensage 
    en caso de un error

    Returns: retorna una cadena de texto
    """
    return print("Ingrese una ruta valida")


def show_folders() -> str:
    """ 
    Esta funcion imprime el nombre las carpteas 
    que existen en una ruta asignada
    """
    try:
        ruta = input("Ingrese la ruta: ")
        with os.scandir(path=ruta) as dirs:
            for _dir in dirs:
                if _dir.is_dir():
                    print(_dir.name)
    except FileNotFoundError:
        message()


def create_folder() -> str:
    """ 
    Esta funcion crea una carpeta en la ruta 
    asignada 
    """
    try:
        ruta = input("Ingrese la ruta: ")
        new_folder = input("Nombre de la carpeta: ")
        path = os.path.join(ruta, new_folder)
        if os.path.exists(path):
            print("la carpeta ya existe")
        else:
            os.mkdir(path)
            print("La carpeta ha sido creada exitosamente")
    except FileNotFoundError:
        message()


def rename_folders() -> str:
    """ 
    Esta funcion renombra una carpeta 
    """
    try:
        ruta = input("Ingrese la ruta: ")
        name_folder = input("Ingrese el nombre de la carpeta a renombrar: ")
        new_folder = input("Ingrese el nuevo nombre: ")
        destino = os.path.join(ruta, new_folder)
        path = os.path.join(ruta, name_folder)
        if os.path.exists(path):
            if os.path.exists(destino):
                print("La carpeta no puede existir")
            else:
                os.rename(path, destino)
                print("La carpeta ha sido renombrada con exito")
        else:
            print("La carpeta no existe")
    except FileNotFoundError:
        message()


def delete_folder() -> str:
    """ 
    Esta funcion elimina carpetas
    """
    try:
        ruta = input("Ingrese la ruta: ")
        name_folder = input("Ingrese el nombre de la carpeta: ")
        path = os.path.join(ruta, name_folder)
        if os.path.exists(path):
            os.rmdir(path)
            print("La carpeta ha sido eliminado con exito")
        else:
            print("La carpeta no existe")
    except FileNotFoundError:
        message()
