import os

from django.conf import settings

from openpyxl import load_workbook, Workbook

from .utils import today_for_filename


class ExportExcel(object):

    DEFAULT_FILENAME = "template-all.xlsx"
    SHEET_ADMISSION = 0
    SHEET_FOLLOWUP = 1
    SHEET_EXIT = 2
    SHEET_OTHER = 3

    def __init__(self, dao, filename=None, template=None):
        self._dao = dao
        self.filename = filename or "easynut.{}.xlsx".format(today_for_filename())
        self._load_workbook(template=template)

    def generate(self):
        """Populate all sheets."""
        self._populate_sheet_admission()
        self._populate_sheet_followup()
        self._populate_sheet_exit()
        self._populate_sheet_other()
        return self.book

    def get_sheet(self, index):
        return self.book.worksheets[index]

    def _load_workbook(self, template=None):
        """Create the workbook from a template file (located in ``EXPORT_TEMPLATES_DIR``)."""
        template_name = template or self.DEFAULT_FILENAME
        self.book = load_workbook(os.path.join(settings.EXPORT_TEMPLATES_DIR, template_name))

    def _populate_sheet_admission(self):
        sheet = self.get_sheet(self.SHEET_ADMISSION)
        return sheet

    def _populate_sheet_followup(self):
        sheet = self.get_sheet(self.SHEET_FOLLOWUP)
        return sheet

    def _populate_sheet_exit(self):
        sheet = self.get_sheet(self.SHEET_EXIT)
        return sheet

    def _populate_sheet_other(self):
        sheet = self.get_sheet(self.SHEET_OTHER)
        return sheet
