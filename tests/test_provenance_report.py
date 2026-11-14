from src.provenance_report import provenance_summary


def test_provenance_summary_accounts_for_all_registered_photos_and_records():
    summary = provenance_summary()
    assert summary["photos"]["total"] >= 190
    assert summary["photos"]["full_details"] + summary["photos"]["being_checked"] == summary["photos"]["total"]
    assert summary["records"]["total"] == 127
    assert summary["records"]["full_details"] + summary["records"]["being_checked"] == summary["records"]["total"]


def test_provenance_summary_does_not_claim_unverified_entries_are_complete():
    summary = provenance_summary()
    assert summary["photos"]["being_checked"] > 0
    assert summary["records"]["being_checked"] > 0
