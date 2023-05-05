from unittest.mock import Mock, patch

import pytest

from vpowerconfig.powercfg import PowerCfg


class TestPowerCfg:

    @patch("vpowerconfig.powercfg.PowerCfg.get_powercfg_list")
    def test_update(self, mock_get_powercfg_list):
        mock_get_powercfg_list.return_value = [
            (
                "01234567-89ab-cdef-0123-456789abcdef",
                "プランA",
                False,
            ),
            (
                "abcd1234-abcd-1234-abcd-1234abcdefab",
                "プラン(B)",
                True,
            )
        ]
        powercfg = PowerCfg()
        assert len(powercfg.configs) == 0
        powercfg.update()
        assert len(powercfg.configs) == 2
        assert powercfg.configs == [
            (
                "01234567-89ab-cdef-0123-456789abcdef",
                "プランA",
                False,
            ),
            (
                "abcd1234-abcd-1234-abcd-1234abcdefab",
                "プラン(B)",
                True,
            )
        ]

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
        assert result == [
            (
                "01234567-89ab-cdef-0123-456789abcdef",
                "プランA",
                False,
            ),
            (
                "abcd1234-abcd-1234-abcd-1234abcdefab",
                "プラン(B)",
                True,
            )
        ]
