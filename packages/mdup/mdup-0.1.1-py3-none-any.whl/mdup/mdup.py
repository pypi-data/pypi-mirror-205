import re
import subprocess
from argparse import ArgumentParser, Namespace
from copy import copy
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Loc:
    beg: int
    end: int
    kind: str
    path: Path


class ParseError(Exception):
    pass


class Transform:
    kinds = {"SRC", "RUN"}
    pattern_beg = f"^(<!-- MDUP:BEG \\(({'|'.join(kinds)}):(.+)\\) -->)$"
    pattern_end = "^(<!-- MDUP:END -->)$"

    def __init__(self, input_file: Path, output_file: Path):
        self.input_file = input_file
        self.output_file = output_file
        self._lines = self._read_lines()

    def _read_lines(self) -> list[str]:
        with open(self.input_file, "rt") as fp:
            return fp.readlines()

    def _parse_pattern_locs(self):
        cur_loc = None
        out = []

        for i, line in enumerate(self._lines):
            if m := re.match(self.pattern_beg, line):
                if cur_loc:
                    raise ParseError(f"Found new BEG before END on line {i+1}")
                cur_loc = Loc(
                    beg=i,
                    end=None,
                    kind=m.group(2),
                    path=self.input_file.parent / m.group(3),
                )

            elif m := re.match(self.pattern_end, line):
                if not cur_loc:
                    raise ParseError(f"Found END without BEG on line {i+1}")
                cur_loc.end = i
                out.append(copy(cur_loc))  # TODO: avoid copy?
                cur_loc = None

        return out

    def transform(self) -> "Transform":
        locs = self._parse_pattern_locs()

        # iterate in reverse order so that we don't have to worry about line numbers
        for loc in reversed(locs):
            res = Transform.kind_to_func(loc.kind)(loc.path)
            self._lines[loc.beg + 1 : loc.end] = res

        return self

    def write(self) -> None:
        with open(self.output_file, "wt") as fp:
            for line in self._lines:
                fp.write(line)

    @staticmethod
    def _fmt_code_block(data: list[str], pre: str) -> list[str]:
        data[-1] = data[-1].rstrip() + "\n"
        return [f"```{pre}\n", *data, "```\n"]

    @staticmethod
    def include_src(path: Path) -> list[str]:
        with open(path, "rt") as fp:
            data = fp.readlines()
        return Transform._fmt_code_block(data, pre=path.suffix.lstrip("."))

    @staticmethod
    def run_src(path: Path) -> list[str]:
        proc = subprocess.run(
            ["bash", "-c", f'"{path.resolve()}"'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        data = proc.stdout.decode("utf-8").splitlines(keepends=True)
        return Transform._fmt_code_block(data, pre="")

    @staticmethod
    def run_cmd(cmd: str) -> list[str]:
        raise NotImplementedError

    @staticmethod
    def kind_to_func(kind: str):
        if kind == "SRC":
            return Transform.include_src
        if kind == "RUN":
            return Transform.run_src

        raise ValueError(f"Unknown {kind=}")


def main():
    args = parse_args()

    tf = Transform(input_file=args.input, output_file=args.output or args.input)
    tf.transform().write()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=Path, required=True, help="Input file.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file. If not specified, it will edit in place.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
