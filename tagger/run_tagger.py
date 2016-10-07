import sys
import utils
import tagger.test_tag as test

test_file_path = sys.argv[1]
out_model_file_path = sys.argv[2]
out_file = sys.argv[3]
if utils.check_file(test_file_path) or utils.check_file(out_model_file_path):
    print "running tagger: " + test_file_path + " " + out_model_file_path + " " + out_file
    test.test_tagger(test_file_path, out_model_file_path, out_file)
else:
    print "error... test file: " + test_file_path + " or model file: " + out_model_file_path + " not found"
