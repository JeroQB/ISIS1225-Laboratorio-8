from DataStructures.Tree import rbt_node as rbn
from DataStructures.List import single_linked_list as sl

def new_map():
    """
    Crea un mapa ordenado implementado con Red-Black Tree.
    """
    
    return {"root":None}

def default_compare(key, node):
    
    node_key = rbn.get_key(node)
    if key == node_key:
        return 0
    elif key > node_key:
        return 1
    elif key < node_key:
        return -1
    
    
def size_tree(root):
    if root is None:
        return 0
    return root['size']

def is_red_node(node):
    if node is None:
        return False
    return rbn.is_red(node)

"""operaciones de cambio de color y rotacion"""

def rotate_left(node):
    
    if node is None or node["right"] is None:
        return node 
    
    x = node["right"]
    node["right"] = x["left"]
    x["left"] = node
    
    x["color"] = node["color"]
    rbn.change_color(node, rbn.RED)
    
    x["size"] = node["size"]
    node["size"] = 1 + size_tree(node["left"]) + size_tree(node["right"])
    
    return x

def rotate_right(node):
    
    if node is None or node["left"] is None:
        return node
    
    x = node["left"]
    node["left"] = x["right"]
    x["right"] = node
    
    x["color"] = node["color"]
    rbn.change_color(node, rbn.RED)
    
    x["size"] = node["size"]
    node["size"] = 1 + size_tree(node["left"]) + size_tree(node["right"])
    
    return x


def flip_node_color(node):
    
    if node is None:
        return None
    
    if node["color"] == rbn.RED:
        rbn.change_color(node, rbn.BLACK)
        
    else:
        rbn.change_color(node, rbn.RED)
        
    return node


def flip_colors(node):
    
    if node is None:
        flip_node_color(node)
        
        if node["left"] is not None:
            flip_node_color(node["left"])
        
        if node["right"] is not None:
            flip_node_color(node["right"])
    
    return node 


def put(my_rbt, key, value):
    
    
    my_rbt["root"] = insert_node(my_rbt["root"], key, value)
    
    if my_rbt["root"] is not None:
        rbn.change_color(my_rbt["root"], rbn.BLACK)
        
    return my_rbt



def insert_node(root, key, value):
    
    if root is None: 
        return rbn.new_node(key, value, rbn.RED)
    
    cmp = default_compare(key, root)
    
    if cmp < 0:
        root["left"] = insert_node(root["left"], key, value)
        
    elif cmp > 0:
        root["right"] = insert_node(root["right"], key, value)   
    
    else: 
        root["value"] = value
        
        
    if is_red_node(root["right"]) and not is_red_node(root["left"]):
        root = rotate_left(root)
         
    if is_red_node(root["left"]) and is_red_node(root["left"]["left"]):
        root = rotate_right(root)
        
    if is_red_node(root["left"]) and is_red_node(root["right"]):
        flip_colors(root)
        
        
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])                             
    return root


def get(my_rbt, key):
    
    node = get_node(my_rbt["root"], key)
    if node is None:
        return None
    return rbn.get_value(node)


def get_node(root, key):
    if root is None:
        return None
    
    cmp = default_compare(key, root)
    
    if cmp < 0:
        return get_node(root["left"], key)
    
    elif cmp > 0:
        return get_node(root["right"], key)
    
    else:
        return root
    
    
def contains(my_rbt, key):
    return get(my_rbt, key) is not None


def size(my_rbt):
    return size_tree(my_rbt["root"])

def is_empty(my_rbt):
    return my_rbt["root"] is None

            
def key_set(my_rbt):
    lst = sl.new_list()
    key_set_tree(my_rbt["root"], lst)
    return lst

def key_set_tree(root, lst):
    if root is not None:
        key_set_tree(root["left"], lst)
        sl.add_last(lst, rbn.get_key(root))
        key_set_tree(root["right"], lst)
    return lst

def value_set(my_rbt):
    lst = sl.new_list()
    value_set_tree(my_rbt["root"], lst)
    return lst

def value_set_tree(root, lst):
    if root is not None:
        value_set_tree(root["left"], lst)
        sl.add_last(lst, rbn.get_value(root))
        value_set_tree(root["right"], lst)
    return lst

def get_min(my_rbt):
    node = get_min_node(my_rbt["root"])
    if node is None:
        return None
    return rbn.get_key(node) 

def get_min_node(root):
    if root is None:
        return None
    if root["left"] is None:
        return root
    return get_min_node(root["left"])

def get_max(my_rbt):
    node = get_max_node(my_rbt["root"])
    if node is None:
        return None
    return rbn.get_key(node)

def get_max_node(root):
    if root is None:
        return None
    if root["right"] is None:
        return root
    return get_max_node(root["right"])


def height(my_rbt):
    return height_tree(my_rbt["root"])

def height_tree(root):
    if root is None:
        return 0
    
    left_height = height_tree(root["left"])
    right_height = height_tree(root["right"])
    
    return 1 + max(left_height, right_height)

def floor(my_rbt, key):
    node = floor_key(my_rbt["root"], key)
    if node is None:
        return None
    return rbn.get_key(node)

def floor_key(root, key):
    if root is None:
        return None
    
    cmp = default_compare(key, root)
    
    if cmp == 0:
        return root
    
    if cmp < 0:
        return floor_key(root["left"], key)
    
    t = floor_key(root["right"], key)
    if t is not None:
        return t
    else:
        return root
    

def ceiling(my_rbt, key):
    
    node = ceiling_key(my_rbt["root"], key)
    if node is None:
        return None
    return rbn.get_key(node)

def ceiling_key(root, key):
    if root is None:
        return None
    
    cmp = default_compare(key, root)
    
    if cmp == 0:
        return root
    
    if cmp > 0:
        return ceiling_key(root["right"], key)
    
    t = ceiling_key(root["left"], key)
    if t is not None:
        return t
    else:
        return root
    
    
def keys(my_rbt, low_key, high_key):
    lst = sl.new_list()
    keys_range(my_rbt["root"], low_key, high_key, lst)
    return lst

def keys_range(root, low_key, high_key, lst):
    
    if root is None:
        return lst
    
    root_key = rbn.get_key(root)
    
    if low_key < root_key:
        keys_range(root["left"], low_key, high_key, lst)
        
    if low_key <= root_key <= high_key:
        sl.add_last(lst, root_key)
    
    if root_key < high_key:
        keys_range(root["right"], low_key, high_key, lst)
        
    return lst

def values(my_rbt, key_lo, key_hi):
    """
    Retorna una lista enlazada con los valores cuyas llaves
    están entre key_lo y key_hi.
    """
    lst = sl.new_list()
    values_range(my_rbt["root"], key_lo, key_hi, lst)
    return lst

def values_range(root, key_lo, key_hi, lst):
    """
    Agrega a la lista los valores cuyas llaves están
    en el rango [key_lo, key_hi].
    """
    if root is None:
        return lst

    root_key = rbn.get_key(root)

    if key_lo < root_key:
        values_range(root["left"], key_lo, key_hi, lst)

    if key_lo <= root_key <= key_hi:
        sl.add_last(lst, rbn.get_value(root))

    if root_key < key_hi:
        values_range(root["right"], key_lo, key_hi, lst)

    return lst
            
    
def select(my_rbt, pos):
    """
    Retorna la llave de rango pos (0-index).
    """
    if pos < 0:
        return None

    node = select_node(my_rbt["root"], pos)
    if node is None:
        return None
    return rbn.get_key(node)


def select_node(root, pos):
    """
    Busca el nodo cuya llave tiene rango pos.
    """
    if root is None:
        return None

    left_size = size_tree(root["left"])

    if pos < left_size:
        return select_node(root["left"], pos)
    elif pos > left_size:
        return select_node(root["right"], pos - left_size - 1)
    else:
        return root



def rank(my_rbt, key):
    """
    Retorna el número de llaves menores que key.
    """
    return rank_node(my_rbt["root"], key)


def rank_node(root, key):
    if root is None:
        return 0

    cmp = default_compare(key, root)

    if cmp < 0:
        return rank_node(root["left"], key)
    elif cmp > 0:
        return 1 + size_tree(root["left"]) + rank_node(root["right"], key)
    else:
        return size_tree(root["left"])



def delete_min(my_rbt):
    """
    Elimina el nodo con la menor llave.
    """
    my_rbt["root"] = delete_min_node(my_rbt["root"])
    return my_rbt


def delete_min_node(root):
    if root is None:
        return None

    if root["left"] is None:
        return root["right"]

    root["left"] = delete_min_node(root["left"])
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root



def delete_max(my_rbt):
    """
    Elimina el nodo con la mayor llave.
    """
    my_rbt["root"] = delete_max_node(my_rbt["root"])
    return my_rbt


def delete_max_node(root):
    if root is None:
        return None

    if root["right"] is None:
        return root["left"]

    root["right"] = delete_max_node(root["right"])
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root


def remove(my_rbt, key):
   
    my_rbt["root"] = remove_node(my_rbt["root"], key)
    return my_rbt


def remove_node(root, key):
    if root is None:
        return None

    cmp = default_compare(key, root)

    if cmp < 0:
        root["left"] = remove_node(root["left"], key)

    elif cmp > 0:
        root["right"] = remove_node(root["right"], key)

    else:
        # Caso 1: sin hijo izquierdo
        if root["left"] is None:
            return root["right"]

        # Caso 2: sin hijo derecho
        if root["right"] is None:
            return root["left"]

        # Caso 3: dos hijos
        temp = root
        root = get_min_node(temp["right"])
        root["right"] = delete_min_node(temp["right"])
        root["left"] = temp["left"]

    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root
