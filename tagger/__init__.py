#!/usr/bin/python
import sys
import utils
import os.path
import tagger.test_tag as test
import tagger.build_tag as build

DATA_DIR = "a2_data"
FILE_DIR = "tagger"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "build_tagger":
            training_file = sys.argv[2]
            devt_file = sys.argv[3]
            out_model_file = sys.argv[4]
            if utils.check_file(os.path.join(DATA_DIR, training_file)):
                print "building tagger: " + training_file + " " + devt_file + " " + out_model_file
                build.train_tagger(training_file, devt_file, out_model_file)
            else:
                print "error... training file: " + training_file + " not found"
        elif cmd == "run_tagger":
            test_file = sys.argv[2]
            out_model_file = sys.argv[3]
            out_file = sys.argv[4]
            if utils.check_file(os.path.join(DATA_DIR, test_file)) or utils.check_file(
                    os.path.join(FILE_DIR, out_model_file)):
                print "running tagger: " + test_file + " " + out_model_file + " " + out_file
                test.test_tagger(test_file, out_model_file, out_file)
            else:
                print "error... test file: " + test_file + " or model file: " + out_model_file + " not found"
    else:
        print "no commands received... pls either run build_tagger [training file] [devt file] [out_model_file] or " \
              "run_tagger [test_tag file] [out_model_file] [out file]"
