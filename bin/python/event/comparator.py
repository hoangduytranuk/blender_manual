class Comparator:
    def compare(self, x, y):
        pass

class DefaultComparator(Comparator):

    def compare(self, x, y):
        if (x < y):
            return -1
        if (x > y):
            return 1
        else:
            return 0


