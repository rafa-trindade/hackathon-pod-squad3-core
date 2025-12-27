from pathlib import Path
from typing import Optional


def get_project_root() -> Path:

    path = Path(__file__).resolve()

    while path.name != "scripts":
        if path.parent == path:
            raise RuntimeError("Não foi possível localizar a raiz do projeto")
        path = path.parent

    return path.parent


def init_md_report(
    report_filename: str,
    dataset_name: Optional[str] = None,
    layer: str = "raw",
):
    """
    Inicializa relatório Markdown em:
    docs/data_profiling/<layer>/<report_filename>
    """

    project_root = get_project_root()

    report_dir = project_root / "docs" / "data_profiling" / layer
    report_dir.mkdir(parents=True, exist_ok=True)

    md_file = report_dir / report_filename

    title = "# Relatório de Profiling"
    if dataset_name:
        title += f": `{dataset_name}`"

    md_file.write_text(f"{title}\n\n", encoding="utf-8")

    return md_file


def print_and_save_md(md: str, md_file: Path):
    """
    Imprime o markdown e salva (append) no arquivo informado.
    """
    print(md)

    with md_file.open("a", encoding="utf-8") as f:
        f.write(md)
        f.write("\n\n---\n\n")

def df_to_md(df):
    return (
        df
        .astype("object") 
        .where(df.notna(), "NULL")
        .to_markdown(index=False)
    )