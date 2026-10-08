"""Check the supported SDK API without contacting Slack."""
from types import SimpleNamespace
from unittest.mock import Mock

from isscloudtools.slack import slack_upload_image


def test_upload_uses_external_upload_api():
    client = Mock()
    client.files_upload_v2.return_value = SimpleNamespace(data={"ok": True})
    assert slack_upload_image(client, "C123", "plot.png", "Scan")
    client.files_upload_v2.assert_called_once_with(
        file="plot.png", initial_comment="Scan", channel="C123"
    )
