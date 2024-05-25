import json
import os
import pandas as pd

import networkx as nx
from networkx.exception import NodeNotFound

# Run notebooks as it would run if was one folder upper in the tree, enabling direct reference to source files
import sys 
sys.path.insert(0, 'src/utils/')

from sem_eval_hierarchy import SemEvalHierarchy

WORKING_DIR = os.getcwd()

DEBUG = True

if __name__ == '__main__':
    
    label_mapping = {
        'Appeal to fear/prejudice': [
            "Appeal to fear/prejudice | Pathos (level 3)",
            "Appeal to fear/prejudice | Justification (level 3)"
            ],
        'Appeal to authority': [
            'Appeal to authority | Ethos (level 3)',
            'Appeal to authority | Justification (level 3)'
            ],
        'Whataboutism': [
            'Whataboutism | Ad Hominem (level 3)',
            'Whataboutism | Distraction'
            ],
        'Bandwagon': [
            'Bandwagon | Ethos (level 3)',
            'Bandwagon | Justification (level 3)'
            ],
        'Flag-waving': [
            'Flag-waving | Pathos (level 3)',
            'Flag-waving | Justification (level 3)'
            ],
        'Transfer': [
            'Transfer | Ethos (level 3)',
            'Transfer | Pathos (level 3)'
        ]
    }
    
    hierarchy = SemEvalHierarchy()
    
    leaf_nodes = hierarchy.get_leaf_nodes()
    # Getting the root name only, removing suffix
    leaf_nodes = {leaf.split('|')[0].strip() for leaf in leaf_nodes}
    

    files_to_process = [
        '/data/semeval/train_labels.json', 
        '/data/semeval/validation_labels.json'
        ]
    
    for file in files_to_process:
        with open(WORKING_DIR + file, 'r') as f:
            json_file = json.load(f)

            discarted_labels = []
            used_labels = []
            for row in json_file:
                new_labels = []
                for label in row['labels']:
                    if label in leaf_nodes:
                        if label in list(label_mapping.keys()):
                            new_labels += label_mapping[label]
                        else:
                            new_labels += [label]
                    else: 
                        discarted_labels.append(label)
                row['labels'] = new_labels
                used_labels += new_labels
            if DEBUG: print(f'Discarted Labels: {set(discarted_labels)}\n')
            if DEBUG: print(f'Used Labels: {set(used_labels)}\n')
            print(f'{file} labels refactored.')

        file_wo_extension = file.split('.')[0]
        with open(WORKING_DIR + file_wo_extension + '_refactor.json', 'a') as f:
            json.dump(json_file, f)