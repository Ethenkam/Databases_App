import os

files_to_list = [
    "backend/database.py",
    "backend/main.py",
    "backend/models.py",
    "backend/routers/__init__.py",
    "backend/routers/budget.py",
    "backend/routers/budget_item.py",
    "backend/routers/contractor.py",
    "backend/routers/department.py",
    "backend/routers/doc_type.py",
    "backend/routers/document.py",
    "backend/routers/employee.py",
    "backend/routers/export.py",
    "backend/routers/olap.py",
    "backend/routers/position.py",
    "backend/seed_data.sql",
    "frontend/index.html",
    "frontend/src/App.vue",
    "frontend/src/components/AppLayout.vue",
    "frontend/src/components/DataTable.vue",
    "frontend/src/components/FormModal.vue",
    "frontend/src/components/OlapChart.vue",
    "frontend/src/components/OlapControls.vue",
    "frontend/src/components/OlapTable.vue",
    "frontend/src/components/Sidebar.vue",
    "frontend/src/main.js",
    "frontend/src/router/index.js",
    "frontend/src/services/api.js",
    "frontend/src/style.css",
    "frontend/src/views/Budget.vue",
    "frontend/src/views/Contractors.vue",
    "frontend/src/views/Dashboard.vue",
    "frontend/src/views/Departments.vue",
    "frontend/src/views/Documents.vue",
    "frontend/src/views/Employees.vue",
    "frontend/src/views/Olap.vue",
    "frontend/src/views/OlapView.vue",
    "frontend/src/views/Positions.vue",
    "frontend/tailwind.config.js",
    "frontend/vite.config.js",
    "generate_report.py"
]

with open("code_listing.md", "w", encoding="utf-8") as f:
    f.write("# Code Listing\n\n")
    for file_path in files_to_list:
        if os.path.exists(file_path):
            f.write(f"## {file_path}\n\n")
            ext = os.path.splitext(file_path)[1][1:]
            if ext == "vue":
                ext = "html" # markdown syntax highlighting
            f.write(f"```{ext}\n")
            with open(file_path, "r", encoding="utf-8") as code_file:
                f.write(code_file.read())
            if not f.tell() == 0:
                pass
            f.write(f"\n```\n\n")

print("Created code_listing.md")
