import KS

class Algo_checks:

    def __init__(self, model:KS.KS_Model):
        self.model = model

    # def marking(self, phi):
    #     if 
    #     for node in self.model.ks_model:

    


    
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

    def exist_next_check(self, next_formula):
        a = next_formula[1][0]
        for node in self.model.ks_model:
            node.add_formula_result(next_formula, False)
        
        for node in self.model.ks_model:
            for t in node.transitions:
                if self.model.ks_model[t].check_formula_result(a):
                    node.add_formula_result(next_formula, True)

    def exist_until(self, eu_formula):
        psi1 = eu_formula[1][0]
        psi2 = eu_formula[1][1]
        for node in self.model.ks_model:
            node.add_formula_result(eu_formula, False)
            node.seenbefore = False

        L: list[KS.KS_Node] = []

        for node in self.model.ks_model:
            if node.check_formula_result(psi2):
                L.append(node)
            
        while len(L) != 0:
            q = L.pop()
            q.add_formula_result(eu_formula, True)
            for node in self.model.ks_model:
                for transition in node.transitions:
                    if self.model.ks_model[transition] == q:
                        if not node.seenbefore:
                            node.seenbefore = True
                            if node.check_formula_result(psi1):
                                L.append(node)

    def always_until(self, au_formula):
        psi1 = au_formula[1][0]
        psi2 = au_formula[1][1]
        for node in self.model.ks_model:
            node.add_formula_result(au_formula, False)
            node.nb = Algo_checks.degree(node)

        L: list[KS.KS_Node] = []

        for node in self.model.ks_model:
            if node.check_formula_result(psi2):
                L.append(node)
        
        while len(L) != 0:
            q = L.pop()
            q.add_formula_result(au_formula, True)
            for node in self.model.ks_model:
                for transition in node.transitions:
                    if self.model.ks_model[transition] == q:
                        node.nb -= 1
                        if node.nb == 0 and node.check_formula_result(psi1) and not node.check_formula_result(au_formula):
                            L.append(node)



    @staticmethod
    def degree(node: KS.KS_Node) -> int:
        return len(node.transitions)