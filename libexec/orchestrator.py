#!/usr/bin/python3
# libexec/orchestrator.py (Explicit Parameter Edition)
import argparse
import subprocess
import os

_XDELTA_DEFAULT_SYSTEMS = [
    "dreamcast",
    "gc",
    "ps2",
    "psp",
    "psx",
    "wii",
]

class EmulatorOrchestrator:
    def __init__(self, prog_name, description):
        self.prog_name = prog_name
        self.description = description

        self._parser = argparse.ArgumentParser(prog=prog_name, description=description)

        # 1. CORE TELEMETRY: Explicitly pass system parameters downstream
        self._parser.add_argument("--rom", required=True, help="Absolute path to the target game file")
        self._parser.add_argument("--system", required=True, help="The internal system tag name (e.g. snes, ps2)")
        self._parser.add_argument("--dry-run", action="store_true", help="Print the final execution pipeline without executing it (useful for debugging)")

        # 2. FEATURE REGISTRATION HOOKS
        self._parser.add_argument("--emu-arg", action="append", default=[], dest="emu_args")
        self._execution_pipeline = []
        self.libexec_path = os.path.dirname(os.path.abspath(__file__))

    def add_feature(self, feature_name, choices=("auto", "force", "disable"), default="auto"):
        flag_name = f"--{feature_name.replace('_', '-')}"
        self._parser.add_argument(flag_name, choices=choices, default=default)
        self._parser.add_argument(f"{flag_name}-arg", action="append", default=[], dest=f"{feature_name}_arg")

        self._execution_pipeline.append(feature_name)
        return self

    # -------------------------------------------------------------------------
    # DECIDED EXPLICIT FEATURE HANDLERS
    # -------------------------------------------------------------------------
    def _handle_unique_memcard(self, args, final_command):
        if args.unique_memcard != "disable" and (args.unique_memcard_arg or args.unique_memcard == "force"):
            exe = os.path.join(self.libexec_path, "rph-unique-memcard")
            # We can now forward --rom down cleanly to sub-tools if needed!
            final_command.extend([exe, "-f", args.rom, *args.unique_memcard_arg, "--"])

    def _handle_savepath_injector(self, args, final_command):
        if args.savepath_injector != "disable":
            exe = os.path.join(self.libexec_path, "rph-savepath-injector")
            final_command.extend([exe, *args.savepath_injector_arg, "--"])

    def _handle_xdelta_patcher(self, args, final_command):
        if args.xdelta_patcher != "disable":
            if args.xdelta_patcher == "force" or args.system in _XDELTA_DEFAULT_SYSTEMS:
                exe = os.path.join(self.libexec_path, "rph-xdelta-patcher")
                # Uses the pristine, explicit args.rom string parameter natively!
                final_command.extend([exe, "-f", args.rom, *args.xdelta_patcher_arg, "--"])

    def _handle_setup_ps3_disc(self, args, final_command):
        if args.setup_ps3_disc != "disable" and (args.setup_ps3_disc_arg or args.setup_ps3_disc == "force"):
            exe = os.path.join(self.libexec_path, "rph-setup-ps3-disc")
            final_command.extend([exe, "-f", args.rom, *args.setup_ps3_disc_arg, "--"])

    def parse_and_execute(self, custom_mutator_fn=None):
        self._parser.add_argument("args", nargs="*")
        args = self._parser.parse_args()

        final_command = []

        # Execute our structured feature pipeline in exact registered order
        for feature in self._execution_pipeline:
            handler = getattr(self, f"_handle_{feature}", None)
            if handler:
                handler(args, final_command)

        emulator_payload = args.args

        # Apply domain-specific mutations if specified
        if custom_mutator_fn and args.emu_args:
            emulator_payload = custom_mutator_fn(emulator_payload, args.emu_args)

        final_command.extend(emulator_payload)
        if args.dry_run:
            print(f"executing {final_command}")
        else:
            subprocess.run(final_command, check=True)
