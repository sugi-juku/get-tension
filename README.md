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
1. Python 3.7.6 was supported.

I\'m both a stringer and a programmer.
I used to develop web applications often with PHP.
This is my first Python application.
Now, I love Python, too.

## Requirement

Maybe it works python 2.7.X or python 3.7.X.


My development environment

* macOS Mojave 10.14.6
* python 2.7.16
* python 3.7.6

## Installation

For example, install python modules for macOS.

```bash
sudo easy_install pip
sudo pip install numpy
sudo pip install matplotlib
sudo pip install pyaudio
sudo pip install sklearn
```

## Usage

- GUI version

    ```bash
    python get_tension_app.py
    ```

- CUI version

    - Record sound

        For example

        ```bash
        python record.py T_45-43_GOMS16-GOAKP16_98_16-19
        python record.py B_25_YOBG66UM
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

    - Get racket tension

        ```bash
        python get_tension.py {wavfilename}
        ```

    - Show training data

        ```bash
        python plt_data.py
        ```

## Author

* Yukihiko Sugimura
* Sugimura private-tutoring school
* Sugimura stringing shop
* E-Mail : sugimura_juku@yahoo.co.jp

## Licence

Copyright (c) 2020 Yukihiko Sugimura

Released under the [MIT license](https://opensource.org/licenses/mit-license.php).
