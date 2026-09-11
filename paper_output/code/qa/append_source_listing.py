"""Refresh the full runnable source appendix without touching authored prose."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'paper_output/final_paper_source.md'
HEADING = '## 附录 D：完整可运行源程序'


def main():
    text = SOURCE.read_text(encoding='utf-8').split(HEADING)[0].rstrip()
    paths = sorted((ROOT / 'paper_output/code/modeling').glob('*.py'))
    paths += sorted((ROOT / 'paper_output/code/visualization').glob('*.py'))
    parts = [text, HEADING,
             '以下按文件列出本次求解与图表、数值检验所用的完整源程序；文件之间的相对导入关系保持不变。运行环境依赖列于最后，运行时在仓库根目录执行附录A给出的命令。']
    for index, path in enumerate(paths, 1):
        parts += [f'### D.{index} {path.relative_to(ROOT).as_posix()}',
                  '```python\n' + '\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines()).rstrip() + '\n```']
    parts += ['### D.末 运行依赖', '```text\n' + (ROOT / 'requirements.txt').read_text(encoding='utf-8').strip() + '\n```']
    SOURCE.write_text('\n\n'.join(parts) + '\n', encoding='utf-8', newline='\n')
    print(f'Updated complete source appendix: {len(paths)} Python files')


if __name__ == '__main__':
    main()
