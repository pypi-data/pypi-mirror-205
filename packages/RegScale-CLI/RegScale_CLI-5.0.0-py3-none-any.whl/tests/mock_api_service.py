#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mock API Service"""

# standard library imports
import os
from pathlib import Path
from flask import Flask, request

app = Flask(__name__)


####################
# Qualys Endpoints #
####################


def get_tests_dir() -> str:
    """
    Get the current working directory
    :return: string of the responses directory with a trailing slash
    :rtype: str
    """
    cur_dir = Path(os.getcwd())
    if cur_dir.stem.lower() == "tests":
        cwd = f".{os.sep}responses{os.sep}"
    else:
        cwd = f".{os.sep}tests{os.sep}responses{os.sep}"
    return cwd


@app.route("/api/checkServer", methods=["GET"])
def check_server():
    """Used to check if the server is running"""
    return "True"


@app.route("/api/2.0/fo/asset/group", methods=["GET"])
def get_asset_groups():
    """Get asset groups
    Example: http://localhost:5050/api/2.0/fo/asset/group?action=list"""
    response = None
    action = request.args.get("action", "list")
    if action == "list":
        with open(
            f"{get_tests_dir()}Qualys{os.sep}asset_groups.xml",
            "r",
            encoding="utf-8",
        ) as f:
            response = f.read()
    return response or ""


@app.route("/api/2.0/fo/asset/host/vm/detection", methods=["GET"])
def get_assets_and_scan_results():
    """Get assets and scan results
    Example: http://localhost:5050/api/2.0/fo/asset/host/vm/detection?action=list&show_asset_id=1
    """
    response = None
    args = request.args
    if args.get("action") == "list" and args.get("show_asset_id") == "1":
        with open(
            f"{get_tests_dir()}Qualys{os.sep}asset_response.xml",
            "r",
            encoding="utf-8",
        ) as f:
            response = f.read()
    return response or ""


@app.route("/api/2.0/fo/knowledge_base/vuln", methods=["GET"])
def get_issue_data_for_assets():
    """Get issue data for assets
    Example: http://localhost:5050/api/2.0/fo/knowledge_base/vuln?action=list&details=All&ids=38167
    """
    response = None
    args = request.args
    if (
        args.get("action") == "list"
        and args.get("details") == "All"
        and args.get("ids")
    ):
        with open(
            f"{get_tests_dir()}Qualys{os.sep}issue_{args.get('ids')}.xml",
            "r",
            encoding="utf-8",
        ) as f:
            response = f.read()
    return response or ""


if __name__ == "__main__":
    app.run(debug=True, port=5050)
