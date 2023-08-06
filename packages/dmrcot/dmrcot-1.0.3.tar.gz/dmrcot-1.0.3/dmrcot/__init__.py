#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Sensors & Signals LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""DMR Trunking Node Controller to Cursor on Target Gateway.

:author: Greg Albrecht <gba@snstac.com>
:copyright: Copyright 2023 Sensors & Signals LLC
:license: Apache License, Version 2.0
:source: <https://github.com/snstac/dmrcot>
"""

from .constants import (  # NOQA
    DEFAULT_POLL_INTERVAL,
    DEFAULT_FEED_URL,
    DEFAULT_COT_TYPE,
    DEFAULT_CLEAR_EMER_ON_START
)

from .functions import dmrnc_to_cot, create_tasks, emer_cot  # NOQA

from .classes import DMRNCWorker  # NOQA

__author__ = "Greg Albrecht <gba@snstac.com>"
__copyright__ = "Copyright 2023 Sensors & Signals LLC"
__license__ = "Apache License, Version 2.0"
