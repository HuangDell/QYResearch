from src.util.report_manager import ReportExcelWriter
from src.util.record_manager import RecordItemManager
from src.util.config import config

report_writer = ReportExcelWriter(config.get_filename())
record_writer = RecordItemManager(config.get_record_file())


