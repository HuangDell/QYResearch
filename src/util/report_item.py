
"""
    设置需要爬取的数据
"""
class ReportItem(object):
    def __init__(self):
        self._id = None
        self._date = None
        self._category = None
        self._link = None
        self._title = None
        self._year = 2024
        self._price = None
        self._pages = None
        self._million_digit = None
        self._cagr_digit = None
        self._summary_text = None
        self._company_text = None
        self._type_text = None
        self._application_text = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, value):
        self._pages = value

    @property
    def million_digit(self):
        return self._million_digit

    @million_digit.setter
    def million_digit(self, value):
        self._million_digit = value

    @property
    def cagr_digit(self):
        return self._cagr_digit

    @cagr_digit.setter
    def cagr_digit(self, value):
        self._cagr_digit = value

    @property
    def summary_text(self):
        return self._summary_text

    @summary_text.setter
    def summary_text(self, value):
        self._summary_text = value

    @property
    def company_text(self):
        return self._company_text

    @company_text.setter
    def company_text(self, value):
        self._company_text = value

    @property
    def type_text(self):
        return self._type_text

    @type_text.setter
    def type_text(self, value):
        self._type_text = value

    @property
    def application_text(self):
        return self._application_text

    @application_text.setter
    def application_text(self, value):
        self._application_text = value
