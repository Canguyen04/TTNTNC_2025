import os, json, sys

# MARKERS trong README.md
STRUCT_START = "<!-- STRUCTURE_START -->"
STRUCT_END = "<!-- STRUCTURE_END -->"
PROCESS_START = "<!-- PROCESS_START -->"
PROCESS_END = "<!-- PROCESS_END -->"

def generate_structure(root="."):
    """
    📁 Hàm: generate_structure(root)
    --------------------------------
    Mục đích:
        - Duyệt toàn bộ thư mục bắt đầu từ `root`
        - Tạo ra cấu trúc thư mục dạng danh sách Markdown (list)
        - Bỏ qua các thư mục không cần thiết như .git, venv, node_modules, v.v.

    Tham số:
        root (str): Đường dẫn thư mục gốc (mặc định là thư mục hiện tại ".")

    Kết quả:
        Trả về chuỗi Markdown biểu diễn cấu trúc thư mục, ví dụ:
            - 📁 project/
              - 📁 src/
                - 📄 main.py
              - 📄 README.md
    """
    ignore = {".git", "__pycache__", ".github", "venv", "node_modules"}
    lines = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Bỏ qua thư mục không cần thiết
        dirnames[:] = [d for d in dirnames if d not in ignore]

        depth = dirpath.count(os.sep)
        indent = "  " * depth
        folder = os.path.basename(dirpath)

        if depth == 0:
            lines.append(f"- 📁 **{folder or '.'}**")
        else:
            lines.append(f"{indent}- 📁 {folder}/")

        for f in filenames:
            # Bỏ qua chính file script này để tránh liệt kê vòng lặp
            if f == os.path.basename(__file__):
                continue
            lines.append(f"{indent}  - 📄 {f}")
    return "\n".join(lines)


def generate_process(path="process.json"):
    """
    📅 Hàm: generate_process(path)
    ------------------------------
    Mục đích:
        - Đọc file `process.json`
        - Sinh bảng tiến độ (Process) dưới dạng Markdown table

    Tham số:
        path (str): Đường dẫn đến file JSON chứa dữ liệu tiến độ

    Kết quả:
        Trả về chuỗi Markdown của bảng Process, ví dụ:

        | Tuần | Nội dung | Trạng thái | Ghi chú |
        |------|-----------|-------------|---------|
        | WEEK 1 | Làm báo cáo | ✅ Hoàn thành | Đã nộp |
    """
    if not os.path.exists(path):
        return "⚠️ *Không tìm thấy process.json*"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    headers = ["Tuần", "Nội dung", "Trạng thái", "Ghi chú"]
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["------"] * len(headers)) + " |\n"

    for row in data:
        table += f"| {row.get('week', '')} | {row.get('task', '')} | {row.get('status', '')} | {row.get('note', '')} |\n"

    return table


def replace_section(text, start, end, new_content):
    """
    🔁 Hàm: replace_section(text, start, end, new_content)
    -----------------------------------------------------
    Mục đích:
        - Thay thế nội dung nằm giữa hai marker trong README.md
          (ví dụ: <!-- STRUCTURE_START --> và <!-- STRUCTURE_END -->)

    Tham số:
        text (str): Nội dung toàn bộ README.md
        start (str): Marker bắt đầu (ví dụ: STRUCT_START)
        end (str): Marker kết thúc (ví dụ: STRUCT_END)
        new_content (str): Nội dung Markdown mới cần chèn vào

    Kết quả:
        Trả về nội dung README.md mới sau khi thay thế.
        Nếu không tìm thấy marker thì giữ nguyên nội dung ban đầu.
    """
    if start in text and end in text:
        before = text.split(start)[0]
        after = text.split(end)[1]
        return before + f"{start}\n\n{new_content}\n\n{end}" + after
    else:
        print(f"⚠️ Không tìm thấy marker {start}/{end}")
        return text


def main():
    """
    🚀 Hàm chính: main()
    --------------------
    Mục đích:
        - Kiểm tra sự tồn tại của file README.md
        - Sinh cấu trúc thư mục và bảng tiến độ
        - Ghi đè các phần tương ứng trong README.md bằng nội dung mới

    Quy trình:
        1. Đọc README.md
        2. Tạo cấu trúc thư mục (generate_structure)
        3. Tạo bảng tiến độ (generate_process)
        4. Thay thế nội dung giữa các marker
        5. Ghi lại file README.md
    """
    if not os.path.exists("README.md"):
        print("❌ Không tìm thấy README.md")
        sys.exit(1)

    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    structure_md = generate_structure(".")
    process_md = generate_process("process.json")

    readme = replace_section(readme, STRUCT_START, STRUCT_END, structure_md)
    readme = replace_section(readme, PROCESS_START, PROCESS_END, process_md)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("✅ README.md đã được cập nhật thành công!")


if __name__ == "__main__":
    main()
