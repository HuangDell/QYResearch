import re

class ContentParser:
    def __init__(self):
        self.us_dollar_pattern=r'US\$\s*([\d,]+\.?\d*)'
        self.cagr_value_pattern=r'CAGR of (\d+\.?\d*)%'
        self.title_pattern = r'Global (.*?) Market Report'
        self.summary_pattern = r'^(.*?)\s*The global'

        pass

    def parser_first_ph(self,content):
        us_dollar_value = re.search(self.us_dollar_pattern, content).group(1)

        cagr_value = re.search(self.cagr_value_pattern, content).group(1)

        summary = re.search(self.summary_pattern, content).group(1)

        return us_dollar_value, cagr_value,summary

    def parser_title(self,content):
        title = re.search(self.title_pattern, content).group(1)
        return title

