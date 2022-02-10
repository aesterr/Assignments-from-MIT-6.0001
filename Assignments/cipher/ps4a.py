# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx


### Defining get_permutations()
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
        return(list(sequence))
    else:
        hold = sequence[0]
        string = sequence[1:]
        
        x = get_permutations(string)
        perms = list()
        for subpart in x:
            for i in range(len(subpart) + 1):
                word = subpart[:i] + hold + subpart[i:]
                perms.append(word)

        return(list(set(perms)))
        
### Testing get_permutations()
if __name__ == '__main__':

    test1 = 'abc'
    print('Input:', test1)
    expected1 = ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
    print('Expected Output:', expected1)
    print('Actual Output:', get_permutations(test1))
    success1 = set(expected1) == set(get_permutations(test1))

    test2 = "aac"
    print("Input:", test2)
    expected2 = ["aac", "aca", "caa"]
    print("Expected Output:", expected2)
    print("Actual Output:", get_permutations(test2))
    success2 = set(expected2) == set(get_permutations(test2))

    test3 = "aaa"
    print("Input:", test3)
    expected3 = ["aaa"]
    print("Expected Output:", expected3)
    print("Actual Output:", get_permutations(test3))
    success3 = set(expected3) == set(get_permutations(test3))

    if (success1 and success2 and success3) == True:
        print("Success")