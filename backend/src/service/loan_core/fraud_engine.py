class FraudDetectionEngine:
    def __init__(self, rules: dict):
        self.rules = rules

    def evaluate(self, app: Application, text_findings: List[str] = None) -> FraudSignals:
        flags, evidence = [], {}
        # Example rules:
        nsf_limit = self.rules.get("nsf_limit_3m", 0)
        name_mismatch_flag = self.rules.get("name_mismatch_flag", True)

        for a in app.applicants:
            if a.nsf_last_3m > nsf_limit:
                flags.append(f"NSF>{nsf_limit} in last 3 months")
        # stub: plug your LandingAI+LLM text checks here
        if text_findings:
            for f in text_findings:
                if "altered" in f.lower():
                    flags.append("Possible document tampering")
                    evidence["tamper"] = f

        score = min(1.0, 0.2 * len(flags))  # simple: 0.2 per flag
        return FraudSignals(flags=flags, score=score, evidence=evidence)