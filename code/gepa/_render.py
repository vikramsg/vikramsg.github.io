from typing import Any

from rich import box
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from _evaluator import EvalRecord, RecordingEvaluator

console = Console()


class QuietLogger:
    """Silences GEPA's unformatted stdout logger so Rich handles all output."""

    def log(self, message: str) -> None:
        pass


def _render_task_eval(
    phase: str,
    task_lm: str,
    system_prompt: str | None,
    records: list[EvalRecord],
    border_style: str,
) -> None:
    if not records:
        return

    avg = sum(r.score for r in records) / len(records)
    table = Table(
        title=f"[bold {border_style}]{phase}[/bold {border_style}]  "
        f"[dim]model={task_lm}  avg={avg:.2f}[/dim]",
        title_justify="left",
        box=box.ROUNDED,
        border_style=border_style,
        show_lines=True,
        expand=True,
    )
    table.add_column("Score", width=7, justify="center")
    table.add_column("Sent → task_lm (user msg)", ratio=2, style="white")
    table.add_column("Received ← task_lm", ratio=3, style="white")
    table.add_column("Evaluator → feedback", ratio=2)

    for rec in records:
        passed = rec.score >= 1.0
        score_cell = Text(f"PASS\n{rec.score:.1f}", style="bold green") if passed else Text(f"FAIL\n{rec.score:.1f}", style="bold red")
        fb_style = "dim green" if passed else "yellow"
        table.add_row(
            score_cell,
            escape(rec.input_text),
            escape(rec.raw_response),
            Text(rec.feedback, style=fb_style),
        )

    if system_prompt is not None:
        console.print(
            Panel(
                escape(system_prompt.strip()),
                title=f"[bold {border_style}]Sent → task_lm (system msg)[/bold {border_style}] [dim]{task_lm}[/dim]",
                border_style=border_style,
                padding=(0, 1),
            )
        )
    console.print(table)


class RichGEPACallback:
    """Renders exact inputs/outputs for task_lm, reflection_lm, and GEPA decisions."""

    def __init__(
        self,
        evaluator: RecordingEvaluator,
        task_lm: str,
        reflection_lm: str,
    ) -> None:
        self._evaluator = evaluator
        self._task_lm = task_lm
        self._reflection_lm = reflection_lm
        self._candidates: dict[int, dict[str, str]] = {}
        self._current_parent_idx: int | None = None
        self._last_proposed: dict[str, str] | None = None
        self._pending_pareto: dict[str, Any] | None = None

    def on_optimization_start(self, event: dict[str, Any]) -> None:
        self._candidates[0] = dict(event["seed_candidate"])
        console.print()
        console.print(Rule("[bold cyan]GEPA Optimization Start[/bold cyan]", style="cyan"))
        console.print(
            f"  [dim]task_lm:[/dim] [bold blue]{self._task_lm}[/bold blue]   "
            f"[dim]reflection_lm:[/dim] [bold yellow]{self._reflection_lm}[/bold yellow]   "
            f"[dim]trainset:[/dim] [bold]{event['trainset_size']}[/bold]   "
            f"[dim]valset:[/dim] [bold]{event['valset_size']}[/bold]"
        )

    def on_iteration_start(self, event: dict[str, Any]) -> None:
        self._last_proposed = None
        console.print()
        console.print(Rule(f"[bold magenta]Iteration {event['iteration']}[/bold magenta]", style="magenta"))

    def on_candidate_selected(self, event: dict[str, Any]) -> None:
        self._current_parent_idx = event["candidate_idx"]
        self._candidates[event["candidate_idx"]] = dict(event["candidate"])
        console.print(
            f"[bold magenta]▸ GEPA SELECT:[/bold magenta] Parent Candidate [bold]#{event['candidate_idx']}[/bold] "
            f"[dim](current val score = {event['score']:.2f})[/dim]"
        )

    def on_minibatch_sampled(self, event: dict[str, Any]) -> None:
        console.print(
            f"[bold magenta]▸ GEPA MINIBATCH:[/bold magenta] Sampled trainset IDs [bold]{event['minibatch_ids']}[/bold]"
        )

    def on_evaluation_end(self, event: dict[str, Any]) -> None:
        records = self._evaluator.drain()
        if event["candidate_idx"] is None:
            sys_prompt = (
                next(iter(self._last_proposed.values()))
                if self._last_proposed
                else None
            )
            _render_task_eval(
                phase="TRAINSET MINIBATCH — Testing Proposed Candidate",
                task_lm=self._task_lm,
                system_prompt=sys_prompt,
                records=records,
                border_style="cyan",
            )
        else:
            cand = self._candidates.get(event["candidate_idx"], {})
            sys_prompt = next(iter(cand.values()), None)
            _render_task_eval(
                phase=f"TRAINSET MINIBATCH — Evaluating Parent #{event['candidate_idx']}",
                task_lm=self._task_lm,
                system_prompt=sys_prompt,
                records=records,
                border_style="blue",
            )

    def on_evaluation_skipped(self, event: dict[str, Any]) -> None:
        console.print(
            f"  [bold yellow]⏭  GEPA SKIPPED REFLECTION:[/bold yellow] "
            f"[dim]{event.get('reason', 'all_scores_perfect')}[/dim]"
        )

    def on_proposal_end(self, event: dict[str, Any]) -> None:
        self._last_proposed = dict(event["new_instructions"])
        parent_label = f"Candidate #{self._current_parent_idx}" if self._current_parent_idx is not None else "parent"

        for comp, new_text in event["new_instructions"].items():
            sent_prompt = event["prompts"].get(comp, "")
            raw_out = event["raw_lm_outputs"].get(comp, "")

            console.print(
                Panel(
                    escape(str(sent_prompt).strip()),
                    title=f"[bold yellow]SENT → reflection_lm[/bold yellow] "
                    f"[dim]({self._reflection_lm} | mutating {parent_label}.{comp})[/dim]",
                    border_style="yellow",
                    padding=(0, 1),
                )
            )
            console.print(
                Panel(
                    escape(str(raw_out).strip()),
                    title=f"[bold orange1]RAW RESPONSE ← reflection_lm[/bold orange1] "
                    f"[dim]({self._reflection_lm})[/dim]",
                    border_style="orange1",
                    padding=(0, 1),
                )
            )
            console.print(
                Panel(
                    escape(new_text.strip()),
                    title=f"[bold cyan]EXTRACTED PROPOSAL → new {comp}[/bold cyan] "
                    f"[dim](proposed by {self._reflection_lm} from {parent_label})[/dim]",
                    border_style="cyan",
                    padding=(0, 1),
                )
            )

    def on_pareto_front_updated(self, event: dict[str, Any]) -> None:
        self._pending_pareto = event

    def on_valset_evaluated(self, event: dict[str, Any]) -> None:
        records = self._evaluator.drain()
        self._candidates[event["candidate_idx"]] = dict(event["candidate"])
        sys_prompt = next(iter(event["candidate"].values()), None)
        badge = " ★ NEW BEST" if event["is_best_program"] else ""
        _render_task_eval(
            phase=f"VALSET EVAL — Candidate #{event['candidate_idx']}{badge}",
            task_lm=self._task_lm,
            system_prompt=sys_prompt,
            records=records,
            border_style="green",
        )
        if self._pending_pareto is not None:
            p = self._pending_pareto
            self._pending_pareto = None
            console.print(
                f"  [bold magenta]▸ GEPA PARETO FRONT:[/bold magenta] "
                f"active=[bold]{p['new_front']}[/bold] "
                f"[dim](displaced={p['displaced_candidates']})[/dim]"
            )

    def on_candidate_accepted(self, event: dict[str, Any]) -> None:
        console.print(
            f"  [bold green]✓ GEPA ACCEPTED:[/bold green] New Candidate [bold]#{event['new_candidate_idx']}[/bold] "
            f"[dim](parent={list(event['parent_ids'])}, minibatch sum={event['new_score']:.1f})[/dim]"
        )

    def on_candidate_rejected(self, event: dict[str, Any]) -> None:
        console.print(
            f"  [bold red]✗ GEPA REJECTED:[/bold red] "
            f"[dim](parent minibatch={event['old_score']:.2f} → proposal={event['new_score']:.2f}, "
            f"reason={event['reason']})[/dim]"
        )

    def on_optimization_end(self, event: dict[str, Any]) -> None:
        console.print()
        console.print(
            Rule(
                f"[bold green]Done — Best Candidate #{event['best_candidate_idx']} "
                f"(metric calls: {event['total_metric_calls']})[/bold green]",
                style="green",
            )
        )


def render_summary(result: Any) -> None:
    table = Table(
        title="[bold]All Accepted Candidates[/bold]",
        title_justify="left",
        box=box.SIMPLE_HEAVY,
    )
    table.add_column("ID", justify="right", style="bold")
    table.add_column("Parents", style="dim")
    table.add_column("Val Score", justify="right")
    table.add_column("Winner?", justify="center")

    for idx, (parents, score) in enumerate(zip(result.parents, result.val_aggregate_scores)):
        is_best = idx == result.best_idx
        score_text = Text(f"{score:.2f}", style="bold green" if is_best else "white")
        table.add_row(f"#{idx}", str(parents), score_text, "★" if is_best else "")

    console.print(table)
    console.print(
        Panel(
            escape(result.best_candidate["system_prompt"].strip()),
            title=f"[bold green]Winning Prompt (Candidate #{result.best_idx})[/bold green]",
            border_style="green",
            padding=(0, 1),
        )
    )
