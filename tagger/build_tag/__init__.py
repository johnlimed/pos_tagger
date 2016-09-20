import os.path
DATA_DIR = "a2_data\\"


def train_tagger():
    training_set = open(os.path.join(os.getcwd(), DATA_DIR + 'sents.train'))
    for line in training_set:
        line_list = line.split(" ")
        for word in line_list:
            print word
