from essential_generators import MarkovTextGenerator
import json

filename = 'markov_textgen.json'

def make_training_data(corpus="corpus.txt", output='markov_textgen.json'):

    with open(corpus, 'r', encoding='utf-8') as fp:
        set4 = fp.read()

    gen = MarkovTextGenerator(load_model=False)
    gen.train(set4)
    gen.save_model(output)

    with open(filename, 'r', encoding='utf-8') as f:
        json_file = json.load(f)
    with open(filename, 'w', encoding='utf-8') as f:
        print(json.dumps(json_file, separators=(',', ':')), file=f)

make_training_data()