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
        wk_dir = os.getcwd()
        if cmd == "build_tagger":
            training_file_path = os.path.join(wk_dir, DATA_DIR, sys.argv[2])
            devt_file_path = os.path.join(wk_dir, DATA_DIR, sys.argv[3])
            out_model_file = sys.argv[4]
            if utils.check_file(training_file_path):
                print "building tagger: " + training_file_path + " " + devt_file_path + " " + out_model_file
                build.train_tagger(training_file_path, devt_file_path, out_model_file)
            else:
                print "error... training file: " + training_file_path + " not found"
        elif cmd == "run_tagger":
            test_file_path = os.path.join(wk_dir, FILE_DIR, DATA_DIR, sys.argv[2])
            out_model_file_path = os.path.join(wk_dir, FILE_DIR, sys.argv[3])
            out_file = os.path.join(wk_dir, FILE_DIR, sys.argv[4])
            if utils.check_file(test_file_path) or utils.check_file(out_model_file_path):
                print "running tagger: " + test_file_path + " " + out_model_file_path + " " + out_file
                test.test_tagger(test_file_path, out_model_file_path, out_file)
            else:
                print "error... test file: " + test_file_path + " or model file: " + out_model_file_path + " not found"
    else:
        print "no commands received... pls either run build_tagger [training file] [devt file] [out_model_file] or " \
              "run_tagger [test_tag file] [out_model_file] [out file]"
