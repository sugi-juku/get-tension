# Get Tension

For people who love Tennis and Badminton.
You can get racket string tension from sound by hitting your racket face.
AI learns sound just finished stringing, and predicts current racket string tension.
It is written in Python.

![python powered](https://raw.githubusercontent.com/sugi-juku/get-tension/master/python-powered-w-200x80.png)

## Description

My stringing shop was closed 2 months for COVID-19 in Spring 2020.
Then I decided to develop an application getting racket string tension from sound.

The work is as follows.

1. I recorded racket string sound just finished stringing and gathered training data.
1. I got fundamental frequency from sound using FFT.
1. I tried to let AI learn training data using scikit-learn Linear Regression.
1. I tried to design good classes.
1. CUI version worked on Mac OS X Python 2.7.16.
1. I tried to add GUI using tkinter.
1. GUI version worked on Mac OS X Python 2.7.16.
1. It worked on Mac OS X Python 3.7.7.
1. It worked on Ubuntu Python 3.7.5.
1. Apple says "Use of Python 2.7 isn\'t recommended as this version is include in macOS for compatibility with legacy software.". So I decided to use Python3.
1. It worked on Windows 10 Python 3.8.3.

I\'m both a stringer and a programmer.
I used to develop web applications often with PHP.
This is my first Python application.
Now, I love Python, too.

## Requirement

Maybe it works on Python 3.6 or higher.

### Tested environment

* Mac OS X  Mojave 10.14.6 (My development environment)

    * python 3.7.7 (Homebrew)

* Ubuntu 19.10

    * pytyon 3.7.5

* Windows 10 Home

    * python 3.8.3

## Installation

### Mac OS X

Install Homebrew from https://brew.sh/

Then, install Python3 with Homebrew.

```
brew install python
```

Then, Install python modules.

```
./install_python_modules_mac.sh
```

### Windows

Install Python3.8.X for Windows from https://www.python.org/downloads/ .
If your PC is x86-64, download  ```Windows x86-64 executable installer``` .

Then install python modules. Double click ```install_python_modules_win.bat``` .

### Ubuntu

Install python and python modules.

```
./install_python_modules_linux.sh
```

## Usage

If you use Windows, you can run ```*.py``` with a double click.

- GUI version

    It is easy to use.

    ```
    python3 get_tension_app.py
    ```

    If it doesn't work well, try to increase the sensitivity of the microphone.

    If you use Mac OS X, you can run ```get_tension.command``` with a double click.

- CUI version

    - get_tension_data_append.py

        If you have just finished stringing, use this version.
        Data is appended to training data.
        For example.

        ```
        python3 get_tension_data_append.py T_45-43_GOMS16-GOAKP16_98_16-19
        python3 get_tension_data_append.py B_25_YOBG66UM
        ```
    - get_tension_data_noappend.py

        If you want to get current racket string tension, use this version.
        For example.

        ```
        python3 get_tension_data_noappend.py T_45-43_GOMS16-GOAKP16_98_16-19
        python3 get_tension_data_noappend.py B_25_YOBG66UM
        ```

        - Argument: Tennis

            ```
            Argument = T_{MainTension}-{CrossTension}_{MainString}-{CrossString}_{FaceSize}_{MainStringNumber}-{CrossStringNumber}

            if MainTension == CrossTension:
                Argument = T_{MainTension}_{MainString}-{CrossString}_{FaceSize}_{MainStringNumber}-{CrossStringNumber}

            if MainString == CrossString:
                Argument = T_{MainTension}-{CrossTension}_{MainString}_{FaceSize}_{MainStringNumber}-{CrossStringNumber}
            ```

        - Argument: Badminton

            ```
            Argument = B_{MainTension}-{CrossTension}_{MainString}-{CrossString}

            if MainTension == CrossTension:
                Argument = B_{MainTension}_{MainString}-{CrossString}
            
            if MainString == CrossString:
                Argument = B_{MainTension}-{CrossTension}_{MainString}
            ```

    - get_tension_from_wav.py

        You can get racket string tension from wavfile.
        {wavfilename} is filename with a relative path from get_tension_from_wav.py.

        ```
        python3 get_tension_from_wav.py {wavfilename}
        ```

    - plt_data.py

        You can see graphs of training data.
        This includes fit_lr.py.

        ```
        python3 plt_data.py
        ```

        If you use Windows.

        ```
        py -m plt_data
        ```

    - plt_tension_change.py

        You can see a graph of tension change from wavfile in target directory.
        For example.

        ```
        python3 plt_tension_change.py tmp/sample
        ```

        If you use Windows.

        ```
        py -m plt_tension_change tmp/sample
        ```

    - fit_lr.py

        Linear model is fitted by training data.
        It is good to run this regularly using cron.

    - remake_stdata.py

        You can remake training data from wavfiles.
        Normally you don\'t have to use it.


## Author

* Yukihiko Sugimura
* E-Mail : sugimura_juku@yahoo.co.jp
* https://sugi-juku.com
* https://tennis.sugi-juku.com

## Licence

Copyright (c) 2020 Yukihiko Sugimura

Released under the [MIT license](https://opensource.org/licenses/mit-license.php).
