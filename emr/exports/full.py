# -*- coding: utf-8 -*-
from openpyxl import Workbook

from ..models import DynamicRegistry

from .base import AbstractExportExcel


class ExportExcelFull(AbstractExportExcel):
    """Create an Excel file containing an export of the whole database."""

    DEFAULT_FILENAME = "easynut-full-export.xlsx"  # Default name for the file.

    def generate(self):
        """Generate the export."""
        self.book = Workbook()
        DynamicRegistry.load_models_config()

        # Loop over all models and fields config.
        for model_id, model_config in DynamicRegistry.models_config.iteritems():
            sheet = self.create_sheet(model_config.name)
            field_ids = []

            # Write headings.
            col = 0; row = 1  # NOQA
            for field_id, field_config in model_config.fields_config.iteritems():
                col += 1
                sheet.cell(column=col, row=row).value = field_config.name
                field_ids.append(field_id)

            # Apply heading style and freeze heading row.
            style = self.get_style(self.STYLE_HEADING)
            max_col = max(len(model_config.fields_config), self.APPLY_STYLE_MIN_NUM_COLS)
            self.apply_style_to_rows(style, sheet, min_row=row, max_row=row, max_col=max_col)
            sheet.freeze_panes = sheet.cell(column=1, row=row + 1)

            # Write values.
            row = 1
            for model in model_config.objects.all():
                col = 0; row += 1  # NOQA
                for field_id in field_ids:
                    col += 1
                    sheet.cell(column=col, row=row).value = model.get_field_value(field_id)

        # Remove the first sheet.
        self.book.remove_sheet(self.book.active)

        return self.book

    def _save_common(self):
        """Provide common steps for "save" methods."""
        if self.book is None:
            self.generate()
        super(ExportExcelFull, self)._save_common()
