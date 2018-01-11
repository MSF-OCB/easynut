# -*- coding: utf-8 -*-

OBFUSCATE_MASK = "***"


class ExcelTemplateFunction(object):
    """Functions available for Excel templates."""

    @classmethod
    def obfuscate(self, value):
        """Obfuscate value."""
        def _obfuscate_word(value):
            if not value:
                return value
            return "{}{}".format(value[0], OBFUSCATE_MASK)

        separator = " "
        if not value or separator not in value:
            return OBFUSCATE_MASK
        return separator.join([_obfuscate_word(w) for w in value.split(separator)])
