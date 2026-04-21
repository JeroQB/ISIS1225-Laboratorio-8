from DataStructures.Tree import bst_node as bn
from DataStructures.List import single_linked_list as sl

def new_map():
    return {"root":None}


def put(my_bst, key, value):
    my_bst["root"] = insert_node(my_bst["root"], key, value)
    return my_bst

def insert_node(root, key, value):
    """
    Inserta recursivamente un nodo en el BST.
    """
    if root is None:
        return bn.new_node(key, value)

    cmp = default_compare(key, root)

    if cmp < 0:
        root["left"] = insert_node(root["left"], key, value)
    elif cmp > 0:
        root["right"] = insert_node(root["right"], key, value)
    else:
        root["value"] = value

    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root


def get(my_bst, key):
    """
    Retorna el valor asociado a la llave. Si no existe, retorna None.
    """
    node = get_node(my_bst["root"], key)
    if node is None:
        return None
    return bn.get_value(node)


def get_node(root, key):
    """
    Busca recursivamente un nodo en el BST.
    """
    if root is None:
        return None

    cmp = default_compare(key, root)

    if cmp < 0:
        return get_node(root["left"], key)
    elif cmp > 0:
        return get_node(root["right"], key)
    else:
        return root
    
def remove(my_bst, key):
    """
    Elimina la pareja llave-valor asociada a key.
    """
    my_bst["root"] = remove_node(my_bst["root"], key)
    return my_bst


def remove_node(root, key):
    """
    Elimina recursivamente un nodo del BST.
    """
    if root is None:
        return None

    cmp = default_compare(key, root)

    if cmp < 0:
        root["left"] = remove_node(root["left"], key)
    elif cmp > 0:
        root["right"] = remove_node(root["right"], key)
    else:
        if root["left"] is None:
            return root["right"]
        if root["right"] is None:
            return root["left"]

        temp = root
        root = get_min_node(temp["right"])
        root["right"] = delete_min_tree(temp["right"])
        root["left"] = temp["left"]

    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root


def contains(my_bst, key):
    """
    Informa si la llave está en la tabla.
    """
    return get(my_bst, key) is not None


def size(my_bst):
    """
    Retorna el número de nodos del árbol.
    """
    return size_tree(my_bst["root"])



def size_tree(root):
    """
    Retorna el tamaño del subárbol cuya raíz es root.
    """
    if root is None:
        return 0
    return root["size"]


def is_empty(my_bst):
    """
    Informa si el árbol está vacío.
    """
    return my_bst["root"] is None


def key_set(my_bst):
    """
    Retorna una lista con todas las llaves del árbol en inorder.
    """
    key_list = sl.new_list()
    return key_set_tree(my_bst["root"], key_list)


def key_set_tree(root, key_list):
    """
    Construye la lista de llaves en inorder.
    """
    if root is not None:
        key_set_tree(root["left"], key_list)
        sl.add_last(key_list, bn.get_key(root))
        key_set_tree(root["right"], key_list)
    return key_list


def value_set(my_bst):
    """
    Retorna una lista con todos los valores del árbol en inorder.
    """
    value_list = sl.new_list()
    return value_set_tree(my_bst["root"], value_list)


def value_set_tree(root, value_list):
    """
    Construye la lista de valores en inorder.
    """
    if root is not None:
        value_set_tree(root["left"], value_list)
        sl.add_last(value_list, bn.get_value(root))
        value_set_tree(root["right"], value_list)
    return value_list

def get_min(my_bst):
    """
    Retorna la menor llave del árbol.
    """
    node = get_min_node(my_bst["root"])
    if node is None:
        return None
    return bn.get_key(node)


def get_min_node(root):
    """
    Retorna el nodo con la menor llave.
    """
    if root is None:
        return None
    if root["left"] is None:
        return root
    return get_min_node(root["left"])


def get_max(my_bst):
    """
    Retorna la mayor llave del árbol.
    """
    node = get_max_node(my_bst["root"])
    if node is None:
        return None
    return bn.get_key(node)


def get_max_node(root):
    """
    Retorna el nodo con la mayor llave.
    """
    if root is None:
        return None
    if root["right"] is None:
        return root
    return get_max_node(root["right"])


def delete_min(my_bst):
    """
    Elimina el nodo con la menor llave.
    """
    my_bst["root"] = delete_min_tree(my_bst["root"])
    return my_bst


def delete_min_tree(root):
    """
    Elimina recursivamente el nodo mínimo.
    """
    if root is None:
        return None

    if root["left"] is None:
        return root["right"]

    root["left"] = delete_min_tree(root["left"])
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root


def delete_max(my_bst):
    """
    Elimina el nodo con la mayor llave.
    """
    my_bst["root"] = delete_max_tree(my_bst["root"])
    return my_bst


def delete_max_tree(root):
    """
    Elimina recursivamente el nodo máximo.
    """
    if root is None:
        return None

    if root["right"] is None:
        return root["left"]

    root["right"] = delete_max_tree(root["right"])
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root


def floor(my_bst, key):
    """
    Retorna la mayor llave menor o igual a key.
    """
    node = floor_key(my_bst["root"], key)
    if node is None:
        return None
    return bn.get_key(node)


def floor_key(root, key):
    """
    Busca el floor de key en el árbol.
    """
    if root is None:
        return None

    cmp = default_compare(key, root)

    if cmp == 0:
        return root

    if cmp < 0:
        return floor_key(root["left"], key)

    temp = floor_key(root["right"], key)
    if temp is not None:
        return temp
    return root


def ceiling(my_bst, key):
    """
    Retorna la menor llave mayor o igual a key.
    """
    node = ceiling_key(my_bst["root"], key)
    if node is None:
        return None
    return bn.get_key(node)


def ceiling_key(root, key):
    """
    Busca el ceiling de key en el árbol.
    """
    if root is None:
        return None

    cmp = default_compare(key, root)

    if cmp == 0:
        return root

    if cmp > 0:
        return ceiling_key(root["right"], key)

    temp = ceiling_key(root["left"], key)
    if temp is not None:
        return temp
    return root


def select(my_bst, pos):
    """
    Retorna la llave de rango pos (0-indexada).
    """
    node = select_key(my_bst["root"], pos)
    if node is None:
        return None
    return bn.get_key(node)


def select_key(root, pos):
    """
    Retorna el nodo cuya llave tiene rango pos.
    """
    if root is None:
        return None

    left_size = size_tree(root["left"])

    if left_size > pos:
        return select_key(root["left"], pos)
    elif left_size < pos:
        return select_key(root["right"], pos - left_size - 1)
    else:
        return root


def rank(my_bst, key):
    """
    Retorna cuántas llaves son menores que key.
    """
    return rank_keys(my_bst["root"], key)


def rank_keys(root, key):
    """
    Calcula recursivamente el rank de una llave.
    """
    if root is None:
        return 0

    cmp = default_compare(key, root)

    if cmp < 0:
        return rank_keys(root["left"], key)
    elif cmp > 0:
        return 1 + size_tree(root["left"]) + rank_keys(root["right"], key)
    else:
        return size_tree(root["left"])


def height(my_bst):
    """
    Retorna la altura del árbol.
    """
    return height_tree(my_bst["root"])


def height_tree(root):
    """
    Retorna la altura del subárbol.
    """
    if root is None:
        return 0
    return 1 + max(height_tree(root["left"]), height_tree(root["right"]))


def keys(my_bst, key_initial, key_final):
    """
    Retorna las llaves en el rango [key_initial, key_final].
    """
    key_list = sl.new_list()
    return keys_range(my_bst["root"], key_initial, key_final, key_list)


def keys_range(root, key_initial, key_final, key_list):
    """
    Construye la lista de llaves en el rango dado.
    """
    if root is None:
        return key_list

    if key_initial < bn.get_key(root):
        keys_range(root["left"], key_initial, key_final, key_list)

    if key_initial <= bn.get_key(root) <= key_final:
        sl.add_last(key_list, bn.get_key(root))

    if key_final > bn.get_key(root):
        keys_range(root["right"], key_initial, key_final, key_list)

    return key_list


def values(my_bst, key_initial, key_final):
    """
    Retorna los valores en el rango [key_initial, key_final].
    """
    value_list = sl.new_list()
    return values_range(my_bst["root"], key_initial, key_final, value_list)



def values_range(root, key_initial, key_final, value_list):
    """
    Construye la lista de valores en el rango dado.
    """
    if root is None:
        return value_list

    if key_initial < bn.get_key(root):
        values_range(root["left"], key_initial, key_final, value_list)

    if key_initial <= bn.get_key(root) <= key_final:
        sl.add_last(value_list, bn.get_value(root))

    if key_final > bn.get_key(root):
        values_range(root["right"], key_initial, key_final, value_list)

    return value_list


def default_compare(key, element):
    """
    Compara una llave con la llave de un nodo.
    """
    if key == bn.get_key(element):
        return 0
    elif key > bn.get_key(element):
        return 1
    return -1