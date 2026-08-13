import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import paddle_watch as pw


class PaddleWatchTests(unittest.TestCase):
    def test_parse_approved_list(self):
        html = """
        <html><body>
        <div>Displaying 1 - 2 of 5,304</div>
        <div>Brand</div><a>Brand A</a>
        <div>Model (Click Name for Detail)</div><a>Model One</a>
        <div>Added</div><a>08/07/2026</a><div>Click to Enlarge</div>
        <div>Brand</div><a>Brand B</a>
        <div>Model (Click Name for Detail)</div><a>Model Two 16mm</a>
        <div>Added</div><a>08/06/2026</a><div>Click to Enlarge</div>
        </body></html>
        """
        result = pw.parse_approved_list(html)
        self.assertEqual(result["approved_list_total"], 5304)
        self.assertEqual(result["recent_approvals"][0]["manufacturer"], "Brand A")
        self.assertEqual(result["recent_approvals"][1]["added_date"], "2026-08-06")

    def test_parse_compliance_report(self):
        html = """
        <html><body>
        <div>Displaying 1 - 2 of 2</div>
        <div>Brand</div><div>Brand A</div>
        <div>Report Date</div><div>05/28/2026</div>
        <div>Model(s)</div><div>Model One</div>
        <div>Compliance Issue or Status</div><div>Under Investigation</div>
        <div>Brand</div><div>Brand B</div>
        <div>Report Date</div><div>03/24/2026</div>
        <div>Model(s)</div><div>Model Two</div>
        <div>Compliance Issue or Status</div><div>Removed from USAP Approved List</div>
        </body></html>
        """
        result = pw.parse_compliance_report(html)
        self.assertEqual(result["compliance_total"], 2)
        self.assertEqual(result["compliance_board"][0]["status"], "Under Investigation")
        self.assertEqual(result["compliance_board"][1]["report_date"], "2026-03-24")

    def test_rolling_window_is_not_a_removal_signal(self):
        previous = {
            "observation_id": "old",
            "approved_list": {
                "approved_list_total": 100,
                "recent_approvals": [{"manufacturer": "Old Brand", "model": "Old Model", "added_date": "2026-08-01"}],
            },
            "compliance_report": {"compliance_board": []},
        }
        current = {
            "observation_id": "new",
            "observed_at_utc": "2026-08-13T00:00:00Z",
            "approved_list": {
                "approved_list_total": 101,
                "recent_approvals": [{"manufacturer": "New Brand", "model": "New Model", "added_date": "2026-08-12"}],
            },
            "compliance_report": {"compliance_board": []},
        }
        change = pw.diff_observations(previous, current)
        self.assertEqual(len(change["new_rows_in_recent_approval_window"]), 1)
        self.assertEqual(len(change["rows_rolled_off_recent_approval_window"]), 1)
        self.assertNotIn("removed_approvals", change)

    def test_compliance_status_change_is_explicit(self):
        previous = {
            "observation_id": "old",
            "approved_list": {"approved_list_total": 100, "recent_approvals": []},
            "compliance_report": {"compliance_board": [
                {"brand": "A", "models": "M", "report_date": "2026-01-01", "status": "Under Investigation"}
            ]},
        }
        current = {
            "observation_id": "new",
            "observed_at_utc": "2026-08-13T00:00:00Z",
            "approved_list": {"approved_list_total": 100, "recent_approvals": []},
            "compliance_report": {"compliance_board": [
                {"brand": "A", "models": "M", "report_date": "2026-08-13", "status": "Compliance Issue Resolved"}
            ]},
        }
        change = pw.diff_observations(previous, current)
        self.assertEqual(len(change["compliance_record_status_or_date_changes"]), 1)
        self.assertTrue(change["has_substantive_change"])


if __name__ == "__main__":
    unittest.main()
