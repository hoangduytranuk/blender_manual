import datetime
from time import gmtime, strftime
from pytz import timezone

class FunctionBase():
    timenow=None
    def __init__(self):
        self.__po_cat = None
        self.__changed = False
        self.__filename = None
        self.__file_count=1
        self.__change_count=0
        self.__master_cat = None

    def setLocalVars(self):
        pass

    @property
    def pofileCategory(self):
        return self.__po_cat

    @pofileCategory.setter
    def pofileCategory(self, c):
        self.__po_cat = c

    @pofileCategory.deleter
    def pofileCategory(self, c):
        del self.__po_cat


    @property
    def category(self):
        return self.__master_cat

    @category.setter
    def category(self, c):
        self.__master_cat = c

    @category.deleter
    def category(self, c):
        del self.__master_cat

    @property
    def fileCount(self):
        return self.__file_count

    @fileCount.setter
    def fileCount(self, increment=1):
        self.__file_count += increment

    @fileCount.deleter
    def fileCount(self):
        self.__file_count = 0

    @property
    def changesCount(self):
        return self.__change_count

    @changesCount.setter
    def changesCount(self, increment=1):
        self.__change_count += increment

    @changesCount.deleter
    def changesCount(self, increment=1):
        self.__change_count = 0

    @property
    def fileName(self):
        return self.__filename

    @fileName.setter
    def fileName(self, file_name):
        self.__filename = file_name

    @fileName.deleter
    def fileName(self, file_name):
        del self.__filename

    @property
    def changed(self):
        return self.___changed

    @changed.setter
    def changed(self, value):
        self.___changed = value

    @changed.deleter
    def changed(self):
        del self.___changed

    def timeNow(self):
        if (FunctionBase.timenow == None):
            local_time=timezone('Europe/London')
            fmt='%Y-%m-%d %H:%M%z'
            loc_dt=local_time.localize(datetime.datetime.now())
            formatted_dt=loc_dt.strftime(fmt)
            FunctionBase.timenow = formatted_dt
        return FunctionBase.timenow


    def run(self):
        pass


