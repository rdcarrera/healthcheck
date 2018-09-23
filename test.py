#!/usr/bin/env python
import sys
from modules.httpGetString import HttpGetString
httpGetStringResult = HttpGetString()
print httpGetStringResult[0]
sys.exit(httpGetStringResult[1])
