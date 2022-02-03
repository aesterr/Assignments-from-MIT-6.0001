# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    if len(secret_word) == 0:
      return(True)
    elif secret_word[0] not in letters_guessed:
      return(False)
    else:
      return(is_word_guessed(secret_word[1:], letters_guessed))





def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    secret_letters = list(secret_word)
    filled = ""

    for letter in secret_letters:
      if letter in letters_guessed:
        filled += " " + letter
      else: 
        filled += " _"

    return(filled)




def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = string.ascii_lowercase

    guessed = dict()
    for letter in letters_guessed:
      guessed[letter] = ""
    
    return(alphabet.translate(str.maketrans(guessed)))

    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    warnings = 3
    num_guesses = 6
    letters_guessed = list()
    vowels = "aeiou"

    total_score = 0
    won = False

    print("Welcome to the game Hangman!" + "\n" 
    + "I am thinking of a word " + str(len(secret_word)) + " letters long." + "\n" 
    + "You have " + str(warnings) + " warnings left.")
    print("---------------------------------------")
    
    while num_guesses > 0:
      print("You have " + str(num_guesses) + " guesses left." + "\n" 
      + "Available letters: " + get_available_letters(letters_guessed))
      guess = input("Please guess a letter: ")
      guess = guess.lower()

      if guess not in string.ascii_lowercase:
        if warnings == 0:
          num_guesses -= 1
          print("Oops! That is not a valid letter. You have no warnings left so you lose one guess: " + get_guessed_word(secret_word, letters_guessed)+ "\n" 
        + "---------------------------------------")
        else:
          warnings -= 1
          print("Oops! That is not a valid letter. You have " + str(warnings) + " warnings left: " + get_guessed_word(secret_word, letters_guessed) + "\n" 
          + "---------------------------------------")
      elif guess in letters_guessed:
        if warnings == 0:
          num_guesses -= 1
          print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess: " + get_guessed_word(secret_word, letters_guessed)+ "\n" 
        + "---------------------------------------")
        else:
          warnings -= 1
          print("Oops! You've already guessed that letter. You have " + str(warnings) + " warnings left: " + get_guessed_word(secret_word, letters_guessed) + "\n" 
          + "---------------------------------------")
      else:
        letters_guessed.append(guess)

        if guess in secret_word:
          print("Good guess: " + get_guessed_word(secret_word, letters_guessed) + "\n" 
        + "---------------------------------------")
        else:
          print("Oops! That letter is not in my word." + "\n"
          + "Please guess a letter: " + get_guessed_word(secret_word, letters_guessed) + "\n" 
        + "---------------------------------------")

          if guess in vowels:
            num_guesses -= 2
          else:
            num_guesses -= 1
        
        if is_word_guessed(secret_word, letters_guessed) == True:
          won = True
          total_score = num_guesses * len(set(secret_word))
          print("Congratulations, you won!" + "\n"
          + "Your total score for this game is: " + str(total_score))
          break

    if won == False:
      print("Sorry, you ran out of guesses. The word was " + "'" + secret_word + "'.")



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace(" ", "")
    if len(my_word) == len(other_word):
      if len(my_word) == 0:
        return(True)
      elif my_word[0] == "_" or my_word[0] == other_word[0]:
        return(match_with_gaps(my_word[1:], other_word[1:]))
      else:
        return(False)



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    list_of_matches = list()
    my_word = my_word.replace(" ", "")
    
    for word in wordlist:
      if len(word) == len(my_word):
        if match_with_gaps(my_word, word) == True:
          list_of_matches.append(word)
        else:
          continue

    if len(list_of_matches) == 0:
        return("No matches found.")
    else:
        return(list_of_matches)



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    warnings = 3
    num_guesses = 6
    letters_guessed = list()
    vowels = "aeiou"

    total_score = 0
    won = False

    print("Welcome to the game Hangman!" + "\n" 
    + "I am thinking of a word " + str(len(secret_word)) + " letters long." + "\n" 
    + "You have " + str(warnings) + " warnings left.")
    print("---------------------------------------")
    
    while num_guesses > 0:
      print("You have " + str(num_guesses) + " guesses left." + "\n" 
      + "Available letters: " + get_available_letters(letters_guessed))
      guess = input("Please guess a letter: ")
      guess = guess.lower()

      if guess == "*":
        print("Possible word matches are:")
        print(show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
        print("---------------------------------------")

      elif guess not in string.ascii_lowercase:
        if warnings == 0:
          num_guesses -= 1
          print("Oops! That is not a valid letter. You have no warnings left so you lose one guess: " + get_guessed_word(secret_word, letters_guessed)+ "\n" 
        + "---------------------------------------")
        else:
          warnings -= 1
          print("Oops! That is not a valid letter. You have " + str(warnings) + " warnings left: " + get_guessed_word(secret_word, letters_guessed) + "\n" 
          + "---------------------------------------")

      elif guess in letters_guessed:
        if warnings == 0:
          num_guesses -= 1
          print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess: " + get_guessed_word(secret_word, letters_guessed)+ "\n" 
        + "---------------------------------------")
        else:
          warnings -= 1
          print("Oops! You've already guessed that letter. You have " + str(warnings) + " warnings left: " + get_guessed_word(secret_word, letters_guessed) + "\n" 
          + "---------------------------------------")
          
      else:
        letters_guessed.append(guess)

        if guess in secret_word:
          print("Good guess: " + get_guessed_word(secret_word, letters_guessed) + "\n" 
        + "---------------------------------------")
        else:
          print("Oops! That letter is not in my word." + "\n"
          + "Please guess a letter: " + get_guessed_word(secret_word, letters_guessed) + "\n" 
        + "---------------------------------------")

          if guess in vowels:
            num_guesses -= 2
          else:
            num_guesses -= 1
        
        if is_word_guessed(secret_word, letters_guessed) == True:
          won = True
          total_score = num_guesses * len(set(secret_word))
          print("Congratulations, you won!" + "\n"
          + "Your total score for this game is: " + str(total_score))
          break

    if won == False:
      print("Sorry, you ran out of guesses. The word was " + "'" + secret_word + "'.")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)