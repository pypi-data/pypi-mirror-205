#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""standard imports"""
import json
import os
import sys

from app.api import Api
from app.application import Application
from app.internal.login import login
from app.logz import create_logger
from app.utils.app_utils import save_data_to
from models.app_models.catalog_compare import CatalogCompare

# create logger function to log errors
logger = create_logger()


class TestCatalogDiagnostic:
    """
    Tests for catalog_diagnostic.py
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
        return master_list

    def test_get_new_catalog(self):
        """Get catalog master list"""
        catalog_url = "https://regscaleblob.blob.core.windows.net/catalogs/NIST-SP800-53-R5_1060.json"
        response = self.api.get(url=catalog_url, headers={})
        try:
            new_catalog = response.json()
        except Exception:
            self.logger.error("Unable to retrieve master catalogs.")
            sys.exit(1)
        assert isinstance(new_catalog, dict)
        assert len(new_catalog) > 0
        return new_catalog

    def test_diagnostics(self):
        """Function to run diagnostics on a catalog"""
        catalog_file = self.test_get_new_catalog()
        diagnostic_results = CatalogCompare().run_new_diagnostics(catalog_file)
        assert isinstance(catalog_file, dict)
        assert isinstance(diagnostic_results.title, str)
        assert isinstance(diagnostic_results.uuid, str)
        assert isinstance(diagnostic_results.keywords, list)
        assert isinstance(diagnostic_results.security_control_count, int)
        assert isinstance(diagnostic_results.cci_count, int)
        assert isinstance(diagnostic_results.objective_count, int)
        assert isinstance(diagnostic_results.parameter_count, int)
        assert isinstance(diagnostic_results.test_count, int)
        assert diagnostic_results.uuid == "fdac0321-959f-43ec-a91d-322da7d9761c"
        assert (
            diagnostic_results.title
            == "Electronic Version of NIST SP 800-53 Rev 5 Controls and SP 800-53A Rev 5 Assessment Procedures"
        )
        assert diagnostic_results.security_control_count == 1189
        assert diagnostic_results.objective_count == 2746
        return diagnostic_results

    def test_output_diagnostic(self):
        """Function to save the returned catalog"""
        diagnostic_file = self.test_diagnostics().dict()
        assert isinstance(diagnostic_file, dict)
        assert len(diagnostic_file) > 0
        save_data_to(
            file_name="diagnostic_output", file_type=".json", data=diagnostic_file
        )
        assert os.path.isfile("diagnostic_output.json")
        with open("diagnostic_output.json", "r", encoding="utf-8") as infile:
            assert json.load(infile) == diagnostic_file
