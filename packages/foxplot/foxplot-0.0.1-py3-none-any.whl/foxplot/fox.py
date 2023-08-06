#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Main class to manipulate dictionary-series data."""

import webbrowser
from typing import List, Optional, TextIO

from .decoders.json import decode_json
from .generate_html import generate_html
from .indexed_series import IndexedSeries
from .node import Node
from .write_tmpfile import write_tmpfile


class Fox:
    """Frequent Observation diXionaries, our main class.

    Our main class to read, access and manipulate series of dictionary data.
    """

    __file: Optional[str]
    __time: str
    data: Node
    length: int

    def __init__(self, from_file: Optional[str] = None, time: str = ""):
        """Initialize series.

        Args:
            from_file: If set, read data from this path.
            time: Label of time index in input dictionaries.
        """
        self.__file = from_file
        self.__time = time
        self.data = Node("/")
        self.length = 0
        if from_file:
            with open(from_file, "r", encoding="utf-8") as file:
                self.read_from_file(file)

    def get_series(self, label: str) -> IndexedSeries:
        """Get time-series data from a given label.

        Args:
            label: Label to the data in input dictionaries, for example
                ``/observation/cpu_temperature``.

        Returns:
            Corresponding time series.
        """
        keys = label.strip("/").split("/")
        return self.data._get_child(keys)

    @property
    def labels(self) -> List[str]:
        """List of all labels present in the data."""
        return self.data._list_labels()

    def plot(
        self,
        left: List[IndexedSeries],
        right: Optional[List[IndexedSeries]] = None,
        title: str = "",
        left_axis_unit: str = "",
        right_axis_unit: str = "",
        open_new_tab: bool = True,
    ) -> None:
        """Plot a set of indexed series.

        Args:
            left: Series to plot on the left axis.
            right: Series to plot on the right axis.
            title: Plot title.
            left_axis_unit: Unit label for the left axis.
            right_axis_unit: Unit label for the right axis.
            open_new_tab: If true (default), open plot in a new browser tab.
        """
        times = (
            self.get_series(self.__time)._get(self.length)
            if self.__time is not None
            else [float(x) for x in range(self.length)]
        )
        left_series = {
            series.label: series._get(self.length) for series in left
        }
        right_series = {
            series.label: series._get(self.length)
            for series in (right if right is not None else [])
        }
        html = generate_html(
            times,
            left_series,
            right_series,
            title,
            left_axis_unit,
            right_axis_unit,
            timestamped=self.__time != "",
        )

        if open_new_tab:
            filename = write_tmpfile(html)
            webbrowser.open_new_tab(filename)
            print("New tab opened in your web browser! ", end="")

        print("The command line is to produce it directly is:\n")
        left_args = " ".join(left_series.keys())
        right_args = ("-r " if right_series else "") + " ".join(
            right_series.keys()
        )
        file = f"{self.__file} " if self.__file is not None else ""
        time = f"-t {self.__time} " if self.__time else ""
        print(f"foxplot {file}{time}-l {left_args} {right_args}")

    def read_from_file(self, file: TextIO) -> None:
        """Process time series data.

        Args:
            file: File to read time series from.
        """
        for unpacked in decode_json(file=file):
            self.unpack(unpacked)

    def set_time(self, time: str):
        """Set label of time index in input dictionaries.

        Args:
            time: Label of time index in input dictionaries.
        """
        self.__time = time

    def unpack(self, unpacked: dict) -> None:
        """Append data from an unpacked dictionary.

        Args:
            unpacked: Unpacked dictionary.
        """
        self.data._update(self.length, unpacked)
        self.length += 1
