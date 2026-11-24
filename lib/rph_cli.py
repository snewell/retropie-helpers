_DEFAULT_SCRATCH = "/dev/shm"


def add_rom_argument(ap, *, required=True, help_text="The rom to execute"):
    ap.add_argument(
        "-r",
        "--rom",
        help=help_text,
        required=required,
    )


def add_workdir_argument(
    ap, *, default=_DEFAULT_SCRATCH, help_text="Directory for temporary files"
):
    ap.add_argument(
        "-w",
        "--work-dir",
        default=default,
        help=help_text,
    )


def add_trailing_arguments(ap, *, arg_name="args", help_text="Command to execute"):
    ap.add_argument(
        arg_name,
        nargs="*",
        help=help_text,
    )


def replace_or_append_arg(args, original, replacement):
    replaced = False
    for index, arg in enumerate(args):
        if arg == original:
            args[index] = replacement
            replaced = True

    if not replaced:
        args.append(replacement)
