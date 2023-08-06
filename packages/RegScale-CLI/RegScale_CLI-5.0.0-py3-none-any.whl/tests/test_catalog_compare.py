#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""standard imports"""
import os

from app.api import Api
from app.application import Application
from app.internal.login import login
from app.logz import create_logger
from app.utils.catalog_utils.compare_catalog import get_new_catalog
from app.utils.catalog_utils.compare_catalog import get_old_catalog
from models.app_models.catalog_compare import CatalogCompare

# create logger function to log errors
logger = create_logger()


class TestCatalogCompare:
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
        data = CatalogCompare.get_master_catalogs(api=self.api)
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_get_new_catalog(self):
        """Get catalog master list"""
        catalog_url = "https://regscaleblob.blob.core.windows.net/catalogs/NIST-SP800-53-R5_1060.json"
        response_catalog = get_new_catalog(url=catalog_url)
        assert isinstance(response_catalog, dict)
        assert len(response_catalog) > 0
        return response_catalog

    def test_new_diagnostics(self):
        """Function to run diagnostics on a catalog"""
        new_catalog_file = self.test_get_new_catalog()
        new_diagnostic_results = CatalogCompare.run_new_diagnostics(
            new_diagnose_cat=new_catalog_file
        )
        assert isinstance(new_catalog_file, dict)
        assert isinstance(new_diagnostic_results["title"], str)
        assert isinstance(new_diagnostic_results["uuid"], str)
        assert isinstance(new_diagnostic_results["keywords"], list)
        assert isinstance(new_diagnostic_results["security_control_count"], int)
        assert isinstance(new_diagnostic_results["cci_count"], int)
        assert isinstance(new_diagnostic_results["objective_count"], int)
        assert isinstance(new_diagnostic_results["parameter_count"], int)
        assert isinstance(new_diagnostic_results["test_count"], int)
        return new_diagnostic_results

    def test_get_old_catalog(self):
        """Function to retrieve the old catalog from a RegScale instance via API & GraphQL"""
        old_catalog_data = get_old_catalog(
            uuid_value="abea4b79-3bd3-4f68-a333-85cbebb5100d",
            api=self.api,
        )
        assert isinstance(old_catalog_data, dict)
        return old_catalog_data

    def test_old_diagnostics(self):
        """Function to run diagnostics on a catalog"""
        old_catalog_file = self.test_get_old_catalog()
        old_diagnostic_results = CatalogCompare.run_old_diagnostics(
            old_diagnose_cat=old_catalog_file
        )
        assert isinstance(old_diagnostic_results, CatalogCompare)
        assert isinstance(old_diagnostic_results["title"], str)
        assert isinstance(old_diagnostic_results["uuid"], str)
        assert isinstance(old_diagnostic_results["keywords"], list)
        assert isinstance(old_diagnostic_results["security_control_count"], int)
        assert isinstance(old_diagnostic_results["cci_count"], int)
        assert isinstance(old_diagnostic_results["objective_count"], int)
        assert isinstance(old_diagnostic_results["parameter_count"], int)
        assert isinstance(old_diagnostic_results["test_count"], int)
        return old_diagnostic_results

    def test_shallow_dict_compare(self):
        """Function to compare two dictionaries"""
        dict_1 = self.test_new_diagnostics()
        dict_2 = self.test_old_diagnostics()
        assert isinstance(dict_1["title"], str)
        assert isinstance(dict_2["title"], str)
        assert isinstance(dict_1["uuid"], str)
        assert isinstance(dict_2["uuid"], str)
        assert isinstance(dict_1["keywords"], list)
        assert isinstance(dict_2["keywords"], list)
        assert isinstance(dict_1["security_control_count"], int)
        assert isinstance(dict_2["security_control_count"], int)
        assert isinstance(dict_1["cci_count"], int)
        assert isinstance(dict_2["cci_count"], int)
        assert isinstance(dict_1["objective_count"], int)
        assert isinstance(dict_2["objective_count"], int)
        assert isinstance(dict_1["parameter_count"], int)
        assert isinstance(dict_2["parameter_count"], int)
        assert isinstance(dict_1["test_count"], int)
        assert isinstance(dict_2["test_count"], int)
