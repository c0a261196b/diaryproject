## いろいろインポート
import argparse
from pathlib import Path
parser = argparse.ArgumentParser(description='日記の作成、閲覧、削除、および外部連携用のプログラムです。')
parser.add_argument('--file_destination', help='日記ファイルの保存位置', default='./diaries')

mode = parser.add_subparsers(dest='mode') # 実行する機能の指定

## 日記を記録するモード
add = mode.add_parser('add')
add.add_argument('title', help='日記のタイトル')
add.add_argument('body', help='日記の本文')
add.add_argument('--tag', nargs='*', help='日記につけるタグ', default='未分類')

## 日記を読み込んで表示するモード
read = mode.add_parser('read')
read.add_argument('date', help='日記を記録した日')
read.add_argument('time', help='日記を記録した時間')
### タグで検索する機能は後でつける予定

## 該当する日記を削除するモード
remove = mode.add_parser('remove')
remove.add_argument('date', help='日記を記録した日')
remove.add_argument('time', help='日記を記録した時間')
### タグで検索する機能は後でつける予定

setting = mode.add_parser('setting')
### 設定機能は後から実装する予定

## 引数解析
args = parser.parse_args()

## 仮置き
print(args.mode)
print(args)