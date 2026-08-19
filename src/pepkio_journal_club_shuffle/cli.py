import json
import sys
from typing import Optional

import click

from .client import PepkioClient
from .config import DEFAULT_API_BASE_URL
from .exceptions import PepkioError


@click.group()
@click.option("--base-url", default=None, help=f"API base URL (default: {DEFAULT_API_BASE_URL})")
@click.option("--api-key", default=None, help="Pepkio API Key.")
@click.version_option(package_name="pepkio-journal-club-shuffle")
@click.pass_context
def main(ctx: click.Context, base_url: Optional[str], api_key: Optional[str]) -> None:
    """Pepkio Journal Club Shuffle Python CLI."""
    ctx.ensure_object(dict)
    ctx.obj["base_url"] = base_url
    ctx.obj["api_key"] = api_key


@main.command()
@click.option("--base-url", default=None, help=f"API base URL (default: {DEFAULT_API_BASE_URL})")
@click.pass_context
def manifest(ctx: click.Context, base_url: Optional[str]) -> None:
    """Fetch and print the tool manifest."""
    try:
        resolved_base_url = base_url or ctx.obj.get("base_url")
        client = PepkioClient(base_url=resolved_base_url)
        data = client.get_manifest()
        click.echo(json.dumps(data, indent=2))
    except PepkioError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--example", type=str, default=None, help="Run manifest example by name.")
@click.option("--input-json", type=str, default=None, help="JSON string for tool input.")
@click.option(
    "--input-file",
    type=click.Path(exists=True),
    default=None,
    help="JSON file path for tool input.",
)
@click.option("--api-key", default=None, help="Pepkio API Key.")
@click.option("--base-url", default=None, help=f"API base URL (default: {DEFAULT_API_BASE_URL})")
@click.option("--label", default=None, help="Optional label for the run.")
@click.option("--idempotency-key", default=None, help="Optional idempotency key.")
@click.pass_context
def run(
    ctx: click.Context,
    example: Optional[str],
    input_json: Optional[str],
    input_file: Optional[str],
    api_key: Optional[str],
    base_url: Optional[str],
    label: Optional[str],
    idempotency_key: Optional[str],
) -> None:
    """Run the journal-club-shuffle tool."""
    try:
        resolved_base_url = base_url or ctx.obj.get("base_url")
        resolved_api_key = api_key or ctx.obj.get("api_key")
        client = PepkioClient(api_key=resolved_api_key, base_url=resolved_base_url)

        input_data = None
        if example:
            manifest_data = client.get_manifest()
            examples = manifest_data.get("examples", [])
            for ex in examples:
                if ex.get("name") == example:
                    input_data = ex.get("input")
                    break
            if input_data is None:
                avail = ", ".join(ex.get("name", "") for ex in examples if "name" in ex)
                click.echo(
                    f"Error: Example '{example}' not found. Available examples: {avail}", err=True
                )
                sys.exit(1)
        elif input_json:
            input_data = json.loads(input_json)
        elif input_file:
            with open(input_file, "r", encoding="utf-8") as f:
                input_data = json.load(f)
        else:
            click.echo("Error: Must specify --example, --input-json, or --input-file.", err=True)
            sys.exit(1)

        result = client.run(
            input_data=input_data,
            label=label,
            idempotency_key=idempotency_key,
        )
        click.echo(json.dumps(result.model_dump(exclude_none=True), indent=2))
    except PepkioError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command(name="get-run")
@click.argument("run_id")
@click.option("--api-key", default=None, help="Pepkio API Key.")
@click.option("--base-url", default=None, help=f"API base URL (default: {DEFAULT_API_BASE_URL})")
@click.pass_context
def get_run(
    ctx: click.Context, run_id: str, api_key: Optional[str], base_url: Optional[str]
) -> None:
    """Get run status and result by run ID."""
    try:
        resolved_base_url = base_url or ctx.obj.get("base_url")
        resolved_api_key = api_key or ctx.obj.get("api_key")
        client = PepkioClient(api_key=resolved_api_key, base_url=resolved_base_url)
        result = client.get_run(run_id)
        click.echo(json.dumps(result.model_dump(exclude_none=True), indent=2))
    except PepkioError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
