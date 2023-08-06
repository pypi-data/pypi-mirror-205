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

"""DMRCOT Class Definitions."""

import asyncio
import warnings
import xml.etree.ElementTree as ET

from typing import Optional

import aiohttp
import pytak

import dmrcot


__author__ = "Greg Albrecht <gba@snstac.com>"
__copyright__ = "Copyright 2023 Sensors & Signals LLC"
__license__ = "Apache License, Version 2.0"


class DMRNCWorker(pytak.QueueWorker):
    """Polls the DMRNC Unit API, serializes it to CoT, and puts onto the TX queue."""

    def __init__(self, queue, config):
        """Initialize this class."""
        super().__init__(queue, config)
        self.session = None
        self.first_run = True
        self.emer_db = {}

    async def handle_data(self, data: list) -> None:
        """Handle Data from DMRNC Unit API, Render to CoT, put on TX queue.

        Parameters
        ----------
        data : `dict`
            List of datum data as key/value arrays.
        """
        if not isinstance(data, dict):
            self._logger.warning("Invalid Unit Information, should be a Python `dict`.")
            return

        if not data:
            self._logger.warning("Empty Unit Information payload.")
            return

        records = data.get("records")
        lor = len(records)
        if not lor:
            self._logger.warning("Empty Unit Information Records.")
            return

        rejected = 0
        rec_num = 1
        self._logger.info("Handling %s Unit Info Records", lor)
        for record in records:
            rec_num += 1

            if not isinstance(record, dict):
                rejected += 1
                self._logger.warning("Record was not a Python `dict`: %s", record)
                continue

            if int(record.get("fix_valid")) != 1:
                rejected += 1
                self._logger.debug("No valid fix for record: %s", record)
                continue

            await self.handle_emer(record)

            event: Optional[bytes] = dmrcot.dmrnc_to_cot(record, self.config)
            if not event:
                self._logger.debug("Empty CoT Event for record=%s", record)
                continue

            self._logger.debug("Handling Record %s/%s", rec_num, lor)
            await self.put_queue(event)

        self.first_run = False
        if rejected:
            self._logger.info("Rejected %s Unit Info Records", rejected)

    async def handle_emer(self, record):
        """Generate a CoT Alert if record contains an emergency."""
        # EMER FLOW - Rests his head on a pillow made of concrete!
        fleet_addr = record.get("fleet_address")
        emer_event: Optional[bytes] = None
        emergency = int(record.get("emergency", 0))
        clear = False

        if emergency:
            self.emer_db[fleet_addr] = emergency
            self._logger.warning("Unit in Emergency @ Fleet Address: %s", fleet_addr)

            emer_event = dmrcot.emer_cot(record, self.config)
            if not emer_event:
                self._logger.error("Empty Emergency CoT for record=%s", record)

        elif self.emer_db.get(fleet_addr) == 1:
            clear = True
        elif self.first_run and self.config.getboolean("CLEAR_EMER_ON_START", dmrcot.DEFAULT_CLEAR_EMER_ON_START):
            self._logger.info("Clearning Emergencies because FIRST_RUN & CLEAR_EMER_ON_START=1")
            clear = True

        if clear:
            self._logger.warning("Unit Cleared Emergency @ Fleet Address: %s", fleet_addr)
            emer_event = dmrcot.emer_cot(record, self.config)

        if emer_event:
            await self.put_queue(emer_event)


    async def poll_feed_once(self, url: bytes) -> None:
        """Poll the API once, hand off return value to Data Handler."""
        async with self.session.get(url) as resp:
            if resp.status != 200:
                response_content = await resp.text()
                self._logger.error("Received HTTP Status %s for %s", resp.status, url)
                self._logger.error(response_content)
                return

            data = await resp.json()
            await self.handle_data(data)

    async def run(self):  # pylint: disable=arguments-differ
        """Run this Thread, Reads from Pollers."""
        self._logger.info("Running %s", self.__class__)

        feed_url = self.config.get("FEED_URL", dmrcot.DEFAULT_FEED_URL)
        if feed_url == dmrcot.DEFAULT_FEED_URL:
            warnings.warn(f"Please specify a FEED_URL. Using default of: {feed_url}")

        poll_interval = self.config.get("POLL_INTERVAL", dmrcot.DEFAULT_POLL_INTERVAL)

        async with aiohttp.ClientSession() as self.session:
            while 1:
                self._logger.info(
                    "%s polling every %ss: %s", self.__class__, poll_interval, feed_url
                )
                await self.poll_feed_once(feed_url)
                await asyncio.sleep(int(poll_interval))