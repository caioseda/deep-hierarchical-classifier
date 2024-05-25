import networkx as nx

class SemEvalHierarchy(nx.DiGraph):
    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)
        
        self.add_edge('Persuasion', "Ethos (level 1)")
        self.add_edge('Ethos (level 1)', "Ad Hominem (level 2)")
        self.add_edge('Ad Hominem (level 2)', "Ad Hominem (level 3)")
        self.add_edge('Ad Hominem (level 3)', "Name calling/Labeling")
        self.add_edge('Ad Hominem (level 3)', "Doubt")
        self.add_edge('Ad Hominem (level 3)', "Smears")
        self.add_edge('Ad Hominem (level 3)', "Reductio ad hitlerum")
        self.add_edge('Ad Hominem (level 3)', "Whataboutism | Ad Hominem (level 3)")

        self.add_edge('Ethos (level 1)', "Ethos (level 2)")
        self.add_edge('Ethos (level 2)', "Ethos (level 3)")
        self.add_edge('Ethos (level 3)', "Bandwagon | Ethos (level 3)")
        self.add_edge('Ethos (level 3)', "Appeal to authority | Ethos (level 3)")
        self.add_edge('Ethos (level 3)', "Glittering generalities (Virtue)")
        self.add_edge('Ethos (level 3)', "Transfer | Ethos (level 3)")

        self.add_edge('Persuasion', "Pathos (level 1)")
        self.add_edge('Pathos (level 1)', "Pathos (level 2)")
        self.add_edge('Pathos (level 2)', "Pathos (level 3)")
        self.add_edge('Pathos (level 3)', "Appeal to (Strong) Emotions")
        self.add_edge('Pathos (level 3)', "Exaggeration/Minimisation")
        self.add_edge('Pathos (level 3)', "Loaded Language")
        self.add_edge('Pathos (level 3)', "Flag-waving | Pathos (level 3)")
        self.add_edge('Pathos (level 3)', "Appeal to fear/prejudice | Pathos (level 3)")
        self.add_edge('Pathos (level 3)', "Transfer | Pathos (level 3)")

        self.add_edge('Persuasion', "Logos (level 1)")
        self.add_edge("Logos (level 1)", "Justification (level 2)")
        self.add_edge("Justification (level 2)", "Justification (level 3)")
        self.add_edge("Justification (level 3)", 'Bandwagon | Justification (level 3)')
        self.add_edge("Justification (level 3)", "Appeal to authority | Justification (level 3)")
        self.add_edge("Justification (level 3)", "Flag-waving | Justification (level 3)")
        self.add_edge("Justification (level 3)", "Appeal to fear/prejudice | Justification (level 3)")
        self.add_edge("Justification (level 3)", "Slogans")

        self.add_edge("Logos (level 1)", "Logos (level 2)")
        self.add_edge("Logos (level 2)", "Logos (level 3)")
        self.add_edge("Logos (level 3)", "Repetition")
        self.add_edge("Logos (level 3)", "Obfuscation, Intentional vagueness, Confusion")

        self.add_edge("Logos (level 1)", "Reasoning")
        self.add_edge('Reasoning', "Distraction")
        self.add_edge('Distraction', "Misrepresentation of Someone's Position (Straw Man)")
        self.add_edge('Distraction', "Presenting Irrelevant Data (Red Herring)")
        self.add_edge('Distraction', "Whataboutism | Distraction")

        self.add_edge('Reasoning', "Simplification")
        self.add_edge('Simplification', "Causal Oversimplification")
        self.add_edge('Simplification', "Black-and-white Fallacy/Dictatorship")
        self.add_edge('Simplification', "Thought-terminating cliché")

    def get_leaf_nodes(self):
        return [x for x in self.nodes() if self.out_degree(x)==0]
# f, subax1 = plt.subplots(1,1,  figsize=(15, 15))
# nx.draw(SemEvalHierarchy, with_labels=True, **{'node_size': 100}, ax=subax1)
    # plt.savefig("path.png")

    # plt.show()