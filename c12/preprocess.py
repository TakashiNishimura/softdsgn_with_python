import os
import re
from typing import List

from gensim.models.doc2vec import LabeledSentence
from tqdm import tqdm

import config
from c12.constant import MorphemeModule, PartOfSpeech

if config.using_morpheme_module == MorphemeModule.MECAB:
    from MeCab import Tagger
elif config.using_morpheme_module == MorphemeModule.JANOME:
    from janome.tokenizer import Tokenizer


def get_all_files_from_directory(directory_path: str) -> List:
    file_paths = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


def read_document_from_files(file_paths: List[str]) -> List[str]:
    documents = []
    for file_path in tqdm(file_paths, desc='INFO : テキストファイルを読み込み中'):
        with open(file_path, 'r', encoding='sjis', errors='ignore') as f:
            document = f.read()
            document = document.replace('　', '')
            documents.append(document)
    return documents


def trim_novel_body_from_document(document: str):
    document = exclude_ruby('≪', '≫', document)
    document = exclude_ruby('《', '》', document)
    document = exclude_no_novel_body(document)
    lines = document.splitlines()
    valid_lines = []
    is_valid = False
    horizontal_rule_cnt = 0
    break_cnt = 0
    for line in lines:
        if horizontal_rule_cnt < 2 and '-----' in line:
            horizontal_rule_cnt += 1
            is_valid = horizontal_rule_cnt == 2
            continue
        if not is_valid:
            continue
        if line == '':
            break_cnt += 1
            is_valid = break_cnt != 3
            continue
        break_cnt = 0
        valid_lines.append(line),
    return ''.join(str(valid_lines))


class Morpheme:

    def analyze(self, document: str) -> List[str]:
        pass


class Janome(Morpheme):

    def __init__(self):
        self.tokenizer = Tokenizer()

    def analyze(self, document: str) -> List[str]:
        words = []
        for token in self.tokenizer.tokenize(document):
            surface = token.surface
            part_of_speech = token.part_of_speech.split(',')
            is_verb = part_of_speech[0] == PartOfSpeech.VERB.value
            is_adjective = part_of_speech[0] == PartOfSpeech.ADJECTIVE.value
            is_adverb = part_of_speech[0] == PartOfSpeech.ADVERB.value
            is_noun_and_not_number = part_of_speech[0] == PartOfSpeech.NOUN.value and part_of_speech[1] != '数'
            if is_verb or is_adjective or is_adverb or is_noun_and_not_number:
                words.append(surface)
        return words


class MeCab(Morpheme):

    def __init__(self):
        self.me_cab = Tagger('-Ochasen')

    def analyze(self, document: str) -> List[str]:
        words = []
        node = self.me_cab.parseToNode(document)
        while node:
            surface = node.surface
            part_of_speech = node.feature.split(',')
            is_verb = part_of_speech[0] == PartOfSpeech.VERB.value
            is_adjective = part_of_speech[0] == PartOfSpeech.ADJECTIVE.value
            is_adverb = part_of_speech[0] == PartOfSpeech.ADVERB.value
            is_noun_and_not_number = part_of_speech[0] == PartOfSpeech.NOUN.value and part_of_speech[1] != '数'
            if is_verb or is_adjective or is_adverb or is_noun_and_not_number:
                words.append(surface)
            node = node.next
        return words


class MorphemeFactory:

    @staticmethod
    def provide(morpheme_module: MorphemeModule = config.using_morpheme_module) -> Morpheme:
        morpheme = Morpheme()
        if morpheme_module == MorphemeModule.MECAB:
            morpheme = MeCab()
        elif morpheme_module == MorphemeModule.JANOME:
            morpheme = Janome()
        return morpheme


def split_into_words(document, name='', morpheme: Morpheme = Morpheme()):
    words = morpheme.analyze(document)
    return LabeledSentence(words=words, tags=[name])


def exclude_ruby(begin_symbol: str, end_symbol: str, document: str) -> str:
    compiled_ruby_pattern = re.compile(begin_symbol + '.*?' + end_symbol)
    pattern = ''
    while pattern is not None:
        match_obj = re.search(compiled_ruby_pattern, document)
        try:
            pattern = match_obj.group(0)
        except AttributeError:
            break
        document = document.replace(pattern, '')

    return document


def exclude_document_information(document: str) -> str:
    compiled_information_pattern = re.compile('-.*-')
    match_obj = re.search(compiled_information_pattern, document)
    try:
        pattern = match_obj.group(0)
        document = document.replace(pattern, '')
    except AttributeError:
        pass
    return document


def exclude_no_novel_body(document: str) -> str:
    compiled_unavailable_kanji_pattern = re.compile('［.*?］')
    pattern = ''
    while pattern is not None:
        match_obj = re.search(compiled_unavailable_kanji_pattern, document)
        try:
            pattern = match_obj.group(0)
            document = document.replace(pattern, '')
        except AttributeError:
            break
    return document
