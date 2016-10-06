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
        viterbi = {0: [(1, SPECIAL_START)], 1: []}
        backpointer = {"start"}
        backpointer.add(SPECIAL_START)
        for tag in pos_tags[1:-1]:
            viterbi[1].append((math.log1p(prob_w_v_t[word_list[1]][tag]), tag))
        for idx, word in enumerate(word_list[2:]):
            viterbi[idx + 2] = []
            for tag in pos_tags[:-1]:
                # print "we are at: " + str(idx+2)
                # print "and tag: " + tag + " and word " + word
                if word in prob_w_v_t:
                    # print "prob w_v_t: " + str(prob_w_v_t[word][tag])
                    viterbi[idx + 2].append(__det_tag_prob(viterbi[idx + 1], prob_t_v_t[tag], prob_w_v_t[word][tag],
                                                           backpointer))
                else:
                    print "FAILLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"
                    # TODO: make unknown words work
                    break
                    # break
                    # break
                    # print viterbi[idx+2]
        # break
        pprint.pprint(viterbi)
        print backpointer
        # viterbi[idx].append()
        # print word, idx


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


def __det_tag_prob(list_of_prev_prob, list_prob_t_v_t, prob_w_given_tag, backpointer):
    # TODO: If prev prob tag is UNKN, determine most likely tag
    max_prob = (0, "NN")
    # max_prob = (float("-Infinity"), "")
    # print list_prob_t_v_t
    for tuple_prob in list_of_prev_prob:
        # print "tuple prob: " + str(tuple_prob)
        prob = math.log1p(tuple_prob[0]) + math.log1p(list_prob_t_v_t[tuple_prob[1]] + math.log1p(prob_w_given_tag))
        if prob > max_prob[0]:
            max_prob = (prob, tuple_prob[1])
            backpointer.add(tuple_prob[1])
    # print "Max prob: " + str(max_prob[0])
    return max_prob


def __determine_unknown_prob(unknown_word):
    print "unknown word... " + unknown_word
    prob = 0 * unknown_word
    return prob
