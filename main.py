import argparse

from launchpadding.model.item import Item


class Formatter(argparse.ArgumentDefaultsHelpFormatter):
    def format_help(self) -> str:
        return super().format_help() + (
            "\nexample usage:\n"
            "  launchpadding show\n"
            "  launchpadding fill\n"
            "  launchpadding sort --method [title|color] [--reverse]\n"
            "  launchpadding reset\n"
        )


def main():
    parser = argparse.ArgumentParser(
        description="macOS Launchpad management", formatter_class=Formatter
    )
    command_parser = parser.add_subparsers(dest="command", required=True)

    command_parser.add_parser("show")
    command_parser.add_parser("fill")
    sort_parser = command_parser.add_parser("sort")
    command_parser.add_parser("reset")
    command_parser.add_parser("help")

    sort_parser.add_argument(
        "--method",
        "-m",
        type=str,
        default="title",
        choices=["title", "color"],
        help="sorting method",
    )
    sort_parser.add_argument(
        "--reverse",
        "-r",
        action="store_true",
        help="sort in descending order",
    )

    args = parser.parse_args()
    match args.command:
        case "show":
            Item.print_layout()
        case "fill":
            Item.fill()
        case "sort":
            match args.method:
                case "title":
                    Item.sort_by_title(reverse=args.reverse)
                case "color":
                    Item.sort_by_color(reverse=args.reverse)
        case "reset":
            Item.reset()
        case "help":
            parser.print_help()


if __name__ == "__main__":
    main()
