import numpy as np
from scipy.io.wavfile import write

def generate(sentence,filename="morse.wav",unit_length=0.1,f=440.0,volume=0.5,fs=44100,data=None):
    """
    sentence:       string of .'s and -'s
    filename:       string of file name for wav file to be saved as
    unit_length:    length of dot in seconds
    f:              sine frequency,Hz,may be float
    volume:         range [0.0,1.0]
    fs:             sampling rate,Hz,must be integer
    """
    dot = np.sin(2*np.pi*np.arange(fs*unit_length)*f/fs)
    dash = np.sin(2*np.pi*np.arange(fs*unit_length*3)*f/fs)
    space = np.zeros(int(fs*unit_length))
    letter_space = np.zeros(int(fs*unit_length*3))
    #word_space = np.zeros(int(fs*unit_length*7))
    data = space

    def add(data,symbol,multi=0):
        for i in range(1): data = np.concatenate((data,symbol))
        return data

    for letter in sentence:
        if letter == ".": data = add(data,dot)
        if letter == "-": data = add(data,dash)
        if letter == " ": data = add(data,letter_space)

        data = add(data,space)
    
    data *= volume
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)

    write('morse.wav', fs, scaled)

def ascii_to_morse(text):
    """
    text: a string of ascii characters to be converted into morse
    """
    morse = {
    "A":".-","B":"-...","C":"-.-.","D":"-..","E":".","F":"..-.",
    "G":"--.","H":"....","I":"..","J":".---","K":"-.-","L":".-..",
    "M":"--","N":"-.","O":"---","P":".--.","Q":"--.-","R":".-.",
    "S":"...","T":"-","U":"..-","V":"...-","W":".--","X":"-..-",
    "Y":"-.--","Z":"--..","1":".----","2":"..---","3":"...--",
    "4":"....-","5":".....","6":"-....","7":"--...","8":"---..",
     "9":"----.","0":"-----",".":".-.-.-",",":"--..--","?":"..--..",
     "/":"-..-.","@":".--.-."
    }

    letters = morse.keys()
    result = ""

    for letter in text.upper():
        if letter in letters: result += morse[letter] + " "
        elif letter == " ": result += "  "

    return result

if __name__ == "__main__":
    morse = ascii_to_morse("this is a test")
    generate(morse)
