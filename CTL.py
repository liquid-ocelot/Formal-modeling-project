from enum import Enum
from tkinter import N

class TokenTypes(Enum):
    OPERATOR = 0
    EXPRESSION = 1
    VALUE = 2
    COMPLEX_EXPRESSION = 3

OP_LIST = [ "not", "/\\", "\\/", "G", "U", "F", "(", ")", "=>", "E", "A", "X"]
VALUE_LIST = ["true", "false"]

def lexer(formula: str):
    words = formula.split(" ")
    expression = []
    for w in words:
        if w in OP_LIST:
            expression.append((TokenTypes.OPERATOR, w))
        elif w in VALUE_LIST:
            if w == "true":
                expression.append((TokenTypes.VALUE, "true"))
            else:
                expression.append((TokenTypes.VALUE, "false"))
        else:
            expression.append((TokenTypes.EXPRESSION, w))
    return expression

def ParseTreeBuilder(token_list):
    tree = []
    token_index = 0
    while token_index < len(token_list):
        if token_list[token_index][1] == "(":
            inc, node = ParseTreeBuilder(token_list[token_index + 1:])
            token_index += inc + 2
            tree.append((TokenTypes.COMPLEX_EXPRESSION, node))
        elif token_list[token_index][1] == ")":
            return token_index, tree
        else:
            tree.append(token_list[token_index])
            token_index += 1
    return tree


def makeCounter():
    n = 0
    def counter():
        nonlocal n
        n += 1
        return n
    return counter

def ASTBuilder(formula: str):
    parse_tree = ParseTreeBuilder(lexer(formula))
    AST = ASTNodeBuilder(parse_tree, makeCounter())
    return AST

def ASTBuilderTransform(formula: str):
    # print(formula == "A ( G ( E ( F ( idle1 /\\ idle2 ) ) ) )")
    parse_tree = ParseTreeBuilder(lexer(formula))
    counter = makeCounter()
    AST = ASTNodeBuilder(parse_tree, counter)
    AST = transform_tree(AST, counter)
    return AST

def ASTNodeBuilder(parse_tree, count_function):


    nodes = []

    for i in range(len(parse_tree)):
        token_type = parse_tree[i][0]
        token_value = parse_tree[i][1]
        


        if token_type == TokenTypes.OPERATOR:
            if token_value == "not":
                nodes.append(("not", [eval_token(parse_tree[i + 1], count_function)[0]], TokenTypes.OPERATOR, count_function()))
            elif token_value == "/\\":
                nodes.append(("/\\", [eval_token(parse_tree[i - 1], count_function)[0], eval_token(parse_tree[i + 1], count_function)[0]], TokenTypes.OPERATOR, count_function()))
            elif token_value == "\\/":
                nodes.append(("\\/", [eval_token(parse_tree[i - 1], count_function)[0], eval_token(parse_tree[i + 1], count_function)[0]], TokenTypes.OPERATOR, count_function()))
            elif token_value == "G":
                nodes.append(("G", [eval_token(parse_tree[i + 1], count_function)[0]], TokenTypes.OPERATOR, count_function()))
                # nodes.append(("not", [("U", [("true", [], TokenTypes.VALUE), ("not", [eval_token(parse_tree[i + 1])[0]], TokenTypes.OPERATOR)], TokenTypes.OPERATOR)], TokenTypes.OPERATOR))
            elif token_value == "F":
                # nodes.append(("F", [eval_token(parse_tree[i + 1])[0]], TokenTypes.OPERATOR))
                nodes.append(("U", [("true", [], TokenTypes.VALUE, count_function()), eval_token(parse_tree[i + 1], count_function)[0]], TokenTypes.OPERATOR, count_function()))
            elif token_value == "U":
                nodes.append(("U", [eval_token(parse_tree[i - 1], count_function, )[0], eval_token(parse_tree[i + 1], count_function)[0]], TokenTypes.OPERATOR, count_function()))
            elif token_value == "=>":
                # nodes.append(("=>", [eval_token(parse_tree[i - 1])[0], eval_token(parse_tree[i + 1])[0]], TokenTypes.OPERATOR))
                nodes.append(("\\/", [("not", [eval_token(parse_tree[i - 1], count_function)[0]], TokenTypes.OPERATOR), eval_token(parse_tree[i + 1], count_function)[0]], TokenTypes.OPERATOR, count_function()))
            elif token_value == "E":
                nodes.append(("E", [eval_token(parse_tree[i + 1], count_function)[0]], TokenTypes.OPERATOR, count_function()))
            elif token_value == "A":
                nodes.append(("A", [eval_token(parse_tree[i + 1], count_function)[0]], TokenTypes.OPERATOR, count_function()))
            elif token_value == "X":

                nodes.append(("X", [eval_token(parse_tree[i + 1], count_function)[0]], TokenTypes.OPERATOR, count_function()))
    return nodes

def eval_token(token, count_function):
    if token[0] == TokenTypes.COMPLEX_EXPRESSION:
        return ASTNodeBuilder(token[1],count_function)
    else:
        return [(token[1], [], TokenTypes.VALUE, count_function())]






def printTree(node, level=0):

    if level == 0:
        node = node[0]

    if len(node[1]) == 0:
        print(' ' * 4 * level + '->', node[0])
    elif len(node[1]) == 1:
        printTree(node[1][0], level + 1)
        print(' ' * 4 * level + '->', node[0])
    else:
        printTree(node[1][0], level + 1)
        print(' ' * 4 * level + '->', node[0])
        printTree(node[1][1], level + 1)



def tree_traversal(AST):

    trav = []

    def add_trav(step):
        trav.append(step)

    if len(AST[0][1]) == 0:
        add_trav(AST[0])
    if len(AST[0][1]) == 1:
        add_trav(AST[0])
        trav += tree_traversal(AST[0][1])
    elif len(AST[0][1]) == 2:
        add_trav(AST[0])
        trav += tree_traversal([AST[0][1][0]])
        trav += tree_traversal([AST[0][1][1]])

    return trav
    

def reverse_tree_traversal(AST):
    return tree_traversal(AST)[::-1]





def transform_tree(AST, count_function):

    for i in range(len(AST)):
        if AST[i][0] == "A":
            if AST[i][1][0][0] == "X":
                AST = [("not", [
                    ("E", [
                        ("X", [
                            ("not", AST[i][1][0][1], TokenTypes.OPERATOR, count_function())
                        ], TokenTypes.OPERATOR, count_function())
                    ], TokenTypes.OPERATOR, count_function())
                ], TokenTypes.OPERATOR, count_function())]
            
            elif AST[i][1][0][0] == "G":
                AST = [("not", [
                    ("E", [
                        ("U", [
                            ("true", [], TokenTypes.VALUE, count_function()),
                            ("not", AST[i][1][0][1], TokenTypes.OPERATOR, count_function())
                        ], TokenTypes.OPERATOR, count_function())
                    ], TokenTypes.OPERATOR, count_function())
                ], TokenTypes.OPERATOR, count_function())]
        

        if len(AST[i][1]) != 0:
            transform_tree(AST[i][1], count_function)
            # print(AST)

    return AST



