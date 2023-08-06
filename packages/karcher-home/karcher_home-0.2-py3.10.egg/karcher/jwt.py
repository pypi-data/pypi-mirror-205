# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

import base64
import json


def get_user_id_from_token(token):
    """Get user ID from token."""
    token_data = token.split(".")[1]
    missing_padding = len(token_data) % 4
    if missing_padding:
        token_data += '=' * (4 - missing_padding)
    data = json.loads(base64.b64decode(token_data))
    auth = json.loads(data["value"])
    return auth["id"]
