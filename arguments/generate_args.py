import sys
import random
import string

def generate_random_name():
    # Generate a random name of length 9 with the last 3 characters as "{?}"
    return ''.join(random.choices(string.ascii_letters, k=6)) + "{?}"

def generate_random_sentence():
    # Generate a random prompt-like sentence of about 60 characters
    words = ["explore", "discover", "imagine", "create", "design", "build", "analyze", "develop", "innovate", "transform"]
    sentence = ' '.join(random.choices(words, k=8))
    return sentence

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <N> <filename>")
        return

    try:
        N = int(sys.argv[1])
    except ValueError:
        print("The first argument must be an integer.")
        return

    filename = sys.argv[2]
    mode = sys.argv[3]

    with open(filename, 'w') as file:
        if mode == "sentence":
            for _ in range(N):
                file.write(generate_random_sentence() + '.\n')
        else:
            for _ in range(N):
                file.write(generate_random_name() + '\n')

if __name__ == "__main__":
    main()