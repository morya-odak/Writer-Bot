"""
File: writer_bot.py
Name: Morya Odak
Purpose: Takes an input file from the user and creates a dictionary 
to map out which words follow each word. It then generates a new 
output based on the information in the input file. 
Course: CSC 120 SP23 001-2
"""
import random
SEED = 8
random.seed(SEED)
    
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

def create_dict(word_list, n):
    """
    Creates a dictionary that maps which words succeed each word. 
    Parameters: word_list(list)- A list of words in a text file, 
    n(int)- A number that determines the size of the keys in the 
    dictionary. 
    Returns: dict(dictionary)- A dictionary that maps which words
    are next to which words in a text file. 
    """
    dict = {}
    NONWORD = ' '
    for i in range(len(word_list)):
        key = ()
        if i < n:
            j = i
            while j < n:
                key += (NONWORD,)
                j += 1
            k = i-1
            while len(key) != n:
                key += (word_list[k],)
                k += 1
        else:
            j = i-n
            while j < i:
                key += (word_list[j],)
                j+=1
        if key not in dict.keys():
            dict[key] = []
        dict[key].append(word_list[i])
    return dict

def create_output(dict, word_list, number_of_words, n):
    """
    Creates the randomly generated text based on the dictionary
    taken as a parameter. The generated text is then put into a list. 
    Parameters: dict(dictionary)- A dictionary that maps which words
    are next to which words in a text file. 
    n(int)- A number that determines the size of the keys in the 
    dictionary,
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
        curr_key = ()
        for j in range(n):
            curr_key += (tlist[i+j],)
        if len(dict[curr_key]) == 1:
            tlist.append(dict[curr_key][0])
        else:
            num = random.randint(0, len(dict[curr_key])-1)
            tlist.append(dict[curr_key][num])
        i+=1
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

def main():
    sfile = input()
    n = int(input())
    number_of_words = int(input())
    word_list = create_word_list(sfile)
    dict = create_dict(word_list, n)
    print(dict)
    tlist = create_output(dict, word_list, number_of_words, n)
    print_output(tlist)
    

main()