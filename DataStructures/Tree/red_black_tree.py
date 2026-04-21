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

            
    
      
    

