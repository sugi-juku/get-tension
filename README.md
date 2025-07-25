# Get Tension

For people who love Tennis and Badminton.
This is an application for estimating racket string tension with AI.
You can get racket string tension from the sound by hitting your racket face.
AI learns sounds just finished stringing and predicts current racket string tension.
It works on Mac, Windows, Linux.
It is written in Python.
By default, training data is my stringing data. If you are a stringer, you can use your own stringing data and get your own tension, too.

![python powered](https://raw.githubusercontent.com/sugi-juku/get-tension/master/python-powered-w-200x80.png)

## Description

My stringing shop was closed about 2 months for COVID-19 in Spring 2020.
So I decided to develop an application getting racket string tension from sound.

There is also a method of measuring Dynamic Tension (DT) with a dedicated measuring machine.
But when you order stringing, you can only specify the tension of the stringing machine.
So I want to know what the tension of the stringing machine is now.

The work is as follows.

1. I assumed that the racket string sound just finished stringing showed the machine tension.
1. I considered the elements necessary for learning. For example, the sound hitting racket face, string diameter, string material, stringing pattern, racket face size, etc.
1. I recorded racket string sounds just finished stringing and gathered training data.
1. I got fundamental frequency from sounds by FFT.
1. I tried to let AI learn training data set by scikit-learn Linear Regression.
1. I tried to design good classes.
1. CUI version worked on macOS Python 2.7.16.
1. I tried to add GUI with tkinter.
1. GUI version worked on macOS Python 2.7.16.
1. It worked on macOS Python 3.7.7.
1. Apple says "Use of Python 2.7 isn\'t recommended as this version is include in macOS for compatibility with legacy software.". So I decided to use Python3.
1. It worked on Ubuntu Python 3.7.5.
1. It worked on Windows 10 Home Python 3.8.3.

I\'m both a stringer and a programmer.
I used to develop web applications often with PHP at several major IT companies.
This is my first application with Python.
Now, I love Python, too.

## Requirement

Maybe it works on Python 3.6 or higher.
It works on Mac, Windows, Linux.
### Tested environment

* macOS Intel 10.14.6 - 13.4.1 (My development environment)

    * python 3.7.7 - 3.9.13

* Ubuntu 19.10 - 20.04 - 22.04

    * pytyon 3.7.5 - 3.10.6

* Windows 10 Home 1909

    * python 3.8.3

## Installation

Download from https://github.com/sugi-juku/get-tension and deploy your PC.

For example.

```
git clone https://github.com/sugi-juku/get-tension.git
```

### Python and Python modules

#### macOS

Install Python3.X for macOS from https://www.python.org/downloads/ .

Then, Install python modules.

```
./install_python_modules_mac.sh
```

#### Windows

Install Python3.X for Windows from https://www.python.org/downloads/ .
If your PC is x86-64, download and install  ```Windows x86-64 executable installer``` .

Then install python modules. Double click ```install_python_modules_win.bat``` .

#### Ubuntu

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

    ![app top image](https://raw.githubusercontent.com/sugi-juku/get-tension/master/app_top.png)

    If it doesn't work well, try to increase the sensitivity of the microphone.

    If you use macOS, you can run ```get_tension.command``` with a double click.

- CUI version

    If you are a stringer, try CUI version.
    Otherwise you don\'t have to use CUI version.

    If you use Windows, replace ```python3``` with ```py``` .

    - get_tension_data_append.py

        If you have just finished stringing, use this to get racket string tension.
        Data is appended to training data set.
        For example.

        ```
        python3 get_tension_data_append.py T_45-43_GOMS16-GOAKP16_98_16-19
        python3 get_tension_data_append.py B_25_YOBG66UM_56
        ```
    - get_tension_data_noappend.py

        If you want to get current racket string tension, use this.
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
            Argument = B_{MainTension}-{CrossTension}_{MainString}-{CrossString}_{FaceSize}

            if MainTension == CrossTension:
                Argument = B_{MainTension}_{MainString}-{CrossString}_{FaceSize}
            
            if MainString == CrossString:
                Argument = B_{MainTension}-{CrossTension}_{MainString}_{FaceSize}
            ```

    - get_tension_from_wav.py

        You can get racket string tension from wavfile.
        {wavfilename} is filename with a relative path from get_tension_from_wav.py.

        ```
        python3 get_tension_from_wav.py {wavfilename}
        ```

    - plt_data.py

        You can see graphs of training data set.
        This includes fit_lr.py.

        ```
        python3 plt_data.py
        ```

    - plt_tension_change.py

        You can see a graph of tension change from wavfile in target directory.
        For example.

        ```
        python3 plt_tension_change.py tmp/sample
        ```

        ![GOSEN AK PRO 16](https://raw.githubusercontent.com/sugi-juku/get-tension/master/GOAKP16.png)

    - fit_lr.py

        Linear model is fitted by training data set.
        It is good to run this regularly using cron.

    - remake_stdata.py

        You can remake training data set from wavfiles.
        Normally you don\'t have to use this.


## Author

* Yukihiko Sugimura
* E-Mail : sugimura_juku@yahoo.co.jp
* https://sugi-juku.com
* https://tennis.sugi-juku.com

## Licence

Copyright (c) 2020 Yukihiko Sugimura

Released under the [MIT license](https://opensource.org/licenses/mit-license.php).
