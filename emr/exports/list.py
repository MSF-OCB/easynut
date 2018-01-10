# -*- coding: utf-8 -*-
from collections import OrderedDict

from ..models import DynamicRegistry
from ..utils import DataDb

from .base import DATA_SLUG_EMPTY_CELL, AbstractExportExcelTemplate


class ExportExcelList(AbstractExportExcelTemplate):
    """Excel export for templates containing a list of records."""

    DEFAULT_FILENAME = "easynut-list.xlsx"  # Default name for the file.
    DEFAULT_TEMPLATE = "export-template-list.xlsx"  # Default template file to use.

    def populate(self):
        """Populate the template with data."""
        super(ExportExcelList, self).populate()

        # Loop over sheets to populate.
        for sheet_index, sheet, config in self._sheets_iterator():
            # Get models and fields needed for this sheet.
            models_fields = self._config[sheet_index]["models_fields"]

            # No config for this sheet? => skip it.
            if len(models_fields) == 0:
                continue

            # Build the SQL statement to get data for this sheet.
            # @TODO: Data are not converted using raw DB queries.
            sql = DynamicRegistry.build_sql(models_fields)

            # Execute the query.
            with DataDb.execute(sql) as c:
                # Loop over data records.
                row = config["start_row"] - 1  # To start the loops with the increment, easier to read.
                for data_row in c.fetchall():
                    # Loop over columns to populate.
                    row += 1
                    for col, data_slug in self._config[sheet_index]["columns"].iteritems():
                        sheet.cell(column=col, row=row).value = data_row[data_slug]

    def _init_config(self):
        """
        Read the template config.

        - See ``AbstractExportExcelTemplate`` for more specs.
        """
        self._config = OrderedDict()  # Reset the config.
        self._init_config_sheets()  # Read config for the sheets to populate.
        self._init_config_columns()  # Read config for the data to populate in each sheet.

    def _init_config_columns(self):
        """
        Read config for the data to populate in each sheet.

        - Data are populated row by row starting at the "starting cell".
        - The first row lists the data slug to populate each cell.
          - We stop the loop at the first empty cell in that row.
          - ``DATA_SLUG_EMPTY_CELL`` allows to leave a column empty while continuing this loop.
        """
        # Loop over the sheets that must be populated to read their columns config.
        for sheet_index, sheet, config in self._sheets_iterator():
            # Loop over the sheet columns. Stop at the first empty cell.
            col = config["start_col"] - 1  # To start the loop with the increment, easier to read.
            row = config["start_row"]
            while True:
                col += 1

                # Get the data slug.
                data_slug = sheet.cell(column=col, row=row).value

                # Empty cell? => stop looking for config information.
                if not data_slug:
                    break

                # Remove the config information from the cell.
                sheet.cell(column=col, row=row).value = ""

                # Skip this column and continue to look for config information.
                if data_slug == DATA_SLUG_EMPTY_CELL:
                    continue

                # Register the data slug to use for this column.
                self._config[sheet_index]["columns"][col] = data_slug

                # Register this model/field for this sheet.
                self._update_models_fields(sheet_index, data_slug)

    def _init_config_sheets(self):
        """
        Read config for the sheets to populate.

        - The first row must contain column headings, and is therefore skipped.
        - The first column lists the index of the sheets that must be populated.
          - The first sheet without taking into account the config sheet has the index ``1``.
          - We stop the loop at the first empty cell in that column.
        - The second column lists the starting cell, using the cell name (e.g. ``B5``).
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

            # Convert the starting cell name into ``(col, row)`` indexes.
            start_col, start_row = self.cell_name_to_col_row(sheet.cell(column=2, row=row).value)

            # Store the config for this sheet.
            self._config[sheet_index] = {
                "start_col": start_col,
                "start_row": start_row,
                "columns": OrderedDict(),  # Populated in ``self._init_config_columns()``.
                "models_fields": OrderedDict(),  # Populated in ``self._init_config_columns()``.
            }

        # Remove the config sheet.
        self.book.remove_sheet(sheet)
