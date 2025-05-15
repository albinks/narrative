"""Generate the API reference pages."""


import mkdocs_gen_files

# Map of module paths to their corresponding documentation files
MODULE_DOCS_MAP = {
    "narrative.core.idg_builder": "api/idg-engine.md",
    "narrative.core.trajectory_explorer": "api/trajectory-explorer.md",
    "narrative.llm.llm_renderer": "api/llm-bridge.md",
}

# Generate the API reference pages
for module_path, doc_path in MODULE_DOCS_MAP.items():
    with mkdocs_gen_files.open(doc_path, "w") as f:
        print(f"# {module_path.split('.')[-1].replace('_', ' ').title()}", file=f)
        print(file=f)
        print(f":::{module_path}", file=f)
        print(file=f)

# Create the .pages file to customize the section title
with mkdocs_gen_files.open("api/.pages", "w") as f:
    print("title: API Reference", file=f)
