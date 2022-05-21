"""
File to test scraping the SEC stuff. Static means the test is running on a file locally and
live means its trying to scrape it in real time. Basically if any of the live ones fail they
all do
"""

from WH_Utils.Connectors.SEC import functions

class TestSECConnector:

    def test_pull_recent_reg_d(self):
        data = functions.get_reg_D_page()
        assert len(data) > 2

    def test_line_parser_static(self):
        with open("tests/test_data/connectors_data/recent_reg_d_webpage.txt", 'r') as f:
            webpage = f.read()

        lines = functions.parse_recent_reg_D(webpage)
        assert len(lines) > 1

    def test_line_parser_live(self):
        data = functions.get_reg_D_page()
        lines = functions.parse_recent_reg_D(data)
        assert len(lines) > 1

    def test_line_extract_static(self):
        with open("tests/test_data/connectors_data/recent_reg_d_webpage.txt", 'r') as f:
            webpage = f.read()

        lines = functions.parse_recent_reg_D(webpage)

        data = functions.get_info_from_line(lines[0])
        actual_keys = list(data.keys())
        expected_keys = ['date', 'form_type', 'form_link', 'CIK_code', 'info', 'company_name']
        assert actual_keys == expected_keys, "Unexcpected keys in return dict. \n Actual keys: {} \n Expected Keys: {}".format(actual_keys, expected_keys)

    def test_line_extract_live(self):
        data = functions.get_reg_D_page()
        lines = functions.parse_recent_reg_D(data)
        data = functions.get_info_from_line(lines[0])
        actual_keys = list(data.keys())
        expected_keys = ['date', 'form_type', 'form_link', 'CIK_code', 'info', 'company_name']
        assert actual_keys == expected_keys, "Unexcpected keys in return dict. \n Actual keys: {} \n Expected Keys: {}".format(
            actual_keys, expected_keys)

    """ these take forever to run. i would avoid
    def test_all_static(self):
        with open("tests/test_data/connectors_data/recent_reg_d_webpage.txt", 'r') as f:
            webpage = f.read()

        data = functions.get_all_recent_reg_D(webpage)
        assert len(data) > 1

    def test_all_live(self):
        webpage = functions.get_reg_D_page()
        data = functions.get_all_recent_reg_D(webpage)
        assert len(data) > 1
    """
