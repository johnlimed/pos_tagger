import os.path
import pprint
import json

DATA_DIR = "a2_data\\"
TRAINING_FILE = "sents.train"
SPECIAL_START = "<S>"
SPECIAL_END = "/<S>"
TAG_V_PREV_TAG_COUNT_FILENAME = 'result_count_tag_prev_tag.json'
WORD_TAG_COUNT_FILENAME = 'result_count_word_tag.json'
COUNT_TAG_V_PREV_TAG = "count_tag_v_prev_tag"
COUNT_W_V_T = "count_w_v_t"
OUTFILE_NAME = "model_file"
pp = pprint.PrettyPrinter()


def train_tagger():
    count_w_v_t, count_t_v_prev_t = __count_bi_word()
    out_dict = {COUNT_W_V_T: count_w_v_t, COUNT_TAG_V_PREV_TAG: count_t_v_prev_t}
    __write_out_file(out_dict, OUTFILE_NAME)


def __count_bi_word():
    total_word_count, count_t_against_previous_t, count_word_against_tag = 0, {}, {}
    training_set = open(os.path.join(os.getcwd(), DATA_DIR + TRAINING_FILE))
    for line in training_set:
        line_list = line.rstrip().split(" ")
        total_word_count += len(line_list)
        line_list.insert(0, SPECIAL_START)
        line_list.append(SPECIAL_END)
        word, tag, previous_tag, no_pass = None, None, None, True
        for idx, word_w_tag in enumerate(line_list):
            if idx == 0:
                no_pass = False
            elif idx == 1:
                no_pass = True
                word, tag = word_w_tag.rsplit('/', 1)
                previous_tag = SPECIAL_START
            elif idx < len(line_list)-1:
                word, tag = word_w_tag.rsplit('/', 1)
                previous_tag = line_list[idx - 1].rsplit('/', 1)[1]
            else:
                previous_tag = line_list[idx - 1].rsplit('/', 1)[1]
                tag = SPECIAL_END
                word = previous_tag
            __count_t_against_previous_t(count_t_against_previous_t, tag, previous_tag, no_pass)
            __count_word_against_tag(count_word_against_tag, word, tag, no_pass)
            # print idx, word, tag, previous_tag
        # break
    # pp.pprint(count_word_against_tag)
    # pp.pprint(count_t_against_previous_t)
    __write_out_file(count_word_against_tag, WORD_TAG_COUNT_FILENAME)
    __write_out_file(count_t_against_previous_t, TAG_V_PREV_TAG_COUNT_FILENAME)
    return count_word_against_tag, count_t_against_previous_t


def __count_t_against_previous_t(count_t_against_previous_t, tag, previous_tag, no_pass):
    if no_pass:
        if previous_tag in count_t_against_previous_t:
            if tag in count_t_against_previous_t[previous_tag]:
                count_t_against_previous_t[previous_tag][tag] += 1
            else:
                count_t_against_previous_t[previous_tag][tag] = 1
        else:
            count_t_against_previous_t[previous_tag] = {tag: 1}


def __count_word_against_tag(count_word_against_tag, word, tag, no_pass):
    if no_pass:
        if tag in count_word_against_tag:
            if word in count_word_against_tag[tag]:
                count_word_against_tag[tag][word] += 1
            else:
                count_word_against_tag[tag][word] = 1
        else:
            count_word_against_tag[tag] = {word: 1}


def __write_out_file(to_write_out, outfile_name):
    with open(outfile_name, 'w') as outfile:
        json.dump(to_write_out, outfile, indent=4)


def __count_cond_probabilities():
    pass