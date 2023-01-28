from flask import Flask, jsonify

from c12.inference_novel import SimilarWordsFinder
from c12.preprocess import split_into_words, MorphemeFactory

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
finder = SimilarWordsFinder()
morpheme = MorphemeFactory.provide()


@app.route('/api/<word>')
def api_finding_similar_words(word: str):
    words = split_into_words(word, morpheme=morpheme).words
    similar_words = finder.find_similar_words(words)
    returning_json = {'words': similar_words}
    return jsonify(returning_json)


if __name__ == '__main__':
    app.run()