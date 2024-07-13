#!/usr/bin/python3
"""This script converts a Markdown file to an HTML file.
First argument: markdown file
Second argument: html file"""

from sys import argv, stderr, exit
import os
import html


def convert_markdown_to_html(md_lines):
    html_lines = []
    unordered_list = []
    ordered_list = []
    paragraphs = []

    for line in md_lines:
        line = line.rstrip()
        if line.startswith('#'):
            level = line.count('#')
            html_lines.append('<h{}>{}</h{}>'.format(level,
                                                     html.escape(line[level+1:].strip()),
                                                     level))
        elif line.startswith('- '):
            unordered_list.append('<li>{}</li>'.format(html.escape(line[2:].strip())))
        elif line.startswith('* '):
            ordered_list.append('<li>{}</li>'.format(html.escape(line[2:].strip())))
        else:
            paragraphs.append(line)

    if unordered_list:
        html_lines.append('<ul>')
        html_lines.extend(unordered_list)
        html_lines.append('</ul>')

    if ordered_list:
        html_lines.append('<ol>')
        html_lines.extend(ordered_list)
        html_lines.append('</ol>')

    if paragraphs:
        paragraph_text = "\n".join(paragraphs).strip()
        if paragraph_text:
            html_lines.append('<p>{}</p>'.format(html.escape(paragraph_text).replace('\n', '<br />')))

    return html_lines


if __name__ == "__main__":
    if len(argv) <= 2:
        print('Usage: ./markdown2html.py README.md README.html', file=stderr)
        exit(1)
    elif not os.path.exists(argv[1]):
        print('Missing {}'.format(argv[1]), file=stderr)
        exit(1)
    else:
        with open(argv[1], 'r') as md_file:
            lines = md_file.readlines()

        html_content = convert_markdown_to_html(lines)

        with open(argv[2], 'w') as html_file:
            html_file.writelines('\n'.join(html_content))

        exit(0)
