# Sora 2 CLI - OpenAI Sora 2 Video Generator Command Line Tool

A powerful command-line tool for generating and editing videos using OpenAI's **Sora 2** and **Sora 2 Pro** API. Create stunning AI-generated videos from text prompts with Sora 2, the latest video generation model from OpenAI.

## What is Sora 2?

**Sora 2** is OpenAI's groundbreaking AI video generation model that creates high-quality videos from text descriptions. Sora 2 builds upon the original Sora model with improved video quality, better prompt understanding, and more realistic motion. With **Sora 2 Pro**, you can generate production-quality cinematic videos perfect for marketing, content creation, and creative projects.

This CLI tool provides easy access to Sora 2's powerful video generation capabilities directly from your terminal.

## Features

- 🎬 **Create Videos**: Generate videos from text prompts using Sora 2 or Sora 2 Pro
- ✨ **AI-Enhanced Prompts**: Automatically improve prompts with GPT-5 for better results
- 🖼️ **Image References**: Use reference images as the first frame of your videos
- 🎨 **Remix Videos**: Edit existing videos with targeted adjustments
- 📊 **Progress Tracking**: Real-time progress bars during video generation
- 💾 **Auto-Download**: Automatically saves videos, thumbnails, and spritesheets

## Installation

### Prerequisites

- Python 3.11 or higher
- [UV package manager](https://github.com/astral-sh/uv)
- OpenAI API key with Sora access

### Setup

1. **Clone or navigate to the project directory**

2. **Install dependencies with UV**
   ```bash
   uv sync
   ```

3. **Install the CLI tool**
   ```bash
   uv pip install -e .
   ```

4. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

   Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

## Usage

### Create Command

Generate new videos from text prompts.

```bash
sora-cli create --prompt "Your prompt here" --output-id video_name
```

#### Options

- `--model` / `-m`: Choose model (`sora-2` or `sora-2-pro`, default: `sora-2`)
- `--prompt` / `-p`: Video generation prompt (required)
- `--seconds` / `-s`: Video duration in seconds (default: 5)
- `--image` / `-i`: Path to reference image (optional)
- `--output-id` / `-o`: Output filename without extension (required)
- `--no-enhance`: Skip GPT-5 prompt enhancement

#### Examples

**Basic video generation:**
```bash
sora-cli create -p "A cat riding a motorcycle through neon-lit streets" -o cat_motorcycle
```

**Use Sora 2 Pro for higher quality:**
```bash
sora-cli create --model sora-2-pro -p "Cinematic sunset over ocean waves" -s 10 -o sunset
```

**With reference image:**
```bash
sora-cli create -p "She turns around and smiles, then walks out of frame" -i reference.jpg -o walking
```

**Skip prompt enhancement (use prompt as-is):**
```bash
sora-cli create -p "Wide shot of desert highway, heat ripples, hard sun" -o desert --no-enhance
```

### Edit Command

Remix existing videos with targeted modifications.

```bash
sora-cli edit --video-id video_abc123 --prompt "Change instructions" --output-id new_version
```

#### Options

- `--video-id` / `-v`: ID of the video to remix (required)
- `--prompt` / `-p`: Remix instructions (required)
- `--output-id` / `-o`: Output filename without extension (required)

#### Examples

**Change color palette:**
```bash
sora-cli edit -v video_abc123 -p "Shift to warm tones with golden hour lighting" -o warm_version
```

**Modify subject:**
```bash
sora-cli edit -v video_abc123 -p "Change the cat to orange color" -o orange_cat
```

## Models

### Sora 2 (`sora-2`)
- **Best for**: Speed and iteration
- **Use cases**: Prototyping, social media, quick feedback
- **Characteristics**: Fast generation, good quality

### Sora 2 Pro (`sora-2-pro`)
- **Best for**: Production quality
- **Use cases**: Marketing, cinematic footage, high-fidelity content
- **Characteristics**: Longer generation time, higher cost, superior quality

## Output Files

Videos are saved in the `videos/` directory:

- `{output-id}.mp4` - The generated video
- `{output-id}_thumbnail.webp` - Thumbnail image
- `{output-id}_spritesheet.jpg` - Spritesheet for scrubbing

## Prompt Enhancement

By default, the CLI uses GPT-5 (o3-mini) to enhance your prompts based on Sora 2 best practices:

- Adds specific camera angles and movements
- Describes lighting and color details
- Clarifies subject actions and timing
- Improves overall cinematographic specificity

To skip enhancement and use your exact prompt, add the `--no-enhance` flag.

## Tips for Better Results

1. **Be specific**: Describe shot type, subject, action, setting, and lighting
2. **One action**: Focus on one clear camera move and one subject action
3. **Visual language**: Use concrete details instead of vague descriptions
4. **Lighting**: Specify light sources and color tones
5. **Remix carefully**: Make single, well-defined changes for best results

## Error Handling

- The tool validates API keys before running
- Progress bars show generation status
- Failed generations display error messages
- Missing files and invalid formats are caught early

## Development

### Project Structure

```
sora-video-cli/
├── .env                    # API key (not in git)
├── .env.example           # Template for .env
├── pyproject.toml         # UV project configuration
├── src/
│   └── sora_cli/
│       ├── cli.py         # Main CLI interface
│       ├── create.py      # Video creation logic
│       ├── edit.py        # Video remix logic
│       └── enhance.py     # Prompt enhancement
└── videos/                # Generated videos
```

### Running in Development

```bash
# Activate virtual environment
source .venv/bin/activate

# Run CLI directly
python -m sora_cli.cli create -p "Test prompt" -o test
```

## Resources

- [OpenAI Sora API Documentation](https://platform.openai.com/docs/guides/video-generation)
- [Sora 2 Prompting Guide](https://cookbook.openai.com/examples/sora/sora2_prompting_guide)
- [Get API Key](https://platform.openai.com/api-keys)

## License

MIT

---

## Keywords

Sora 2, Sora 2 Pro, OpenAI Sora, Sora video generator, AI video generation, text to video, Sora API, Sora CLI, video generation CLI, OpenAI video AI, Sora 2 API, AI video creation, automated video generation, Sora command line tool
