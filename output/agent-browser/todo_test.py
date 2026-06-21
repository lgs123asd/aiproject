#!/usr/bin/env python3
"""
TodoMVC 自动化测试脚本
可复现完整流程：创建任务 → 标记完成 → 验证状态

依赖: pip install playwright
安装浏览器: playwright install chromium
"""

import random
import string
import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect


def generate_random_name(length: int = 10) -> str:
    """生成随机字符串作为任务名称"""
    return ''.join(random.choices(
        string.ascii_letters + string.digits, k=length
    ))


def main():
    # 输出目录
    base_dir = Path(__file__).parent
    screenshots_dir = base_dir / "screenshots"
    record_dir = base_dir / "record"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    record_dir.mkdir(parents=True, exist_ok=True)

    # 生成三个随机任务名称
    task_names = [generate_random_name(10) for _ in range(3)]
    print(f"任务 1: {task_names[0]}")
    print(f"任务 2: {task_names[1]}")
    print(f"任务 3: {task_names[2]}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # ===================== Step 1 =====================
        print("\n[Step 1] 打开 TodoMVC 页面...")
        page.goto("https://demo.playwright.dev/todomvc/")
        page.wait_for_load_state("networkidle")

        # 检查并记录已有任务
        existing_todos = page.locator(".todo-list li")
        existing_count = existing_todos.count()
        print(f"  已有任务数: {existing_count}")

        # 截图 Step 1
        page.screenshot(path=str(screenshots_dir / "step1-initial.png"))
        print("  截图已保存: step1-initial.png")

        # ===================== Step 2 =====================
        print("\n[Step 2] 创建三个随机字符串任务...")

        todo_input = page.locator(".new-todo")
        for i, name in enumerate(task_names):
            todo_input.fill(name)
            todo_input.press("Enter")
            print(f"  创建任务 {i+1}: {name}")

        page.wait_for_timeout(500)

        # 截图 Step 2
        page.screenshot(path=str(screenshots_dir / "step2-three-tasks-created.png"))
        print("  截图已保存: step2-three-tasks-created.png")

        # ===================== Step 3 =====================
        print("\n[Step 3] 标记第 1 和第 3 个任务为已完成...")

        todos = page.locator(".todo-list li")
        todo_count = todos.count()
        assert todo_count == 3, f"期望 3 个任务，实际 {todo_count} 个"
        print(f"  当前任务总数: {todo_count}")

        # 标记第 1 个任务为已完成
        first_toggle = todos.nth(0).locator(".toggle")
        first_toggle.check()
        page.wait_for_timeout(300)
        print(f"  已标记任务 1 为完成: {task_names[0]}")

        # 标记第 3 个任务为已完成
        third_toggle = todos.nth(2).locator(".toggle")
        third_toggle.check()
        page.wait_for_timeout(300)
        print(f"  已标记任务 3 为完成: {task_names[2]}")

        # 截图 Step 3
        page.screenshot(path=str(screenshots_dir / "step3-tasks-completed.png"))
        print("  截图已保存: step3-tasks-completed.png")

        # ===================== Step 4 =====================
        print("\n[Step 4] 验证结果...")
        all_pass = True

        # 4.1 验证所有任务状态
        todos = page.locator(".todo-list li")
        for i in range(todo_count):
            li = todos.nth(i)
            label_text = li.locator("label").inner_text()
            is_completed = "completed" in (li.get_attribute("class") or "")
            is_checked = li.locator(".toggle").is_checked()

            print(f"\n  任务 {i+1}:")
            print(f"    名称: {label_text}")
            print(f"    CSS completed: {is_completed}")
            print(f"    checkbox checked: {is_checked}")

            if i == 0 or i == 2:
                # 任务 1 和 3 应为已完成
                assert is_completed, f"任务 {i+1} ({label_text}) 应为已完成状态"
                assert is_checked, f"任务 {i+1} ({label_text}) checkbox 应为已选中"
                print(f"    ✅ 验证通过: 任务 {i+1} 已正确标记为完成")
            else:
                # 任务 2 应为未完成
                assert not is_completed, f"任务 {i+1} ({label_text}) 不应为已完成状态"
                assert not is_checked, f"任务 {i+1} ({label_text}) checkbox 不应为已选中"
                # 验证名称
                assert label_text == task_names[1], \
                    f"未完成任务名称应为 '{task_names[1]}'，实际为 '{label_text}'"
                print(f"    ✅ 验证通过: 未完成任务名称匹配 '{task_names[1]}'")

        # 4.2 Active 过滤器验证
        print("\n  [4.2] Active 过滤器验证...")
        page.locator("a", has_text="Active").click()
        page.wait_for_timeout(300)

        active_todos = page.locator(".todo-list li")
        active_count = active_todos.count()
        assert active_count == 1, f"Active 视图应显示 1 个任务，实际 {active_count} 个"
        active_label = active_todos.nth(0).locator("label").inner_text()
        assert active_label == task_names[1], \
            f"Active 任务名称应为 '{task_names[1]}'，实际为 '{active_label}'"
        print(f"    ✅ Active 视图仅显示 1 个任务: '{active_label}'")

        # 截图 Step 4
        page.screenshot(path=str(screenshots_dir / "step4-active-filter.png"))
        print("  截图已保存: step4-active-filter.png")

        # 4.3 Completed 过滤器验证
        print("\n  [4.3] Completed 过滤器验证...")
        page.locator("a", has_text="Completed").click()
        page.wait_for_timeout(300)

        completed_todos = page.locator(".todo-list li")
        completed_count = completed_todos.count()
        assert completed_count == 2, f"Completed 视图应显示 2 个任务，实际 {completed_count} 个"
        print(f"    ✅ Completed 视图显示 {completed_count} 个已完成任务")

        # 截图 Completed 视图
        page.screenshot(path=str(screenshots_dir / "step5-completed-view.png"))
        print("  截图已保存: step5-completed-view.png")

        # ===================== 保存验证数据 =====================
        verification_data = [
            {
                "index": 1,
                "label": task_names[0],
                "completed": True,
                "checked": True
            },
            {
                "index": 2,
                "label": task_names[1],
                "completed": False,
                "checked": False
            },
            {
                "index": 3,
                "label": task_names[2],
                "completed": True,
                "checked": True
            }
        ]
        (record_dir / "verification.json").write_text(
            json.dumps(verification_data, indent=2, ensure_ascii=False)
        )

        browser.close()

    # ===================== 最终总结 =====================
    print("\n" + "=" * 50)
    print("  所有验证通过! ✅")
    print("=" * 50)
    print(f"  任务列表: {task_names}")
    print(f"  已完成: 任务 1 ({task_names[0]}), 任务 3 ({task_names[2]})")
    print(f"  未完成: 任务 2 ({task_names[1]})")
    print(f"\n  截图目录: {screenshots_dir}")
    print(f"  数据目录: {record_dir}")


if __name__ == "__main__":
    main()
