# -*- coding: utf-8 -*-
import json
import os

from django.conf import settings

from openpyxl import load_workbook, Workbook
from openpyxl.utils import coordinate_from_string, column_index_from_string

from .models import DynamicRegistry
from .utils import now_for_filename, xlsx_download_response_factory


class ExportDataModel(object):
    """Create an Excel file containing a list of all tables and fields with their data slug."""

    DEFAULT_FILENAME = "easynut-data-model.{}.xlsx"
    VERBOSE = True

    def __init__(self):
        self.book = None
        self.filename = self.DEFAULT_FILENAME.format(now_for_filename())

    def generate(self):
        self.book = Workbook()
        sheet = self.book.active
        self._write_headings(sheet)
        self._write_data(sheet)
        return self.book

    def save(self, filename=None):
        """Save as Excel file."""
        self._save_common()
        if not filename:
            filename = self.filename

        file_path = os.path.join(settings.EXPORTS_ROOT, filename)
        self.book.save(file_path)
        return file_path

    def save_to_response(self):
        """Save the Excel in an HTTP response."""
        self._save_common()

        response = xlsx_download_response_factory(self.filename)
        self.book.save(response)
        return reponse

    def _save_common(self):
        """Common steps for "save" methods."""
        if self.book is None:
            self.generate()

    def _write_data(self, sheet):
        DynamicRegistry.load_models_config()
        row = 1

        # Loop over all models and fields config.
        for model_id, model_config in DynamicRegistry.models_config.iteritems():
            for field_id, field_config in model_config.fields_config.iteritems():
                row += 1

                # Build values.
                values = [
                    "{}: {}".format(model_config.name, field_config.name),
                    field_config.data_slug,
                    None,
                    model_id,
                    model_config.name,
                    field_id,
                    field_config.name,
                ]
                if self.VERBOSE:
                    values += [
                        field_config.kind,
                        json.dumps(field_config.values_list) if field_config.values_list else "",
                    ]

                # Write values.
                col = 0
                for value in values:
                    col += 1
                    if value is not None:
                        sheet.cell(column=col, row=row).value = value

    def _write_headings(self, sheet):
        headings = ["Data Name", "Data Slug", None, "Table ID", "Table Name", "Field ID", "Field Name"]
        if self.VERBOSE:
            headings += ["Type", "Values List"]
        col = 0
        for value in headings:
            col += 1
            if value is not None:
                sheet.cell(column=col, row=1).value = value


class AbstractExportExcel(object):

    DEFAULT_TEMPLATE = None

    def __init__(self, template=None, filename=None):
        self.template = template
        self.filename = filename

        # The workbook.
        self.book = None

        # Config of the loaded template.
        self._config = OrderedDict()

        # Registry of DB data tables and their fields in use in the loaded template.
        self._db_tables = {}

        # Load the template.
        self.load_template(template)

    def cell_name_to_col_row(self, cell):
        """Convert a cell name into ``(col, row)`` indexes. E.g. ``B5`` => ``(2, 5)``."""
        col, row = coordinate_from_string(cell)
        col = column_index_from_string(col)
        return col, row

    # def get_new_sheet(self, key, title):
    #     """Create a new sheet."""
    #     if len(self.sheets) == 0:
    #         sheet = self.book.active
    #         sheet.title = title
    #     else:
    #         sheet = self.book.create_sheet(title=title)
    #     return sheet

    def get_sheet(self, index):
        """Return a sheet identified by its ID."""
        return self.book.worksheets[index]

    # def get_sheet_names(self):
    #     return self.book.sheetnames

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

    def populate(self, data):
        """Populate the template with the given data."""
        if self.book is None:
            raise Exception("No template loaded.")

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
        return reponse

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
        if self.book is None:
            raise Exception("No template loaded.")

        # Ensure the filename is defined.
        if not self.filename:
            self._generate_filename()

    def _sheets_iterator(self, for_config=False):
        """Iterate over sheets to populate."""
        for index, config in self._config.iteritems():
            sheet = self.get_sheet(name)
            col, row = config["start_col"], config["start_row"]
            if for_config:  # For config purpose.
                yield index, sheet, col, row
            else:  # For normal use.
                yield sheet, col, row, config["columns"]

    def _update_db_tables(self, data_slug):
        """Register the table and field."""
        # Split the data slug into ``(table_id, field_id)``.
        table_id, field_id = self._split_data_slug(data_slug)

        # Register
        if table_id not in self._db_tables:
            self._db_tables[table_id] = []
        if field_id not in self._db_tables[table_id]:
            self._db_tables[table_id].append(field_id)


class ExportExcelList(AbstractExportExcel):
    """Excel export for templates containing a list of records."""

    DEFAULT_TEMPLATE = "easynut-list.xlsx"

    def populate(self, data):
        """Populate the template with the given data."""
        super(ExportExcelList, self).populate(data)

        # Loop over sheets to populate.
        for sheet, col, row, columns in self._sheets_iterator():
            # To start the loops with the increment, easier to read.
            col -= 1; row -= 1  # NOQA

            # Loop over data records.
            for model in data.iteritems():
                row += 1
                # Loop over columns to populate.
                for data_slug in columns:
                    col += 1
                    sheet.cell(column=col, row=row).value = model.get_value_from_slug(data_slug)

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
                if not data_slug:
                    break
                self._config[index]["columns"].append(data_slug)
                self._update_db_tables(data_slug)

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
            index -= 1  # Adapt the index as in the code counting starts at 0.

            # Convert the starting cell name into ``(col, row)`` indexes.
            start_col, start_row = self.cell_name_to_col_row(sheet.cell(column=2, row=row).value)

            # Store the config for this sheet.
            self._config[index] = {
                "start_col": start_col,
                "start_row": start_row,
                "columns": [],  # Populated here below.
            }

        # Remove the config sheet.
        self.book.remove_sheet(sheet)


class ExportExcelDetail(AbstractExportExcel):
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
