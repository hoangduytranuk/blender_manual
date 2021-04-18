class Key(str):
    def __init__(self, key):
        str.__init__(key)

    def __hash__(self):
        k = self.lower()
        key_len = len(k)
        k = (key_len, k)
        hash_value = hash(k)
        # dd(f'__hash__ key:[{k}], hash_value:{hash_value}')
        return hash_value

    def __eq__(self, other):
        local = self.lower()
        extern = other.lower()
        cond = (local == extern)
        # dd(f'__eq__ local:[{local}] extern:[{extern}]')
        return cond

    def __le__(self, other):
        local = self.lower()
        extern = other.lower()
        cond = (local < extern)
        # dd(f'__le__ local:[{local}] extern:[{extern}]')
        return cond

    def __gt__(self, other):
        local = self.lower()
        extern = other.lower()
        cond = (local > extern)
        # dd(f'__gt__ local:[{local}] extern:[{extern}]')
        return cond