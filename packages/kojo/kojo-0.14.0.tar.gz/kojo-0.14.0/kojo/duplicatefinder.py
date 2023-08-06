class DuplicateFinder:
    def __init__(self, create_uniq_callback):
        self.create_uniq_callback = create_uniq_callback
        self.uniqs = {}

    def __call__(self, item):
        uniq = self.create_uniq_callback(item)
        if uniq in self.uniqs:
            item.log.error("Found duplicate(s)", duplicates=[*self.uniqs[uniq]])
            self.uniqs[uniq].append(item)
        else:
            self.uniqs[uniq] = [item]
        return item
