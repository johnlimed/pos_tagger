import pprint
import tagger.utils as utils

SPECIAL_START = "<S>"
SPECIAL_END = "/<S>"
PREV_TAG_V_TAG_COUNT_FILENAME = 'result_count_prev_tag_tag.json'
TAG_WORD_COUNT_FILENAME = 'result_count_tag_word.json'
COUNT_TAG_FILENAME = "result_count_tag.json"
PROB_TAG_GIVEN_PREV_TAG_FILENAME = "result_prob_tag_given_prev_tag.json"
PROB_WORD_GIVEN_TAG_FILENAME = "result_prob_word_given_tag.json"
COUNT_PREV_TAG_V_TAG = "count_prev_tag_v_tag"
COUNT_TAG = "count_total_tag"
COUNT_T_V_W = "count_t_v_w"
PROB_PREV_TAG_V_TAG = "prob_tag_v_prev_tag"
PROB_T_V_W = "prob_w_v_t"
pp = pprint.PrettyPrinter()


def train_tagger(training_file, devt_file, out_file):
    count_t_v_w, count_prev_t_v_t, count_tag = __count_bi_word(training_file)
    prob_t_given_prev_t, prob_w_given_t = __count_cond_probabilities(count_t_v_w, count_prev_t_v_t, count_tag)
    out_dict = {
        COUNT_T_V_W: count_t_v_w,
        COUNT_PREV_TAG_V_TAG: count_prev_t_v_t,
        COUNT_TAG: count_tag,
        PROB_PREV_TAG_V_TAG: prob_t_given_prev_t,
        PROB_T_V_W: prob_w_given_t
    }
    utils.write_out_file(out_dict, out_file)


def __count_bi_word(training_file):
    total_word_count, count_previous_t_against_t, count_tag_against_word, count_tag = 0, {}, {}, {}
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
                    count_tag[SPECIAL_START] = 1
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
            __count_previous_t_against_t(count_previous_t_against_t, tag, previous_tag, no_pass)
            __count_tag_against_word(count_tag_against_word, word, tag, count_tag, no_pass)
            # print idx, word, tag, previous_tag
            # break
    # pp.pprint(count_tag_against_word)
    # pp.pprint(count_previous_t_against_t)
    utils.write_out_file(count_tag_against_word, TAG_WORD_COUNT_FILENAME)
    utils.write_out_file(count_previous_t_against_t, PREV_TAG_V_TAG_COUNT_FILENAME)
    utils.write_out_file(count_tag, COUNT_TAG_FILENAME)
    return count_tag_against_word, count_previous_t_against_t, count_tag


def __count_previous_t_against_t(count_previous_t_against_t, tag, previous_tag, no_pass):
    if no_pass:
        if previous_tag in count_previous_t_against_t:
            if tag in count_previous_t_against_t[previous_tag]:
                count_previous_t_against_t[previous_tag][tag] += 1
            else:
                count_previous_t_against_t[previous_tag][tag] = 1
        else:
            count_previous_t_against_t[previous_tag] = {tag: 1}


def __count_tag_against_word(count_tag_against_word, word, tag, count_tag, no_pass):
    if no_pass:
        if tag in count_tag_against_word:
            if word in count_tag_against_word[tag]:
                count_tag_against_word[tag][word] += 1
            else:
                count_tag_against_word[tag][word] = 1
        else:
            count_tag_against_word[tag] = {word: 1}
        if tag in count_tag:
            count_tag[tag] += 1
        else:
            count_tag[tag] = 1


def __count_cond_probabilities(count_t_v_w, count_prev_t_v_t, count_tag):
    prob_t_given_prev_t, prob_w_given_t = {}, {}
    for tag in count_t_v_w:
        prob_w_given_t[tag] = {}
        for word in count_t_v_w[tag]:
            prob_w_given_t[tag][word] = count_t_v_w[tag][word] / float(count_tag[tag])
    for prev_tag in count_prev_t_v_t:
        prob_t_given_prev_t[prev_tag] = {}
        for tag in count_prev_t_v_t[prev_tag]:
            prob_t_given_prev_t[prev_tag][tag] = count_prev_t_v_t[prev_tag][tag] / float(count_tag[prev_tag])
    # pp.pprint(prob_w_given_t)
    # pp.pprint(prob_t_given_prev_t)
    utils.write_out_file(prob_t_given_prev_t, PROB_TAG_GIVEN_PREV_TAG_FILENAME)
    utils.write_out_file(prob_w_given_t, PROB_WORD_GIVEN_TAG_FILENAME )
    return prob_t_given_prev_t, prob_w_given_t
