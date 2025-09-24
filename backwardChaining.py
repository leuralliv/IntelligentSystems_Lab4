class ExpertSystem:
    def __init__(self):
        self.facts = set()
        self.rules = [] 
 
    def add_fact(self, fact):
        self.facts.add(fact) 

    def add_rule(self, rule):
        self.rules.append(rule) 

    def infer_forward(self):
        new_fact_found = True
        while new_fact_found:
            new_fact_found = False
            for rule in self.rules:
                antecedent = rule['antecedent']
                consequent = rule['consequent']

                if all(condition in self.facts for condition in antecedent):
                    if consequent not in self.facts:
                        self.facts.add(consequent)
                        new_fact_found = True
                        print(f"Inferred new fact: {consequent}")

        print("\nForward inference complete. Final facts:")
        for fact in sorted(self.facts):
            print(f"- {fact}")
    

    def infer_backward(self, goal, visited=None): 
        if visited is None:
            visited = set()

        print(f"Checking goal: {goal}")

        if goal in visited:
            return 0 

        visited.add(goal)

        if goal in self.facts:
            print(f"'{goal}' is a known fact. (100%)")
            return 100

        applicable_rules = [rule for rule in self.rules if rule['consequent'] == goal]

        if not applicable_rules:
            print(f"'{goal}' is unknown. No rules conclude it. (0%)")
            return 0

        best_score = 0
        for rule in applicable_rules:
            ante_count = len(rule['antecedent'])
            if ante_count == 0:
                continue

            weight = 100 / ante_count
            score = 0

            print(f"Attempting to prove rule: IF {', '.join(rule['antecedent'])} THEN {rule['consequent']}")

            for condition in rule['antecedent']:
                condition_score = self.infer_backward(condition, visited.copy())
                if condition_score > 0: 
                    score += weight

            print(f"Rule confidence for '{goal}': {score:.2f}%")
            if score > best_score:
                best_score = score
                if best_score == 100:
                    break

        if best_score > 0:
            print(f"Adding '{goal}' with confidence {best_score:.2f}% to facts.")
            self.facts.add(goal)

        return best_score
    


if __name__ == "__main__":
    system = ExpertSystem()

    # Known Facts
    # system.add_fact("has_fur")
    system.add_fact("eats_meat")
    system.add_fact("has_tawny_color")
    system.add_fact("has_dark_spots")

    system.add_rule({
        "antecedent": ["has_fur", "eats_meat"],
        "consequent": "carnivore"
    })
    system.add_rule({
        "antecedent": ["carnivore", "has_mane", "lives_in_groups"],
        "consequent": "lion"
    })
    system.add_rule({
        "antecedent": ["has_fur", "eats_meat", "has_tawny_color", "has_dark_spots"],
        "consequent": "cheetah"
    })
    system.add_rule({
        "antecedent": ["has_fur", "eats_meat", "has_tawny_color", "has_black_stripes"],
        "consequent": "tiger"
    })
    system.add_rule({
        "antecedent": ["has_feathers", "can_fly", "lays_eggs"],
        "consequent": "bird"
    })
    system.add_rule({
        "antecedent": ["mammal"],
        "consequent": "has_fur"
    })
    system.add_rule({
        "antecedent": ["mammal", "has_hooves"],
        "consequent": "ungulate"
    })

    goal = input("Enter the animal to identify (e.g., 'cheetah'): ")
    result = system.infer_backward(goal)

    print(f"\nConclusion: The hypothesis that it is a '{goal}' is {result:.2f}%.")
    print(f"Final set of facts: {system.facts}")