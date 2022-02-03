
import KS
import CTL

class Algo_checks:

    def __init__(self, model:KS.KS_Model):
        self.model = model

    def run(self, CTL_Formula: str):
        ast = CTL.ASTBuilderTransform(CTL_Formula)


        instruction_list =CTL.reverse_tree_traversal(ast)

        hold = None

        for intr in instruction_list:
            if intr[2] == CTL.TokenTypes.VALUE:
                self.marking(intr)
            else:
                if intr[0] == "/\\":
                    self.and_check(intr)
                elif intr[0] == "not":
                    self.not_check(intr)
                elif intr[0] == "X":
                    hold = intr
                elif intr[0] == "U":
                    hold = intr
                elif intr[0] == "E":
                    if hold[0] == "X":
                        self.exist_next_check(hold, intr)
                    elif hold[0] == "U":
                        self.exist_until(hold, intr)
                    else:
                        raise RuntimeError()
                    hold = None
                elif intr[0] == "A":
                    if hold[0] == "U":
                        self.always_until(hold, intr)
                    else:
                        raise RuntimeError()
                    hold = None
                else:
                    raise RuntimeError()
            # print(intr)
        
        result = True
        detailed_result = False

        for node in self.model.ks_model:
            
            if detailed_result:
                print(node.name + ": " + str(node.check_formula_result(ast[0])))


            if not node.check_formula_result(ast[0]):
                result = False

        if result:
            print("TRUE")
        else:
            print("FALSE")
                


    def marking(self, marking_formula):
        for node in self.model.ks_model:
            if marking_formula[0] == "false":
                node.add_formula_result(marking_formula, False)
            elif marking_formula[0] == "true":
                node.add_formula_result(marking_formula, True)
            else:
                if marking_formula[0] in node.label:
                    node.add_formula_result(marking_formula, True)
                else:
                    node.add_formula_result(marking_formula, False)

    


    
    def and_check(self, and_formula):
        a = and_formula[1][0]
        b = and_formula[1][1]
        for node in self.model.ks_model:
            result = node.check_formula_result(a) and node.check_formula_result(b)
            node.add_formula_result(and_formula, result)

    def not_check(self, not_formula):
        a = not_formula[1][0]
        for node in self.model.ks_model:
            result = not node.check_formula_result(a)
            node.add_formula_result(not_formula, result)

    def exist_next_check(self, next_formula, upper):
        a = next_formula[1][0]
        for node in self.model.ks_model:
            node.add_formula_result(next_formula, False)
            node.add_formula_result(upper, False)
        
        for node in self.model.ks_model:
            for t in node.transitions:
                if self.model.ks_model[t].check_formula_result(a):
                    node.add_formula_result(next_formula, True)
                    node.add_formula_result(upper, True)

    def exist_until(self, eu_formula, upper):
        psi1 = eu_formula[1][0]
        psi2 = eu_formula[1][1]
        for node in self.model.ks_model:
            node.add_formula_result(eu_formula, False)
            node.add_formula_result(upper, False)
            node.seenbefore = False

        L: list[KS.KS_Node] = []

        for node in self.model.ks_model:
            if node.check_formula_result(psi2):
                L.append(node)
            


        while len(L) != 0:
            q = L.pop()
            q.add_formula_result(eu_formula, True)
            q.add_formula_result(upper, True)
            for node in self.model.ks_model:
                for transition in node.transitions:
                    if self.model.ks_model[transition] == q:
                        if not node.seenbefore:
                            node.seenbefore = True
                            if node.check_formula_result(psi1):
                                L.append(node)

    def always_until(self, au_formula, upper):
        psi1 = au_formula[1][0]
        psi2 = au_formula[1][1]
        for node in self.model.ks_model:
            node.add_formula_result(au_formula, False)
            node.add_formula_result(upper, False)
            node.nb = Algo_checks.degree(node)

        L: list[KS.KS_Node] = []

        for node in self.model.ks_model:
            if node.check_formula_result(psi2):
                L.append(node)
        
        while len(L) != 0:
            q = L.pop()
            q.add_formula_result(au_formula, True)
            q.add_formula_result(upper, True)
            for node in self.model.ks_model:
                for transition in node.transitions:
                    if self.model.ks_model[transition] == q:
                        node.nb -= 1
                        if node.nb == 0 and node.check_formula_result(psi1) and not node.check_formula_result(au_formula):
                            L.append(node)



    @staticmethod
    def degree(node: KS.KS_Node) -> int:
        return len(node.transitions)