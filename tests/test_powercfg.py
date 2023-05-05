from unittest.mock import Mock, patch

import pytest

from vpowerconfig.powercfg import PowerCfg


class TestPowerCfg:

    @pytest.mark.parametrize("input_str, expected", [
        ("電源設定の GUID: 01234567-89ab-cdef-0123-456789abcdef  (プランA)", ("01234567-89ab-cdef-0123-456789abcdef", "プランA")), # noqa
        ("電源設定の GUID: abcd1234-abcd-1234-abcd-1234abcdefab  (プラン(B)) *", ("abcd1234-abcd-1234-abcd-1234abcdefab", "プラン(B)")), # noqa
    ])
    def test_extract_uuid_and_name(self, input_str, expected):
        assert PowerCfg.extract_uuid_and_name(input_str) == expected

    @patch('subprocess.run')
    def test_get_powercfg_list(self, mock_run):
        mock_stdout = Mock()
        mock_stdout.decode.return_value = """

既存の電源設定 (* アクティブ)
-----------------------------------
電源設定の GUID: 01234567-89ab-cdef-0123-456789abcdef  (プランA)
電源設定の GUID: abcd1234-abcd-1234-abcd-1234abcdefab  (プラン(B)) *
"""
        mock_run.return_value = Mock(stdout=mock_stdout)

        result = PowerCfg.get_powercfg_list()
        assert isinstance(result, list)
        assert len(result) == 2

        assert result[0].uuid == "01234567-89ab-cdef-0123-456789abcdef"
        assert result[0].name == "プランA"

        assert result[1].uuid == "abcd1234-abcd-1234-abcd-1234abcdefab"
        assert result[1].name == "プラン(B)"
