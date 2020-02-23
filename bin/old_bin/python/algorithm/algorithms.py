import sys
from comparator import DefaultComparator

class Algo:

    def position(sorted_list , item_to_find , cmp=None) -> int:
        if (cmp == None):
            return None

        #print("sorted_list: {}, len:{}".format(sorted_list, len(sorted_list)))
        lo  = 0
        hi  = len(sorted_list)
        mid = -1
        while (lo < hi):
            mid  = (lo + hi) // 2
            item_on_sorted_list = sorted_list[mid]
            #print("mid:{}, item_on_sorted_list: {}".format(mid, item_on_sorted_list))
            comp_val = cmp.compare(item_on_sorted_list, item_to_find)
            if (comp_val == 0):
                return [mid, mid]
            elif (comp_val < 0):
                lo = mid + 1  # range in the higher part
            else:
                hi = mid  # range in the lower part
        return [-1, mid]

    # -----------------------------------------------------------------------------
    # binarySearch
    # Use this function to search a sorted list to enhance the speed of execution
    # You might need to write your own compare (cmp) function, follow the example above
    #
    def binarySearch(sorted_list , item_to_find , cmp=None) -> object:
        if (cmp == None):
            return None
        found_object  = None

        find_index, mid = Algo.position(sorted_list, item_to_find, cmp)
        is_found = (find_index >= 0)
        if (is_found):
            found_object = sorted_list[find_index]
        #return found_object

    def findInsertPosition(sorted_list , item_to_find , cmp=None) -> int:
        """
        Find the position to insert the item at the found index. The item should insert AFTER
        the index returned.

        :param item_to_find: Item used to find position for.
        :param cmp: Function to compare the item (f(x, y): x < y => -1; x > y => 1; x = y => 0. x is the item on the list and y is item_to_find.
        :return: -2 if compare function is not provided. -1 if the position should be before the entire list, 0 is after the first item, len-1 is to insert after the list
        """
        if (cmp == None):
            return -2

        find_index, mid = Algo.position(sorted_list, item_to_find, cmp)
        item_at_mid = sorted_list[mid]
        comp_value = cmp.compare(item_at_mid, item_to_find)
        if (comp_value > 0):
            find_index = (mid - comp_value)
        return find_index
