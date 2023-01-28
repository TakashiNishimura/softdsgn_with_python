from enum import Enum
from typing import List


class MorphemeModule(Enum):
    MECAB = 'mecab'
    JANOME = 'janome'


class ExecutionMode(Enum):
    VERY_HIGH = 'very_high'
    HIGH = 'high'
    MIDDLE = 'middle'
    LOW = 'low'
    NO_RECOMMENDED = 'no_recommended'
    DEBUG = 'debug'


class PartOfSpeech(Enum):
    NOUN = '名詞'
    VERB = '動詞'
    ADJECTIVE = '形容詞'
    ADVERB = '副詞'
    POSTPOSITIONAL_PARTICLE = '助詞'
    CONJUNCTION = '接続詞'
    AUXILIARY_VERB = '助動詞'

    @staticmethod
    def as_str(part_of_speeches: List) -> List[str]:
        poses = []
        for pos in part_of_speeches:
            poses.append(pos.value)
        return poses


class Color(Enum):
    WHITE = '0'
    RED = '31'
    GREEN = '32'
    BLUE = '34'
