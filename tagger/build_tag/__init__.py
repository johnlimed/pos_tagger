import os.path
import pprint
import json
DATA_DIR = "a2_data\\"
pp = pprint.PrettyPrinter()

def train_tagger():
    __count_words()


def __count_words():
    total_word_count = 0
    word_type_count = dict()
    training_set = open(os.path.join(os.getcwd(), DATA_DIR + 'sents.train'))
    for line in training_set:
        line_list = line.split(" ")
        for word_with_tag in line_list:
            word, tag = word_with_tag.rstrip().rsplit('/', 1)
            total_word_count += 1
            # print word, tag, total_word_count
            if tag in word_type_count:
                if word in word_type_count[tag]:
                    word_type_count[tag][word] += 1
                else:
                    total_word_count += 1
                    word_type_count[tag][word] = 1
            else:
                word_type_count[tag] = {word: 1}
    pp.pprint(word_type_count)
    with open('result.json', 'w') as outfile:
        json.dump(word_type_count, outfile)

def __count_cond_words():
    total_word_count = 0
    cond_word_types = dict()
