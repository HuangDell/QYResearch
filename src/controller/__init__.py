from src.util.recorder import ReportExcelWriter
from src.util.config import config

report_writer = ReportExcelWriter(config.get_filename())

