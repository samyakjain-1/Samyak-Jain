import asyncio
from sqlalchemy.orm import Session
from .agents import hypothesis_agent, context_agent, research_agent, contradiction_agent, synthesis_agent, alert_agent
from ..database import crud

async def run_analysis(hypothesis: str, db: Session) -> dict:
    """
    This is the main orchestrator for the agentic workflow.
    """
    print(f"Orchestrator received hypothesis: {hypothesis}")

    # 1. Structure the hypothesis
    structured_hypothesis_obj = await hypothesis_agent.structure_hypothesis(hypothesis)
    if structured_hypothesis_obj.get("error"):
        return structured_hypothesis_obj
    
    structured_hypothesis = structured_hypothesis_obj.get("structured_hypothesis", "")
    print(f"Structured hypothesis: {structured_hypothesis}")

    # 1.5. Get context
    context = await context_agent.get_context(structured_hypothesis)
    if context.get("error"):
        return context
    print(f"Generated context: {context}")

    # 2. Gather evidence in parallel
    supporting_evidence_task = research_agent.find_supporting_evidence(structured_hypothesis_obj)
    contradictory_evidence_task = contradiction_agent.find_contradictory_evidence(structured_hypothesis_obj)

    supporting_evidence, contradictory_evidence = await asyncio.gather(
        supporting_evidence_task,
        contradictory_evidence_task
    )
    print(f"Found {len(supporting_evidence)} supporting pieces of evidence.")
    print(f"Found {len(contradictory_evidence)} contradictory pieces of evidence.")

    # 3. Synthesize the final report
    final_report = await synthesis_agent.synthesize_evidence(
        structured_hypothesis_obj,
        supporting_evidence,
        contradictory_evidence
    )
    print("Final report generated.")

    # 4. Save the report to the database
    if "error" not in final_report:
        # The hypothesis to save should be the structured one for consistency
        hypothesis_to_save = structured_hypothesis
        db_report = crud.save_report(db=db, hypothesis=hypothesis_to_save, report_data=final_report)
        
        # 5. Generate and save alerts
        alerts = await alert_agent.generate_alerts(final_report)
        crud.save_alerts(db=db, report_id=db_report.id, alerts_data=alerts)
        
        # Manually convert the SQLAlchemy object to a dictionary to ensure serialization
        report_dict = {c.name: getattr(db_report, c.name) for c in db_report.__table__.columns}
        return report_dict

    return final_report
