from random import randint
from os import mkdir
import os.path

if __name__ == '__main__':
    if not os.path.isdir('input'):
        mkdir('input')

    for k in range(10):
        sequence = list()
        for i in range(100):
            job = [randint(0, 3), randint(1, 8)]
            if sequence:
                job[0] += sequence[i - 1][0]
            sequence.append(job)
        sequence = [item for sublist in sequence for item in sublist]
        with open(f'input/{k}.txt', 'w') as inputfile:
            inputfile.write(' '.join(map(str, sequence)))
