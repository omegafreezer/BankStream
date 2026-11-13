import unittest
import pandas as pd
from bankstream.transform import standardize_transactions, validate_transactions

class PipelineTransformTests(unittest.TestCase):
    def test_valid_record_is_accepted(self):
        frame = pd.DataFrame([{
            "transaction_id":" t001 ", "account_id":" a00001 ",
            "transaction_ts":"2025-01-01 10:00:00", "amount":"250.50",
            "currency":"inr", "transaction_type":"debit", "channel":"UPI",
            "status":"success", "source_file":"sample.csv"
        }])
        clean = standardize_transactions(frame)
        accepted, rejected = validate_transactions(clean, {"A00001"})
        self.assertEqual(len(accepted), 1)
        self.assertEqual(len(rejected), 0)
        self.assertEqual(accepted.iloc[0]["transaction_id"], "T001")

    def test_negative_amount_is_rejected(self):
        frame = pd.DataFrame([{
            "transaction_id":"T002", "account_id":"A00001",
            "transaction_ts":"2025-01-01 10:00:00", "amount":"-1",
            "currency":"INR", "transaction_type":"Debit", "channel":"ATM",
            "status":"SUCCESS"
        }])
        clean = standardize_transactions(frame)
        accepted, rejected = validate_transactions(clean, {"A00001"})
        self.assertEqual(len(accepted), 0)
        self.assertIn("amount_must_be_positive", rejected.iloc[0]["rejection_reason"])

if __name__ == "__main__":
    unittest.main()
