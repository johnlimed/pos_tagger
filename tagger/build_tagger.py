#!/usr/bin/python
import sys
import utils
import tagger.build_tag as build

training_file_path = sys.argv[1]
devt_file_path = sys.argv[2]
out_model_file = sys.argv[3]
if utils.check_file(training_file_path):
    print "building tagger: " + training_file_path + " " + devt_file_path + " " + out_model_file
    build.train_tagger(training_file_path, devt_file_path, out_model_file)
else:
    print "error... training file: " + training_file_path + " not found"
