# Get Tension

テニスとバドミントン愛好家の皆さんへ。
パソコンでこのアプリケーションを使うと、ラケットの面を叩いた音からラケットのテンションを測定できます。
張った直後の音を学習したAIが現在のラケットのテンションを推定します。
Mac, Windows, Linuxで動作し、
Pythonで書かれています。

![python powered](https://raw.githubusercontent.com/sugi-juku/get-tension/master/python-powered-w-200x80.png)

## Description

私のガット張りの店はCOVID-19のため2020年の春に約2ヶ月間休業しました。
そこで私は音からラケットのテンションを測定するアプリケーションを開発してみることにしました。

面圧(DT)を専用の計測機械で計測するという方法もあります。
でもガット張りを注文するときには張り機のテンションを指定することしかできません。
だから私は張り機のテンションで今何ポンドなのかを知りたいと思いました。

開発内容は以下の通りです。

1. AIの学習に必要な要素を考えました。例えばストリングの太さや素材、ストリングパターン、面の大きさなど。
1. 張った直後のラケットの面を叩いた音を録音し、学習データを集めました。
1. FFTを使って基本周波数を得ました。
1. Scikit-Learnの線形回帰モデルを使って、AIに学習データを学習させました。
1. 良いクラスを設計してみました。
1. CUI版がMac OS X Python 2.7.16で動作しました。
1. tkinterを使ってGUI版を開発してみました。
1. GUI版がMac OS X Python 2.7.16で動作しました。
1. Mac OS X Python 3.7.7で動作しました。
1. Appleは言っています。「Python 2.7を使うのはお勧めできません。このバージョンは過去のソフトウェアとの互換性のために含まれています。」そこで私はPython3を使うことにしました。
1. Ubuntu Python 3.7.5で動作しました。
1. Windows 10 Home Python 3.8.3で動作しました。

私はストリンガーでもありプログラマーでもあります。
かつてLinuxでPHPを使ったウェブアプリケーションをよく開発していました。
これは私の初めてのPythonアプリケーションです。
今ではPythonも大好きになりました。

## Requirement

Mac, Windows, LinuxのPython 3.6以上で動作すると思います。

### 動作確認済みの環境

* Mac OS X  Mojave 10.14.6 (私の開発環境)

    * python 3.7.7 - 3.7.8 (Homebrew)

* Ubuntu 19.10 - 20.04

    * pytyon 3.7.5 - 3.8.2

* Windows 10 Home 1909

    * python 3.8.3

## Installation

### Mac OS X

https://brew.sh/ からHomebrewをインストールします。

次にHomebrewでPython3をインストールします。

```
brew install python
```

次にPythonのモジュールをインストールします。

```
./install_python_modules_mac.sh
```

### Windows

https://www.python.org/downloads/ からWindows版Python 3.8.Xをインストールします。
もしあなたのパソコンがx86-64系なら、```Windows x86-64 executable installer``` 
をダウンロードしてインストールします。
次にPythonのモジュールをインストールします。```install_python_modules_win.bat```をダブルクリックして実行してください。 

### Ubuntu

PythonとPythonのモジュールをインストールします。

```
./install_python_modules_linux.sh
```

## Usage

Windowsを使っている場合は ```*.py``` ファイルをダブルクリックで実行できます。

- GUI版

    簡単に使えます。

    ```
    python3 get_tension_app.py
    ```

    上手く動かない場合は、マイクの感度を上げてみてください。

    Macを使っているなら ```get_tension.command``` をダブルクリックしても実行できます。

- CUI版

    Windowsを使っている場合は ```python3``` を ```py``` に置き換えてください。

    - get_tension_data_append.py

        張った直後の場合はこれを使ってください。
        データが学習データに追加されます。
        例。

        ```
        python3 get_tension_data_append.py T_45-43_GOMS16-GOAKP16_98_16-19
        python3 get_tension_data_append.py B_25_YOBG66UM
        ```
    - get_tension_data_noappend.py

        現在のテンションを測定したい場合はこれを使ってください。
        例。

        ```
        python3 get_tension_data_noappend.py T_45-43_GOMS16-GOAKP16_98_16-19
        python3 get_tension_data_noappend.py B_25_YOBG66UM
        ```

        - 引数: Tennis

            ```
            Argument = T_{MainTension}-{CrossTension}_{MainString}-{CrossString}_{FaceSize}_{MainStringNumber}-{CrossStringNumber}

            if MainTension == CrossTension:
                Argument = T_{MainTension}_{MainString}-{CrossString}_{FaceSize}_{MainStringNumber}-{CrossStringNumber}

            if MainString == CrossString:
                Argument = T_{MainTension}-{CrossTension}_{MainString}_{FaceSize}_{MainStringNumber}-{CrossStringNumber}
            ```

        - 引数: Badminton

            ```
            Argument = B_{MainTension}-{CrossTension}_{MainString}-{CrossString}

            if MainTension == CrossTension:
                Argument = B_{MainTension}_{MainString}-{CrossString}
            
            if MainString == CrossString:
                Argument = B_{MainTension}-{CrossTension}_{MainString}
            ```

    - get_tension_from_wav.py

        wavファイルからテンションを測定します。
        {wavfilename} は get_tension_from_wav.py からの相対パスで指定してください。

        ```
        python3 get_tension_from_wav.py {wavfilename}
        ```

    - plt_data.py

        学習データをグラフで見ることができます。
        fit_lr.py の内容を含んでいます。

        ```
        python3 plt_data.py
        ```

    - plt_tension_change.py

        対象ディレクトリの中のwavファイルからテンションの変化をグラフ化します。
        例。

        ```
        python3 plt_tension_change.py tmp/sample
        ```

    - fit_lr.py

        学習データを使って学習を行います。
        cronで定期的に実行するとよいでしょう。

    - remake_stdata.py

        wavファイルから学習データを作り直します。
        通常は使う必要はありません。


## Author

* Yukihiko Sugimura
* E-Mail : sugimura_juku@yahoo.co.jp
* https://sugi-juku.com
* https://tennis.sugi-juku.com

## Licence

Copyright (c) 2020 Yukihiko Sugimura

Released under the [MIT license](https://opensource.org/licenses/mit-license.php).