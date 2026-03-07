#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Legado书源调试器 - 简化测试脚本
逐步显示进度，最后输出汇总结果
"""
import sys
import os
import json
import argparse
from datetime import datetime

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
os.chdir(parent_dir)


def format_log_time() -> str:
    now = datetime.now()
    return f"[{now.minute:02d}:{now.second:02d}.{now.microsecond // 1000:03d}]"


def run_test(source_file: str, keyword: str):
    with open(source_file, 'r', encoding='utf-8') as f:
        source_data = json.loads(f.read())

    if isinstance(source_data, list):
        source_data = source_data[0]

    from debugger.engine import BookSource, DebugEngine

    book_source = BookSource.from_dict(source_data)
    engine = DebugEngine(book_source)

    print(f"============================================================")
    print(f" Legado Book Source Debugger")
    print(f"============================================================")
    print(f"Book Source: {book_source.bookSourceName}")
    print(f"URL: {book_source.bookSourceUrl}")
    print(f"Keyword: {keyword}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"============================================================")
    print()

    # 正文测试（包含搜索->详情->目录->正文完整流程）
    print(f"[4] Content Test...")
    print(f"  → Searching...")

    content_result = engine.test_content(search_keyword=keyword)

    # 收集日志用于最后输出
    log_lines = []
    
    if hasattr(content_result, 'steps') and content_result.steps:
        current_step = ""
        for step_info in content_result.steps:
            if isinstance(step_info, dict):
                step_name = step_info.get('step', '正文')
                msg = step_info.get('message', '')
                state = step_info.get('state')
                
                # 显示进度
                if step_name != current_step:
                    current_step = step_name
                    if step_name == "搜索":
                        print(f"  → Searching...")
                    elif step_name == "详情":
                        print(f"  → Getting book info...")
                    elif step_name == "目录":
                        print(f"  → Getting chapter list...")
                    elif step_name == "正文":
                        print(f"  → Getting content...")
                
                # 收集日志
                if state in [10, 20, 30, 40]:
                    if msg:
                        log_lines.append(f"[{step_name}] HTML长度: {len(msg)}")
                elif msg:
                    log_lines.append(f"[{step_name}] {msg}")

    print()
    print(f"============================================================")
    print(f" Summary")
    print(f"============================================================")

    if content_result.success:
        print(f"[{format_log_time()}] Content: PASS")
        print(f"[{format_log_time()}] Overall: ALL PASS")
        
        if content_result.data:
            content_text = content_result.data.text
            print(f"\nContent Length: {len(content_text)}")
            print(f"\n--- 正文预览 ---")
            print(content_text[:500] + "..." if len(content_text) > 500 else content_text)
    else:
        print(f"[{format_log_time()}] Content: FAIL")
        print(f"[{format_log_time()}] Overall: FAILED")
        print(f"\nError: {content_result.message}")
        
        # 输出详细日志帮助调试
        if log_lines:
            print(f"\n--- 详细日志 ---")
            for line in log_lines[-20:]:  # 只显示最后20行
                print(f"  {line}")

    # 保存到文件
    with open('test_result.txt', 'w', encoding='utf-8') as f:
        f.write(f"============================================================\n")
        f.write(f" Legado Book Source Debugger\n")
        f.write(f"============================================================\n")
        f.write(f"Book Source: {book_source.bookSourceName}\n")
        f.write(f"URL: {book_source.bookSourceUrl}\n")
        f.write(f"Keyword: {keyword}\n")
        f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"============================================================\n\n")
        
        f.write(f"============================================================\n")
        f.write(f" Summary\n")
        f.write(f"============================================================\n")
        f.write(f"Content: {'PASS' if content_result.success else 'FAIL'}\n")
        f.write(f"Overall: {'ALL PASS' if content_result.success else 'FAILED'}\n")
        f.write(f"Message: {content_result.message}\n")
        
        if content_result.data:
            f.write(f"\nContent Length: {len(content_result.data.text)}\n")
            f.write(f"\n--- 正文内容 ---\n")
            f.write(content_result.data.text)
        
        if log_lines:
            f.write(f"\n\n--- 详细日志 ---\n")
            for line in log_lines:
                f.write(f"{line}\n")

    print(f"\n日志已保存到 test_result.txt")

    return content_result.success


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Legado Book Source Debugger")
    parser.add_argument("source", help="Book source JSON file")
    parser.add_argument("-k", "--keyword", default="斗破苍穹", help="Search keyword")

    args = parser.parse_args()

    run_test(args.source, args.keyword)
