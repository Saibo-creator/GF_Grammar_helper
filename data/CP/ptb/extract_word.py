import re
import argparse

def extract_words(line):
    word_list = re.findall(r'\(\w+\s+([^()]+)', line)
    return word_list

def extract_and_save_words(input_file, output_file):
    with open(input_file, 'r') as input_f:
        with open(output_file, 'w') as output_f:
            for line in input_f:
                words = extract_words(line)
                output_f.write(' '.join(words) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract masked words from a tree bank parse tree file.')
    parser.add_argument('input_file', type=str, help='Path to the input file')
    args = parser.parse_args()

    # Derive the output file name based on the input file
    output_file = args.input_file.replace('.txt', '-only-text.txt')

    # Extract words and save them to the output file
    extract_and_save_words(args.input_file, output_file)

    print('Extraction complete. Output file:', output_file)

