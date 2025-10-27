#!/usr/bin/env python3
"""Static Site Generator - Converts markdown files to HTML."""

import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import markdown


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from markdown content.

    Args:
        content: Markdown content with frontmatter

    Returns:
        Tuple of (metadata dict, markdown content)
    """
    # Match frontmatter between --- delimiters
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return {}, content

    # Parse simple YAML frontmatter
    frontmatter_text = match.group(1)
    markdown_content = match.group(2)

    metadata = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            # Remove quotes if present
            value = value.strip().strip('"').strip("'")
            metadata[key.strip()] = value

    return metadata, markdown_content


def process_markdown_file(filepath: Path) -> dict:
    """Process a single markdown file.

    Args:
        filepath: Path to markdown file

    Returns:
        Dictionary with metadata and HTML content
    """
    content = filepath.read_text()
    metadata, md_content = parse_frontmatter(content)

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['fenced_code', 'codehilite'])
    html_content = md.convert(md_content)

    return {
        'title': metadata.get('title', 'Untitled'),
        'date': metadata.get('date', ''),
        'author': metadata.get('author', 'Anonymous'),
        'content': html_content,
        'filename': filepath.stem + '.html',
        'source': filepath.name,
    }


def generate_site(content_dir: Path, template_dir: Path, output_dir: Path):
    """Generate static site from markdown files.

    Args:
        content_dir: Directory containing markdown files
        template_dir: Directory containing Jinja2 templates
        output_dir: Directory to write HTML files
    """
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(str(template_dir)))

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Process all markdown files
    posts = []
    md_files = sorted(content_dir.glob('*.md'))

    if not md_files:
        print("❌ No markdown files found in content/")
        return

    for md_file in md_files:
        print(f"Processing {md_file.name}...")
        post_data = process_markdown_file(md_file)
        posts.append(post_data)

        # Generate individual post page
        template = env.get_template('post.html')
        html = template.render(**post_data)

        output_file = output_dir / post_data['filename']
        output_file.write_text(html)
        print(f"  ✅ Generated {output_file.name}")

    # Sort posts by date (newest first)
    posts.sort(key=lambda p: p['date'], reverse=True)

    # Generate index page
    template = env.get_template('index.html')
    html = template.render(posts=posts)

    index_file = output_dir / 'index.html'
    index_file.write_text(html)
    print(f"\n✅ Generated {index_file.name}")

    print(f"\n🎉 Site generated successfully!")
    print(f"   Output: {output_dir}/")
    print(f"   Posts: {len(posts)}")


def main():
    """Main entry point."""
    content_dir = Path("content")
    template_dir = Path("templates")
    output_dir = Path("output")

    print("Static Site Generator")
    print("=" * 60)
    print()

    # Check directories exist
    if not content_dir.exists():
        print(f"❌ Content directory not found: {content_dir}")
        return 1

    if not template_dir.exists():
        print(f"❌ Template directory not found: {template_dir}")
        return 1

    generate_site(content_dir, template_dir, output_dir)
    return 0


if __name__ == "__main__":
    exit(main())
