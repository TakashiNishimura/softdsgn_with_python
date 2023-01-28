from gensim import models

import config
from c12.preprocess import split_into_words, MorphemeFactory


class SimilarWordsFinder:

    def __init__(self, model_path: str = config.dir_to_save_model+'aozora2vec.model'):
        self.model = models.Doc2Vec.load(model_path)
        print(self.model.wv.vector_size)

    def find_similar_words(self, words):
        similarities = []
        for word in words:
            for result in self.model.wv.most_similar(positive=word, topn=10):
                similarities.append(result[0])
            break
        return similarities

    def find_similar_novel(self, words):
        novels = []
        x = self.model.infer_vector(words)
        similar_texts = self.model.docvecs.most_similar([x])
        for similar_text in similar_texts:
            novels.append(similar_text)
        return novels


if __name__ == '__main__':
    print('文章を入力してください: ', end='')
    text = input()
    finder = SimilarWordsFinder()
    morpheme = MorphemeFactory.provide()
    words = split_into_words(text, morpheme=morpheme).words
    similar_words = finder.find_similar_words(words)
    similar_novels = finder.find_similar_novel(words)
    print(similar_words)
    print(similar_novels)