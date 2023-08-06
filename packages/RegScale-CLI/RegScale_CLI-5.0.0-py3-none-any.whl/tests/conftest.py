#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Standard Imports """
from os import getenv
from os.path import exists


def pytest_configure(config):
    """PyTest Configuration called automatically by PyTest"""
    init = f"""
        oscalLocation: /opt/OSCAL
        adAccessToken: Bearer <my token>
        adAuthUrl: https://login.microsoftonline.com/
        adClientId: <myclientidgoeshere>
        adAccessToken: Bearer <my token>
        adAuthUrl: https://login.microsoftonline.com/
        adClientId: <myclientidgoeshere>
        adGraphUrl: myUrl
        adSecret: <mysecretgoeshere>
        adTenantId: <mytenantidgoeshere>
        domain: https://dev.regscale.io
        jiraApiToken: <jiraAPIToken>
        jiraUrl: myjiraUrl
        jiraUserName: VALUE
        maxThreads: 100
        snowPassword: VALUE
        snowUrl: myUrl
        snowUserName: VALUE
        token: Bearer bunk_string
        userId: enter user id here
        wizAccessToken: <createdProgrammatically>
        wizAuthUrl: VALUE
        wizExcludes: VALUE
        wizScope: VALUE
        wizUrl: https://auth.wiz.io/oauth/token
        tenableAccessKey: {getenv("TENABLE_ACCESS")}
        tenableSecretKey: {getenv("TENABLE_SECRET")}
        tenableUrl: https://sc.tenalab.online
        qualysUserName: testuser
        qualysPassword: MyPassword
        qualysUrl: http://localhost:5050/
        issue:
            tenable:
              critical: 3
              high: 5
              moderate: 30
              status: Draft
            qualys:
              high: 5
              low: 3
              moderate: 30
              status: Draft
    """
    file_exists = exists("init.yaml")
    if not file_exists:
        with open("init.yaml", "w", encoding="utf-8") as file:
            file.write(init)


# other config
