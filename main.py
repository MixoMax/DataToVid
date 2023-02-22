import os
import PIL
import PIL.Image
import ast

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def read_data(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    return data

class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right


def build_tree(freq_dict):
    nodes = []
    for char, freq in freq_dict.items():
        nodes.append(Node(freq, char))
    
    while len(nodes) > 1:
        # sort nodes by frequency and merge the two lowest
        nodes = sorted(nodes, key=lambda x: x.freq)
        left, right = nodes[0], nodes[1]
        parent = Node(freq=left.freq+right.freq, left=left, right=right)
        nodes = nodes[2:] + [parent]
    
    return nodes[0]


def traverse_tree(node, code='', code_dict={}):
    if node.char is not None:
        code_dict[node.char] = code
    else:
        traverse_tree(node.left, code+'0', code_dict)
        traverse_tree(node.right, code+'1', code_dict)
    
    return code_dict

def huffman_encoding(data):
    freq_dict = {}
    for char in data:
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1
    
    # build Huffman tree and traverse to generate binary code
    tree = build_tree(freq_dict)
    code_dict = traverse_tree(tree)
    
    # store tree and binary output
    encoded_data = ''.join([code_dict[char] for char in data])
    tree_str = str(freq_dict)
    
    return encoded_data, tree_str


def huffman_decoding(data, tree_str):
    freq_dict = eval(tree_str)
    # build Huffman tree and traverse to decode binary data
    tree = build_tree(freq_dict)
    
    decoded_data = ''
    node = tree
    for bit in data:
        if bit == '0':
            node = node.left
        else:
            node = node.right
            
        if node.char is not None:
            decoded_data += node.char
            node = tree
    
    return decoded_data


def to_binary(data):
    # Return the binary representation of data as a byte string

    # convert string to list of ints
    new_data = []
    for char in data:
        try:
            int(char)
        except ValueError:
            char = ord(char)
            if char > 255:
                continue
        new_data.append(char)


    return bytes([int(char) for char in new_data])


def huffman_join(data):
    encoded_data, tree_str = huffman_encoding(data)
    tree_bin = to_binary(tree_str)
    tree_len = bin(len(tree_bin))[2:].zfill(16)

    if len(tree_len) > 64:
        raise ValueError('Tree is too large to encode')
    else:
        # pad tree length to 64 bits
        nulls = '0' * (64 - len(tree_len))
        tree_len = nulls + tree_len

    return str(tree_len) + str(tree_bin) + encoded_data


def huffman_split(data):
    tree_len = int(data[:64], 2)
    tree_bin = data[64:64+tree_len]
    tree_str = ast.literal_eval(tree_bin.decode('ascii'))  # decode the byte string and evaluate as a Python object
    encoded_data = huffman_decoding(data[64+tree_len:], tree_str)

    return encoded_data

data = read_data('test_file.txt')
encoded_data, tree_str = huffman_encoding(data)
encoded_data_2 = huffman_join(data)


decoded_data = huffman_split(encoded_data_2)

print(decoded_data == data)



