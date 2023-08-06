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

"""DMRCOT Functions."""

import datetime
import xml.etree.ElementTree as ET

from configparser import SectionProxy
from typing import Optional, Set, Union

import pytak
import dmrcot


__author__ = "Greg Albrecht <gba@snstac.com>"
__copyright__ = "Copyright 2023 Sensors & Signals LLC"
__license__ = "Apache License, Version 2.0"


APP_NAME = "dmrcot"


def create_tasks(
    config: SectionProxy, clitool: pytak.CLITool
) -> Set[pytak.Worker,]:
    """Create specific coroutine task set for this application.

    Parameters
    ----------
    config : `SectionProxy`
        Configuration options & values.
    clitool : `pytak.CLITool`
        A PyTAK Worker class instance.

    Returns
    -------
    `set`
        Set of PyTAK Worker classes for this application.
    """
    tasks = set()
    tasks.add(dmrcot.DMRNCWorker(clitool.tx_queue, config))
    return tasks


def dmrnc_to_cot_xml(  # NOQA pylint: disable=too-many-locals,too-many-branches,too-many-statements
    unit: dict,
    config: Union[SectionProxy, dict, None] = None
) -> Optional[ET.Element]:
    """Serialize a Unit Information as Cursor on Target XML.

    Parameters
    ----------
    craft : `dict`
        Key/Value data struct of decoded ADS-B aircraft data.
    config : `configparser.SectionProxy`
        Configuration options and values.
        Uses config options: UID_KEY, COT_STALE, COT_HOST_ID

    Returns
    -------
    `xml.etree.ElementTree.Element`
        Cursor on Target XML ElementTree object.
    """
    config = config or {}
    lat = unit.get("latitude")
    lon = unit.get("longitude")
    fleet_addr = unit.get("fleet_address")

    if fleet_addr is None:
        return None

    badpos = [None, 0, 0.0, "0", "0.0"]
    if lat in badpos and lon in badpos:
        return None

    config = config or {}

    remarks_fields: list = []

    emer = unit.get("emergency")
    if emer:
        remarks_fields.append("EMERGENCY")

    remarks_fields.append(f"Alias: {unit.get('alias')}")
    remarks_fields.append(f"Fleet Address: {fleet_addr}")
    remarks_fields.append(f"Address: {unit.get('address')}")
    remarks_fields.append(f"RSSI: {unit.get('rssi')}")
    remarks_fields.append(f"Uplink RSSI: {unit.get('uplink_rssi')}")
    remarks_fields.append(f"Site: {unit.get('last_site_name')}")

    cot_uid = f"DMRCOT-{fleet_addr}"
    cot_type = str(config.get("COT_TYPE", dmrcot.DEFAULT_COT_TYPE))
    callsign = unit.get("alias", cot_uid)
    cot_stale = int(config.get("COT_STALE", pytak.DEFAULT_COT_STALE))

    lrt = unit.get("last_response_time")
    fmt = '%Y%m%dT%H%M%SZ'
    time = datetime.datetime.strptime(lrt, fmt)
    start = time
    stale = time + datetime.timedelta(seconds=int(cot_stale))

    point: ET.Element = ET.Element("point")
    point.set("lat", str(lat))
    point.set("lon", str(lon))
    point.set("ce", str("9999999.0"))
    point.set("le", str("9999999.0"))
    point.set("hae", str("9999999.0"))

    contact: ET.Element = ET.Element("contact")
    contact.set("callsign", callsign)

    track: ET.Element = ET.Element("track")
    track.set("course", str(unit.get("course", "9999999.0")))

    speed: Union[int, str] = int(unit.get("speed", 0))
    if int(speed) > 0:
        speed = str(0.6214 * int(speed))
    track.set("speed", str(speed))

    detail = ET.Element("detail")
    detail.append(contact)
    detail.append(track)

    remarks = ET.Element("remarks")

    _remarks = " ".join(list(filter(None, remarks_fields)))

    remarks.text = _remarks
    detail.append(remarks)

    root = ET.Element("event")
    root.set("version", "2.0")
    root.set("type", cot_type)
    root.set("uid", cot_uid)
    root.set("how", "m-g")
    root.set("time", str(time.strftime(pytak.ISO_8601_UTC)))
    root.set("start", str(start.strftime(pytak.ISO_8601_UTC)))
    root.set("stale", str(stale.strftime(pytak.ISO_8601_UTC)))

    root.append(point)
    root.append(detail)

    return root


def dmrnc_to_cot(
    craft: dict,
    config: Optional[SectionProxy] = None,
) -> Optional[bytes]:
    """Return CoT XML object as an XML string."""
    cot: Optional[ET.Element] = dmrnc_to_cot_xml(craft, config)
    return (
        b"\n".join([pytak.DEFAULT_XML_DECLARATION, ET.tostring(cot)]) if cot else None
    )


def emer_cot_xml(unit: dict, config: Union[SectionProxy, dict, None] = None) -> Optional[ET.Element]:
    """Serialize a Unit Information as Cursor on Target XML.

    Parameters
    ----------
    craft : `dict`
        Key/Value data struct of decoded ADS-B aircraft data.
    config : `configparser.SectionProxy`
        Configuration options and values.
        Uses config options: UID_KEY, COT_STALE, COT_HOST_ID

    Returns
    -------
    `xml.etree.ElementTree.Element`
        Cursor on Target XML ElementTree object.
    """
    config = config or {}
    lat = unit.get("latitude")
    lon = unit.get("longitude")
    fleet_addr = unit.get("fleet_address")

    if fleet_addr is None:
        return None

    badpos = [None, 0, 0.0, "0", "0.0"]
    if lat in badpos and lon in badpos:
        return None

    cot_uid = f"DMRCOT-{fleet_addr}-9-1-1"
    cot_type = "b-a-o-tbl"
    callsign = f"{unit.get('alias', fleet_addr)}-Alert"

    point: ET.Element = ET.Element("point")
    point.set("lat", str(lat))
    point.set("lon", str(lon))
    point.set("ce", str("9999999.0"))
    point.set("le", str("9999999.0"))
    point.set("hae", str("9999999.0"))

    contact: ET.Element = ET.Element("contact")
    contact.set("callsign", callsign)

    track: ET.Element = ET.Element("track")
    track.set("course", str(unit.get("course", "9999999.0")))

    speed: Union[int, str] = int(unit.get("speed", 0))
    if int(speed) > 0:
        speed = str(0.6214 * int(speed))
    track.set("speed", str(speed))

    detail = ET.Element("detail")
    detail.append(contact)
    detail.append(track)

    emergency = ET.Element("emergency")
    emergency.text = callsign
    if unit.get("emergency"):
        emergency.set("type", "DMR Emergency")
        cot_type = "b-a-o-tbl"

        link = ET.Element("link")
        link.set("relation", "p-p")
        link.set("uid", f"DMRCOT-{fleet_addr}")
        link.set("type", str(config.get("COT_TYPE", dmrcot.DEFAULT_COT_TYPE)))
        detail.append(link)
    else:
        emergency.set("cancel", "true")
        cot_type = "b-a-o-can"
    detail.append(emergency)

    root = ET.Element("event")
    root.set("version", "2.0")
    root.set("type", cot_type)
    root.set("uid", cot_uid)
    root.set("how", "m-g")
    root.set("time", pytak.cot_time())
    root.set("start", pytak.cot_time())
    root.set("stale", pytak.cot_time(10))

    root.append(point)
    root.append(detail)

    return root


def emer_cot(unit: dict, config: Union[SectionProxy, dict, None] = None) -> Optional[bytes]:
    """Return CoT XML object as an XML string."""
    cot: Optional[ET.Element] = emer_cot_xml(unit, config)
    return (
        b"\n".join([pytak.DEFAULT_XML_DECLARATION, ET.tostring(cot)]) if cot else None
    )
