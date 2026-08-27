#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

def split_blocks(lines):
    """
    将文本按以下格式分割成 (标题, 内容行列表) 的块：
        =====...
        章节标题
        =====...
        内容行...
        =====...
        下一个标题
        =====...
        下一个内容...
    """
    # 找出所有分隔线的行索引
    sep_indices = [i for i, line in enumerate(lines) if re.match(r'^={5,}', line)]
    if not sep_indices:
        return [("Unknown", lines)]

    # 按分隔线切割文本段，段 i 为 sep_indices[i-1]+1 到 sep_indices[i]-1
    prev = 0
    segments = []
    for idx in sep_indices:
        segments.append(lines[prev:idx])   # 不包括分隔线本身
        prev = idx + 1
    segments.append(lines[prev:])          # 最后一段

    blocks = []
    # 从第1段开始（第0段通常是文件头或空），两两配对：奇数段为标题，偶数段为内容
    for i in range(1, len(segments), 2):
        title_segment = segments[i]
        # 提取标题：取第一个非空行
        title = None
        for line in title_segment:
            if line.strip():
                title = line.strip()
                break
        if title is None:
            continue
        # 内容段是下一个段（如果存在）
        content_segment = segments[i+1] if i+1 < len(segments) else []
        blocks.append((title, content_segment))
    return blocks

def parse_commands(lines):
    md = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('  ') and not line.startswith('    '):
            md.append(f"## {line.strip()}")
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.startswith('  ') and not nxt.startswith('    '):
                    break
                stripped = nxt.strip()
                if stripped.startswith('Usage:'):
                    # 提取命令内容，去掉前缀，并用反引号包裹
                    cmd = stripped[len('Usage:'):].strip()
                    md.append(f"- Usage: `{cmd}`")
                elif stripped.startswith('Perm:'):
                    # 提取权限值，去掉前缀，并用反引号包裹
                    perm = stripped[len('Perm:'):].strip()
                    md.append(f"- Perm: `{perm}`")
                i += 1
        else:
            i += 1
    return '\n'.join(md)

def parse_table(lines):
    """解析表格章节（CHARACTERS / WEAPONS），返回 Markdown 表格。"""
    if not lines:
        return ""

    # 找出表头行、分隔行和数据行
    header_row = None
    sep_row = None
    data_rows = []
    for line in lines:
        if not line.strip():
            continue
        if re.search(r'---', line) and re.search(r'\s', line):
            sep_row = line
            continue
        if header_row is None:
            header_row = line
        else:
            data_rows.append(line)

    if header_row is None:
        return ""

    # 如果有分隔行，用分隔行确定列边界
    if sep_row:
        matches = list(re.finditer(r'-+', sep_row))
        if not matches:
            return ""

        col_boundaries = []
        for idx, m in enumerate(matches):
            start = m.start()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(sep_row)
            col_boundaries.append((start, end))

        # 提取表头
        header_cols = [header_row[s:e].strip() for s, e in col_boundaries]
        md_lines = [
            '| ' + ' | '.join(header_cols) + ' |',
            '| ' + ' | '.join(['---'] * len(header_cols)) + ' |'
        ]
        # 处理数据行
        for row in data_rows:
            cols = [row[s:e].strip() for s, e in col_boundaries]
            md_lines.append('| ' + ' | '.join(cols) + ' |')
        return '\n'.join(md_lines)
    else:
        # 无分隔行，按两个以上空格拆分（容错）
        header_cols = re.split(r'\s{2,}', header_row.strip())
        md_lines = [
            '| ' + ' | '.join(header_cols) + ' |',
            '| ' + ' | '.join(['---'] * len(header_cols)) + ' |'
        ]
        for row in data_rows:
            cols = re.split(r'\s{2,}', row.strip())
            while len(cols) < len(header_cols):
                cols.append('')
            md_lines.append('| ' + ' | '.join(cols) + ' |')
        return '\n'.join(md_lines)

def is_table_content(lines):
    """检测内容中是否包含表格分隔行（如 '--------  ----------'）"""
    for line in lines:
        if re.search(r'---', line) and re.search(r'\s', line):
            return True
    return False

def convert_txt_to_md(txt):
    lines = txt.splitlines()
    blocks = split_blocks(lines)
    md_parts = []

    for title, content in blocks:
        if not title:
            continue

        upper_title = title.upper()

        # 1. 命令章节
        if 'COMMANDS' in upper_title:
            md_parts.append(f"# {title}\n\n{parse_commands(content)}")
        # 2. 表格章节（不再限制标题名，只看内容是否有分隔线）
        elif is_table_content(content):
            md_parts.append(f"# {title}\n\n{parse_table(content)}")
        # 3. 其他未知内容，保留原样
        else:
            md_parts.append(f"# {title}\n\n```\n" + '\n'.join(content) + "\n```")

    return '\n\n'.join(md_parts)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python txt2md.py 输入文件.txt [输出文件.md]")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'handbook.md'
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            txt = f.read()
        md = convert_txt_to_md(txt)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"转换成功！输出文件：{output_file}")
    except Exception as e:
        print(f"出错: {e}")
        sys.exit(1)