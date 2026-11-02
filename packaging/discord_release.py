#!/usr/bin/env python3
"""packaging/discord_release.py TAG [NOTES]: posts a release to the Discord server's #releases
channel. DISCORD_RELEASES_WEBHOOK is the channel's webhook URL (a repository secret; the release
workflow calls this after `gh release create`). NOTES defaults to docs/releases/TAG.md: its summary,
"What's new" list and "Feedback we need", "Known issues" and "Good to know" sections are the post.
DRY_RUN=1 prints the message instead of sending it."""
import json
import os
import pathlib
import re
import sys
import urllib.request

REPO = 'bloodborne-native/bloodborne-mac'
# Pinned to a commit: Discord keeps an image by its URL, so a changed icon needs a new URL.
ICON = 'https://raw.githubusercontent.com/bloodborne-native/bloodborne-launcher/19f6178/src-tauri/icons/128x128%402x.png'


def unwrap(lines):
    """The notes are wrapped at 100 columns; Discord would keep those breaks. Joins each list item
    and paragraph into one line."""
    out = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            out.append('')
        elif out and out[-1] and not re.match(r'([-*] |\d+\. |#)', stripped):
            out[-1] += ' ' + stripped
        else:
            out.append(stripped)
    return '\n'.join(out).strip()


def section(text, title):
    """The lines under a '## title' heading (or, for the summary, between the heading and the
    first '## ')."""
    lines = text.splitlines()
    if title is None:
        body = []
        for line in lines[1:]:
            if line.startswith('## '):
                break
            body.append(line)
        return body
    for i, line in enumerate(lines):
        if line.strip() == f'## {title}':
            body = []
            for rest in lines[i + 1:]:
                if rest.startswith('## '):
                    break
                body.append(rest)
            return body
    return []


def plain(text):
    """Discord's posts carry no links or bold from the notes: labels and words only."""
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return text.replace('**', '')


def bullets(text):
    return '\n'.join('• ' + line[2:] if line.startswith('- ') else line for line in text.splitlines())


def post_section(text, title):
    body = bullets(plain(unwrap(section(text, title))))
    return f'{title}\n{body}' if body else ''


def message(tag, notes):
    """The project's release post: the version, one line, What's new, optional Feedback we need,
    Known issues and Good to know, the download, how to update and go back, and the credit."""
    text = notes.read_text()
    summary = plain(unwrap(section(text, None)))
    intro, _, listed = summary.partition("What's new:")
    version = tag.lstrip('v').replace('-rc.', ' RC ')
    back = re.search(r'install (\S+) again', text)
    parts = [f'Version {version} is out 🩸', intro.strip(), "What's new\n" + bullets(listed.strip())]
    for title in ('Feedback we need', 'Known issues', 'Good to know'):
        part = post_section(text, title)
        if part:
            parts.append(part)
    parts.append(f'Download: https://github.com/{REPO}/releases/tag/{tag}')
    update = 'Replace Bloodborne.app; saves and settings are preserved.'
    parts.append(update + (f' To go back, reinstall {back.group(1)}.' if back else ''))
    parts.append('Built on bbport by @deadinside and shadPS4 ❤️')
    content = '\n\n'.join(p for p in parts if p)
    if len(content) > 2000:  # Discord's limit; the release page has the rest
        content = content[:1900].rsplit('\n', 1)[0] + f'\n…\n\nFull notes: https://github.com/{REPO}/releases/tag/{tag}'
    return {'username': 'bloodborne-native', 'avatar_url': ICON, 'content': content,
            'allowed_mentions': {'parse': []}}


def main():
    tag = sys.argv[1]
    notes = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else f'docs/releases/{tag}.md')
    body = message(tag, notes)
    if os.environ.get('DRY_RUN') == '1':
        print(json.dumps(body, indent=1, ensure_ascii=False))
        return
    url = os.environ.get('DISCORD_RELEASES_WEBHOOK')
    if not url:
        print('DISCORD_RELEASES_WEBHOOK is not set: not posted')
        return
    request = urllib.request.Request(url + '?wait=true', data=json.dumps(body).encode(), method='POST',
                                     headers={'Content-Type': 'application/json',
                                              'User-Agent': 'bloodborne-native release'})
    with urllib.request.urlopen(request) as reply:
        print(f'Posted to Discord ({reply.status})')


if __name__ == '__main__':
    main()
