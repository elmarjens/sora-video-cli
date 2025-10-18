"""Video creation logic with polling and progress display."""

import json
import sys
import time
from pathlib import Path
from typing import Optional

import click
from openai import OpenAI

from .enhance import enhance_prompt


def create_video(
    client: OpenAI,
    model: str,
    prompt: str,
    seconds: int,
    output_id: str,
    image_path: Optional[str] = None,
    enhance: bool = True,
) -> None:
    """
    Create a video using Sora 2 API.

    Args:
        client: OpenAI client instance
        model: Model name (sora-2 or sora-2-pro)
        prompt: User prompt for video generation
        seconds: Video duration in seconds
        output_id: Output identifier for the video file
        image_path: Optional path to reference image
        enhance: Whether to enhance the prompt with GPT-5
    """
    # Enhance prompt if requested
    if enhance:
        click.echo(click.style("\n🔍 Enhancing prompt with GPT-5...", fg="cyan"))
        enhanced_prompt = enhance_prompt(prompt, client)
        click.echo(click.style(f"\n✨ Enhanced prompt:", fg="green"))
        click.echo(f"   {enhanced_prompt}\n")
    else:
        enhanced_prompt = prompt

    # Prepare parameters
    params = {
        "model": model,
        "prompt": enhanced_prompt,
        "seconds": str(seconds),
    }

    # Start video generation
    click.echo(click.style(f"🎬 Starting video generation with {model}...", fg="cyan"))
    click.echo(f"   Duration: {seconds}s")
    if image_path:
        click.echo(f"   Reference image: {image_path}")

    # Add image reference if provided
    if image_path:
        image_file = Path(image_path)
        if not image_file.exists():
            click.echo(click.style(f"❌ Error: Image file not found: {image_path}", fg="red"))
            sys.exit(1)

        # Determine content type
        ext = image_file.suffix.lower()
        content_type_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }
        content_type = content_type_map.get(ext)
        if not content_type:
            click.echo(click.style(f"❌ Error: Unsupported image format: {ext}", fg="red"))
            click.echo("   Supported formats: .jpg, .jpeg, .png, .webp")
            sys.exit(1)

        with open(image_file, "rb") as f:
            params["input_reference"] = (image_file.name, f, content_type)
            video = client.videos.create(**params)
    else:
        video = client.videos.create(**params)

    print("\n" + "="*80)
    print("OPENAI API RESPONSE (videos.create):")
    print("="*80)
    print(json.dumps(video.model_dump(), indent=2, default=str))
    print("="*80 + "\n")

    click.echo(click.style(f"\n✓ Video generation started", fg="green"))
    click.echo(f"  Video ID: {video.id}\n")

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
            getattr(video, "error", None), "message", "Video generation failed"
        )
        click.echo(click.style(f"❌ Error: {error_message}", fg="red"))
        sys.exit(1)

    click.echo(click.style("✓ Video generation completed!", fg="green"))

    # Create videos directory if it doesn't exist
    videos_dir = Path("videos")
    videos_dir.mkdir(exist_ok=True)

    # Download video content
    click.echo(click.style("\n📥 Downloading video...", fg="cyan"))
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

    click.echo(click.style("\n🎉 All done!", fg="green", bold=True))
    click.echo(f"   Video ID: {video.id}")
    click.echo(f"   Video file: {video_path}")
