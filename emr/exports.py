# -*- coding: utf-8 -*-
import json
import os
from collections import OrderedDict

from django.conf import settings

from openpyxl import load_workbook, Workbook
from openpyxl.utils import coordinate_from_string, column_index_from_string

from .models import DynamicRegistry
from .utils import DataDb, now_for_filename, xlsx_download_response_factory


DATA_SLUG_EMPTY_CELL = "#"  # Value allowing to skip a cell while continuing to read config of other columns.


class AbstractExportExcel(object):

    def __init__(self):
        self.book = None
        self.filename = None

    def cell_name_to_col_row(self, cell):
        """Convert a cell name into ``(col, row)`` indexes. E.g. ``B5`` => ``(2, 5)``."""
        col, row = coordinate_from_string(cell)
        col = column_index_from_string(col)
        return col, row

    def create_sheet(self, title):
        """Create a new sheet."""
        return self.book.create_sheet(title=title)

    def get_sheet(self, index):
        """Return a sheet identified by its ID."""
        return self.book.worksheets[index]

    # def get_sheet_names(self):
    #     return self.book.sheetnames

    def save(self, filename=None):
        """Save the Excel file (under ``EXPORTS_ROOT``)."""
        self._save_common()
        if not filename:
            filename = self.filename

        file_path = os.path.join(settings.EXPORTS_ROOT, filename)
        self.book.save(file_path)
        return file_path

    def save_to_response(self):
        """Save the Excel file in an HTTP response."""
        self._save_common()

        response = xlsx_download_response_factory(self.filename)
        self.book.save(response)
        return response

    def _save_common(self):
        """Common steps for "save" methods."""
        if self.book is None:
            raise Exception("No Excel Workbook to save.")

        # Set active sheet to first one.
        self.book.active = 0


class ExportDataModel(AbstractExportExcel):
    """Create an Excel file containing a list of all tables and fields with their data slug."""

    DEFAULT_FILENAME = "easynut-data-model.{}.xlsx"
    VERBOSE = True

    def __init__(self):
        super(ExportDataModel, self).__init__()
        self.filename = self.DEFAULT_FILENAME.format(now_for_filename())

    def generate(self):
        self.book = Workbook()
        DynamicRegistry.load_models_config()

        self._generate_data_slugs()
        self._generate_tables()

        return self.book

    def _generate_data_slugs(self):
        sheet = self.get_sheet(0)
        sheet.title = "Data Slugs"

        headings = ["Table Name", "Field Name", "Data Slug"]
        if self.VERBOSE:
            headings += [None, "Table ID", "Field ID", "Type", "Values List"]
        self._write_headings(sheet, headings)

        self._write_data_slugs(sheet)

    def _generate_tables(self):
        sheet = self.create_sheet("Tables")

        headings = ["Table Name"]
        if self.VERBOSE:
            headings += ["Table ID"]
        self._write_headings(sheet, headings)

        self._write_data_tables(sheet)

    def _save_common(self):
        """Common steps for "save" methods."""
        try:
            super(ExportDataModel, self)._save_common()
        except Exception:
            self.generate()

    def _write_data_tables(self, sheet):
        row = 1

        # Loop over all models config.
        for model_id, model_config in DynamicRegistry.models_config.iteritems():
            row += 1

            # Build values.
            values = [model_config.name]
            if self.VERBOSE:
                values += [model_id]

            # Write values.
            self._write_values(sheet, row, values)

    def _write_data_slugs(self, sheet):
        row = 1

        # Loop over all models and fields config.
        for model_id, model_config in DynamicRegistry.models_config.iteritems():
            for field_id, field_config in model_config.fields_config.iteritems():
                row += 1

                # Build values.
                values = [
                    model_config.name,
                    field_config.name,
                    field_config.data_slug,
                ]
                if self.VERBOSE:
                    values += [
                        None,
                        model_id,
                        field_id,
                        field_config.kind,
                        json.dumps(field_config.values_list) if field_config.values_list else "",
                    ]

                # Write values.
                self._write_values(sheet, row, values)


    def _write_values(self, sheet, row, values):
        """Write values on the given row."""
        col = 0
        for value in values:
            col += 1
            if value is not None:
                sheet.cell(column=col, row=row).value = value

    def _write_headings(self, sheet, headings):
        """Write heading row."""
        col = 0
        for value in headings:
            col += 1
            if value is not None:
                sheet.cell(column=col, row=1).value = value


class AbstractExportExcelTemplate(AbstractExportExcel):

    DEFAULT_TEMPLATE = None

    def __init__(self, template=None, filename=None):
        super(AbstractExportExcelTemplate, self).__init__()
        self.template = template
        self.filename = filename

        # Config of the loaded template.
        self._config = OrderedDict()

        # Registry of DB data tables and their fields in use in the loaded template.
        self._db_tables = {}

        # Load the template.
        self.load_template(template)

    def load_template(self, template=None):
        """Create the workbook from a template file (located under ``EXPORTS_TEMPLATES_DIR``)."""
        # Set the current template.
        if template is None:
            template = self.DEFAULT_TEMPLATE
        self.template = template

        # Load the template.
        file_path = os.path.join(settings.EXPORTS_TEMPLATES_DIR, self.template)
        self.book = load_workbook(file_path)

        # Read the template config.
        self._init_config()

    def populate(self):
        """Populate the template with data."""
        if self.book is None:
            raise Exception("No template loaded.")

    def _generate_filename(self):
        """Generate a filename based on the template name and "today"."""
        # Split filename and extension. /!\ The extension contains the/starts with a ".".
        filename, ext = os.path.splitext(os.path.basename(self.template))
        # Insert "today" between the filename and the extension.
        self.filename = "{}.{}{}".format(filename, now_for_filename(), ext)

    def _init_config(self):
        """
        Read the template config.

        - The config sheet must be the first sheet in the workbook.
          It is automatically removed.
        - See the concrete class for more specs.
        """
        raise NotImplemented()

    def _save_common(self):
        """Common steps for "save" methods."""
        super(AbstractExportExcelTemplate, self)._save_common()

        # Ensure the filename is defined.
        if not self.filename:
            self._generate_filename()

    def _sheets_iterator(self, for_config=False):
        """Iterate over sheets to populate."""
        for index, config in self._config.iteritems():
            sheet = self.get_sheet(index)
            col, row = config["start_col"], config["start_row"]
            if for_config:  # For config purpose.
                yield index, sheet, col, row
            else:  # For normal use.
                yield index, sheet, col, row, config["columns"]

    def _update_db_tables(self, sheet_index, data_slug):
        """Register the tables and fields for a given sheet."""
        # Split the data slug into ``(table_id, field_id)``.
        table_id, field_id = DynamicRegistry.split_data_slug(data_slug)

        # Register
        if table_id not in self._config[sheet_index]["db_tables"]:
            self._config[sheet_index]["db_tables"][table_id] = []
        if field_id not in self._config[sheet_index]["db_tables"][table_id]:
            self._config[sheet_index]["db_tables"][table_id].append(field_id)


class ExportExcelList(AbstractExportExcelTemplate):
    """Excel export for templates containing a list of records."""

    DEFAULT_TEMPLATE = "easynut-list.xlsx"

    def populate(self):
        """Populate the template with data."""
        super(ExportExcelList, self).populate()

        # Loop over sheets to populate.
        for index, sheet, col, row, columns in self._sheets_iterator():
            tables_fields = self._config[index]["db_tables"]
            if len(tables_fields) == 0:
                continue

            sql = DynamicRegistry.build_sql(tables_fields)

            with DataDb.execute(sql) as c:
                # To start the loops with the increment, easier to read.
                row -= 1  # NOQA

                # Loop over data records.
                for data_row in c.fetchall():
                    row += 1

                    # Loop over columns to populate.
                    for col, data_slug in self._config[index]["columns"].iteritems():
                        sheet.cell(column=col, row=row).value = data_row[data_slug]

    def _init_config(self):
        """
        Read the template config.

        - See the abstract class for more specs.
        - The first row must contain column headings, and is therefore skipped.
        - The first column lists the index of the sheets that must be populated.
          The first sheet without taking into account the config sheet has the index ``1``.
          We stop the loop at the first empty cell in that column.
        - The second column lists the starting cell, using the cell name (e.g. ``B5``).
        """
        self._config = OrderedDict()
        self._init_config_sheets()  # Read config for the sheets to populate.
        self._init_config_columns()  # Read config for the data to populate in each sheet.

    def _init_config_columns(self):
        """Read config for the data to populate in each sheet."""
        # Loop over the sheets that must be populated to read their columns config.
        for index, sheet, col, row in self._sheets_iterator(for_config=True):
            # Loop over the sheet columns. Stop at the first empty cell.
            col -= 1  # To start the loop with the increment, easier to read.
            while True:
                col += 1
                # Get the data slug.
                data_slug = sheet.cell(column=col, row=row).value
                sheet.cell(column=col, row=row).value = ""
                if not data_slug:
                    break
                if data_slug == DATA_SLUG_EMPTY_CELL:
                    continue
                self._config[index]["columns"][col] = data_slug
                self._update_db_tables(index, data_slug)

    def _init_config_sheets(self):
        """Read config for the sheets to populate."""
        sheet = self.get_sheet(0)  # Get the config sheet.

        # Loop over rows starting from the second one (first row contains column headings).
        row = 1
        while True:
            row += 1
            # Get the sheet index from the first column. Stop at the first empty cell.
            index = sheet.cell(column=1, row=row).value
            if not index:
                break
            index = int(index) - 1  # Adapt the index as in the code counting starts at 0 (+ force int, not long).

            # Convert the starting cell name into ``(col, row)`` indexes.
            start_col, start_row = self.cell_name_to_col_row(sheet.cell(column=2, row=row).value)

            # Store the config for this sheet.
            self._config[index] = {
                "start_col": start_col,
                "start_row": start_row,
                "columns": OrderedDict(),  # Populated in ``self._init_config_columns()``.
                "db_tables": OrderedDict(),  # Populated in ``self._init_config_columns()``.
            }

        # Remove the config sheet.
        self.book.remove_sheet(sheet)


class ExportExcelDetail(AbstractExportExcelTemplate):
    """Excel export for templates containing the data of a single record."""

    DEFAULT_TEMPLATE = "easynut-detail.xlsx"

    def populate(self, data):
        """Populate the template with the given data."""
        super(ExportExcelList, self).populate(data)
        raise NotImplemented()  # @TODO

    def _init_config(self):
        """
        Read the template config.

        - See the abstract class for more specs.
        - @TODO
        """
        raise NotImplemented()  # @TODO
