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
    _resolution = Literal["1/1", "1/2a", "1/2b", "1/4", "1/8", "1/16", "1/32"]

    def __init__(self, DMODE0, DMODE1, DMODE2, CLK, ENABLE, DIR, LO1=None, LO2=None, AGC0=None, AGC1=None):
        self.DMODE0 = DMODE0
        self.DMODE1 = DMODE1
        self.DMODE2 = DMODE2
        self.CLK = CLK
        self.ENABLE = ENABLE
        self.DIR = DIR
        self.LO1 = LO1
        self.LO2 = LO2
        self.AGC0 = AGC0
        self.AGC1 = AGC1
        self.output = gpio.OUT
        self.input = gpio.IN
        self.low = gpio.LOW
        self.high = gpio.HIGH
        self.direction_set = {"CW": self.high,
                              "CCW": self.low}
        self.direction = self.direction_set["CW"]
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)


    def turning_direction(self, direction: _direction = "CW", args=_direction):
        exist_direction = get_args(args)
        assert direction in exist_direction, f"'{direction}' is not in {exist_direction}"
        self.direction = self.direction_set[direction]
        gpio.output(self.DIR, self.direction)

    def base_config(self):
        gpio.setup(self.DMODE0, self.output)
        gpio.setup(self.DMODE1, self.output)
        gpio.setup(self.DMODE2, self.output)
        gpio.setup(self.CLK, self.output)
        gpio.setup(self.DIR, self.output)
        gpio.setup(self.ENABLE, self.output)
        if self.LO1 is not None:
            gpio.setup(self.LO1, self.input)
        if self.LO2 is not None:
            gpio.setup(self.LO2, self.input)
        if self.AGC0 is not None:
            gpio.setup(self.AGC0, self.output)
        if self.AGC1 is not None:
            gpio.setup(self.AGC1, self.output)

    def mode(self, resolution: _resolution = "1/1", args=_resolution):
        exist_mode = get_args(args)
        assert resolution in exist_mode, f"'{resolution}' is not in {exist_mode}"
        if resolution == "1/1":
            gpio.output(self.DMODE0, self.low)
            gpio.output(self.DMODE1, self.low)
            gpio.output(self.DMODE2, self.high)
        if resolution == "1/2a":
            gpio.output(self.DMODE0, self.low)
            gpio.output(self.DMODE1, self.high)
            gpio.output(self.DMODE2, self.low)
        if resolution == "1/2b":
            gpio.output(self.DMODE0, self.high)
            gpio.output(self.DMODE1, self.low)
            gpio.output(self.DMODE2, self.low)
        if resolution == "1/4":
            gpio.output(self.DMODE0, self.low)
            gpio.output(self.DMODE1, self.high)
            gpio.output(self.DMODE2, self.high)
        if resolution == "1/8":
            gpio.output(self.DMODE0, self.high)
            gpio.output(self.DMODE1, self.low)
            gpio.output(self.DMODE2, self.high)
        if resolution == "1/16":
            gpio.output(self.DMODE0, self.high)
            gpio.output(self.DMODE1, self.high)
            gpio.output(self.DMODE2, self.low)
        if resolution == "1/32":
            gpio.output(self.DMODE0, self.high)
            gpio.output(self.DMODE1, self.high)
            gpio.output(self.DMODE2, self.high)

