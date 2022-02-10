# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

from pydoc import plain
from re import L
import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'
word_list = load_words(WORDLIST_FILENAME)

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = word_list

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return(self.message_text)

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        word_list_copy = self.valid_words.copy()
        return(word_list_copy)

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        lower_case = string.ascii_lowercase*2
        upper_case = string.ascii_uppercase*2

        def shifter(alphabet):
            shift_dict = dict()
            for i in range(26):
                plain_letter = alphabet[i]
                cipher_letter = alphabet[i+shift]
                
                shift_dict[plain_letter] = cipher_letter

            return(shift_dict)

        shifted_lower_case = shifter(lower_case)
        shifted_upper_case = shifter(upper_case)
        return(shifted_lower_case | shifted_upper_case)

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        plain_message = self.message_text
        shift_dict = self.build_shift_dict(shift)

        ciphered_message = ""
        for character in plain_message:
            if character in string.ascii_letters:
                ciphered_message = ciphered_message + shift_dict[character]
            else:
                ciphered_message = ciphered_message + character
        
        return(ciphered_message)

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return(self.shift)

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        encryption_dict_copy = self.encryption_dict.copy()
        return(encryption_dict_copy)

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return(self.message_text_encrypted)

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        scores = dict()
        for i in range(26):
            score = list()
            plain_message = self.apply_shift(i)
            plain_message_copy = plain_message.split()
            
            for word in plain_message_copy:
                score.append(is_word(word_list, word))
            
            score = sum(score)
            scores[i] = [score, (i, plain_message)]
        
        best_score = 0
        best_plain = None
        for score,tuple in scores.values():
            if score > best_score:
                best_score = score
                best_plain = tuple
                
        return(best_plain)
            
        

if __name__ == '__main__':

   #Example test case (PlaintextMessage)
   plaintext = PlaintextMessage('hello there, you are a BUM!', 2)
   print('Expected Output: jgnnq vjgtg, aqw ctg c DWO!')
   print('Actual Output:', plaintext.get_message_text_encrypted())

   plain2 = PlaintextMessage("This is haha!", 2)
   plain2.change_shift(1)
   print('Expected Output: Uijt jt ibib!')
   print('Actual Output:', plain2.get_message_text_encrypted())

   #Example test case (CiphertextMessage)
   ciphertext = CiphertextMessage('jgnnq')
   print('Expected Output:', (24, 'hello'))
   print('Actual Output:', ciphertext.decrypt_message())

   cipher2 = CiphertextMessage("jgnnq vjgtg, aqw ctg c DWO!")
   print('Expected Output:', (24, 'hello there, you are a BUM!'))
   print('Actual Output:', cipher2.decrypt_message())

   cipher3 = CiphertextMessage("eat my bum!!!")
   print('Expected Output:', (0, 'eat my bum!!!'))
   print('Actual Output:', cipher3.decrypt_message())

   #Example test on story.txt
   fname = "story.txt"
   fhand = open(fname)
   story = fhand.read()
   print(story)

   encrypted_story = CiphertextMessage(story)
   print(encrypted_story.decrypt_message())