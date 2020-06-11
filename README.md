# Get Tension

For people who love Tennis and Badminton.
You can get racket string tension from sound by hitting your racket face.
AI learn stringing data just finished stringing, and estimate current racket string tension.
It is written by Python.

## Description

My stringing shop was closed for COVID-19 in Spring 2020.
Then I decided to develop an application getting racket string tension from sound with Python.

The work is as follows.

1. I recorded racket string sound just finished stringing and gathered training data.
1. I got fundamental frequency from sound by FFT.
1. I tried to let AI learn training data by sciket-learn Linear Regression.
1. I tried to design good classes.
1. CUI version was working on Python 2.7.16.
1. I tried to add GUI by tkinter.
1. GUI version was working on Python 2.7.16.
1. Python 3.7.7 was supported.

I\'m both a stringer and a programmer.
I used to develop web applications often with PHP.
This is my first Python application.
Now, I love Python, too.

## Requirement

Maybe it works python 2.7.X or python 3.7.X.


My development environment

* Mac OS X  Mojave 10.14.6
* python 2.7.16
* python 3.7.7

## Installation

For example, install python modules for Mac OS X.

```bash
sudo easy_install pip
pip install numpy
pip install matplotlib
pip install pyaudio
pip install sklearn
```

## Usage

- GUI version

    ```bash
    python get_tension_app.py
    ```

- CUI version

    - Append training data version

        If you have just finished stringing, use this version.

        Because making an argument is not easy, I recommend GUI version.

        For example

        ```bash
        python get_tension_data_append.py T_45-43_GOMS16-GOAKP16_98_16-19
        python get_tension_data_append.py B_25_YOBG66UM
        ```
    - NOT append training data version

        If you want to get current tension, use this version.

        For example

        ```bash
        python get_tension_data_noappend.py T_45-43_GOMS16-GOAKP16_98_16-19
        python get_tension_data_noappend.py B_25_YOBG66UM
        ```


        - Argument: Tennis

            ```bash
            Argument = T_{MainTension}-{CrossTension}_{MainString}-{CrossString}_{FaceSize}_{MainStringNumber}-{CrossStringNumber}

            if MainTension == CrossTension:
                Argument = T_{MainTension}_{MainString}-{CrossString}_{FaceSize}_{MainStringNumber}-{CrossStringNumber}

            if MainString == CrossString:
                Argument = T_{MainTension}-{CrossTension}_{MainString}_{FaceSize}_{MainStringNumber}-{CrossStringNumber}
            ```

        - Argument: Badminton

            ```bash
            Argument = B_{MainTension}-{CrossTension}_{MainString}-{CrossString}

            if MainTension == CrossTension:
                Argument = B_{MainTension}_{MainString}-{CrossString}
            
            if MainString == CrossString:
                Argument = B_{MainTension}-{CrossTension}_{MainString}
            ```

    - Get racket tension from wavfile

        {wavfilename} is filename with a relative path from get_tension_from_wav.py.

        ```bash
        python get_tension_from_wav.py {wavfilename}
        ```

    - Show training data

        ```bash
        python plt_data.py
        ```

    - Show tension change

        You can see tension change from wavfile in target directory.

        For example

        ```bash
        python plt_tension_change.py tmp/sample
        ```

## Author

* Yukihiko Sugimura
* E-Mail : sugimura_juku@yahoo.co.jp
* https://sugi-juku.com
* https://tennis.sugi-juku.com

## Licence

Copyright (c) 2020 Yukihiko Sugimura

Released under the [MIT license](https://opensource.org/licenses/mit-license.php).
