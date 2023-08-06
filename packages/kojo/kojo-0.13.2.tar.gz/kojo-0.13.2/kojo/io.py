import csv
import itertools
import json
import os

from .item import Item


class CSVReader:
    """Read a CSV line by line

    CSVReader reads the header and then yields each line as an Item, where the
    keys are taken from the header and the values from the line. All values are
    of type string.
    """

    def __init__(self, path, **reader_options):
        self.path = path
        self.fp = open(self.path, "r")
        self.iterator = csv.reader(self.fp, **reader_options)
        self.headers = next(self.iterator)
        self.index = 0

    def __del__(self):
        self.fp.close()

    def __next__(self):
        row = next(self.iterator)
        item = Item({self.headers[i]: cell for (i, cell) in enumerate(row)})
        item.meta["filename"] = os.path.basename(self.path)
        item.meta["index"] = self.index
        self.index += 1
        return item

    def __iter__(self):
        return self


class CSVWriter:
    def write(self, iterator, filename):
        keys = []
        iter0, iter1 = itertools.tee(iterator, 2)

        for item in iter0:
            k = list(filter(lambda k: k not in keys, item.keys()))
            keys += k

        with open(filename, "w") as file:
            writer = csv.writer(file)
            writer.writerow(keys)

            for item in iter1:
                row = [item.get(k, "") for k in keys]
                writer.writerow(row)


class NDJSONReader:
    """Read a NDJSON file line by line

    NDJSONReader reads a file and yields each line interpreted as JSON.
    """

    def __init__(self, path):
        self.path = path
        self.fp = open(self.path, "r")
        self.index = 0

    def __del__(self):
        self.fp.close()

    def __next__(self):
        line = next(self.fp)
        try:
            item = Item(json.loads(line))
        except Exception as e:
            item = Item()
            item.log.critical(
                "Could not parse JSON", error=type(e).__name__, message=str(e)
            )

        item.meta["filename"] = os.path.basename(self.path)
        item.meta["index"] = self.index
        self.index += 1
        return item

    def __iter__(self):
        return self
