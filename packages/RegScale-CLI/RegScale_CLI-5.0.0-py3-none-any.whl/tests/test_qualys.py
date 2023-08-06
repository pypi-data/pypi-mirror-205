#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Qualys Integrations while using mock API service"""
import os

# standard library imports
import requests

from app.internal.login import login
from app.application import Application
from app.commercial.qualys import (
    get_asset_groups_from_qualys,
    get_qualys_assets_and_scan_results,
    get_issue_data_for_assets,
)
from app.logz import create_logger


class Test_Qualys:
    """Test Qualys Integrations"""

    app = Application()
    app.config["qualysUrl"] = "http://localhost:5050/"
    app.config["domain"] = "https://dev.regscale.io/"
    config = app.config
    logger = create_logger()

    def test_init(self):
        """Init"""
        with open("init.yaml", "r", encoding="utf-8") as file:
            data = file.read()
            self.logger.debug("init file: %s", data)
            assert len(data) > 5
        login(
            str_user=os.getenv("REGSCALE_USER"),
            str_password=os.getenv("REGSCALE_PASSWORD"),
            app=self.app,
        )
        # test mock server
        try:
            response = requests.get(f"{self.config['qualysUrl']}api/checkServer")
            assert response.ok
        except requests.exceptions.ConnectionError:
            assert False

    def test_config(self):
        """Make sure Qualys values are present"""
        assert "qualysUrl" in self.config

    def test_asset_groups(self):
        """Test fetching Qualys asset groups"""
        asset_groups = get_asset_groups_from_qualys()
        assert asset_groups

    def test_vulns(self):
        """
        Map Qualys assets & vulns to RegScale SSP
        """
        qualys_assets = get_qualys_assets_and_scan_results()
        qualys_assets_and_issues, total_vuln_count = get_issue_data_for_assets(
            qualys_assets
        )
        assert qualys_assets
        assert qualys_assets_and_issues
        assert total_vuln_count
