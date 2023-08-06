grammar = {
    'S': [['a', 'B'], ['b', 'S'], ['c']],
    'B': [['d'], ['e']]
}

first_sets = compute_first(grammar)
print(first_sets)