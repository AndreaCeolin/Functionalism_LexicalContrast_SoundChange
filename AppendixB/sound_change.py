#!/usr/bin/env python3

import random
import sys
import matplotlib.pyplot as plt
import numpy as np


'''
1. ALPHABET and LEXICON

This part defines the alphabet of the language, and maps symbols to indexes.

The vowel dictionary maps 15 different symbols onto different indexes.
The consonant dictionary maps 26 different symbols onto different indexes.
'''

vowels = {'i': 0, 'e': 1, 'a': 2, 'o': 3, 'u': 4, 'ou':5, 'ei':6, 'ea':7, 'ee':8, 'oo':9, 'ai':10, 'oa':11,
          'oi':12, 'io':13, 'ie':14}


consonants = {'m': 0, 'p':1, 'b':2, 'f': 3, 'v': 4, 'd': 5, 't': 6, 'l': 7, 'n': 8, 'r': 9, 's': 10, 'k': 11,
              'y': 12, 'g': 13, 'j':14, 'h': 15, 'c':16, ' ':17, 'th':18, 'sh':19, 'wh':20, 'ch':21, 'tw':22,
              'x':23, 'w':24, 'z':25}

'''
With this dictionary, we can represent each word as an integer tuple. Words are initially read from a text file
in the form of 3-dimensional tuples of the type (onset, nucleus, coda). For instance the word "dog" will be 
processed in the form of a 3-dimensional tuple ('d', 'o', 'g'). Then, we can use the two dictionaries to transform 
each word into a integer vector, through a helper function, for computation purposes. The word "dog" will be 
transformed in the tuple (5, 3, 13).
'''

dog = ('d', 'o', 'g')

def vectorize(word):
    onset, nucleus, coda = word
    return consonants[onset], vowels[nucleus], consonants[coda]

print(vectorize(dog))


'''
The lexicon is a list of words (tuples), and is stored as a global variable, since we need to modify it as sound change
occurs. A wordlist containing the words "dog", "cat", and "pig" will be a represented by the following variable:
'''

wordlist = [('d', 'o', 'g'), ('c', 'a', 't'), ('p', 'i', 'g')]

'''
Since we want to keep track of the number of symbols and the possible environments, we also store three sets that
contain the onsets, nuclei and codas available in the lexicon in its current state. These three sets are all 
global variables.
'''

def get_onset(wordlist):
    return {word[0] for word in wordlist}

def get_nucleus(wordlist):
    return {word[1] for word in wordlist}

def get_coda(wordlist):
    return {word[2] for word in wordlist}


onset, nucleus, coda = get_onset(wordlist), get_nucleus(wordlist), get_coda(wordlist)

print(onset)
print(nucleus)
print(coda)


'''
For illustratory purposes, we need a reverse-dictionary, which can be used to retrieve the symbols given their index,
and a helper function to retrieve the word (in string format) given its integer vector representation:
'''

rev_vowels = {code: letter for letter, code in vowels.items()}
rev_consonants = {code: letter for letter, code in consonants.items()}


dog = (5, 3, 13)

def vectorize_inverse(word):
    onset, nucleus, coda = word
    return rev_consonants[onset] + rev_vowels[nucleus] + rev_consonants[coda]

print(vectorize_inverse(dog))


'''
Another helper function that we need is a function that returns the average Levenshtein distance within a wordlist:
'''

def average(wordlist):
    av_length = []
    for index, word in enumerate(wordlist):
        for word2 in wordlist[index+1:]:
            lev = 0
            for i, letter in enumerate(word):
                if word2[i] != letter:
                    lev += 1
            av_length.append(lev)
    return sum(av_length)/len(av_length)


print(average(wordlist))


'''
2. SOUND CHANGE FUNCTIONS

This part defines the sound change functions. These functions modify the lexicon by applying sound changes.
The first function represents a sound change that targets the onset of the word.
'''

def change_onset():
    #call the lexicon list and the onset set
    global lexicon, onset
    #prepare a new empty list, that will be filled with the form of the words after the sound change apply
    new_lexicon = []
    #determine an index for the onset (this represents place of articulation)
    i = random.choice(range(len(rev_consonants)-1))
    #Here we pick two adjacent phonemes. merg_2 is the outcome of the merger.
    merg_1, merg_2 = random.sample(sorted(list(rev_consonants))[i:i+2], 2)
    #determine the boundary of the conditioning environment (the nucleus)
    threshold = random.choice(list(rev_vowels))
    #if we are merging to a back consonant (higher index), the conditioning environment is back vowels
    if merg_1 < merg_2:
        environment = [phoneme for phoneme in nucleus if phoneme >= threshold]
    #if we are merging to a front consonant (lower index), the conditioning environment is front vowels
    else:
        environment = [phoneme for phoneme in nucleus if phoneme <= threshold]
    for word in lexicon:
        #check if the onset and the environment are relevant for the merger
        if word[0] == merg_1 and word[1] in environment:
                new_lexicon.append((merg_2, word[1], word[2]))
        else:
            new_lexicon.append(word)
    #this prints a line describing the change that happened
    print('/' + rev_consonants[merg_1] + '/ becomes /' + rev_consonants[merg_2] + '/ in onset before ['
          + ' '.join([rev_vowels[index] for index in environment]) + ']')
    #Update lexicon and onsets
    lexicon = new_lexicon
    onset = get_onset(lexicon)

'''
The following two functions will apply a change to the nucleus. The only difference between the two is whether
the conditioning environment is the onset or the coda.
'''

def change_nucleus():
    # call the lexicon list and the nucleus set
    global lexicon, nucleus
    #prepare a new empty list, that will be filled with the form of the words after the sound change apply
    new_lexicon = []
    #determine an index for the nucleus (this represents place of articulation)
    i = random.choice(range(len(rev_vowels)-1))
    #Here we pick two adjacent phonemes. merg_2 is the outcome of the merger.
    merg_1, merg_2 = random.sample(sorted(list(rev_vowels))[i:i+2], 2)
    #determine the boundary of the conditioning environment (the onset)
    threshold = random.choice(list(rev_consonants))
    #if we are merging to a back vowel (high index), the conditioning environment is back consonants
    if merg_1 < merg_2:
        environment = [phoneme for phoneme in onset if phoneme >= threshold]
    #if we are merging to a front vowel (lower index), the conditioning environment is front consonants
    else:
        environment = [phoneme for phoneme in onset if phoneme <= threshold]
    for word in lexicon:
        #check if the nucleus and the environment are relevant for the merger
        if word[0] in environment and word[1] == merg_1:
                new_lexicon.append((word[0], merg_2, word[2]))
        else:
            new_lexicon.append(word)
    #this prints a line describing the change that happened
    print('/' + rev_vowels[merg_1] + '/ becomes /' + rev_vowels[merg_2] + '/ after ['
          + ' '.join([rev_consonants[index] for index in environment]) + ']')
    #Update lexicon and nuclei
    lexicon = new_lexicon
    nucleus = get_nucleus(lexicon)

def change_nucleus2():
    # call the lexicon list and the nucleus set
    global lexicon, nucleus
    #prepare a new empty list, that will be filled with the form of the words after the sound change apply
    new_lexicon = []
    #determine an index for the nucleus (this represents place of articulation)
    i = random.choice(range(len(rev_vowels)-1))
    #Here we pick two adjacent phonemes. merg_2 is the outcome of the merger.
    merg_1, merg_2 = random.sample(sorted(list(rev_vowels))[i:i+2], 2)
    #determine the boundary of the conditioning environment (the onset)
    threshold = random.choice(list(rev_consonants))
    #if we are merging to a back vowel (high index), the conditioning environment is back consonants
    if merg_1 < merg_2:
        environment = [phoneme for phoneme in coda if phoneme >= threshold]
    #if we are merging to a front vowel (lower index), the conditioning environment is front consonants
    else:
        environment = [phoneme for phoneme in coda if phoneme <= threshold]
    for word in lexicon:
        #check if the nucleus and the environment are relevant for the merger
        if word[2] in environment and word[1] == merg_1:
                new_lexicon.append((word[0], merg_2, word[2]))
        else:
            new_lexicon.append(word)
    #this prints a line describing the change that happened
    print('/' + rev_vowels[merg_1] + '/ becomes /' + rev_vowels[merg_2] + '/ before ['
          + ' '.join([rev_consonants[index] for index in environment]) + ']')
    #Update lexicon and nuclei
    lexicon = new_lexicon
    nucleus = get_nucleus(lexicon)

'''
Finally, this function changes the coda consonant.
'''


def change_coda():
    #call the lexicon list and the coda set
    global lexicon, coda
    #prepare a new empty list, that will be filled with the form of the words after the sound change apply
    new_lexicon = []
    #determine an index for the coda (this represents place of articulation)
    i = random.choice(range(len(rev_consonants)-1))
    #Here we pick two adjacent phonemes. merg_2 is the outcome of the merger.
    merg_1, merg_2 = random.sample(sorted(list(rev_consonants))[i:i+2], 2)
    #determine the boundary of the conditioning environment (the nucleus)
    threshold = random.choice(list(rev_vowels))
    #if we are merging to a back consonant (higher index), the conditioning environment is back vowels
    if merg_1 < merg_2:
        environment = [phoneme for phoneme in nucleus if phoneme >= threshold]
    #if we are merging to a front consonant (lower index), the conditioning environment is front vowels
    else:
        environment = [phoneme for phoneme in nucleus if phoneme <= threshold]
    for word in lexicon:
        #check if the coda and the environment are relevant for the merger
        if word[2] == merg_1 and word[1] in environment:
                new_lexicon.append((word[0], word[1], merg_2))
        else:
            new_lexicon.append(word)
    #this prints a line describing the change that happened
    print('/' + rev_consonants[merg_1] + '/ becomes /' + rev_consonants[merg_2] + '/ in coda after ['
          + ' '.join([rev_vowels[index] for index in environment]) + ']')
    #Update lexicon and codas
    lexicon = new_lexicon
    coda = get_coda(lexicon)


'''
3. THE SOUND CHANGE SIMULATIONS

The following function initiates the sound change simulations and prints the graphs presented in the chapter.
The functions takes three arguments: the name of the file containing the wordlist, the number of changes, and the
number of simulations.
'''


def main(file, n_changes, iterations):
    for i in range(int(iterations)):
        print('#######Language Change is happening!')
        global onset, nucleus, coda, lexicon
        #the initial lexicon is read from a text file. Onsets, nuclei and codas are separated by a '-'
        initial_lexicon = [element.strip('\n').split('-') for element in open(file)]
        #this line loads the lexicon in the format described above: a list of integer tuples
        lexicon = [(consonants[word[0]], vowels[word[1]], consonants[word[2]]) for word in initial_lexicon]
        #this line gets the onset, nucleus, and coda sets
        onset, nucleus, coda = get_onset(lexicon), get_nucleus(lexicon), get_coda(lexicon)
        #this line will be used to define the sound change functions used in the simulation and their weight
        #with this setting, each function is equally weighted
        functions = [change_onset, change_nucleus, change_nucleus2, change_coda]
        #we initialize lists that will keep track of the number of the iteration, the number of the phonemes,
        #and the average distance
        x_axis = [0]
        phonemes = [len(onset.union(coda)) + len(nucleus)]
        av_length = [average(lexicon)]
        for n in range(int(n_changes)):
            #this line selects a sound change function at random and applies it
            random.choice(functions)()
            #This is needed to make the plot lighter. For the toy example in Figure 2.2, '500' has been reduced to '1'
            if n % 500 == 0:
                #we update the lists that keep track of the number of the iteration, the number of the phonemes, and the
                #average distance
                x_axis.append(n+1)
                phonemes.append(len(onset.union(coda)) + len(nucleus))
                av_length.append(average(lexicon))
                #this loop prints the shape of the lexicon at the beginning of the simulation and after the
                #sound changes applied
                for index, word in enumerate(lexicon):
                    print(''.join(initial_lexicon[index]) + '->' + ''.join(rev_consonants[word[0]] + rev_vowels[word[1]] + rev_consonants[word[2]]))
            print('#######Language Change is finished!')
            print('###################################!')
        #After the simulation has ended, we plot the change in the number of phonemes and in the average distance
        #during the simulation
        #plot phoneme size
        plt.subplot(1, 2, 1)
        plt.plot(x_axis, phonemes)
        #plt.xticks(np.arange(1, 4, step=1)) #This is for the toy example in Figure 2.2
        #plt.yticks(np.arange(36, 39, step=1)) #This is for the toy example in Figure 2.2
        plt.title('Number of Phonemes')
        plt.xlabel('Iterations')
        plt.ylabel('Counts')
        #plot av_length
        plt.subplot(1, 2, 2)
        plt.plot(x_axis, av_length)
        #plt.xticks(np.arange(1, 4, step=1))  #This is for the toy example in Figure 2.2
        plt.title('Average Levenshtein Distance')
        plt.xlabel('Iterations')
        plt.ylabel('Counts')
    plt.show()


if __name__ == "__main__":
    print('###################################!')
    main(sys.argv[1], sys.argv[2], sys.argv[3])


