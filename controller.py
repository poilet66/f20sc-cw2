from typing import Dict, Callable

from enum import Enum, auto
class Event(Enum):
    A = auto()


class Controller:
    def __init__(self):
        self.listeners: Dict[Event, list[Callable[[], None]]] = {}
        self.plot_l_listeners = list[Callable[[list[float]], None]]


    
    def add_listener(self, event: Event, fn: Callable[[], None]):
        if self.listeners[event]:
            self.listeners[event].append(fn)
        else:
            self.listeners[event] = [fn]

    def call_listener(self, event: Event):
        listeners = self.listeners[event]
        if listeners:
            for listener in listeners:
                listener()




