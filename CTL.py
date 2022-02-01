from enum import Enum

class TokenTypes(Enum):
    OPERATOR = 0
    EXPRESSION = 1
    VALUE = 2
    COMPLEX_EXPRESSION = 3

OP_LIST = [ "not", "/\\", "\\/", "G", "U", "F", "(", ")", "=>", "E"]
VALUE_LIST = ["true", "false"]

def lexer(formula: str):
    words = formula.split(" ")
    expression = []
    for w in words:
        if w in OP_LIST:
            expression.append((TokenTypes.OPERATOR, w))
        elif w in VALUE_LIST:
            if w == "true":
                expression.append((TokenTypes.VALUE, True))
            else:
                expression.append((TokenTypes.VALUE, False))
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



def ASTBuilder(formula: str):
    parse_tree = ParseTreeBuilder(lexer(formula))
    AST = ASTNodeBuilder(parse_tree)
    return AST

def ASTNodeBuilder(parse_tree):


    nodes = []
    for i in range(len(parse_tree)):
        token_type = parse_tree[i][0]
        token_value = parse_tree[i][1]
        
        if token_type == TokenTypes.OPERATOR:
            if token_value == "not":
                nodes.append(("not", [eval_token(parse_tree[i + 1])[0]]))
            elif token_value == "/\\":
                nodes.append(("/\\", [eval_token(parse_tree[i - 1])[0], eval_token(parse_tree[i + 1])[0]]))
            elif token_value == "\\/":
                nodes.append(("\\/", [eval_token(parse_tree[i - 1])[0], eval_token(parse_tree[i + 1])[0]]))
            elif token_value == "G":
                nodes.append(("G", [eval_token(parse_tree[i + 1])[0]]))
            elif token_value == "F":
                nodes.append(("F", [eval_token(parse_tree[i + 1])[0]]))
            elif token_value == "U":
                nodes.append(("U", [eval_token(parse_tree[i - 1])[0], eval_token(parse_tree[i + 1])[0]]))
            elif token_value == "=>":
                nodes.append(("=>", [eval_token(parse_tree[i - 1])[0], eval_token(parse_tree[i + 1])[0]]))
            elif token_value == "E":
                nodes.append(("E", [eval_token(parse_tree[i + 1])[0]]))
    return nodes

def eval_token(token):
    if token[0] == TokenTypes.COMPLEX_EXPRESSION:
        return ASTNodeBuilder(token[1])
    else:
        return [token[1]]




def printTree(node, level=0):

    if level == 0:
        node = node[0]

    if type(node) == str:
        print(' ' * 4 * level + '->', node)
        return

    if len(node[1]) == 1:
        printTree(node[1][0], level + 1)
        print(' ' * 4 * level + '->', node[0][0])
    else:
        printTree(node[1][0], level + 1)
        print(' ' * 4 * level + '->', node[0][0])
        printTree(node[1][0], level + 1)



def tree_traversal(AST):

    trav = []

    def add_trav(step):
        trav.append(step)

    if type(AST) == str:
        add_trav(AST)
        return trav
    
    if len(AST[0][1]) == 1:
        add_trav(AST[0])
        trav += tree_traversal(AST[0][1])
    if len(AST[0][1]) == 2:
        add_trav(AST[0])
        trav += tree_traversal(AST[0][1][0])
        trav += tree_traversal(AST[0][1][1])

    return trav
    

def reverse_tree_traversal(AST):
    return tree_traversal(AST)[::-1]







# print(lexer("P /\\ not Q"))
# print(ParseTreeBuilder(lexer("not ( ( A /\\ B ) \\/ A )")))
# print(ASTBuilder("not ( ( A /\\ B ) \\/ A )"))

# print(ParseTreeBuilder(lexer("G ( E ( F ( idle1 /\\ idle2 ) ) )")))
# print(ASTBuilder("G ( E ( F ( idle1 /\\ idle2 ) ) )"))
# print(ParseTreeBuilder(lexer("F ( idle1 /\\ idle2 )")))
# print(ASTBuilder("F ( ( idle1 \\/ idle3 ) /\\ idle2 )"))

# print(ASTBuilder("G ( E ( F ( idle1 /\\ idle2 ) ) )"))
printTree(ASTBuilder("G ( E ( F ( idle1 /\\ idle2 ) ) )"))
# print(tree_traversal(ASTBuilder("G ( E ( F ( idle1 /\\ idle2 ) ) )")))
# print(reverse_tree_traversal(ASTBuilder("G ( E ( F ( idle1 /\\ idle2 ) ) )")))

for i in reverse_tree_traversal(ASTBuilder("G ( E ( F ( idle1 /\\ idle2 ) ) )")):
    print(i)