from sys import argv


def read_output(filename):
    response = dict()
    with open(filename, 'r') as outfile:
        lines = outfile.readlines()
        response['inputs'] = len(lines)
        response['width'] = len(lines[0].split(' '))
        response['output'] = map(lambda x: x.strip(), ' '.join(lines).split(' '))
    return response


if __name__ == '__main__':
    argv.pop(0)
    bodies = dict()
    for filename in argv:
        bodies[filename] = read_output(filename)
    output = (bodies[argv[0]]['output'],
              bodies[argv[1]]['output'])
    line = 0
    column = int()
    for i, (yours, mine) in enumerate(zip(*output)):
        column = i % bodies[argv[0]]['width']
        if column == 0:
            line += 1
        if float(yours) != float(mine):
            print(f'failed: {yours} != {mine}, line {line} column {column}')
            exit(1)
    print('passed')
