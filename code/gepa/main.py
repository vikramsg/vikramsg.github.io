import gepa

from _evaluator import RecordingEvaluator
from _render import QuietLogger, RichGEPACallback, render_summary

trainset = [
    {
        "input": "Our production API is returning 503 errors and we want a refund.",
        "additional_context": {"rule": "Active outages / 5xx errors always go to urgent_eng."},
        "answer": "### urgent_eng",
    },
    {
        "input": "Can I get a $25 refund for an add-on I clicked by mistake?",
        "additional_context": {"rule": "Refunds of $50 or less go to general, not billing."},
        "answer": "### general",
    },
    {
        "input": "We were double-charged $180 on this month's invoice.",
        "additional_context": {"rule": "Refunds or invoice issues over $50 go to billing."},
        "answer": "### billing",
    },
    {
        "input": "Please refund $50 for the seat we removed.",
        "additional_context": {"rule": "Refunds of $50 or less (inclusive) go to general."},
        "answer": "### general",
    },
    {
        "input": "Last week's outage is resolved—can we claim our SLA credit?",
        "additional_context": {"rule": "Post-incident SLA credit requests go to billing."},
        "answer": "### billing",
    },
    {
        "input": "How do I invite a new teammate?",
        "additional_context": {"rule": "How-to questions go to general."},
        "answer": "### general",
    },
]

valset = [
    {
        "input": "I was charged $15 for extra storage—can you refund it?",
        "additional_context": {"rule": "Refunds <= $50 go to general."},
        "answer": "### general",
    },
    {
        "input": "Production jobs are failing with HTTP 500, and we want an invoice credit.",
        "additional_context": {"rule": "Active 5xx errors go to urgent_eng."},
        "answer": "### urgent_eng",
    },
    {
        "input": "Our $320 invoice has the wrong VAT number and needs a refund.",
        "additional_context": {"rule": "Refunds > $50 go to billing."},
        "answer": "### billing",
    },
    {
        "input": "Refund $49 please, I forgot to cancel my trial.",
        "additional_context": {"rule": "Refunds <= $50 go to general."},
        "answer": "### general",
    },
]

seed_prompt = {
    "system_prompt": (
        "Classify the support message into one bucket: billing, urgent_eng, or general. "
        "Put your final answer in the format '### <bucket>'."
    )
}

TASK_LM = "gemini/gemini-3.5-flash-lite"
REFLECTION_LM = "gemini/gemini-3.5-flash-lite"

evaluator = RecordingEvaluator()

result = gepa.optimize(
    seed_candidate=seed_prompt,
    trainset=trainset,
    valset=valset,
    task_lm=TASK_LM,
    reflection_lm=REFLECTION_LM,
    evaluator=evaluator,
    logger=QuietLogger(),
    callbacks=[RichGEPACallback(evaluator, task_lm=TASK_LM, reflection_lm=REFLECTION_LM)],
    max_metric_calls=25,
)

render_summary(result)
