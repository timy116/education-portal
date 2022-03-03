import re as default_re

ACCESS_CODE_REGEX = "[a-zA-Z]{5}|[a-zA-Z]{2}[0-9]{3}"
ACCESS_CODE_PATTERN = default_re.compile(rf"^{ACCESS_CODE_REGEX}$")
