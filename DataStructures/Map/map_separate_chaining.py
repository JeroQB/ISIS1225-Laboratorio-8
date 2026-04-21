import random 
from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl
from DataStructures.Map import map_entry as me


def new_map(num_elements=17, load_factor=4, prime=109345121):
    """
    Crea una nueva tabla hash con separate chaining.
    """
    if num_elements <= 0:
        num_elements = 17

    if load_factor <= 0:
        load_factor = 4

    capacity = mf.next_prime(num_elements / load_factor)

    table = al.new_list()
    for _ in range(capacity):
        al.add_last(table, sl.new_list())

    my_map = {
        "prime": prime,
        "capacity": capacity,
        "scale": random.randint(1, prime - 1),
        "shift": random.randint(0, prime - 1),
        "table": table,
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0
    }
    return my_map


def put(my_map, key, value):
    """
    Agrega una nueva pareja llave-valor al mapa.
    Si la llave ya existe, actualiza su valor.
    """
    hash_val = mf.hash_value(my_map, key)
    bucket = al.get_element(my_map["table"], hash_val)

    pos = sl.is_present(bucket, key, default_compare)

    if pos != -1:
        entry = sl.get_element(bucket, pos)
        me.set_value(entry, value)
    else:
        entry = me.new_map_entry(key, value)
        sl.add_last(bucket, entry)
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

        if my_map["current_factor"] > my_map["limit_factor"]:
            my_map = rehash(my_map)

    return my_map

def default_compare(key, entry):
    """
    Compara una llave con la llave de una entrada.
    """
    entry_key = me.get_key(entry)

    if key == entry_key:
        return 0
    elif key > entry_key:
        return 1
    return -1


def contains(my_map, key):
    """
    Informa si una llave está en el mapa.
    """
    hash_val = mf.hash_value(my_map, key)
    bucket = al.get_element(my_map["table"], hash_val)
    pos = sl.is_present(bucket, key, default_compare)
    return pos != -1


def remove(my_map, key):
    """
    Elimina la pareja llave-valor asociada a la llave.
    """
    hash_val = mf.hash_value(my_map, key)
    bucket = al.get_element(my_map["table"], hash_val)

    pos = sl.is_present(bucket, key, default_compare)
    if pos != -1:
        sl.delete_element(bucket, pos)
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

    return my_map


def get(my_map, key):
    """
    Retorna el valor asociado a la llave.
    Si no existe, retorna None.
    """
    hash_val = mf.hash_value(my_map, key)
    bucket = al.get_element(my_map["table"], hash_val)

    pos = sl.is_present(bucket, key, default_compare)
    if pos != -1:
        entry = sl.get_element(bucket, pos)
        return me.get_value(entry)

    return None


def size(my_map):
    """
    Retorna la cantidad de elementos del mapa.
    """
    return my_map["size"]


def is_empty(my_map):
    """
    Informa si el mapa está vacío.
    """
    return my_map["size"] == 0


def key_set(my_map):
    """
    Retorna una lista con todas las llaves del mapa.
    """
    keys = al.new_list()

    for i in range(al.size(my_map["table"])):
        bucket = al.get_element(my_map["table"], i)

        for j in range(sl.size(bucket)):
            entry = sl.get_element(bucket, j)
            al.add_last(keys, me.get_key(entry))

    return keys


def value_set(my_map):
    """
    Retorna una lista con todos los valores del mapa.
    """
    values = al.new_list()

    for i in range(al.size(my_map["table"])):
        bucket = al.get_element(my_map["table"], i)

        for j in range(sl.size(bucket)):
            entry = sl.get_element(bucket, j)
            al.add_last(values, me.get_value(entry))

    return values


def rehash(my_map):
    """
    Realiza rehash del mapa duplicando la capacidad
    y reinsertando todos los elementos en la misma estructura.
    """
    old_table = my_map["table"]
    old_capacity = my_map["capacity"]

    new_capacity = mf.next_prime(old_capacity * 2)

    new_table = al.new_list()
    for _ in range(new_capacity):
        al.add_last(new_table, sl.new_list())

    # Guardamos temporalmente los datos viejos y reiniciamos el mapa actual
    my_map["table"] = new_table
    my_map["capacity"] = new_capacity
    my_map["scale"] = random.randint(1, my_map["prime"] - 1)
    my_map["shift"] = random.randint(0, my_map["prime"] - 1)
    my_map["size"] = 0
    my_map["current_factor"] = 0

    # Reinsertar elementos del mapa viejo
    for i in range(al.size(old_table)):
        bucket = al.get_element(old_table, i)

        for j in range(sl.size(bucket)):
            entry = sl.get_element(bucket, j)
            put(my_map, me.get_key(entry), me.get_value(entry))

    return my_map