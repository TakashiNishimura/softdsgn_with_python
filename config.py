
import os

from c12.constant import MorphemeModule

# プロジェクトのベースとなるパスの指定（変更非推奨）
base_dir = os.path.dirname(os.path.abspath(__file__))
# データディレクトリのパスの指定（変更非推奨）
data_dir = base_dir + os.sep + 'data' + os.sep
# Doc2Vecのモデルの保存先のパスの指定（変更非推奨）
dir_to_save_model = base_dir + os.sep + 'model' + os.sep


# コンピュータ構成のスキャン機能の適用
scan = True  # (True or False)

# 形態素解析に使用するツール（MeCabでShift-JISの辞書をインストールした人はMECAB推奨）
using_morpheme_module = MorphemeModule.JANOME  # (MorphemeModule.JANOME or MorphemeModule.MECAB)

# モデルの検証に使用するデータ数
validating_data_count = 100  # (Default is 100. if you run on DEBUG mode, change its adjusting number.)
