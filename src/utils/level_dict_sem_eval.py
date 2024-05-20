'''Dictionary for SemEval hierarchy.
'''

hierarchy = {
    'Persuasion':{
        'Ethos (level 1)':{
            'Ad Hominem (level 2)':{
                'Ad Hominem (level 3)':{
                    'Name Calling': {},
                    'Doubt': {},
                    'Smears': {},
                    'Reductio ad Hitlerum': {},
                    'Whataboutism - Ad Hominem (level 3)': {},

                }
            },
            'Ethos (level 2)':{
                'Ethos (level 3)':{
                    'Bandwagon - Ethos (level 3)':{},
                    'Appeal to Authority - Ethos (level 3)':{},
                    'Glittering Generalities':{},
                    'Transfer - Ethos (level 3)':{},
                }
            }
        },
        'Pathos (level 1)':{
            'Pathos (level 2)':{
                'Pathos (level 3)':{
                    'Appeal to Emotion (Visual)': {},
                    'Exaggeration': {},
                    'Loaded Language': {},
                    'Flag Waving - Pathos (level 3)': {},
                    'Appeal to Fear - Pathos (level 3)': {},
                    'Transfer - Pathos (level 3)': {},
                }
            }
        },
        'Logos (level 1)':{
            'Justification (level 2)':{
                'Justification (level 3)':{
                    'Bandwagon - Justification (level 3)': {},
                    'Appeal to Authority - Justification (level 3)': {},
                    'Flag Waving - Justification (level 3)': {},
                    'Appeal to Fear - Justification (level 3)': {},
                    'Slogans': {},
                }
            },
            'Logos (level 2)':{
                'Logos (level 3)':{
                    'Repetition': {},
                    'Intentional Vagueness': {}
                }
            },
            'Reasoning':{
                'Distraction':{
                    'Straw Man': {},
                    'Red Herring': {},
                    'Whataboutism - Distraction': {},
                },
                'Simplification':{
                    'Causal Oversimplification': {},
                    'Black & White Fallacy': {},
                    'Thought Termination Cliché': {},
                }
            }
        }
    }
}

    
def check_relation_in_hierarchy(tree, parent, child, level = 0, debug = False) -> bool:
    '''
    Checks if parent and child have a relation in a giver hierarchy. 

    tree: dict - Hierarchy represented in nested dicts where the value represents the name of the node and value
                 its children. If a node its a leaf, them the value should be a empty dict.
    
    parent: str - String representing the parent node.

    child: str - String representing the child node.

    level: int - The level that the hierarchy is. (This argument can be removed)

    deug: bool - Whether to print the search process or not
    '''
    has_relation = False
    children = tree.keys()
    for node in children:
        subtree = tree[node]
        subtree_children = list(subtree.keys())
        
        if debug:
            print(f'# (level {level})')
            print(f'Parent: {node}')
            print(f'Childs: {subtree_children}\n')

        if node == parent:
            return child in subtree_children
        else:
            has_relation = check_relation_in_hierarchy(subtree, parent, child, level=level+1)
        
    return has_relation

relation = check_relation_in_hierarchy(
    hierarchy,
    parent='Reasoning',
    child='Distraction'
)

print(relation)