# 1/usr/bin/python3

import argparse
import grp
import os
import os.path
import pwd
import re
import shutil
import sys

from datetime import datetime

_MEMINFO_RE = re.compile(r"MemTotal:\s+(\d+)\s+kB")


def _get_ram_total():
    with open("/proc/meminfo", "r", encoding="utf-8") as mi:
        for line in mi:
            m = _MEMINFO_RE.match(line)
            if m:
                kb_size = int(m.group(1))
                # convert to GB
                return int(kb_size / 1000 / 1000)
    raise RuntimeError("Failed to extract ram size")


def _guess_tmpfs_size():
    print("  Guessing tmpfs size...")
    total_mem = _get_ram_total()
    print(f"    ...detected {total_mem} GB...")
    to_use = int(total_mem / 2)
    if to_use == 0:
        raise RuntimeError("Inssufficient memory for a tmpfs")
    print(f"    ...reserving {to_use} for tmpfs")
    return to_use


def _guess_user():
    print("  Guessing username...")
    uid = os.getuid()
    if uid == 0:
        # running as root
        print("    ...running as root...")
        sudo_user = os.environ.get("SUDO_USER")
        if sudo_user:
            print(f"    ...sudo running as {sudo_user}...")
            return sudo_user
        raise RuntimeError("Unable to determine real user")
    user_info = pwd.getpwuid(uid)
    return user_info.pw_name


def _guess_group():
    print("  Guessing group...")
    uid = os.getuid()
    real_gid = None
    if uid == 0:
        print("    ...running as root...")
        sudo_gid = os.environ.get("SUDO_GID")
        if sudo_gid:
            real_gid = int(sudo_gid)
            print(f"    ...running with gid {real_gid}")
        else:
            raise RuntimeError("Unable to determine real group")
    else:
        user_info = pwd.getpwuid(uid)
        real_gid = user_info.pw_gid
    group_info = grp.getgrgid(real_gid)
    return group_info.gr_name


def _check_fstab_options(options, user, group, size):
    options_split = options.split(",")
    errors = []
    got_size = False
    got_uid = False
    got_gid = False
    got_mode = False
    got_noatime = False
    for o in options_split:
        o_parts = o.split("=")
        if o_parts[0] == "size":
            if o_parts[1] != f"{size}G":
                errors.append(f"Incorrect size ({o_parts[1]})")
            got_size = True
        elif o_parts[0] == "uid":
            if o_parts[1] != user:
                errors.append(f"Incorrect uid ({o_parts[1]})")
            got_uid = True
        elif o_parts[0] == "gid":
            if o_parts[1] != group:
                errors.append(f"Incorrect gid ({o_parts[1]})")
            got_gid = True
        elif o_parts[0] == "mode":
            if o_parts[1] != "755":
                errors.append(f"Incorrect mode ({o_parts[1]})")
            got_mode = True
        elif o_parts[0] == "noatime":
            got_noatime = True
        else:
            print(f"Unexpected option: {o_parts[0]}")

    if not got_size:
        errors.append("Missing size option")
    if not got_uid:
        errors.append("Missing uid option")
    if not got_gid:
        errors.append("Missing gid option")
    if not got_mode:
        errors.append("Missing mode option")
    if not got_noatime:
        errors.append("Missing noatime option")

    return errors


def _check_fstab(mount_point, user, group, size):
    with open("/etc/fstab", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "#" in line:
                line = line.split("#", 1)[0].strip()
                if not line:  # Line was just a comment
                    continue

            parts = line.split()

            if len(parts) < 4:
                # we need at least filesystem, mount point, fs type, and options
                continue

            if parts[1] == mount_point:
                # we found our point
                errors = []
                if parts[0] != "tmpfs":
                    errors.append(f"Incorrect filesystem ({parts[0]})")
                if parts[2] != "tmpfs":
                    errors.append(f"Incorrect filesystem type ({parts[2]})")
                errors += _check_fstab_options(parts[3], user, group, size)
                if len(parts) > 4 and parts[4] != "0":
                    print(f"Unexpected dump value ({parts[4]})", file=sys.stderr)
                if len(parts) > 5 and parts[5] != "0":
                    print(f"Unexpected backup value ({parts[5]})", file=sys.stderr)

                if errors:
                    raise RuntimeError("\n".join(errors))
                return True
    return False


def _main():
    parser = argparse.ArgumentParser(
        prog="setup-tmpfs",
        description="Generate a tmpfs entry in /etc/fstab for scratch work",
    )
    parser.add_argument(
        "-s",
        "--size",
        help="Size (GB) of the tmpfs",
        type=int,
    )
    parser.add_argument(
        "-u",
        "--user",
        help="Username of the primary user",
    )
    parser.add_argument(
        "-g",
        "--group",
        help="Group of the primary user",
    )
    parser.add_argument(
        "-p",
        "--path",
        help="Path to mount the tmpfs",
        default="/mnt/scratch",
    )
    parser.add_argument(
        "--execute",
        help="Automatically add the line to tmpfs (requires root)",
        action="store_true",
    )
    parser.add_argument(
        "--check",
        help="Check if the entry already exists",
        action="store_true",
    )
    args = parser.parse_args()
    if args.execute:
        uid = os.getuid()
        if uid != 0:
            print(f"--execute requires root")
            sys.exit(1)

    if args.size is None:
        args.size = _guess_tmpfs_size()
    if args.size < 4:
        print(
            "    WARNING: Low memory, consider disabling xdelta-patcher for large games"
        )
    if args.user is None:
        args.user = _guess_user()
    if args.group is None:
        args.group = _guess_group()

    tmpfs_line = f"tmpfs\t{args.path}\ttmpfs\tsize={args.size}G,uid={args.user},gid={args.group},mode=755,noatime 0 0\n"

    if args.execute:
        print("Checking /etc/fstab...")
        if _check_fstab(args.path, args.user, args.group, args.size):
            print("    ...already configured, nothing to do")
        else:
            now = datetime.now()
            timestamp_str = now.strftime("%Y%m%d-%H%M%S")
            backup_file = f"/etc/fstab.{timestamp_str}"
            print(f"    ...backing up to {backup_file}")
            shutil.copy2("/etc/fstab", backup_file)
            with open("/etc/fstab", "a", encoding="utf-8") as f:
                f.write("\n\n# Automatically generated by rph-setup-tmpfs\n")
                f.write(f"{tmpfs_line}\n")
        print(f"Verifying that mount point exists...")
        if not os.path.exists(args.path):
            print(f"    ...creating mount point directory {args.path}")
            os.makedirs(args.path, mode=0o755, exist_ok=True)
            print("    ...done")
        else:
            print("    ...mount point already exists")
    elif args.check:
        print("Checking /etc/fstab")
        if _check_fstab(args.path, args.user, args.group, args.size):
            print("    ...already configured!")
        else:
            print("    ...no entry")
    else:
        print(f"Expected line: {tmpfs_line}")


if __name__ == "__main__":
    _main()
