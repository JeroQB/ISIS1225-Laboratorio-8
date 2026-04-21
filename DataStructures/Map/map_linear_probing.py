import random
from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as al
from DataStructures.Map import map_entry as me


def new_map(num_elements=17, load_factor=0.5, prime=109345121):
    if num_elements <= 0:
        num_elements = 17

    if load_factor <= 0 or load_factor >= 1:
        load_factor = 0.5

    capacity = mf.next_prime(int(num_elements / load_factor))

    table = al.new_list()
    for _ in range(capacity):
        al.add_last(table, me.new_map_entry(None, None))

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
    hash_value = mf.hash_value(my_map, key)
    found, pos = find_slot(my_map, key, hash_value)

    if found:
        entry = al.get_element(my_map["table"], pos)
        me.set_value(entry, value)
    else:
        entry = al.get_element(my_map["table"], pos)
        me.set_key(entry, key)
        me.set_value(entry, value)

        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

        if my_map["current_factor"] > my_map["limit_factor"]:
            rehash(my_map)

    return my_map


def contains(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    found, _ = find_slot(my_map, key, hash_value)
    return found


def get(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    found, pos = find_slot(my_map, key, hash_value)

    if found:
        entry = al.get_element(my_map["table"], pos)
        return me.get_value(entry)
    return None


def remove(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    found, pos = find_slot(my_map, key, hash_value)

    if found:
        entry = al.get_element(my_map["table"], pos)
        me.set_key(entry, "__EMPTY__")
        me.set_value(entry, None)

        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

    return my_map


def size(my_map):
    return my_map["size"]


def is_empty(my_map):
    return my_map["size"] == 0


def key_set(my_map):
    keys = al.new_list()

    for i in range(al.size(my_map["table"])):
        entry = al.get_element(my_map["table"], i)
        key = me.get_key(entry)

        if key is not None and key != "__EMPTY__":
            al.add_last(keys, key)

    return keys


def value_set(my_map):
    values = al.new_list()

    for i in range(al.size(my_map["table"])):
        entry = al.get_element(my_map["table"], i)
        key = me.get_key(entry)

        if key is not None and key != "__EMPTY__":
            al.add_last(values, me.get_value(entry))

    return values


def is_available(table, pos):
    entry = al.get_element(table, pos)
    key = me.get_key(entry)
    return key is None or key == "__EMPTY__"


def default_compare(key, entry):
    entry_key = me.get_key(entry)

    if key == entry_key:
        return 0
    elif key > entry_key:
        return 1
    return -1


def find_slot(my_map, key, hash_value):
    first_avail = None
    occupied = False
    start = hash_value

    while True:
        entry = al.get_element(my_map["table"], hash_value)
        entry_key = me.get_key(entry)

        if entry_key is None:
            if first_avail is None:
                first_avail = hash_value
            return occupied, first_avail

        elif entry_key == "__EMPTY__":
            if first_avail is None:
                first_avail = hash_value

        elif default_compare(key, entry) == 0:
            return True, hash_value

        hash_value = (hash_value + 1) % my_map["capacity"]

        if hash_value == start:
            return occupied, first_avail


def rehash(my_map):
    old_table = my_map["table"]
    old_capacity = my_map["capacity"]

    new_capacity = mf.next_prime(old_capacity * 2)

    new_table = al.new_list()
    for _ in range(new_capacity):
        al.add_last(new_table, me.new_map_entry(None, None))

    my_map["table"] = new_table
    my_map["capacity"] = new_capacity
    my_map["scale"] = random.randint(1, my_map["prime"] - 1)
    my_map["shift"] = random.randint(0, my_map["prime"] - 1)
    my_map["size"] = 0
    my_map["current_factor"] = 0

    for i in range(al.size(old_table)):
        entry = al.get_element(old_table, i)
        key = me.get_key(entry)

        if key is not None and key != "__EMPTY__":
            put(my_map, key, me.get_value(entry))

    return my_map