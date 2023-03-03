#!/usr/bin/python

from typing import Literal, get_args
import RPi.GPIO as gpio


"""
main.py to będzie główny blok do zarządzania
początek jest jaki jest bo będzie to na linuxa
i to na razie na tyle będzie z tego, czas lutować i pomału zapisywać co będzie potrzebne do odbierania a co do nadawania sygnału

Tutaj stworzymy bibliotekę do sterowania hardware-owo sterownikiem

03.03.2023
Trzeba przebudować aplikację, aby błędy można było ładować jako jeden moduł i w razie błędu sygnalizować go jakoś - do tego utworzymy inną klasę (do błędów) i wykonamy dziedziczenie klas
"""


# def _errors(func):
#     def detect_flag():
#         if gpio.input(self.LO1) and not gpio.input(self.LO2):
#             print("Detected motor load open (OPD)")
#         if gpio.input(self.LO2) and not gpio.input(self.LO1):
#             print("Detect over current (ISD)")
#         if not gpio.input(self.LO1) and not gpio.input(self.LO2):
#             print("Detect over thermal (TSD)")
#
#     return detect_flag()


class _error_handler:
    def __init__(self, LO1, LO2, AGC0, AGC1, ELO1=None, ELO2=None):
        self.LO1 = LO1
        self.LO2 = LO2
        self.AGC0 = AGC0
        self.AGC1 = AGC1
        self.elo1 = ELO1
        self.elo2 = ELO2
        self.elo = bool
        self.output = gpio.OUT
        self.input = gpio.IN
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)

        if (self.elo1 is None and self.elo2 is not None) or (self.elo2 is None and self.elo1 is not None):
            raise AssertionError("All errors pins must be assignment")

        if self.elo2 and self.elo1:
            self.elo = True
            gpio.setup(self.elo1, self.output)
            gpio.setup(self.elo2, self.output)

        if self.LO1 is not None:
            gpio.setup(self.LO1, self.input)
        if self.LO2 is not None:
            gpio.setup(self.LO2, self.input)
        if self.AGC0 is not None:
            gpio.setup(self.AGC0, self.output)
        if self.AGC1 is not None:
            gpio.setup(self.AGC1, self.output)

    def detect_flag(self):
        if gpio.input(self.LO1) and not gpio.input(self.LO2):
            print("Detected motor load open (OPD)")
        if gpio.input(self.LO2) and not gpio.input(self.LO1):
            print("Detect over current (ISD)")
        if not gpio.input(self.LO1) and not gpio.input(self.LO2):
            print("Detect over thermal (TSD)")

    def error_out(self):
        pass


class TB67S249FTG (_error_handler):

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

    def __init__(self, DMODE0, DMODE1, DMODE2, CLK, ENABLE, DIR, LO1, LO2, AGC0, AGC1):
        super().__init__(LO1, LO2, AGC0, AGC1)
        self.DMODE0 = DMODE0
        self.DMODE1 = DMODE1
        self.DMODE2 = DMODE2
        self.CLK = CLK
        self.ENABLE = ENABLE
        self.DIR = DIR
        self.output = gpio.OUT
        self.input = gpio.IN
        self.low = gpio.LOW
        self.high = gpio.HIGH
        self.direction_set = {"CW": self.high,
                              "CCW": self.low}
        self.direction = self.direction_set["CW"]

        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)

        gpio.setup(self.DMODE0, self.output)
        gpio.setup(self.DMODE1, self.output)
        gpio.setup(self.DMODE2, self.output)
        gpio.setup(self.CLK, self.output)
        gpio.setup(self.DIR, self.output)
        gpio.setup(self.ENABLE, self.output)

        gpio.output(self.DIR, self.direction)
        gpio.output(self.ENABLE, self.low)
        gpio.output(self.DMODE0, self.low)
        gpio.output(self.DMODE1, self.low)
        gpio.output(self.DMODE2, self.high)

    def turning_direction(self, direction: _direction = "CW", args=_direction):
        exist_direction = get_args(args)
        assert direction in exist_direction, f"'{direction}' is not in {exist_direction}"
        self.direction = self.direction_set[direction]
        gpio.output(self.DIR, self.direction)

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

    def enable(self):
        gpio.output(self.ENABLE, self.high)

    def disable(self):
        gpio.output(self.ENABLE, self.low)

    def rotation(self):
        _error_handler.detect_flag(self)
        gpio.output(self.CLK, self.high)
        gpio.output(self.CLK, self.low)
