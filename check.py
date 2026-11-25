#!/usr/bin/env python3
"""PulseGym AI public check. Sends the 10 sample questions to your /ask endpoint
and shows what came back, so you know your app speaks our API.
Usage: python3 check.py [base_url]   (default http://localhost:8080). No extra packages.
"""
import json, os, sys, urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080").rstrip("/")
QS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample-questions.json"), encoding="utf-8"))
ok = 0
for q in QS:
    req = urllib.request.Request(BASE + "/ask", data=json.dumps({"question": q["question"]}).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        out = json.loads(urllib.request.urlopen(req, timeout=60).read())
    except Exception as e:
        print(f"FAIL {q['id']}: {e}"); continue
    shape = isinstance(out.get("answer"), str) and out.get("status") in ("answered", "unknown", "refused") and isinstance(out.get("rule_ids"), list)
    status = out.get("status") == q["expected_status"]
    rules = set(q["expected_rule_ids"]) <= {str(i).upper() for i in out.get("rule_ids", [])}
    ok += shape and status and rules
    print(f"\n{q['id']}  {q['question']}")
    print(f"   your status: {out.get('status')}  (expected {q['expected_status']})   rule_ids: {out.get('rule_ids')}  (expected {q['expected_rule_ids']})")
    print(f"   your answer: {out.get('answer')}")
    print(f"   should say:  {'; '.join(q['key_facts'])}")
    if not shape:
        print("   FAIL: response does not match API-CONTRACT.md")
print(f"\n{ok}/{len(QS)} samples matched the expected status and rule IDs. The hidden test has 30 different questions.")
