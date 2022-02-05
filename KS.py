import json
from random import random



class KS_Node:

    def __init__(self, name, transitions, label):
        self.name = name
        self.transitions = transitions
        self.label: list[str] = label
        self.check_results = {}
        self.seenbefore = False
        self.nb = 0

    def check_formula_result(self, formula) -> bool:
        return self.check_results[formula[3]]
    
    def add_formula_result(self, formula, result):
        self.check_results[formula[3]] = result

    def __str__(self) -> str:
        return self.name + ": transition:" + str(self.transitions) +" label:" + str(self.label)
 

class Generated_Node:
    def __init__(self, name):
        self.name = name
        self.transitions = []
        self.label: list[str] = []

    def to_dict(self):
        return {"name": self.name, "transitions": self.transitions, "label":self.label}



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

    @staticmethod
    def generate(nb_state:int, label_list:list[str], filepath ,transition_probability:float = 0.4, label_probability: float = 0.4):
        node_list: list[Generated_Node] = []

        #generate all nodes
        for i in range(nb_state):
            node_list.append(Generated_Node("s" + str(i)))

        #generate transitions
        i = 0
        while i < nb_state:
            placed = False
            for k in range(nb_state):
                if k != i and random() > transition_probability:
                    node_list[k].transitions.append(i)
                    placed = True
            if placed:
                i += 1

        #generate labels
        i = 0
        while i < len(label_list):
            placed = False
            for k in range(nb_state):
                if random() > label_probability:
                    node_list[k].label.append(label_list[i])
                    placed = True
            if placed:
                i += 1
                    

        node_list_json = []
        for i in range(nb_state):
            node_list_json.append(node_list[i].to_dict())

        with open(filepath, "w") as file:
            json.dump({'model':node_list_json}, file)



# test_model = KS_Model("ks.json")
# print(test_model)
# KS_Model.generate(3, ["a", "b"])


