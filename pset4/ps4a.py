# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    if len(sequence) == 1:
        return sequence

    permutations=[]

    first_char = sequence[0]
    sub_sequence = get_permutations(sequence[1:])
    for word in sub_sequence:
        for i in range(len(word)+1):
            word_to_list = list(word)
            word_to_list.insert(i,first_char)
            new_word=''.join(word_to_list)
            permutations.append(new_word)
    return permutations

if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))

#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a
#    sequence of length n)

    example_input = 'cde'
    print('Input:', example_input)
    print('Expected Output:', ['cde', 'dce', 'dec', 'ced', 'ecd', 'edc'])
    print('Actual Output:', get_permutations(example_input))
