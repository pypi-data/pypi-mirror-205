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

"""DMRCOT Constants."""

__author__ = "Greg Albrecht <gba@snstac.com>"
__copyright__ = "Copyright 2023 Sensors & Signals LLC"
__license__ = "Apache License, Version 2.0"


# DMR Trunking Node Controller : Unit API - URL
DEFAULT_FEED_URL: str = "http://localhost:1880/cecapi"

# Default feed polling interval, in seconds.
DEFAULT_POLL_INTERVAL: str = "30"

DEFAULT_COT_TYPE: str = "a-f-G-E-V"

DEFAULT_CLEAR_EMER_ON_START: str = "1"