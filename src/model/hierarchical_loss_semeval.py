
'''Hierarchical Loss Network
'''

import pickle
import torch
import torch.nn as nn
from src.utils.helper import read_meta
from pprint import pprint
from typing import Generator


class HierarchicalLossNetwork:
    # TODO: 
    #   Apesar de da lógica da classe e seus métodos ter sido adaptada para atender as demandas do SemEval,
    #   tudo foi desenvolvido utilizando apenas Python. Devemos adaptar para utilizar tensores do PyTorch.
    #   Essa abordagem não foi realizada logo de início pois foi realizada antes de construirmos um 
    #   DataLoader para o dataset do SemEval.

    def __init__(self, hierarchical_labels, device='cpu', total_level=2, alpha=1, beta=0.8, p_loss=3):
        '''Param init.
        '''
        self.total_level = total_level
        self.alpha = alpha
        self.beta = beta
        self.p_loss = p_loss
        self.device = device
        
        self.class_labels_by_level = self.get_class_labels_by_level(hierarchical_labels)

        self.hierarchical_labels = hierarchical_labels
        self.hierarchical_index = self.convert_hierarchy_to_integers(hierarchical_labels)

        self.children_by_index = self.get_children_by_index(self.hierarchical_index)
        self.children_by_label = self.get_children_by_index(self.hierarchical_labels)

        

    def get_class_labels_by_level(self, hierarchy_labels, debug=False):
        '''
        Returns a list that each index is a list with unique labels for that level.
        '''
        classes_names_by_level = []
        for node, children, depth in self.iterate_hierarchy(hierarchy_labels, debug=debug):
            while len(classes_names_by_level) <= depth:
                classes_names_by_level.append([])
            classes_names_by_level[depth].append(node)
        return classes_names_by_level

    def convert_hierarchy_to_integers(self, tree, level=0, counter=None):
        '''
        Converts the class names in the hierarchy to integers, starting from 0 at each level, with unique values within each sibling set.

        tree: dict - Hierarchy represented in nested dicts.
        level: int - Current level in the hierarchy (used for recursion).

        Returns a new hierarchy with the class names replaced by integers.
        '''
        hierarchy_integers = {}
        for key in tree.keys():
            new_index = self.class_labels_by_level[level].index(key)
            
            if tree[key]:
                hierarchy_integers[new_index] = self.convert_hierarchy_to_integers(tree[key], level=level+1)
            else:
                hierarchy_integers[new_index] = {}
        return hierarchy_integers
    
    def iterate_hierarchy(self, tree: dict, depth: int = 0, debug: bool = False) -> Generator[dict, dict, int]:
        '''
        A generator function that iterates through the hierarchy.

        tree: dict - Hierarchy represented in nested dicts.
        
        depth: int - Current depth in the hierarchy.

        debug: bool - Whether to print the search process or not.
        '''

        for parent, children in tree.items():
            if debug:
                print(f'Visiting node: {parent} at depth {depth} with children: {list(children.keys())}')
            yield parent, children, depth
            # Recursively iterate through the children
            for child in self.iterate_hierarchy(children, depth + 1, debug):
                yield child

    def get_children_by_index(self, tree: dict, debug=False):
        '''
            Retrieves the children of each node in the hierarchy and returns them as a dictionary
            where the keys are the node indices and the values are lists of children indices.

            Parameters:
            tree (dict): The hierarchy represented as nested dictionaries. Each key is a node,
                        and its value is another dictionary representing its children. If a node
                        is a leaf, its value should be an empty dictionary.
            debug (bool): Optional; default is False. If True, debug information about the
                        iteration process will be printed.

            Returns:
            dict: A dictionary where the keys are node indices (integers) and the values are lists
                of their respective children indices (integers). Leaf nodes will have empty lists
                as their values.
        '''
        children_by_index = {}
        for node, children, depth in self.iterate_hierarchy(tree, debug=debug):
            if children:
                children_by_index[node] = list(children.keys())
            else: 
                children_by_index[node] = []
        return children_by_index

    def check_hierarchy(self, parent: str, child: str, hierarchy_representation='index',) -> bool:
        '''
        Checks if the predicted class at level l is a child of the class predicted at level l-1 for the entire batch.

        Parameters:
        parent (str): A string representing the parent node(s). This can be a single parent node or a batch of parent nodes.
        child (str): A string representing the child node(s). This can be a single child node or a batch of child nodes.
        hierarchy_representation (str): The representation of the hierarchy to use. Valid options are 'index' or 'label'.
                                        'index' refers to hierarchical levels represented by integers.
                                        'label' refers to hierarchical levels represented by their original names/labels.
                                        Default is 'index'.

        Returns:
        list: A list of boolean values where each boolean indicates whether the corresponding child node is a child of the parent node.
        '''
        if hierarchy_representation == 'index':
            children_by_representation = self.children_by_index
        elif hierarchy_representation == 'label':
            children_by_representation = self.children_by_label
        else:
            raise Exception('hierarchy_representation valid options are "index" or "label".')

        is_children = [child_i in children_by_representation[parent_i] for i, (parent_i, child_i) in enumerate(zip(parent, child))]
        return is_children

    def label_to_index(self, class_label_by_level):
        # TODO
        class_index_by_level = []
        
        count = 0
        for i, level in enumerate(class_label_by_level):
            class_index_by_level.append([])
            for j in range(count, count + len(level)):
                class_index_by_level[i].append(j)

        return class_index_by_level
    
    def calculate_lloss(self, predictions, true_labels):
        '''Calculates the layer loss.
        '''
        # TODO: Implement Layer Loss for multi-level hierarchy
        pass

    def calculate_dloss(self, predictions, true_labels):
        '''Calculate the dependence loss.
        '''
        # TODO: Implement Dependency Loss for multi-level hierarchy
        pass