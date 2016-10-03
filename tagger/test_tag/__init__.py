import pprint
import tagger.utils as utils

FILE_DIR = "tagger"
COUNT_PREV_TAG_V_TAG = "count_prev_tag_v_tag"
COUNT_TAG = "count_total_tag"
COUNT_T_V_W = "count_t_v_w"
PROB_PREV_TAG_V_TAG = "prob_tag_v_prev_tag"
PROB_T_V_W = "prob_w_v_t"
pp = pprint.PrettyPrinter()

# stats_dict = {
    #     COUNT_T_V_W: count_t_v_w,
    #     COUNT_PREV_TAG_V_TAG: count_prev_t_v_t,
    #     COUNT_TAG: count_tag,
    #     PROB_PREV_TAG_V_TAG: prob_t_given_prev_t,
    #     PROB_T_V_W: prob_w_given_t
    # }


def test_tagger(test_file, in_filename, out_file):
    stats_dict = utils.read_file(in_filename)
    # pp.pprint(stats_dict)

