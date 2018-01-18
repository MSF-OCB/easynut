# -*- coding: utf-8 -*-
import re

from ..utils import is_data_slug


class ExcelTemplateFunctionError(Exception): pass  # NOQA


class AbstractExcelTemplateFunction(object):
    """
    Base object for functions available for Excel templates.

    Usage: ``#functionName(ARG1[, ARG2, ...])``
    """

    # Template function format and validation.
    TEMPLATE_FUNCTION_CLASS_FORMAT = "TemplateFunction_{name}"  # ``name`` must be in lowercase.
    TEMPLATE_FUNCTION_FORMAT = "#{name}({args})"
    RE_TEMPLATE_FUNCTION_SPLIT = re.compile(r"^#(?P<name>[a-z]+)\((?P<args>[^\),]+,?)?\)$")
    RE_TEMPLATE_FUNCTION_VALIDATION = re.compile(r"^#([a-z]+)\(([^\)]+)?\)$")
    ARGS_SPLIT_SEPARATOR = ","

    def __init__(self, *args):
        self.args = args

        # Initialize this dict with the data slugs as keys. Values are populated via ``self.load_data_slug_values()``.
        self.data_slug_values = {arg: None for arg in self.args if is_data_slug(arg)}

    def __call__(self, data_row):
        """Execute the function."""
        self.load_data_slug_values(data_row)  # Initialize the values of the args.
        self.init_values()  # Store the values of the data slugs.
        return self._exec()  # Return the computed value of the function.

    @classmethod
    def factory(cls, value):
        """Return an template function object according to the given value."""
        try:
            # Extract the name and the args string.
            name, args_string = cls.RE_TEMPLATE_FUNCTION_SPLIT.match(value).groups()
            # Split the args string into args values.
            args = [arg.strip() for arg in args_string.split(cls.ARGS_SPLIT_SEPARATOR)]
        except Exception:
            raise ExcelTemplateFunctionError()

        # Compose the name of the class for the given template function.
        function_class = cls.TEMPLATE_FUNCTION_CLASS_FORMAT.format(name.lower())
        # Create the template function object with the given args.
        return function_class(*args)

    @classmethod
    def is_template_function(cls, value):
        """Return whether the value is a template function."""
        return value is not None and cls.RE_TEMPLATE_FUNCTION_VALIDATION(value) is not None

    def get_arg_value(self, index):
        """Return the value of an arg (i.e. resolve the data slug or return the value itself)."""
        value = self.args[index]
        return self.data_slug_values.get(value, value)

    def get_args_data_slugs(self):
        """Return the data slugs mentionned in the args."""
        return self.data_slug_values.keys()

    def init_values(self):
        """Initialize the values of the args."""
        raise NotImplementedError()

    def load_data_slug_values(self, data_row):
        """Store the values of the data slugs."""
        for data_slug in self.get_args_data_slugs():
            # Retrieve the value from the DB results.
            self.data_slug_values = data_row[data_slug]

    def _exec(self):
        """Return the computed value of the function."""
        raise NotImplementedError()


class TemplateFunction_at(AbstractExcelTemplateFunction):
    """
    Excel template function to retrieve the value of a field at a given date.

    Usage: ``#at(FIELD_DATA_SLUG, DATE_DATA_SLUG)``
    """

    def init_values(self):
        """Initialize the values of the args."""
        self.value = self.get_arg_value(0)
        self.date = self.get_arg_value(1)

    def _exec(self):
        """Return the computed value of the function."""
        # Return the empty value mask if value is empty or it's a single chunk.
        if not self.value or self.OBFUSCATE_SPLIT_SEPARATOR not in self.value:
            return self.OBFUSCATE_MASK_EMPTY

        # Obfuscate each chunk.
        chunks = str(self.value).split(self.OBFUSCATE_SPLIT_SEPARATOR)
        return self.OBFUSCATE_JOIN_SEPARATOR.join([self._obfuscate_chunk(chunk) for chunk in chunks])


class TemplateFunction_obfuscate(AbstractExcelTemplateFunction):
    """
    Excel template function to obfuscate values.

    Usage: ``#obfuscate(FIELD_DATA_SLUG)``
    """

    OBFUSCATE_SPLIT_SEPARATOR = " "
    OBFUSCATE_JOIN_SEPARATOR = ""
    OBFUSCATE_MASK = "."
    OBFUSCATE_MASK_EMPTY = "***"

    def init_values(self):
        """Initialize the values of the args."""
        self.value = self.get_arg_value(0)

    def _exec(self):
        """Return the computed value of the function."""
        # Return the empty value mask if value is empty or it's a single chunk.
        if not self.value or self.OBFUSCATE_SPLIT_SEPARATOR not in self.value:
            return self.OBFUSCATE_MASK_EMPTY

        # Obfuscate each chunk.
        chunks = str(self.value).split(self.OBFUSCATE_SPLIT_SEPARATOR)
        return self.OBFUSCATE_JOIN_SEPARATOR.join([self._obfuscate_chunk(chunk) for chunk in chunks])

    def _obfuscate_chunk(self, value):
        """Obfuscate the value."""
        # Return an empty string if there's no value.
        if not value:
            return ""

        # Keep the first letter and obfuscate the rest.
        return "{}{}".format(value[0], self.OBFUSCATE_MASK)
