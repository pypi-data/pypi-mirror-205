import copy
import logging


def flatten(item, prefix=""):
    flat_dict = {}
    for k, v in item.items():
        kk = k
        if prefix:
            kk = prefix + "." + k

        if type(v) is dict:
            for ksub, vsub in flatten(v, kk).items():
                flat_dict[ksub] = vsub
        else:
            flat_dict[kk] = v
    return flat_dict


class ItemLogEntry:
    def __init__(self, _level, _message, **details):
        self.level = _level
        self.message = _message
        self.details = details

    def __repr__(self):
        d = "".join([", {}={}".format(k, repr(v)) for k, v in self.details.items()])
        return "ItemLogEntry(logging.{}, {}{})".format(
            logging.getLevelName(self.level), repr(self.message), d
        )

    def __contains__(self, key):
        return key in self.details

    def __getitem__(self, key):
        return self.details[key]


class ItemLog:
    def __init__(self):
        self.level = logging.NOTSET
        self.entries = []

    def log(self, _level, _message, **details):
        entry = ItemLogEntry(_level, _message, **details)
        self.entries.append(entry)
        if _level > self.level:
            self.level = _level

    def debug(self, _message, **details):
        self.log(logging.DEBUG, _message, **details)

    def info(self, _message, **details):
        self.log(logging.INFO, _message, **details)

    def warning(self, _message, **details):
        self.log(logging.WARNING, _message, **details)

    def error(self, _message, **details):
        self.log(logging.ERROR, _message, **details)

    def critical(self, _message, **details):
        self.log(logging.CRITICAL, _message, **details)

    def clone(self):
        log = ItemLog()
        log.level = self.level
        log.entries = copy.copy(self.entries)
        return log

    def __repr__(self):
        return "ItemLog(" + ", ".join([repr(entry) for entry in self.entries]) + ")"

    def __len__(self):
        return len(self.entries)

    def __add__(self, other):
        if type(other) != ItemLog:
            raise TypeError(
                "TypeError: unsupported operand type(s) for +: 'ItemLog' and '{}'".format(
                    type(other).__name__
                )
            )
        log = ItemLog()
        for entry in self:
            log.log(entry.level, entry.message, **entry.details)
        for entry in other:
            log.log(entry.level, entry.message, **entry.details)
        return log

    def __getitem__(self, index):
        return self.entries[index]


class Item(dict):
    """
    Item extends the dictionary class.

    Item behaves like a dict but provides additional functionality

    Each Item has an log list to report comments and incidents found while
    transforming, for example validation errors or import notes.

    Each Item has an empty dict of meta when being created. meta is
    used to track import information as the name of the file or the line
    number.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = ItemLog()
        self.meta = {}

    def clone(self):
        item = copy.copy(self)
        item.log = self.log.clone()
        item.meta = copy.copy(self.meta)
        return item

    def flatten(self):
        item = Item(flatten(self))
        item.log = self.log.clone()
        item.meta = copy.copy(self.meta)
        return item
