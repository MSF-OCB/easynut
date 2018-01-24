# -*- coding: utf-8 -*-
from collections import OrderedDict

from ..models import DynamicRegistry
from ..utils import DataDb, is_data_slug

from .base import AbstractExportExcelTemplate
from .template_functions import AbstractExcelTemplateFunction


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
                        # Handle template functions or data slug.
                        if self.is_template_function(data_slug):
                            value = data_slug(data_row)
                        else:
                            value = data_row[data_slug]

                        # Set cell value.
                        self.set_cell_value(sheet.cell(column=col, row=row), value)

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
          - If the value is not a data slug, we skip that column and contine the loop.
          - The value of the cell is emptied.
        """
        # Loop over the sheets that must be populated to read their columns config.
        for sheet_index, sheet, config in self._sheets_iterator():
            # Loop over the sheet columns. Stop at the first empty cell.
            col = config["start_col"] - 1  # To start the loop with the increment, easier to read.
            row = config["start_row"]
            while True:
                col += 1
                cell = sheet.cell(column=col, row=row)

                # Save the cell value (as emptied below).
                cell_value = cell.value

                # Empty cell? => stop looking for config information.
                if not cell_value:
                    break

                # Remove the config information from the cell.
                cell.value = ""

                # If the value is a data slug…
                if is_data_slug(cell_value):
                    # Register the data slug to use for this column.
                    self._config[sheet_index]["columns"][col] = cell_value

                    # Register this model/field for this sheet.
                    self._update_models_fields(sheet_index, cell_value)

                # If the value is a template function…
                elif self.is_template_function(cell_value):
                    # Create the template function object.
                    function = AbstractExcelTemplateFunction.factory(cell_value)

                    # Register the template function to use for this column.
                    self._config[sheet_index]["columns"][col] = function

                    # Register these models/fields for this sheet.
                    for data_slug in function.get_args_data_slugs():
                        self._update_models_fields(sheet_index, data_slug)

                # Else, skip this column and continue to look for config information.
                else:
                    continue

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
                # Format: ``{col_index: data_slug}``. Populated in ``self._init_config_columns()``.
                "columns": OrderedDict(),
                # Format: ``{model_id: [field_id, ...]}``. Populated in ``self._init_config_columns()``.
                "models_fields": OrderedDict(),
            }

        # Remove the config sheet.
        self.book.remove_sheet(sheet)
