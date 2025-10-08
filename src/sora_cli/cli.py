"""CLI interface for Sora 2 video generation."""

import os
import sys
from pathlib import Path

import click
from dotenv import load_dotenv
from openai import OpenAI

from .create import create_video
from .edit import edit_video


# Load environment variables from .env file
load_dotenv()


def get_openai_client() -> OpenAI:
    """Get OpenAI client with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.echo(
            click.style(
                "❌ Error: OPENAI_API_KEY not found in environment variables", fg="red"
            )
        )
        click.echo("\nPlease set your API key:")
        click.echo("  1. Copy .env.example to .env")
        click.echo("  2. Add your OpenAI API key to .env")
        click.echo("  3. Get your API key from: https://platform.openai.com/api-keys")
        sys.exit(1)

    return OpenAI(api_key=api_key)


@click.group()
@click.version_option(version="0.1.0", prog_name="sora-cli")
def cli():
    """
    Sora Video CLI - Generate and edit videos using OpenAI's Sora API.

    Create stunning videos with Sora 2 and Sora 2 Pro models.
    """
    pass


@cli.command()
@click.option(
    "--model",
    type=click.Choice(["sora-2", "sora-2-pro"], case_sensitive=False),
    default="sora-2",
    help="Sora model to use (default: sora-2)",
)
@click.option(
    "--prompt",
    "-p",
    required=True,
    help="Video generation prompt",
)
@click.option(
    "--seconds",
    "-s",
    type=int,
    default=5,
    help="Video duration in seconds (default: 5)",
)
@click.option(
    "--image",
    "-i",
    type=click.Path(exists=True),
    help="Optional reference image path",
)
@click.option(
    "--output-id",
    "-o",
    required=True,
    help="Output video identifier (filename without extension)",
)
@click.option(
    "--no-enhance",
    is_flag=True,
    help="Skip prompt enhancement with GPT-5",
)
def create(model: str, prompt: str, seconds: int, image: str, output_id: str, no_enhance: bool):
    """
    Create a new video with Sora 2.

    Examples:

      # Create a 5-second video with sora-2
      sora-cli create -p "A cat on a motorcycle" -o cat_video

      # Create a 10-second video with sora-2-pro
      sora-cli create --model sora-2-pro -p "Cinematic sunset" -s 10 -o sunset

      # Create with reference image
      sora-cli create -p "She smiles and walks away" -i frame.jpg -o walking
    """
    client = get_openai_client()

    create_video(
        client=client,
        model=model,
        prompt=prompt,
        seconds=seconds,
        output_id=output_id,
        image_path=image,
        enhance=not no_enhance,
    )


@cli.command()
@click.option(
    "--video-id",
    "-v",
    required=True,
    help="ID of the video to remix",
)
@click.option(
    "--prompt",
    "-p",
    required=True,
    help="Remix instructions",
)
@click.option(
    "--output-id",
    "-o",
    required=True,
    help="Output video identifier (filename without extension)",
)
def edit(video_id: str, prompt: str, output_id: str):
    """
    Remix/edit an existing video.

    Make targeted adjustments to a previously generated video without regenerating
    from scratch. Works best with single, well-defined changes.

    Examples:

      # Change color palette
      sora-cli edit -v video_abc123 -p "Change to warm tones" -o warm_version

      # Modify subject
      sora-cli edit -v video_abc123 -p "Change monster to orange" -o orange_monster
    """
    client = get_openai_client()

    edit_video(
        client=client,
        video_id=video_id,
        prompt=prompt,
        output_id=output_id,
    )


if __name__ == "__main__":
    cli()
