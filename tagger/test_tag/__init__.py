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


def test_tagger(test_file, in_filename, out_file):
    stats_dict = utils.read_file(in_filename)
    count_t_v_t = stats_dict[COUNT_PREV_TAG_V_TAG]
    prob_w_v_t = stats_dict[PROB_W_V_T]
    prob_t_v_t = stats_dict[PROB_PREV_TAG_V_TAG]
    pos_tags = stats_dict[COUNT_TAG].keys()[:-1]
    out_line = ""
    in_file = open(test_file)
    for line in in_file:
        word_list = line.rstrip().split(" ")
        num_of_words = len(word_list)
        # pos_tags.insert(0, SPECIAL_START)
        # pos_tags.append(SPECIAL_END)
        best_score = {}
        best_edge = {}
        best_score["0 " + SPECIAL_START] = 0
        best_edge["0 " + SPECIAL_START] = None
        for idx, word in enumerate(word_list):
            for pre_tag in pos_tags:
                for next_tag in pos_tags:
                    if str(idx) + " " + pre_tag in best_score and pre_tag in count_t_v_t and next_tag in count_t_v_t[pre_tag]:
                        if word in prob_w_v_t:
                            score = best_score[str(idx) + " " + pre_tag] + -(
                                math.log(prob_t_v_t[next_tag][pre_tag])) + -(math.log(prob_w_v_t[word][next_tag]))
                        else:
                            "print unknown word"
                            score = best_score[str(idx) + " " + pre_tag] + -(
                                math.log(prob_t_v_t[next_tag][pre_tag])) + -(math.log(8e-50))
                        if str(idx + 1) + " " + next_tag not in best_score or best_score[
                                            str(idx + 1) + " " + next_tag] > score:
                            best_score[str(idx + 1) + " " + next_tag] = score
                            best_edge[str(idx + 1) + " " + next_tag] = str(idx) + " " + pre_tag
        for tag in pos_tags:
            curr_node = str(num_of_words)+" "+tag
            next_node = str(num_of_words+1)+" "+SPECIAL_END
            if curr_node in best_score and tag in count_t_v_t and SPECIAL_END in count_t_v_t[tag]:
                score = best_score[curr_node] + -(math.log(prob_t_v_t[SPECIAL_END][tag]))
                if next_node not in best_score or best_score[next_node] > score:
                    best_score[next_node] = score
                    best_edge[next_node] = curr_node
        # backtracing
        tags = []
        next_edge = best_edge[str(num_of_words+1) + " " + SPECIAL_END]
        while next_edge is not None:
            position, tag = next_edge.split(" ")
            tags.append(tag)
            next_edge = best_edge[next_edge]
            # print next_edge
        tags.reverse()
        tags.pop(0)
        for idx, word in enumerate(word_list):
            out_line += word+"/"+tags[idx]+" "
        out_line += "\n"
    print out_line
    with open(out_file, "w") as write_file:
        write_file.write(out_line)