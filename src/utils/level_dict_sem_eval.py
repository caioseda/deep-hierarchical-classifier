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