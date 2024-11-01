import argparse

from launchpadding.model.item import Item


class Formatter(argparse.ArgumentDefaultsHelpFormatter):
    def format_help(self) -> str:
        return super().format_help() + (
            "\nexample usage:\n"
            "  launchpadding show --column 7\n"
            "  launchpadding fill\n"
            "  launchpadding reset\n"
        )


def main():
    parser = argparse.ArgumentParser(
        description="macOS Launchpad management", formatter_class=Formatter
    )
    parser.add_argument("command", type=str, choices=["show", "fill", "reset", "help"])
    parser.add_argument(
        "--column", "-c", type=int, default=7, help="columns of items per page"
    )

    args = parser.parse_args()

    match args.command:
        case "show":
            Item.print_layout(column=args.column)
        case "fill":
            Item.fill()
        case "reset":
            Item.reset()
        case "help":
            parser.print_help()
        case _:
            raise Exception(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
