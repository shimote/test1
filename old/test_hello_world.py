# -*- coding: utf-8 -*-

import hello_world

def test_get_hello_world_string():
    """
    get_hello_world_string関数が"Hello World"を返すかテストする
    """
    assert hello_world.get_hello_world_string() == "Hello World"