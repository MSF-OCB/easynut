import os

from django.conf import settings

from openpyxl import load_workbook, Workbook
from openpyxl.utils import coordinate_from_string, column_index_from_string

from .utils import today_for_filename


FIELD_SLUG_SEPARATOR = "#"


class AbstractExportExcel(object):

    DEFAULT_FILENAME = None

    def __init__(self, dao, template=None, filename=None):
        self._dao = dao
        self.template = template
        self.filename = filename
        self.book = None

        # Config of the loaded template.
        self._config = OrderedDict()

        # Registry of DB data tables and their fields in use in the loaded template.
        self._db_tables = {}

        if self.template:
            self.load_template(template)

    def load_template(self, file_path):
        """Create the workbook from a template file (located in ``EXPORT_TEMPLATES_DIR``)."""
        self.book = load_workbook(os.path.join(settings.EXPORT_TEMPLATES_DIR, file_path))
        self._init_config()

    def populate(self, data):
        """Populate the template with the given data."""
        if self.book is None:
            raise Exception("No template loaded.")

    def save(self):
        """Save the Excel file."""
        if self.book is None:
            raise Exception("No template loaded.")

        if not self.filename:
            self._generate_filename()
        self.book.save(self.filename)

    def get_sheet(self, index):
        """Return a sheet identified by its ID."""
        return self.book.worksheets[index]

    def cell_name_to_col_row(self, cell):
        """Convert a cell name into ``(col, row)`` indexes. E.g. ``B5`` => ``(2, 5)``."""
        col, row = coordinate_from_string(cell)
        col = column_index_from_string(col)
        return col, row

    # def get_sheet_names(self):
    #     return self.book.sheetnames

    # def get_new_sheet(self, key, title):
    #     """Create a new sheet."""
    #     if len(self.sheets) == 0:
    #         sheet = self.book.active
    #         sheet.title = title
    #     else:
    #         sheet = self.book.create_sheet(title=title)
    #     return sheet

    def _init_config(self):
        """
        Read the template config.

        - The config sheet must be the first sheet in the workbook.
          It is automatically removed.
        - See the concrete class for more specs.
        """
        raise NotImplemented()

    def _sheets_iterator(self, for_config=False):
        """Iterate over sheets to populate."""
        for index, config in self._config.iteritems():
            sheet = self.get_sheet(name)
            col, row = config["start_col"], config["start_row"]
            if for_config:  # For config purpose.
                yield index, sheet, col, row
            else:  # For normal use.
                yield sheet, col, row, config["columns"]

    def _generate_filename(self):
        """Generate a filename based on the template name and "today"."""
        # Split filename and extension. /!\ The extension contains the/starts with a ".".
        filename, ext = os.path.splitext(os.path.basename(self.template))
        # Insert "today" between the filename and the extension.
        self.filename = "{}.{}{}".format(filename, today_for_filename(), ext)

    def _update_db_tables(self, field_slug):
        """Register the table and field."""
        # Split the field slug into ``(table_id, field_id)``.
        table_id, field_id = self._split_field_slug(field_slug)

        # Register
        if table_id not in self._db_tables:
            self._db_tables[table_id] = []
        if field_id not in self._db_tables[table_id]:
            self._db_tables[table_id].append(field_id)

    def _split_field_slug(self, field_slug):
        """Split the field slug into ``(table_id, field_id)``."""
        return [int(v) for v in field_slug.split(FIELD_SLUG_SEPARATOR)]


class ExportExcelList(AbstractExportExcel):
    """Excel export for templates containing a list of records."""

    DEFAULT_FILENAME = "default-list.xlsx"

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
                for field_slug in columns:
                    col += 1
                    sheet.cell(column=col, row=row).value = model.get_value_from_slug(field_slug)

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

    def _init_config_columns(self):
        """Read config for the data to populate in each sheet."""
        # Loop over the sheets that must be populated to read their columns config.
        for index, sheet, col, row in self._sheets_iterator(for_config=True):
            # Loop over the sheet columns. Stop at the first empty cell.
            col -= 1  # To start the loop with the increment, easier to read.
            while True:
                col += 1
                # Get the field slug. E.g. ``03#15`` (= ``tabla_3.campo_15``).
                field_slug = sheet.cell(column=col, row=row).value
                if not field_slug:
                    break
                self._config[index]["columns"].append(field_slug)
                self._update_db_tables(field_slug)


class ExportExcelDetail(ExportExcel):
    """Excel export for templates containing the data of a single record."""

    DEFAULT_FILENAME = "default-detail.xlsx"

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
