# pos_tagger
##Data files
Data files must be placed in tagger/a2_data directory.
- sents.devt
- sents.out
- sents.test
- sents.train

Model output file will be generated in tagger/a2_data directory named model_file.

##Running tagger
Two commands, either build_tagger or test_tagger

cmd to build:
python build_tagger sents.train sents.devt model_file

cmd to test:
python run_tagger sents.test model_file sents.out