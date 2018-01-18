# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.utils.encoding import force_text

from ..models import RE_DATA_SLUG_VALIDATION

from .base import AbstractExportExcelTemplate


class ExportExcelDetail(AbstractExportExcelTemplate):
    """Excel export for templates containing the data of a single record."""

    DEFAULT_FILENAME = "easynut-detail.xlsx"  # Default name for the file.
    DEFAULT_TEMPLATE = "export-template-detail.xlsx"  # Default template file to use.
    DEFAULT_LIST_CONFIG = {
        "col_inc": 1,
        "row_inc": 0,
        "max_values": 10,
    }

    def __init__(self, model, **kwargs):
        super(ExportExcelDetail, self).__init__(**kwargs)
        self.model = model

    def populate(self):
        """Populate the template with data."""
        super(ExportExcelDetail, self).populate()

        # Loop over sheets to populate.
        for sheet_index, sheet, config in self._sheets_iterator():
            # Loop over cells to populate.
            for cell_name, data_slug in config["cells"].iteritems():
                col, row = self.cell_name_to_col_row(cell_name)

                # Get values for this data slug.
                values = self.model.get_value_from_data_slug(data_slug)
                if type(values) in (list, tuple):
                    list_config = config["lists_config"].get(cell_name, self.DEFAULT_LIST_CONFIG)
                    max_values = list_config["max_values"]
                    list_col, list_row = col, row
                    for value in values[:max_values]:
                        self.set_cell_value(sheet.cell(column=list_col, row=list_row), value)
                        list_col += list_config["col_inc"]
                        list_row += list_config["row_inc"]
                else:
                    self.set_cell_value(sheet.cell(column=col, row=row), values)

    def _init_config(self):
        """
        Read the template config.

        - See ``AbstractExportExcelTemplate`` for more specs.
        """
        self._config = OrderedDict()  # Reset the config.
        self._init_config_sheets()  # Read config for the sheets to populate.
        self._init_config_cells()  # Read config for the data to populate in each sheet.

    def _init_config_cells(self):
        """
        Read config for the data to populate in each sheet.

        - Data are populated in configured cells.
        - We scan every cell in the cell area for config information.
        """
        # Loop over the sheets that must be populated to scan for config information.
        for sheet_index, sheet, config in self._sheets_iterator():
            # Loop over the cell range.
            for col in range(config["start_col"], config["end_col"] + 1):
                for row in range(config["start_row"], config["end_row"] + 1):
                    # Get cell value (potential data slug).
                    data_slug = force_text(sheet.cell(column=col, row=row).value)

                    # If it's not a config information, skip it.
                    if RE_DATA_SLUG_VALIDATION.match(data_slug) is None:
                        continue

                    # Remove the config information from the cell.
                    sheet.cell(column=col, row=row).value = ""

                    # Register the data slug to use for this column.
                    cell_name = self.cell_col_row_to_name(col, row)
                    self._config[sheet_index]["cells"][cell_name] = data_slug

    def _init_config_lists(self, sheet):
        """Read config for lists of data."""
        START_COL = 4

        # Loop over rows starting from the second one (first row contains column headings).
        row = 1
        while True:
            row += 1

            # Get the sheet index from the first column. Stop at the first empty cell.
            sheet_index = sheet.cell(column=START_COL, row=row).value

            # Empty cell? => stop looking for config information.
            if not sheet_index:
                break

            # Adapt the index as in the code counting starts at 0 (+ force int, not long).
            sheet_index = int(sheet_index) - 1

            # Store the config for this cell.
            cell_name = sheet.cell(column=START_COL + 1, row=row).value
            self._config[sheet_index]["lists_config"][cell_name] = {
                "col_inc": int(sheet.cell(column=START_COL + 2, row=row).value),
                "row_inc": int(sheet.cell(column=START_COL + 3, row=row).value),
                "max_values": int(sheet.cell(column=START_COL + 4, row=row).value),
                "kind": str(sheet.cell(column=START_COL + 5, row=row).value).lower(),
            }

    def _init_config_sheets(self):
        """
        Read config for the sheets to populate.

        - The first row must contain column headings, and is therefore skipped.
        - The first column lists the index of the sheets that must be populated.
          - The first sheet without taking into account the config sheet has the index ``1``.
          - We stop the loop at the first empty cell in that column.
        - The second column lists the cell range (e.g. ``A1:AN99``) to scan for config information.
        """
        sheet = self.get_sheet(0)  # Get the config sheet.

        # Loop over rows starting from the second one (first row contains column headings).
        row = 1
        while True:
            row += 1

            # Get the sheet index from the first column. Stop at the first empty cell.
            sheet_index = sheet.cell(column=1, row=row).value

            # Empty cell? => stop looking for config information.
            if not sheet_index:
                break

            # Adapt the index as in the code counting starts at 0 (+ force int, not long).
            sheet_index = int(sheet_index) - 1

            # Convert the cell range into ``(col, row)`` indexes.
            cell_range = sheet.cell(column=2, row=row).value.split(":")
            start_col, start_row = self.cell_name_to_col_row(cell_range[0])
            end_col, end_row = self.cell_name_to_col_row(cell_range[1])

            # Store the config for this sheet.
            self._config[sheet_index] = {
                "start_col": start_col,
                "start_row": start_row,
                "end_col": end_col,
                "end_row": end_row,
                # Format: ``{cell_name: data_slug}``. Populated in ``self._init_config_cells()``.
                "cells": OrderedDict(),
                # Format: ``{cell_name: {...}}``. Populated in ``self._init_config_cells()``.
                "lists_config": {},
            }

        # Read config for lists of data.
        self._init_config_lists(sheet)

        # Remove the config sheet.
        self.book.remove_sheet(sheet)
