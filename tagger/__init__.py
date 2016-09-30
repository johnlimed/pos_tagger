#!/usr/bin/python
import sys
import tagger.test_tag as test
import tagger.build_tag as build

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "build_tagger":
            training_file = sys.argv[2]
            devt_file = sys.argv[3]
            out_model_file = sys.argv[4]
            print "building tagger: " + training_file + " " + devt_file + " " + out_model_file
            build.train_tagger(training_file, devt_file, out_model_file)
        elif cmd == "run_tagger":
            test_file = sys.argv[2]
            out_model_file = sys.argv[3]
            out_file = sys.argv[4]
            print "running tagger: " + test_file + " " + out_model_file + " " + out_file
            test.test_tagger(test_file, out_model_file, out_file)
    else:
        print "no commands received... pls either run build_tagger [training file] [devt file] [out_model_file] or "\
              "run_tagger [test_tag file] [out_model_file] [out file]"
