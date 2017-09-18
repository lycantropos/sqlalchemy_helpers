from hypothesis import strategies

MIN_POSITIVE_INTEGER_VALUE = 1
MAX_SMALLINT_VALUE = 32767
integers = strategies.integers(min_value=MIN_POSITIVE_INTEGER_VALUE,
                               max_value=MAX_SMALLINT_VALUE)
