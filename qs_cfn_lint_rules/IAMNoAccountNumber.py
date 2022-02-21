"""
  Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.

  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import re
import six
import json
import os
from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch
from qs_cfn_lint_rules.common import deep_get

LINT_ERROR_MESSAGE = "Hard-coded account IDs are unacceptable."
CFN_NAG_RULES = [
    "W21",
    "W15",
]


def determine_account_id_in_principal(resource_path, resource):
    return re.search(r"[0-9]{12}", str(resource))


class IAMResourceWildcard(CloudFormationLintRule):
    """Check ARN for partition agnostics."""

    id = "EIAMAccountIDInPrincipal"
    shortdesc = "Hard-coded account IDs are unacceptable."
    description = "Hard-coded account IDs are unacceptable."
    source_url = (
        "https://github.com/qs_cfn_lint_rules/qs-cfn-python-lint-rules"
    )
    tags = ["iam"]
    SEARCH_PROPS = ["Principal"]

    def match(self, cfn):
        """Basic Matching"""
        violation_matches = []
        term_matches = []
        for prop in self.SEARCH_PROPS:
            term_matches += cfn.search_deep_keys(prop)
        for tm in term_matches:
            violating_principal = determine_account_id_in_principal(
                tm[:-1], tm[-1]
            )
            if violating_principal:
                violation_matches.append(
                    RuleMatch(tm[:-1], LINT_ERROR_MESSAGE)
                )
        return violation_matches
