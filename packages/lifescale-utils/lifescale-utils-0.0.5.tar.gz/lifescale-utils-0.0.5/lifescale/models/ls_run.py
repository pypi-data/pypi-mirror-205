"""Modelling a LifeScale run

Copyright (C) 2022  Andreas Hellerschmied <heller182@gmx.at>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import datetime as dt
import pytz
import numpy as np
import pickle
import os
import sys

import pandas as pd

# from gravtools.models.lsm import LSM


class LSRun:
    """LifeScale run object.

    A LS run contains:


    - run name and description
    - input data
    - settings

    Attributes
    ----------
    run_name : str
        Name of the lsm run.
    output_directory : str
        Path to output directory (all output files are stored there).
    pgm_version : str
        Version of the program.
    """

    def __init__(self,
                 campaign_name,
                 output_directory,
                 surveys=None,  # Always use non-mutable default arguments!
                 stations=None,  # Always use non-mutable default arguments!
                 lsm_runs=None,  # Always use non-mutable default arguments!
                 ref_delta_t_dt=None  # Reference time for drift determination
                 ):
        """
        Parameters
        """