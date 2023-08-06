#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""standard imports"""
import json
import os

from app.api import Api
from app.application import Application
from app.internal.login import login
from app.logz import create_logger
from app.utils.app_utils import save_data_to
from app.utils.catalog_utils.export_catalog import get_new_catalog
from models.app_models.catalog_compare import CatalogCompare


class TestCatalogExport:
    """
    Tests for catalog_export.py
    """

    # create logger function to log errors
    logger = create_logger()

    # set environment and application configuration
    app = Application()
    api = Api(app)
    config = {}
    try:
        # load the config from YAML
        config = app.load_config()
    except FileNotFoundError:
        logger.error("ERROR: No init.yaml file or permission error when opening file.")

    def test_init(self):
        """simple init test"""
        with open("init.yaml", "r", encoding="utf-8") as file:
            data = file.read()
            self.logger.debug("init file: %s", data)
            assert len(data) > 5

    def test_login(self):
        """Login to RegScale instance and get a new JWT"""
        self.logger.debug(os.getenv("REGSCALE_USER"))
        self.logger.debug(os.getenv("REGSCALE_PASSWORD"))

        jwt = login(
            os.getenv("REGSCALE_USER"), os.getenv("REGSCALE_PASSWORD"), app=self.app
        )
        self.logger.info(jwt)
        assert jwt is not None

    def test_master_catalog(self):
        """Get catalog master list"""
        master_list = CatalogCompare.get_master_catalogs(api=self.api)
        assert isinstance(master_list, dict)
        assert len(master_list) > 0

    def test_get_new_catalog(self):
        """Get catalog master list"""
        catalog_url = "https://regscaleblob.blob.core.windows.net/catalogs/NIST-SP800-53-R5_1060.json"
        new_catalog = get_new_catalog(url=catalog_url)
        assert isinstance(new_catalog, dict)
        assert len(new_catalog) > 0
        return new_catalog

    def test_output_catalog(self):
        """Function to save the returned catalog"""
        catalog_file = self.test_get_new_catalog()
        save_data_to(file_name="test_catalog", file_type=".json", data=catalog_file)
        assert isinstance(catalog_file, dict)
        assert os.path.isfile("test_catalog.json")
        with open("test_catalog.json", "r", encoding="utf-8") as infile:
            assert json.load(infile) == catalog_file
