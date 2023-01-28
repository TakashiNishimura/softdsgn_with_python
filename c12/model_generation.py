import collections
import random
import logging

import config
from gensim import models
from tqdm import tqdm

from c12.constant import Color
from c12.function import mean
from c12.preprocess import get_all_files_from_directory, read_document_from_files, trim_novel_body_from_document, \
    MorphemeFactory, split_into_words
from c12.utility import print_colored_text, TrainSetting

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)


if __name__ == '__main__':
    # PC構成から学習データの規模を設定
    train_setting = TrainSetting(scan=config.scan)
    # config.data_dir下のファイルをすべて読み込む
    paths = get_all_files_from_directory(config.data_dir)
    # 学習データの規模に応じたファイル数でデータを抽出する
    extracted_paths = random.sample(paths, train_setting.extraction_count)
    # ファイルから文章を読み取る
    raw_docs = read_document_from_files(extracted_paths)
    # 文章に含まれる小説でない部分（著者情報等）を抜き取る
    trammed_doc = []
    for doc in tqdm(raw_docs, desc='INFO : テキストから本文を抽出中'):
        trammed_doc.append(trim_novel_body_from_document(doc))
    # データの形式を(words, doc_id)とする
    # wordsは文章を形態素解析した結果の単語群、doc_idは小説のidで読み込んだ順にidを付与する
    split_doc = []
    morpheme = MorphemeFactory.provide(config.using_morpheme_module)
    for doc, path in zip(tqdm(trammed_doc, desc='INFO : 形態素解析中'), extracted_paths):
        split_doc.append(split_into_words(doc, path, morpheme))
    # 学習用のモデルを準備する
    print_colored_text('INFO : モデルを準備します', Color.RED)
    model = models.Doc2Vec(vector_size=400, alpha=0.001, sample=1e-4, min_count=20, workers=4)
    model.build_vocab(split_doc)
    print_colored_text('INFO : モデルの準備を完了しました。', Color.RED)
    print_colored_text('INFO : 学習中...', Color.RED)
    model.train(split_doc, total_examples=model.corpus_count, epochs=train_setting.epochs)
    print_colored_text('INFO : 学習が完了しました。', Color.RED)
    # モデルを保存する
    model.save(config.dir_to_save_model + 'aozora2vec.model')
    # モデルの精度を検証する
    similarities = []
    for document_ordinal in tqdm(range(config.validating_data_count), desc='INFO : モデルの精度の検証をしています'):
        inferred_vector = model.infer_vector(split_doc[document_ordinal].words)
        document_paths_and_similarities = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
        similarity = [names for names, _ in document_paths_and_similarities] \
            .index(split_doc[document_ordinal].tags[0])
        similarities.append(similarity)
    loss = mean(similarities)
    accuracy = collections.Counter(similarities)[0] / config.validating_data_count
    print_colored_text(f'Loss: {loss:.5f}\t accuracy: {accuracy:.5f}\t', Color.RED, end='')
    print_colored_text(str(similarities), Color.BLUE)
