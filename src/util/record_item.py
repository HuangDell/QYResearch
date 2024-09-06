
"""
用于表示上次爬取的页面和索引的数据结构，
"""
class RecordItem:
    def __init__(self, page=1, index=0):
        self._page = page
        self._index = index

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        if not isinstance(value, int):
            raise ValueError("Page must be an integer")
        if value < 1:
            raise ValueError("Page must be greater than or equal to 1")
        self._page = value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if not isinstance(value, int):
            raise ValueError("Index must be an integer")
        if value < 0 or value > 9:
            raise ValueError("Index must be between 0 and 9 (inclusive)")
        self._index = value

    def __str__(self):
        return f"RecordItem(page={self._page}, index={self._index})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {"page": self._page, "index": self._index}

    @classmethod
    def from_dict(cls, data):
        return cls(data["page"], data["index"])
