from typing import Dict


def get_auth_header(api_key: str) -> Dict:
	return {"Authorization": f"Bearer {api_key}"}
