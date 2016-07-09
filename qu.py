#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: test.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-07-09 22:02:42 (CST)
# Last Update:星期日 2016-7-10 2:6:25 (CST)
#          By:
# Description:
# **************************************************************************
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "s, q"
tags = "Draw, Line"

import cocos
from cocos.director import director
from cocos import draw
import pyglet
import math
from cocos.actions import *


class TestFigure(draw.Canvas):
    def render(self):
        x, y = director.get_window_size()
        self.set_color((255, 0, 255, 255))
        self.set_stroke_width(10)
        self.move_to((20, 398))  # start
        self.line_to((20, 402))  # end
        self.move_to((400, 398))  # start
        self.line_to((400, 402))  # end
        self.set_color((255, 255, 0, 255))
        self.move_to((20, 8))  # start
        self.line_to((20, 12))  # end
        self.move_to((400, 8))  # start
        self.line_to((400, 12))  # end


class MouseDisplay(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(MouseDisplay, self).__init__()

        self.text = cocos.text.Label('提醒', font_size=18, x=100, y=420)
        self.add(self.text)

        self.spt = []
        self.pos = [(20, 20), (20, 400), (400, 20), (400, 400), (190, 190)]
        self.num = 0
        for i in [20, 400]:
            sprite = cocos.sprite.Sprite('2.png')
            sprite.scale = 0.1
            sprite.position = i, 400
            self.add(sprite, z=1)
            self.spt.append(sprite)

        for i in [20, 400]:
            sprite = cocos.sprite.Sprite('3.png')
            sprite.position = i, 20
            sprite.scale = 0.1
            self.add(sprite, z=1)
            self.spt.append(sprite)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.num += 1
        if self.num == 1:
            # 按下第一次时得到棋子
            self.chess = self.get_chess(x, y)
        else:
            # 按下第二次时移动
            self.num = 0
            self.move_chess(x, y)

    def get_chess(self, x, y):
        for spt in self.spt:
            a, b = spt.position
            c = (400 - 20) / 4
            if c > abs(x - a) and c > abs(y - b):
                return spt

    def move_chess(self, x, y):
        if x <= (400 - 20) / 4:
            if y <= (400 - 20) / 4:
                a, b = 20, 20
            else:
                a, b = 20, 400
        elif x >= 3 * (400 - 20) / 4:
            if y <= (400 - 20) / 4:
                a, b = 400, 20
            else:
                a, b = 400, 400
        else:
            c = (400 - 20) / 2
            a, b = c, c
        aa = []
        for i in self.spt:
            aa.append(i.position)
        cc = self.can_move_place()
        for i in aa:
            if i in cc:
                cc.remove(i)
        if (a, b) not in cc:
            self.text.element.text = '移动错误'
        else:
            self.chess.position = director.get_virtual_coordinates(a, b)
        self.pos = [(20, 20), (20, 400), (400, 20), (400, 400), (190, 190)]

    def can_move_place(self):
        a, b = self.chess.position
        if (a, b) == (20, 20):
            can_place = [(20, 400), (400, 20), (190, 190)]
        elif (a, b) == (20, 400):
            can_place = [(20, 20), (400, 400), (190, 190)]
        elif (a, b) == (400, 20):
            can_place = [(20, 20), (190, 190)]
        elif (a, b) == (400, 400):
            can_place = [(20, 400), (190, 190)]
        else:
            can_place = [(20, 400), (20, 20), (400, 400), (400, 20)]
        return can_place



class TestLayer(cocos.layer.Layer):
    def __init__(self):
        super(TestLayer, self).__init__()
        line = draw.Line((20, 20), (400, 400), (255, 255, 255, 255))
        self.add(line)
        line = draw.Line((20, 400), (400, 400), (255, 255, 255, 255))
        self.add(line)
        line = draw.Line((20, 20), (400, 20), (255, 255, 255, 255))
        self.add(line)
        line = draw.Line((20, 20), (20, 400), (255, 255, 255, 255))
        self.add(line)
        line = draw.Line((20, 400), (400, 20), (255, 255, 255, 255))
        self.add(line)

        # self.add(TestFigure())
        # self.schedule(lambda x: 0)


def main():
    director.init()
    test_layer = TestLayer()
    a = MouseDisplay()
    main_scene = cocos.scene.Scene(test_layer, a)
    director.run(main_scene)


if __name__ == '__main__':
    main()
