import re

class ContentParser:
    def __init__(self):
        self.us_dollar_pattern=r'US\$\s*([\d,]+\.?\d*)'
        self.cagr_value_pattern=r'CAGR of (\d+\.?\d*)%'
        self.title_pattern = r'Global (.*?) Market'
        self.summary_pattern = r'^(.*?)\s*The global'

        pass

    def parser_first_ph(self, content):
        # 使用条件语句处理美元值匹配
        us_dollar_match = re.search(self.us_dollar_pattern, content)
        us_dollar_value = us_dollar_match.group(1) if us_dollar_match else ""

        # 使用条件语句处理CAGR值匹配
        cagr_match = re.search(self.cagr_value_pattern, content)
        cagr_value = cagr_match.group(1) if cagr_match else ""

        # 使用条件语句处理摘要匹配
        summary_match = re.search(self.summary_pattern, content)
        summary = summary_match.group(1) if summary_match else ""

        return us_dollar_value, cagr_value,self.clean_string(summary)

    def parser_title(self,content):
        title = re.search(self.title_pattern, content).group(1)
        return title

    def clean_string(self,s):
        return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', str(s))

    def parser_table(self,table):
        contents = table.split('\n')
        company_text=''
        type_text=''
        application_text=''
        for index, content in enumerate(contents):
            if 'Companies Covered' in content:
                company_text=contents[index+1]
            elif 'by Type' in content:
                for i in range(index+1, len(contents)):
                    if 'by Application' in contents[i]:
                        break
                    type_text+=contents[i]+'\r\n'
            elif 'by Application' in content:
                for i in range(index+1, len(contents)):
                    if contents[i]=='Forecast Units':
                        break
                    application_text+=contents[i]+'\r\n'
        company_text=company_text.replace(', ','\r\n')
        return company_text,type_text,application_text




