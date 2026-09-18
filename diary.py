## いろいろインポート
import argparse
import json
from pathlib import Path
from datetime import datetime

parser = argparse.ArgumentParser(description='日記の作成、閲覧、削除、および外部連携用のプログラムです。')
parser.add_argument('--file_destination', help='日記ファイルの保存位置', default='./diaries')

mode = parser.add_subparsers(dest='mode') # 実行する機能の指定

## 日記を記録するモード
add = mode.add_parser('add')
add.add_argument('title', type=str, help='日記のタイトル')
add.add_argument('body', type=str, help='日記の本文')
add.add_argument('--tags', type=str, nargs='*', help='日記につけるタグ', default=['未分類'])

## 日記を読み込んで表示するモード
read = mode.add_parser('read')
read.add_argument('date', type=str, help='日記を記録した日')
read.add_argument('time', type=str, help='日記を記録した時間')
### タグで検索する機能は後でつける予定

## 該当する日記を削除するモード
remove = mode.add_parser('remove')
remove.add_argument('date', type=str, help='日記を記録した日')
remove.add_argument('time', type=str, help='日記を記録した時間')
### タグで検索する機能は後でつける予定

setting = mode.add_parser('setting')
### 設定機能は後から実装する予定

## 引数解析
args = parser.parse_args()

## ファイルを格納する場所を変数に格納＆なかったら作成
diaries_path = Path(args.file_destination) / datetime.now().strftime('%Y')
diaries_path.mkdir(parents=True, exist_ok=True)

match args.mode:
    case 'add':
        ## ファイル名, ファイルパスを自動生成
        filename = f'{datetime.now().strftime("%m")}_diary.json'
        diary_path = diaries_path / filename

        ## データを格納する変数を定義
        diary_filedata = None

        ## try-except文でファイルの存在やその中身が壊れてないかチェック
        ## エラーがなければデータを格納する変数にそのままjsonのデータが入る
        try:
            with open(diaries_path / filename, 'r', encoding='utf-8') as f:
                diary_filedata = json.load(f)

        ## ファイルがなかったら空配列を代わりに代入
        except FileNotFoundError:
            print('今月分の日記を格納するファイルが存在しません')
            print(f'次のファイルを新規作成します: {filename}')
            diary_filedata = []

        ## json構造が壊れてたらファイルごとバックアップしたうえでファイルがなかった時の動作を実行する
        ## (月)_diary.json -> (月)_diary_corrupt_(日)(時分秒).jsonという感じ
        ## ファイル名変更に何らかの理由で失敗した場合はデータが飛んでしまう可能性があるのでraise Exceptionで停止させる
        except json.JSONDecodeError as e:
            print(f'json構造が破損しています: [{e}]')
            print(f'ファイルをバックアップし、次のファイルを新規作成します: {filename}')
            try:
                backup_filename = diary_path.with_name(f'{datetime.now().strftime("%m")}_diary_corrupt_{datetime.now().strftime("%d%H%M%S")}.json')
                diary_path.rename(backup_filename)
            except Exception as e:
                print('予期しないエラーが発生しました:')
                raise Exception(e)
            diary_filedata = []

        ## jsonデータを用意
        diarydata = {
            'title': args.title,
            'date': datetime.now().strftime('%m/%d-%H:%M:%S'),
            'body': args.body,
            'tags': args.tags
        }

        ## 用意したdiarydataをfiledata配列に追加
        diary_filedata.append(diarydata)

        ## json.dumpを用いてデータをファイルに上書き保存
        try:
            with open(diaries_path / filename, 'w', encoding='utf-8') as f:
                json.dump(diary_filedata, f, ensure_ascii=False, indent=4)
            print('保存しました')
        except Exception as e:
            print('予期しないエラーが発生しました:')
            raise Exception(e)

    case _:
        ## 処理方法が決まってないので仮置き
        pass