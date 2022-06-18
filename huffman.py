#umożliwia zapisanie słownika do pliku, później do konwertowania
import json


# Otwieranie z pliku
with open('tekst.txt') as x:
    file_content = x.read()


def calculate_signs_occurrences(text_input):
    # Zliczanie ilości danego znaku w tekście
    how_many_letters = dict()
    distinct_signs = set(text_input)

    for i in distinct_signs:
        how_many_letters[i] = text_input.count(i)
    sorted_how_many_letters = sorted(how_many_letters.items(), key=lambda x: x[1], reverse=True)
    return sorted_how_many_letters


def convert_letters_to_binary(text_input, letter_bin_key):
    # zamiana znaku na kod binarny zgodny z kluczem
    converted = ''.join((letter_bin_key[i] for i in text_input))
    return converted


def make_up_to_eightBIT(bin_input):
    # dopełnienie wartości binarnych do ośmiu (ze względu na tabelę ASCI, która ma 8 znaków)
    index = 1
    counter = 0
    result_list = list()
    sign = ''
    for i in bin_input:
        sign += i
        counter += 1
        if counter == 7 and len(sign) == 7:
            sign = '0' + sign
            result_list.append(sign)
            sign = ''
            counter = 0
        elif len(sign) != 7 and index == len(bin_input):
            sign = ((8-counter) * '0') + sign
            result_list.append(sign)
            sign = ''
        index += 1
    return result_list


def convert_binary_to_ascii(binary_list):
    # przekonwertowanie wartości binarnych do ich odpowiedników w ascii
    output = ''
    for i in binary_list:
        dec_num = int(i, 2)
        output += chr(dec_num)
    return output


def save_compressed_file(text_input, text_key):
    # zpisywanie do pliku z skompresowans
    to_save = json.dumps(text_key) + "\n" + text_input
    with open('compressed_file.txt', 'w') as f:
        f.write(to_save)


class NodeTree:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return self.left, self.right

    def __str__(self):
        return self.left, self.right


def huffman_code_tree(node, bin_string=''):
    # Find Huffman Code
    if type(node) is str:
        return {node: bin_string}
    (left, right) = node.children()
    result_dict = dict()
    result_dict.update(huffman_code_tree(left, bin_string + '0'))
    result_dict.update(huffman_code_tree(right, bin_string + '1'))
    return result_dict


def make_tree(nodes):
    # Utwórz drzewo z węzłów i zwróć korzeń tego drzewa (typ min)
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return nodes[0][0]

# Wypisywanie
if __name__ == '__main__':
    print("Wyniki programu znajdują się w nowo utworzonym pliku compressed_file.txt \n Użyty tekst:")
    print(file_content)
    txt = file_content
    freq = calculate_signs_occurrences(txt)
    node = make_tree(freq)
    encoding = huffman_code_tree(node)
    x = convert_letters_to_binary(txt, encoding)
    y = make_up_to_eightBIT(x)
    z = convert_binary_to_ascii(y)
    save_compressed_file(z, encoding)
