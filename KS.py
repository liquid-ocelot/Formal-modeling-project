import json



class KS_Node:

    def __init__(self, name, transitions, label):
        self.name = name
        self.transitions = transitions
        self.label = label
        self.check_results = {}
        self.seenbefore = False
        self.nb = 0

    def check_formula_result(self, formula) -> bool:
        return self.check_results[formula]
    
    def add_formula_result(self, formula, result):
        self.check_results[formula] = result

    def __str__(self) -> str:
        return self.name + ": transition:" + str(self.transitions) +" label:" + str(self.label)
 



class KS_Model:
    
    def __init__(self, json_path):
        with open(json_path, "r") as file:
            self.ks_model: list[KS_Node] = []
            model = json.loads(file.read())
            for n in model["model"]:
                node = KS_Node(n["name"], n["transitions"], n["label"])
                self.ks_model.append(node)

    def __str__(self) -> str:
        string_rep = ""
        for node in self.ks_model:
            string_rep += str(node) + "\n"
        return string_rep


test_model = KS_Model("ks.json")
print(test_model)


