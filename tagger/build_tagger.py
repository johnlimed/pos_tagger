#!/usr/bin/python
import sys
import utils
import pprint

SPECIAL_START = "<S>"
SPECIAL_END = "/<S>"
TAG_PREV_TAG_COUNT_FILENAME = 'result_count_tag_prev_tag.json'
PREV_TAG_V_TAG_COUNT_FILENAME = 'result_count_prev_tag_tag.json'
TAG_WORD_COUNT_FILENAME = 'result_count_tag_word.json'
WORD_TAG_COUNT_FILENAME = 'result_word_tag_count.json'
COUNT_TAG_FILENAME = "result_count_tag.json"
PROB_TAG_GIVEN_PREV_TAG_FILENAME = "result_prob_tag_given_prev_tag.json"
PROB_WORD_GIVEN_TAG_FILENAME = "result_prob_word_given_tag.json"
COUNT_PREV_TAG_V_TAG = "count_prev_tag_v_tag"
COUNT_TAG = "count_total_tag"
COUNT_T_V_W = "count_t_v_w"
COUNT_W_V_T = "count_w_v_t"
PROB_TAG_V_PREV_TAG = "prob_tag_v_prev_tag"
PROB_W_V_T = "prob_w_v_t"
pp = pprint.PrettyPrinter()


def train_tagger(training_file, devt_file, out_file):
    count_t_v_w, count_w_v_t, count_t_v_prev_t, count_prev_t_v_t, count_tag = __count_bi_word(training_file)
    prob_t_given_prev_t, prob_w_given_t = __count_cond_probabilities(count_w_v_t, count_t_v_prev_t, count_tag)
    out_dict = {
        COUNT_PREV_TAG_V_TAG:  count_prev_t_v_t,
        COUNT_TAG: count_tag,
        PROB_TAG_V_PREV_TAG: prob_t_given_prev_t,
        PROB_W_V_T: prob_w_given_t
    }
    utils.write_out_file(out_dict, out_file)


def __count_bi_word(training_file):
    total_word_count, count_t_against_previous_t, count_tag_against_word, count_word_against_tag = 0, {}, {}, {}
    count_tag, count_prev_t_against_t = {}, {}
    training_set = open(training_file)
    for line in training_set:
        line_list = line.rstrip().split(" ")
        total_word_count += len(line_list)
        line_list.insert(0, SPECIAL_START)
        line_list.append(SPECIAL_END)
        word, tag, previous_tag, no_pass = None, None, None, True
        for idx, word_w_tag in enumerate(line_list):
            if idx == 0:
                no_pass = False
                if SPECIAL_START in count_tag:
                    count_tag[SPECIAL_START] += 1
                else:
                    count_tag = {SPECIAL_START: 1}
            elif idx == 1:
                no_pass = True
                word, tag = word_w_tag.rsplit('/', 1)
                previous_tag = SPECIAL_START
            elif idx < len(line_list) - 1:
                word, tag = word_w_tag.rsplit('/', 1)
                previous_tag = line_list[idx - 1].rsplit('/', 1)[1]
            else:
                previous_tag = line_list[idx - 1].rsplit('/', 1)[1]
                tag = SPECIAL_END
                word = previous_tag
            __count_t_against_previous_t(count_t_against_previous_t, count_prev_t_against_t, tag, previous_tag, no_pass)
            __count_word_against_tag(count_word_against_tag, word, tag, count_tag, no_pass)
    count_word_against_tag["UNKN"] = {}
    utils.write_out_file(count_word_against_tag, WORD_TAG_COUNT_FILENAME)
    utils.write_out_file(count_prev_t_against_t, PREV_TAG_V_TAG_COUNT_FILENAME)
    utils.write_out_file(count_t_against_previous_t, TAG_PREV_TAG_COUNT_FILENAME)
    utils.write_out_file(count_tag, COUNT_TAG_FILENAME)
    return count_tag_against_word, count_word_against_tag, count_t_against_previous_t, count_prev_t_against_t, count_tag


def __count_t_against_previous_t(count_t_against_previous_t, count_prev_t_against_t, tag, previous_tag, no_pass):
    if no_pass:
        if tag in count_t_against_previous_t:
            if previous_tag in count_t_against_previous_t[tag]:
                count_t_against_previous_t[tag][previous_tag] += 1
            else:
                count_t_against_previous_t[tag][previous_tag] = 1
        else:
            count_t_against_previous_t[tag] = {previous_tag: 1}
        if previous_tag in count_prev_t_against_t:
            if tag in count_prev_t_against_t[previous_tag]:
                count_prev_t_against_t[previous_tag][tag] += 1
            else:
                count_prev_t_against_t[previous_tag][tag] = 1
        else:
            count_prev_t_against_t[previous_tag] = {tag: 1}


def __count_word_against_tag(count_word_against_tag, word, tag, count_tag, no_pass):
    if no_pass:
        if word in count_word_against_tag:
            if tag in count_word_against_tag[word]:
                count_word_against_tag[word][tag] += 1
            else:
                count_word_against_tag[word][tag] = 1
        else:
            count_word_against_tag[word] = {tag: 1}
        if tag in count_tag:
            count_tag[tag] += 1
        else:
            count_tag[tag] = 1


def __count_cond_probabilities(count_w_v_t, count_t_v_prev_t, count_tag):
    prob_t_given_prev_t, prob_w_given_t, prob_t_given_w = {}, {}, {}

    for tag in count_tag.keys():
        for word in count_w_v_t:
            if word not in prob_w_given_t:
                prob_w_given_t[word] = {}
            if tag in count_w_v_t[word]:
                prob_w_given_t[word][tag] = count_w_v_t[word][tag] / float(count_tag[tag])
            else:
                prob_w_given_t[word][tag] = 8e-50
        for cur_tag in count_t_v_prev_t:
            if cur_tag not in prob_t_given_prev_t:
                prob_t_given_prev_t[cur_tag] = {}
            if tag in count_t_v_prev_t[cur_tag].keys():
                prob_t_given_prev_t[cur_tag][tag] = count_t_v_prev_t[cur_tag][tag] / float(count_tag[cur_tag])
            else:
                prob_t_given_prev_t[cur_tag][tag] = 8e-50
    # utils.write_out_file(prob_t_given_prev_t, PROB_TAG_GIVEN_PREV_TAG_FILENAME)
    # utils.write_out_file(prob_w_given_t, PROB_WORD_GIVEN_TAG_FILENAME)
    return prob_t_given_prev_t, prob_w_given_t


training_file_path = sys.argv[1]
devt_file_path = sys.argv[2]
out_model_file = sys.argv[3]
if utils.check_file(training_file_path):
    print "building tagger: " + training_file_path + " " + devt_file_path + " " + out_model_file
    train_tagger(training_file_path, devt_file_path, out_model_file)
else:
    print "error... training file: " + training_file_path + " not found"

