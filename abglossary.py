"""
A command line utility to query the A/B test terminology data.
"""

import click
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.table import Column
import yaml

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

with open("terminology.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

for x in data:
    if x["orgs"] is None:
        x["orgs"] = []


def filter_articles(term: str = None, org: str = None) -> list:
    """Find the articles relevant to the given term and organization."""

    hits = data[:]

    if term:
        hits = [x for x in data if term in x["terms"].keys()]

    if org:
        hits = [x for x in hits if org in x["orgs"]]

    return hits


def filter_terms(hits: list, term: str) -> list:
    """For each entry in the results (hits), keep only the term requested by the
    user.
    """
    for hit in hits:
        hit["terms"] = {k: v for k, v in hit["terms"].items() if k == term}

    return hits


def build_results_table(hits: list, sort: str = None):
    """Convert dict-format entries into a nice-looking table for console printing."""

    ## Build the list of results.
    results = []
    for hit in hits:
        for item, definition in hit["terms"].items():
            results.append(
                (
                    ", ".join(hit["orgs"]),  # Orgs
                    hit["title"],  # Title without link (to be deleted after sorting)
                    f"[link={hit['link']}]{hit['title']}[/link]",  # Title with link
                    item,
                    definition,
                )
            )

    ## Sort the results according to user's instructions.
    sort_choices = {"orgs": 0, "sources": 1, "terms": 3}
    if sort is not None:
        results = sorted(results, key=lambda x: x[sort_choices[sort]])

    ## Convert the table to a Rich table for console printing.
    table = Table(
        Column("Organizations", style="Magenta", width=20),
        Column("Source", width=40),
        Column("Term", style="Cyan"),
        "Definition",
        title="Results",
        show_lines=True,
    )

    # Remember to only add the title with the link.
    for result in results:
        table.add_row(result[0], result[2], result[3], result[4])

    return table


@click.group(context_settings=CONTEXT_SETTINGS)
def abglossary():
    pass


@abglossary.command(context_settings=CONTEXT_SETTINGS)
@click.option("-t", "--term", help="Filter results to a specific term.")
@click.option("-o", "--org", help="Filter results to this organization.")
@click.option(
    "-s",
    "--sort",
    type=click.Choice(["sources", "orgs", "terms"], case_sensitive=False),
    help="Which output column to sort by.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="If specified, print entire entries instead of condensed table.",
)
def query(
    term: str = None, org: str = None, sort: str = None, verbose: bool = False
) -> dict:
    """Query term definitions, filtering by organization and/or term."""

    hits = filter_articles(term, org)

    if term:
        hits = filter_terms(hits, term)

    if verbose:
        results = hits

    else:
        results = build_results_table(hits, sort)

    console = Console()
    console.print(results)
    return results


@abglossary.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    "field", type=click.Choice(["sources", "orgs", "terms"], case_sensitive=False)
)
def list(field):
    """List all organizations, terms, or sources present in the data file."""
    console = Console()

    if field == "sources":
        results = sorted([x["title"] for x in data])

    elif field == "orgs":
        results = [org for x in data for org in x["orgs"]]
        results = sorted(dict.fromkeys(results).keys())

    elif field == "terms":
        results = [term for x in data for term in x["terms"].keys()]
        results = sorted(dict.fromkeys(results).keys())

    else:
        console.log("That's not a valid field.")
        return

    console.print(results)


if __name__ == "__main__":
    results = abglossary()
