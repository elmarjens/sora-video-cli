"""Video remix/edit logic with polling and progress display."""

import json
import sys
import time
from pathlib import Path

import click
from openai import OpenAI


def edit_video(
    client: OpenAI,
    video_id: str,
    prompt: str,
    output_id: str,
) -> None:
    """
    Remix/edit an existing video using Sora 2 API.

    Args:
        client: OpenAI client instance
        video_id: ID of the video to remix
        prompt: Remix instructions
        output_id: Output identifier for the remixed video file
    """
    click.echo(click.style(f"\n🎬 Starting video remix...", fg="cyan"))
    click.echo(f"   Source video ID: {video_id}")
    click.echo(f"   Remix prompt: {prompt}\n")

    # Start remix
    try:
        video = client.videos.remix(
            video_id=video_id,
            prompt=prompt,
        )

        print("\n" + "="*80)
        print("OPENAI API RESPONSE (videos.remix):")
        print("="*80)
        print(json.dumps(video.model_dump(), indent=2, default=str))
        print("="*80 + "\n")

    except Exception as e:
        click.echo(click.style(f"❌ Error starting remix: {e}", fg="red"))
        sys.exit(1)

    click.echo(click.style(f"✓ Remix started", fg="green"))
    click.echo(f"  New video ID: {video.id}\n")

    # Poll for completion with progress bar
    progress = getattr(video, "progress", 0)
    bar_length = 30

    while video.status in ("in_progress", "queued"):
        # Refresh status
        video = client.videos.retrieve(video.id)

        print("\n" + "="*80)
        print("OPENAI API RESPONSE (videos.retrieve):")
        print("="*80)
        print(json.dumps(video.model_dump(), indent=2, default=str))
        print("="*80 + "\n")

        progress = getattr(video, "progress", 0)

        filled_length = int((progress / 100) * bar_length)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)
        status_text = "Queued" if video.status == "queued" else "Processing"

        sys.stdout.write(f"\r{status_text}: [{bar}] {progress:.1f}%")
        sys.stdout.flush()
        time.sleep(2)

    # Move to next line after progress loop
    sys.stdout.write("\n\n")

    # Check for failure
    if video.status == "failed":
        error_message = getattr(
            getattr(video, "error", None), "message", "Video remix failed"
        )
        click.echo(click.style(f"❌ Error: {error_message}", fg="red"))
        sys.exit(1)

    click.echo(click.style("✓ Video remix completed!", fg="green"))

    # Create videos directory if it doesn't exist
    videos_dir = Path("videos")
    videos_dir.mkdir(exist_ok=True)

    # Download video content
    click.echo(click.style("\n📥 Downloading remixed video...", fg="cyan"))
    video_path = videos_dir / f"{output_id}.mp4"

    content = client.videos.download_content(video.id, variant="video")
    content.write_to_file(str(video_path))

    click.echo(click.style(f"✓ Video saved: {video_path}", fg="green"))

    # Download thumbnail
    click.echo(click.style("📥 Downloading thumbnail...", fg="cyan"))
    thumb_path = videos_dir / f"{output_id}_thumbnail.webp"

    try:
        thumb_content = client.videos.download_content(video.id, variant="thumbnail")
        thumb_content.write_to_file(str(thumb_path))
        click.echo(click.style(f"✓ Thumbnail saved: {thumb_path}", fg="green"))
    except Exception as e:
        click.echo(click.style(f"⚠ Could not download thumbnail: {e}", fg="yellow"))

    # Download spritesheet
    click.echo(click.style("📥 Downloading spritesheet...", fg="cyan"))
    sprite_path = videos_dir / f"{output_id}_spritesheet.jpg"

    try:
        sprite_content = client.videos.download_content(video.id, variant="spritesheet")
        sprite_content.write_to_file(str(sprite_path))
        click.echo(click.style(f"✓ Spritesheet saved: {sprite_path}", fg="green"))
    except Exception as e:
        click.echo(click.style(f"⚠ Could not download spritesheet: {e}", fg="yellow"))

    click.echo(click.style("\n🎉 Remix complete!", fg="green", bold=True))
    click.echo(f"   Video ID: {video.id}")
    click.echo(f"   Video file: {video_path}")
