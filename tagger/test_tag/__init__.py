import math
import pprint
import tagger.utils as utils

FILE_DIR = "tagger"
COUNT_PREV_TAG_V_TAG = "count_prev_tag_v_tag"
COUNT_TAG = "count_total_tag"
COUNT_T_V_W = "count_t_v_w"
COUNT_W_V_T = "count_w_v_t"
PROB_PREV_TAG_V_TAG = "prob_tag_v_prev_tag"
PROB_W_V_T = "prob_w_v_t"
SPECIAL_START = "<S>"
SPECIAL_END = "/<S>"
pp = pprint.PrettyPrinter()

# stats_dict = {
#     PROB_PREV_TAG_V_TAG: prob_t_given_prev_t,
#     PROB_W_V_T: prob_w_given_t
# }


def test_tagger(test_file, in_filename, out_file):
    stats_dict = utils.read_file(in_filename)
    prob_w_v_t = stats_dict[PROB_W_V_T]
    prob_t_v_t = stats_dict[PROB_PREV_TAG_V_TAG]
    pos_tags = stats_dict[COUNT_TAG].keys()
    # pp.pprint(stats_dict)
    in_file = open(test_file)
    for line in in_file:
        word_list = line.rstrip().split(" ")
        word_list.insert(0, SPECIAL_START)
        word_list.append(SPECIAL_END)
        viterbi = {0: [1], 1: []}
        backpointer = {}
        for tags in pos_tags[1:-1]:
            viterbi[1].append(math.log1p(prob_w_v_t[word_list[1]][tags]))
            backpointer[tags] = {1: 0}
            # print viterbi[1]
        pprint.pprint(viterbi)
        # for idx, word in enumerate(word_list[2:]):
        #     print word



        # for idx, word in enumerate(word_list[:-1]):
        #     print idx, word
        #     if idx == 0:
        #         viterbi[0] = 1, SPECIAL_START
        #         print "probability: " + str(viterbi[idx])
        #     else:
        #         if word in prob_w_v_t:
        #             viterbi[idx] = 0, ""
        #             for tag in prob_w_v_t[word]:
        #                 if prob_w_v_t[word][tag] > viterbi[idx][0]:
        #                     viterbi[idx] = prob_w_v_t[word][tag], tag
        #             print "probability: " + str(viterbi[idx][0]) + " and should be the tag: " + viterbi[idx][1]
        #
        #             # for tag in prob_w_v_t[word]:
        #             #     viterbi[idx, tag] = prob_w_v_t[word][tag]
        #             # print prob_w_v_t[word]
        #         else:
        #             __determine_unknown_prob(word)


def __determine_unknown_prob(unknown_word):
    print "unknown word... " + unknown_word
    prob = 0*unknown_word
    return prob