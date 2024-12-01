"""
File: writer_bot_ht.py
Name: Morya Odak
Purpose: Takes an input file from the user and creates a dictionary 
to map out which words follow each word. It then generates a new 
output based on the information in the input file. 
Course: CSC 120 SP23 001-2
"""

import sys
import random
SEED = 8
random.seed(SEED)

class Hashtable:
    """
    An instance of this class describes a 2d list where the first 
    index of each value is a n-gram and the second index is a list
    of words that follow that ngram in a certain text. 
    Methods:
    _decrement(self, hash_value)
    _hash(self, key)
    put(self, key, value)
    get(self, key)
    get_index(key)
    """
    def __init__(self, size):
        """
        Constructs a hashtable object where a list is created of the 
        size specified. 
        Parameters:
        size(int)- A number describing the size of a hashtable object.
        Returns: None
        """
        self._pairs = [None]*size
        self._size = size
    
    def _decrement(self, hash_value):
        """
        Iterates through the hashtable starting from the hash value 
        and going down until it hits an empty index. 
        Parameters: hash_value(int)- The value that a key hashes to
        Returns: hash_value(int)- The new index where a key can be placed
        at. 
        """
        while self._pairs[hash_value] != None:
            hash_value -=1
            if hash_value == -1:
                hash_value = self._size-1
        return hash_value
    
    def _hash(self, key):
        """
        Hashes a string to an integer multiples the position of each 
        character in the string by its ord value.
        Parameters: key(str)- The string that is to be hashed and 
        found an indexes for. 
        Returns: A value that represents an index in the hashtable
        """
        p = 0
        for c in key:
            p = 31*p + ord(c)
        return p % self._size

    def put(self, key, value):
        """
        Puts a key-value pair into a hashtable object by
        finding its hash value and, if necessary, using linear
        probing to reach an empty index. 
        Parameters: 
        key(str)- The string that is to be hashed and 
        found an indexes for. 
        value(str)- The string that represents the words followed
        by an ngram in a file. 
        Returns: none
        """
        hash_value = self._hash(key)
        if self._pairs[hash_value] == None:
            self._pairs[hash_value] = [key, value]
        else:
            decr_value = self._decrement(hash_value)
            self._pairs[decr_value] = [key, value]

    def get(self, key):
        """
        Gets the value that corresponds to the key specified by
        the user. 
        Parameters: key(str)- A string that represents an ngram in
        a file. 
        Returns: The value paired with the key specified. 
        """
        hash_value = self._hash(key)
        start = hash_value
        while self._pairs[hash_value][0] != key:
            if start == start+1 or self._pairs[hash_value] == None:
                start += 1
                return None
            elif self._pairs[hash_value][0] == key:
                return self._pairs[hash_value][1]
            else:
                hash_value -= 1
                if hash_value < 0:
                    hash_value = len(self._pairs) -1
        return self._pairs[hash_value][1]                

    def __contains__(self, key):
        """
        Checks if a key string is in a hashtable object. 
        Paramters: key(str)- A string that represents an ngram in
        a file. 
        Returns: none
        """
        hash_value = self._hash(key)
        if self._pairs[hash_value] is None:
            return False
        elif self._pairs[hash_value][0] == key:
            return True
        else:
            while self._pairs[hash_value] is not None \
                  and self._pairs[hash_value][0] != key:
                hash_value = hash_value -1
                if hash_value <0:
                    hash_value = self._size -1
            if self._pairs[hash_value] == None:
                return False
            else:
                return True
            
    
    def get_index(self, key):
        """
        Gets the index in self._pairs that holds key as its
        first value
        Parameters: key(str)- A string that represents an ngram in
        a file. 
        Returms: index(int)- The index where the key is located in the 
        self._pairs. 
        """
        index = self._hash(key)
        while self._pairs[index][0] != key:
            if self._pairs[index][0] == key:
                return index
            else:
                index -= 1
                if index < 0:
                    index = len(self._pairs) -1
        return index 

    def __str__(self):
        """
        Creates the string representing a hashtable object
        Parameters: none
        Returns: A string
        """
        return str(self._pairs)
    
def main():
    sfile = input()
    M = int(input())
    n = int(input())
    if n < 1:
        print("ERROR: specified prefix size is less than one")
        sys.exit(0)
    number_of_words = int(input())
    if number_of_words < 1:
        print("ERROR: specified size of the generated text is less than one")
        sys.exit(0)
    word_list = create_word_list(sfile)
    t = create_hash_table(word_list, M, n)
    tlist = create_output(t, word_list, n, number_of_words)
    print_output(tlist)

def create_word_list(sfile):
    """
    Takes a file name from the user and creats a list of all the words
    that occur in the document, punctuation included. 
    Parameters: sfile(str)- Name of a file
    Returns: word_list(list)- A list of all the words in a text file
    """
    file = open(sfile, 'r')
    word_list = []
    for line in file:
        line = line.split()
        for word in line:
            word_list.append(word)
    file.close()
    return word_list

def create_hash_table(word_list, M, n):
    """
    Creates a hashtable object and iterates through the 
    list of words in the text file, mapping each n-gram 
    to the words that follow it. 
    Paramters: 
    word_list(list)- A list containing all the words in
    a text file.
    M(int)- The number representing the size of the output
    of the program.
    n(int)- The size of each n-gram
    Returns: t(Hashtable)- An object that maps each ngram
    in a text file to the words it precedes. 
    """
    t = Hashtable(M)
    for i in range(len(word_list)):
        key = ''
        NONWORD = '@'
        if i < n:
            j = i
            while j < n:
                key += NONWORD
                j += 1
            k = i-1
            while len(key.split()) != n:
                key +=  ' ' + word_list[k]
                k += 1
        else:
            j = i-n
            while j < i:
                if len(key) == 0:
                    key += word_list[j]
                else:
                    key += ' ' + word_list[j]
                j += 1
        if key not in t:
            value = [word_list[i]]
            t.put(key, value)
        else:
            index = t.get_index(key)
            t._pairs[index][1].append(word_list[i])
    return t

def create_output(t, word_list, n, number_of_words):
    """
    Creates the randomly generated text based on the hashtable
    taken as a parameter. The generated text is then put into a list. 
    Parameters: t(Hashtable)- An object that maps each ngram
    in a text file to the words it precedes. 
    n(int)- The size of each n-gram
    word_list(list)- A list of words in a text file, 
    number_of_words(int)- The number of words that should be in the 
    generated text
    Returns: tlist(list)- A list of all the words in the output. 
    """
    tlist = []
    for i in range(n):
        tlist.append(word_list[i])
    i = 0
    while len(tlist) < number_of_words:
        curr_key = ''
        for j in range(n):
            if len(curr_key) == 0:
                curr_key += tlist[i+j]
            else:
                curr_key += ' ' + tlist[i+j]
        if len(t.get(curr_key)) == 1:
            tlist.append(t.get(curr_key)[0])
        else:
            num = random.randint(0, len(t.get(curr_key))-1)
            tlist.append(t.get(curr_key)[num])
        i +=1
    return tlist

def print_output(tlist):
    """
    Prints the output of the program, 10 words per line
    Parameters: tlist(list)- A list of all the words in the output. 
    Returns: none
    """
    for i in range(0, len(tlist), 10):
        return_string = ''
        for j in range(0, 10):
            if i+j < len(tlist):
                return_string += tlist[i+j] + ' '
        print(return_string)

            

main()