import argparse
from rich.console import Console
from rich.table import Table

from data_access_layer.database import (
    create_students_table,
    seed_demo_students,
    add_student,
    get_students,
    find_by_major,
    update_gpa,
    delete_student
)

console = Console()


def print_students(rows):
    if not rows:
        console.print("[yellow]No students found[/yellow]")
        return

    table = Table(title="Students")

    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Major")
    table.add_column("GPA", justify="right")
    table.add_column("Status")
    table.add_column("Last Updated")

    for r in rows:
        table.add_row(
            str(r["id"]),
            r["name"],
            r["email"],
            r["major"],
            f"{r['gpa']:.2f}",
            r["status"],
            r["last_updated"]
        )

    console.print(table)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    initp = sub.add_parser("init-db")
    initp.add_argument("--seed", action="store_true", help="Seed the DB with two demo students")

    add = sub.add_parser("add")
    add.add_argument("--name", required=True)
    add.add_argument("--email", required=True)
    add.add_argument("--major", required=True)
    add.add_argument("--gpa", type=float, required=True)
    add.add_argument("--status", default="active")

    lst = sub.add_parser("list")
    lst.add_argument("--status")

    find = sub.add_parser("find-major")
    find.add_argument("major")

    upd = sub.add_parser("update-gpa")
    upd.add_argument("--id", type=int, required=True)
    upd.add_argument("--gpa", type=float, required=True)

    dele = sub.add_parser("delete")
    dele.add_argument("--id", type=int, required=True)

    args = parser.parse_args()

    try:
        if args.command == "init-db":
            create_students_table()
            console.print("[green]Database initialized[/green]")
            if getattr(args, "seed", False):
                added = seed_demo_students()
                console.print(f"[green]Seed complete. Inserted {added} demo students.[/green]")

        elif args.command == "add":
            sid = add_student(
                args.name,
                args.email,
                args.major,
                args.gpa,
                args.status
            )
            console.print(f"[green]Student added with ID {sid}[/green]")

        elif args.command == "list":
            rows = get_students(args.status)
            print_students(rows)

        elif args.command == "find-major":
            rows = find_by_major(args.major)
            print_students(rows)

        elif args.command == "update-gpa":
            count = update_gpa(args.id, args.gpa)
            console.print(f"[green]Updated rows: {count}[/green]")

        elif args.command == "delete":
            count = delete_student(args.id)
            console.print(f"[green]Deleted rows: {count}[/green]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


if __name__ == "__main__":
    main()
