import pandas as pd
from typing import List
from report_item import ReportItem



class ReportExcelWriter:
    def __init__(self, filename: str):
        self.filename = filename
        self.df = None

    def write_items(self, items: List[ReportItem]):
        # 将 ReportItem 对象转换为字典列表
        data = []
        for item in items:
            data.append({
                'ID': item.id,
                'Date': item.date,
                'Category': item.category,
                'Link': item.link,
                'Title': item.title,
                'Year': item.year,
                'Price': item.price,
                'Pages': item.pages,
                'Million Digit': item.million_digit,
                'CAGR Digit': item.cagr_digit,
                'Summary Text': item.summary_text,
                'Company Text': item.company_text,
                'Type Text': item.type_text,
                'Application Text': item.application_text
            })

        # 创建 DataFrame
        self.df = pd.DataFrame(data)

    def save(self):
        if self.df is None:
            raise ValueError("No data to write.")

        # 创建一个 ExcelWriter 对象
        with pd.ExcelWriter(self.filename, engine='openpyxl') as writer:
            # 将 DataFrame 写入 Excel
            self.df.to_excel(writer, sheet_name='Report Items', index=False)

            # 获取 xlsxwriter 对象
            workbook = writer.book
            worksheet = writer.sheets['Report Items']

            # 设置列宽
            for i, col in enumerate(self.df.columns):
                column_len = max(self.df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.column_dimensions[chr(65 + i)].width = column_len

            # 设置表头格式
            for cell in worksheet["1:1"]:
                cell.font = cell.font.copy(bold=True)
                cell.alignment = cell.alignment.copy(horizontal='center')

            # 冻结首行
            worksheet.freeze_panes = 'A2'


# 使用示例
if __name__ == "__main__":
    # 假设我们有一些 ReportItem 实例
    report_items = [
        ReportItem(),
        ReportItem(),
    ]

    # 填充一些示例数据
    for i, item in enumerate(report_items):
        item.id = f"ID_{i + 1}"
        item.title = f"Report Title {i + 1}"
        item.date = "2023-05-20"
        item.category = "Category A"
        # ... 设置其他属性

    # 创建 Excel 写入器并写入数据
    writer = ReportExcelWriter("report_items_pandas.xlsx")
    writer.write_items(report_items)
    writer.save()
    print("Excel file has been created successfully using pandas.")
