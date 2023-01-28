
try:
    import janome
    import gensim
    import tqdm
    import flask
except ImportError:
    print('ライブラリのインポートに失敗しました。PyCharm下部の「Terminal」を開いて次のコマンドを実行してください。')
    print('pip install -r requirements.txt')
