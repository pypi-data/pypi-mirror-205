#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   utils.py
@Author  :   Raighne.Weng
@Version :   0.7.4
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Utils Class module
'''

import os
import glob
from pathlib import Path

SUPPORTED_FILE_EXTENSIONS = [
    '*.jpg', '*.JPG', '*.png', '*.PNG', '*.jpeg', '*.JPEG', '*.mp4', '*.MP4',
    "*.dcm", "*.DCM", '*.nii', '*.NII'
]


def get_asset_metadata_limit_by_tier(tier: str) -> int:
    """Get asset limit by tier.

    :param tier: the tier of the project owner
    :return: limit in bytes
    """
    # professional tier 0.5kb
    if tier == "professional":
        return 500
    # developer tier 0.3kb
    if tier == "developer":
        return 300
    # free tier 0kb
    return 0


def find_all_assets(path: Path) -> [str]:
    """
    List all assets under folder, include sub folder.

    :param path: The folder to upload assets.
    :return: assets path list.
    """
    file_paths = []

    # find all assets under folder and sub folders
    for file_ext in SUPPORTED_FILE_EXTENSIONS:
        file_paths.extend(
            glob.glob(os.path.join(path, '**', file_ext), recursive=True))

    return file_paths
