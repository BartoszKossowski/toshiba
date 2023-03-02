#!/usr/bin/python

from typing import Literal, get_args
import RPi.GPIO as gpio

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
        self.LO1 = LO1
        self.LO2 = LO2
        self.AGC0 = AGC0
        self.AGC1 = AGC1
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)

    def turning_direction(self, direction: _direction = "CW", args=_direction):
        exist_direction = get_args(args)
        assert direction in exist_direction, f"'{direction} is not in {exist_direction}'"
        self.direction = direction

    def base_config(self):
        gpio.setup(self.DMODE0, gpio.OUT)
        gpio.setup(self.DMODE1, gpio.OUT)
        gpio.setup(self.DMODE2, gpio.OUT)
        gpio.setup(self.CLK, gpio.OUT)
        gpio.setup(self.DIR, gpio.OUT)
        gpio.setup(self.ENABLE, gpio.OUT)
        if self.LO1 is not None:
            gpio.setup(self.LO1, gpio.IN)
        if self.LO2 is not None:
            gpio.setup(self.LO2, gpio.IN)
        if self.AGC0 is not None:
            gpio.setup(self.AGC0, gpio.OUT)
        if self.AGC1 is not None:
            gpio.setup(self.AGC1, gpio.OUT)






print("moje hocki klocki")
