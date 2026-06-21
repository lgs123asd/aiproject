"""
TodoMVC Web自动化测试脚本
============================
使用 Playwright 自动化完成以下任务：
1. 打开 TodoMVC 演示页面
2. 检查已有任务
3. 创建三个随机字符串任务
4. 将第1和第3个任务标记为已完成
5. 验证任务状态

依赖: pip install playwright
需要先运行: playwright install chromium
"""

import os
import random
import string
from pathlib import Path
from playwright.sync_api import sync_playwright


# ============================================================
# 配置
# ============================================================
TODOMVC_URL = "https://demo.playwright.dev/todomvc/"
OUTPUT_DIR = Path(__file__).parent  # 脚本所在目录
SCREENSHOTS_DIR = OUTPUT_DIR / "screenshots"
RECORD_DIR = OUTPUT_DIR / "record"


def ensure_dirs():
    """确保输出目录存在"""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    RECORD_DIR.mkdir(parents=True, exist_ok=True)


def generate_random_string(length=8):
    """生成指定长度的随机字符串（字母+数字）"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def screenshot(page, name):
    """截图并保存到 screenshots 目录"""
    path = str(SCREENSHOTS_DIR / name)
    page.screenshot(path=path, full_page=False)
    print(f"  📸 Screenshot saved: {path}")
    return path


def save_record(filename, data):
    """保存记录到 record 目录"""
    import json
    path = RECORD_DIR / filename
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  📝 Record saved: {path}")


# ============================================================
# 主测试流程
# ============================================================
def run_test():
    ensure_dirs()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True 可无头运行
        context = browser.new_context()
        page = context.new_page()

        # ----------------------------------------------------------
        # 步骤 1：导航到 TodoMVC
        # ----------------------------------------------------------
        print("=" * 60)
        print("Step 1: Navigate to TodoMVC")
        print("=" * 60)
        page.goto(TODOMVC_URL)
        page.wait_for_load_state("networkidle")
        print(f"  Page title: {page.title()}")
        screenshot(page, "step1-initial-page.png")

        # ----------------------------------------------------------
        # 步骤 2：检查已有任务
        # ----------------------------------------------------------
        print("\n" + "=" * 60)
        print("Step 2: Check existing tasks")
        print("=" * 60)
        todo_items = page.locator(".todo-list li").all()
        existing_tasks = []
        for item in todo_items:
            label = item.locator("label").inner_text()
            existing_tasks.append(label)

        print(f"  Existing tasks: {existing_tasks if existing_tasks else '(none)'}")
        save_record("snapshot-initial.json", {
            "step": "initial-state",
            "url": page.url,
            "title": page.title(),
            "existing_tasks": existing_tasks,
            "note": "No existing todo items on page" if not existing_tasks else f"Found {len(existing_tasks)} existing items"
        })

        # ----------------------------------------------------------
        # 步骤 3：创建三个随机字符串任务
        # ----------------------------------------------------------
        print("\n" + "=" * 60)
        print("Step 3: Create 3 random string tasks")
        print("=" * 60)

        # 生成并记录随机任务名称
        task_names = [generate_random_string(8) for _ in range(3)]
        print(f"  Generated task names:")
        for i, name in enumerate(task_names, 1):
            print(f"    Task {i}: {name}")

        # 输入框
        input_box = page.get_by_placeholder("What needs to be done?")

        for i, name in enumerate(task_names, 1):
            input_box.fill(name)
            input_box.press("Enter")
            print(f"  ✅ Task {i} '{name}' created")
            page.wait_for_timeout(300)  # 等待动画

        screenshot(page, "step2-three-tasks-created.png")

        # 验证三个任务都已创建
        todo_items = page.locator(".todo-list li").all()
        assert len(todo_items) == 3, f"Expected 3 tasks, found {len(todo_items)}"
        print(f"  ✅ All 3 tasks created successfully")

        # ----------------------------------------------------------
        # 步骤 4：标记第1和第3个任务为已完成
        # ----------------------------------------------------------
        print("\n" + "=" * 60)
        print("Step 4: Mark tasks 1 and 3 as completed")
        print("=" * 60)

        # 点击第1个任务的复选框
        task1_checkbox = page.locator(".todo-list li").nth(0).locator(".toggle")
        task1_checkbox.click()
        print(f"  ✅ Task 1 '{task_names[0]}' marked as completed")

        # 点击第3个任务的复选框
        task3_checkbox = page.locator(".todo-list li").nth(2).locator(".toggle")
        task3_checkbox.click()
        print(f"  ✅ Task 3 '{task_names[2]}' marked as completed")

        page.wait_for_timeout(300)
        screenshot(page, "step3-tasks-1-3-completed.png")

        # 验证 "1 item left" 显示
        items_left = page.locator(".todo-count strong").inner_text()
        assert items_left == "1", f"Expected 1 item left, found {items_left}"
        print(f"  ✅ Items left counter shows: {items_left}")

        # ----------------------------------------------------------
        # 步骤 5：验证测试结果
        # ----------------------------------------------------------
        print("\n" + "=" * 60)
        print("Step 5: Verify task states")
        print("=" * 60)

        # 5.1 Active 视图验证
        print("\n  5.1 Active view verification")
        page.get_by_role("link", name="Active").click()
        page.wait_for_timeout(300)
        screenshot(page, "step4-verify-active-view.png")

        active_items = page.locator(".todo-list li").all()
        active_names = [item.locator("label").inner_text() for item in active_items]
        print(f"  Active tasks: {active_names}")

        # 验证：仅剩任务2 (jl8Rb4lU) 未完成
        assert len(active_items) == 1, f"Expected 1 active task, found {len(active_items)}"
        assert active_names[0] == task_names[1], \
            f"Expected active task '{task_names[1]}', found '{active_names[0]}'"
        print(f"  ✅ Active view PASS: only '{task_names[1]}' remains uncompleted")

        # 5.2 Completed 视图验证
        print("\n  5.2 Completed view verification")
        page.get_by_role("link", name="Completed").click()
        page.wait_for_timeout(300)
        screenshot(page, "step5-verify-completed-view.png")

        completed_items = page.locator(".todo-list li").all()
        completed_names = [item.locator("label").inner_text() for item in completed_items]
        print(f"  Completed tasks: {completed_names}")

        # 验证：任务1和任务3为已完成
        assert len(completed_items) == 2, f"Expected 2 completed tasks, found {len(completed_items)}"
        assert task_names[0] in completed_names, \
            f"Task 1 '{task_names[0]}' not found in completed list"
        assert task_names[2] in completed_names, \
            f"Task 3 '{task_names[2]}' not found in completed list"
        print(f"  ✅ Completed view PASS: tasks 1 and 3 are completed")

        # ----------------------------------------------------------
        # 保存最终验证结果
        # ----------------------------------------------------------
        save_record("verification-results.json", {
            "verification_time": "completed",
            "tasks_created": [
                {"index": 1, "name": task_names[0], "status": "completed"},
                {"index": 2, "name": task_names[1], "status": "active"},
                {"index": 3, "name": task_names[2], "status": "completed"},
            ],
            "verification_results": {
                "task_1_completed": True,
                "task_3_completed": True,
                "remaining_uncompleted": task_names[1],
                "name_match": True,
                "active_count": 1,
                "completed_count": 2,
                "all_checks_passed": True,
            },
            "active_view_only_shows": [task_names[1]],
            "completed_view_shows": [task_names[0], task_names[2]],
        })

        # ----------------------------------------------------------
        # 最终总结
        # ----------------------------------------------------------
        print("\n" + "=" * 60)
        print("ALL VERIFICATIONS PASSED! 🎉")
        print("=" * 60)
        print(f"  Task 1 '{task_names[0]}': ✅ Completed")
        print(f"  Task 2 '{task_names[1]}': ⬜ Active")
        print(f"  Task 3 '{task_names[2]}': ✅ Completed")
        print(f"\n  Task names used (for reproduction):")
        print(f"    TASK_NAMES = {task_names}")

        # 清理
        browser.close()


if __name__ == "__main__":
    run_test()
