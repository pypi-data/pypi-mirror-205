"""
Main program execution.
"""

from kireji.comms.group import group


def main(args: list[str] | None = None):
    """
    Run the main Kireji program.
    """

    group.main(args, prog_name="kireji")


if __name__ == "__main__":
    main()
