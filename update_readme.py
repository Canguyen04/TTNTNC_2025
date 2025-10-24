import os, json, sys

# ========================
# 🔖 MARKERS trong README.md
# ========================
# Các thẻ dùng để đánh dấu vị trí nội dung trong README.md
# Khi script chạy, phần giữa các marker này sẽ được cập nhật tự động.
STRUCT_START = "<!-- STRUCTURE_START -->"
STRUCT_END = "<!-- STRUCTURE_END -->"
PROCESS_START = "<!-- PROCESS_START -->"
PROCESS_END = "<!-- PROCESS_END -->"


# ==============================================================
# 📁 Hàm: generate_structure(root)
# --------------------------------------------------------------
# Mục đích:
#   - Duyệt toàn bộ cây thư mục từ thư mục gốc `root`
#   - Tạo cấu trúc thư mục dạng cây (tree) bằng ký tự ├──, │, └──
#   - Bỏ qua các thư mục không cần thiết như .git, __pycache__, .ipynb_checkpoints, v.v.
# ==============================================================

def generate_structure(root="."):
    ignore = {".git", "__pycache__", ".ipynb_checkpoints", "venv", "node_modules"}
    ignore_exts = {".zip"}  # ⚡ Bỏ qua các file .zip
    
    def _tree(dir_path, prefix=""):
        """Hàm đệ quy tạo chuỗi cây thư mục"""
        entries = sorted(
            [e for e in os.listdir(dir_path) if e not in ignore]
        )
        result = ""
        for i, entry in enumerate(entries):
            path = os.path.join(dir_path, entry)
            connector = "└── " if i == len(entries) - 1 else "├── "
            result += prefix + connector + entry + "\n"
            if os.path.isdir(path):
                extension = "    " if i == len(entries) - 1 else "│   "
                result += _tree(path, prefix + extension)
        return result

    return f"```\n{_tree(root)}```"


# ==============================================================
# 📅 Hàm: generate_process(path)
# --------------------------------------------------------------
# Mục đích:
#   - Đọc nội dung file process.json
#   - Tạo bảng tiến độ công việc (Process Table) dạng Markdown
# ==============================================================

def generate_process(path="process.json"):
    if not os.path.exists(path):
        return "⚠️ *Không tìm thấy process.json để tạo bảng tiến độ!*"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Tiêu đề bảng Markdown
    headers = ["Tuần", "Nội dung", "Trạng thái", "Ghi chú"]
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["------"] * len(headers)) + " |\n"

    # Duyệt từng dòng trong file JSON và ghi vào bảng
    for row in data:
        table += f"| {row.get('week', '')} | {row.get('task', '')} | {row.get('status', '')} | {row.get('note', '')} |\n"

    return table


# ==============================================================
# 🔁 Hàm: replace_section(text, start, end, new_content)
# --------------------------------------------------------------
# Mục đích:
#   - Tìm đoạn văn bản nằm giữa 2 marker trong README.md
#   - Thay thế bằng nội dung Markdown mới (cấu trúc hoặc tiến độ)
# ==============================================================

def replace_section(text, start, end, new_content):
    if start in text and end in text:
        before = text.split(start)[0]
        after = text.split(end)[1]
        return before + f"{start}\n\n{new_content}\n\n{end}" + after
    else:
        print(f"⚠️ Không tìm thấy marker {start}/{end} trong README.md — thêm mới phần đó.")
        # Nếu chưa có marker, thêm phần mới vào cuối file
        return text.strip() + f"\n\n{start}\n\n{new_content}\n\n{end}"


# ==============================================================
# 🚀 Hàm chính: main()
# --------------------------------------------------------------
# Mục đích:
#   - Đọc file README.md hiện tại
#   - Sinh mới phần cấu trúc thư mục và bảng tiến độ
#   - Thay thế nội dung giữa các marker
#   - Ghi lại file README.md
# ==============================================================

def main():
    if not os.path.exists("README.md"):
        print("❌ Không tìm thấy README.md trong thư mục hiện tại.")
        sys.exit(1)

    # Đọc nội dung README.md hiện tại
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    # Sinh nội dung mới
    structure_md = generate_structure(".")
    process_md = generate_process("process.json")

    # Cập nhật 2 phần trong README.md
    readme = replace_section(readme, STRUCT_START, STRUCT_END, structure_md)
    readme = replace_section(readme, PROCESS_START, PROCESS_END, process_md)

    # Ghi lại vào README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("✅ README.md đã được cập nhật thành công!")
    print("   - Cấu trúc thư mục đã được làm mới.")
    print("   - Bảng tiến độ đã được cập nhật.")


# ==============================================================
# ⚙️ Chạy chương trình
# --------------------------------------------------------------
# Khi bạn chạy:  python update_readme.py
# chương trình sẽ tự động thực hiện các bước trong hàm main().
# ==============================================================

if __name__ == "__main__":
    main()
