#!/usr/bin/python

from typing import Literal, get_args

"""
main.py to będzie główny blok do zarządzania
początek jest jaki jest bo będzie to na linuxa
i to na razie na tyle będzie z tego, czas lutować i pomału zapisywać co będzie potrzebne do odbierania a co do nadawania sygnału

Tutaj stworzymy bibliotekę do sterowania hardware-owo sterownikiem
"""


class TB67S249FTG:

    # constans
    """
    Wybór rodzaju rozdzielczości:
    DMODE0
    DMODE1
    DMODE2

    Nadawania obrotów impulsami:
    CLK

    Włączanie silnika (ON/OFF)
    ENABLE

    Kierunek kręcenia wirnika:
    CW/CCW
    na razie jako DIR

    Na None jak na razie:
    AGC0 / AGC1 / LO1 / LO2
    """

    _direction = Literal["CW", "CCW"]

    def __init__(self, DMODE0, DMODE1, DMODE2, CLK, ENABLE, DIR, LO1=None, LO2=None, AGC0=None, AGC1=None):
        self.DMODE0 = DMODE0
        self.DMODE1 = DMODE1
        self.DMODE2 = DMODE2
        self.CLK = CLK
        self.ENABLE = ENABLE
        self.DIR = DIR
        self.direction = None

    def turning_direction(self, direction: _direction = "CW", args=_direction):
        exist_direction = get_args(args)
        assert direction in exist_direction, f"'{direction} is not in {exist_direction}'"
        self.direction = direction

    def base_config(self):
        pass





print("moje hocki klocki")
