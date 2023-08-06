def apply(iterable, *processes):
    for item in iterable:
        item = apply_on_item(item, *processes)
        if item is not None:
            yield item


def apply_on_item(item, *processes):
    for process in processes:
        for step in process.steps:
            if item is None:
                return None
            item = step(item)
    return item


class MapStep:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, item):
        return self.fn(item)


class FilterStep:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, item):
        keep = self.fn(item)
        return item if keep else None


class Process:
    def __init__(self):
        self.steps = []

    def map(self, fn):
        self.steps.append(MapStep(fn))
        return self

    def filter(self, fn):
        self.steps.append(FilterStep(fn))
        return self

    def run(self, iterator):
        return apply(iterator, self)
