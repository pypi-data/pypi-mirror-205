class PropertiesConverter:
    def __init__(self, *, strict=False):
        self.strict = strict
        self.registry = {}

    def register(self, key, callback):
        self.registry[key] = callback
        return self  # make method chainable

    def __call__(self, item):
        unhandled = set(item.keys())
        for key, callback in self.registry.items():
            unhandled.discard(key)
            key_exists = key in item
            try:
                original_value = item.get(key)
                value = callback(original_value)

                # If value did not change we can continue with the next property.
                #
                # This catches even the case, that the original value is None
                # because the key did not exist and the new value is None, too.
                # In this case we do not want to add a property with a null
                # value and can continue with the next property.
                if value == original_value and type(value) == type(original_value):
                    continue

                item[key] = value

                details = {"key": key}
                if key_exists:
                    details["originalValue"] = original_value
                    item.log.info("Transformed property", **details)
                else:
                    item.log.info("Added property", **details)

            except Exception as e:
                details = dict(key=key, error=type(e).__name__, message=str(e))
                if key_exists:
                    item.log.error("Transformation error", **details)
                else:
                    item.log.error("Adding error", **details)

        if self.strict:
            if len(unhandled) > 0:
                item.log.warning("Unhandled keys", keys=sorted(unhandled))

        return item
