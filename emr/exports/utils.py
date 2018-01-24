# -*- coding: utf-8 -*-
OBFUSCATE_SPLIT_SEPARATOR = " "
OBFUSCATE_JOIN_SEPARATOR = ""
OBFUSCATE_MASK = "."
OBFUSCATE_MASK_EMPTY = "***"


def obfuscate(value):
    """Obfuscate the value."""

    def _obfuscate_chunk(self, value):
        """Obfuscate the value."""
        # Return an empty string if there's no value.
        if not value:
            return ""

        # Keep the first letter and obfuscate the rest.
        return "{}{}".format(value[0], OBFUSCATE_MASK)

    # Return the empty value mask if value is empty or it's a single chunk.
    if not value or OBFUSCATE_SPLIT_SEPARATOR not in value:
        return OBFUSCATE_MASK_EMPTY

    # Obfuscate each chunk.
    chunks = str(value).split(OBFUSCATE_SPLIT_SEPARATOR)
    return OBFUSCATE_JOIN_SEPARATOR.join([_obfuscate_chunk(chunk) for chunk in chunks])
