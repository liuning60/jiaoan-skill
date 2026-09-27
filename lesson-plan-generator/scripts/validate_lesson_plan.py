#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
教案数据校验脚本（lesson-plan-generator v1.1）
===============================================
自动校验教案生成的硬约束：
  1) 时间安排各环节分钟相加 == 总课时分钟（如 4 课时 = 180 分钟）
  2) 配图数量 >= 该课型配图下限（上机/实训 6、混合 5、理论 4，可 --min-images 覆盖）

输入：文本文件或 stdin，每行一条，格式：
  total_minutes=180      # 总课时分钟（必填）
  min_images=6           # 配图下限（可选，缺省 4）
  images=6               # 本课实际配图数（可选，缺省 0）
  导入=10                # 环节=分钟（可多个环节，名称不限，含中文）
  讲授=40
  演示=15
  学生独立练习=45
  教师巡回辅导=15
  点评小结=25
  # 以 # 开头为注释，空行忽略

用法：
  python validate_lesson_plan.py plan_data.txt
  python validate_lesson_plan.py --min-images 5 < plan_data.txt

退出码：0 = 通过；1 = 约束不满足；2 = 输入错误/无法解析
输出：JSON 报告（含各环节、合计、校验结论）
"""
import argparse
import json
import re
import sys

def parse_line(line):
    """解析 '名称=值' 行；值只支持整数。返回 (key, value) 或 None。"""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if "=" not in line:
        return None
    key, _, val = line.partition("=")
    key = key.strip()
    val = val.strip()
    if not re.fullmatch(r"\d+", val):
        return None
    return key, int(val)

def main():
    ap = argparse.ArgumentParser(description="教案硬约束校验：时间预算 + 配图下限")
    ap.add_argument("file", nargs="?", help="数据文件路径；缺省读 stdin")
    ap.add_argument("--min-images", type=int, default=None,
                    help="配图下限，覆盖数据内的 min_images（缺省 4）")
    args = ap.parse_args()

    try:
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                raw = f.read()
        else:
            raw = sys.stdin.read()
    except OSError as e:
        print(json.dumps({"success": False, "error": f"读取失败: {e}"}, ensure_ascii=False))
        return 2

    total_minutes = None
    min_images = None
    images = 0
    phases = []          # (名称, 分钟)
    parse_errors = []

    for lineno, line in enumerate(raw.splitlines(), 1):
        parsed = parse_line(line)
        if parsed is None:
            if line.strip() and not line.lstrip().startswith("#") and "=" in line:
                parse_errors.append({"line": lineno, "text": line.strip()})
            continue
        key, val = parsed
        if key == "total_minutes":
            total_minutes = val
        elif key == "min_images":
            min_images = val
        elif key == "images":
            images = val
        else:
            phases.append((key, val))

    if args.min_images is not None:
        min_images = args.min_images

    problems = []
    if total_minutes is None:
        problems.append("缺少 total_minutes（总课时分钟）")
    else:
        phase_sum = sum(v for _, v in phases)
        if phase_sum != total_minutes:
            problems.append(f"时间安排分钟相加 {phase_sum} != 总课时 {total_minutes}")
        if not phases:
            problems.append("未解析到任何教学环节")

    if min_images is None:
        min_images = 4
    if images < min_images:
        problems.append(f"配图数量 {images} < 配图下限 {min_images}")

    report = {
        "success": len(problems) == 0 and total_minutes is not None,
        "total_minutes": total_minutes,
        "phase_sum": sum(v for _, v in phases) if phases else 0,
        "phases": phases,
        "min_images": min_images,
        "images": images,
        "problems": problems,
        "parse_errors": parse_errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if parse_errors:
        return 2
    return 0 if len(problems) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
