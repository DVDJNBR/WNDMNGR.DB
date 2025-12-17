"""
Fix missing semicolons in PostgreSQL files
Temporary script
"""
from pathlib import Path
import re

BASE_DIR = Path(__file__).parent
TABLES_DIR = BASE_DIR / 'TABLES'

def fix_semicolons(sql_content: str) -> str:
    """Add missing semicolons to SQL statements"""

    lines = sql_content.split('\n')
    fixed_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith('--'):
            fixed_lines.append(line)
            continue

        # Check if this line ends a statement (ends with ) or value) and doesn't have ;
        if stripped.endswith(')') and not stripped.endswith(';'):
            # Check if next line is empty, comment, or starts new statement
            is_end_of_statement = False

            if i + 1 >= len(lines):
                # Last line
                is_end_of_statement = True
            else:
                next_line = lines[i + 1].strip()
                # Next line is empty, comment, or starts with INSERT/CREATE
                if (not next_line or
                    next_line.startswith('--') or
                    next_line.upper().startswith('INSERT') or
                    next_line.upper().startswith('CREATE')):
                    is_end_of_statement = True

            if is_end_of_statement:
                fixed_lines.append(line + ';')
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def main():
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    print("=" * 60)
    print("FIX SQL SEMICOLONS")
    print("=" * 60)
    print()

    sql_files = list(TABLES_DIR.glob('**/*.sql'))

    print(f"Found {len(sql_files)} SQL files")
    print()

    fixed_count = 0

    for sql_file in sql_files:
        relative_path = sql_file.relative_to(TABLES_DIR)

        # Read file
        with open(sql_file, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # Fix semicolons
        fixed_content = fix_semicolons(original_content)

        # Check if changed
        if original_content != fixed_content:
            with open(sql_file, 'w', encoding='utf-8') as f:
                f.write(fixed_content)

            print(f"✓ Fixed: {relative_path}")
            fixed_count += 1
        else:
            print(f"  Skip:  {relative_path} (no changes)")

    print()
    print("=" * 60)
    print(f"✓ Fixed {fixed_count}/{len(sql_files)} files")
    print("=" * 60)


if __name__ == '__main__':
    main()
