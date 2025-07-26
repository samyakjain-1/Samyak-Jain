from sqlalchemy.orm import Session
from . import models
from typing import List

def save_report(db: Session, hypothesis: str, report_data: dict) -> models.Report:
    """
    Saves a completed analysis report to the database.
    """
    db_report = models.Report(
        hypothesis=hypothesis,
        summary=report_data.get("summary"),
        confidence_score=report_data.get("confidence_score"),
        recommendation=report_data.get("recommendation"),
        confirmations=report_data.get("confirmations", []),
        contradictions=report_data.get("contradictions", [])
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    print(f"Report saved with ID: {db_report.id}")
    return db_report

def save_alerts(db: Session, report_id: int, alerts_data: List[dict]) -> List[models.Alert]:
    """
    Saves a list of alerts associated with a report.
    """
    alerts = []
    for alert_data in alerts_data:
        if "error" in alert_data:
            continue
        db_alert = models.Alert(
            report_id=report_id,
            type=alert_data.get("type"),
            message=alert_data.get("message"),
            priority=alert_data.get("priority")
        )
        db.add(db_alert)
        alerts.append(db_alert)
    
    db.commit()
    for alert in alerts:
        db.refresh(alert)
    
    print(f"Saved {len(alerts)} alerts for report ID: {report_id}")
    return alerts
