from dataclasses import dataclass

from mypy.nodes import CallExpr, IntExpr, RefExpr, Var

from refurb.error import Error
from refurb_json_minify.common import format_json_func, is_valid_json_call


@dataclass
class ErrorInfo(Error):
    """
    Don't dump integers to JSON values, just convert them to strings since
    they use the same representation.

    Bad:

    ```
    data = json.dumps(123)
    ```

    Good:

    ```
    data = str(123)
    ```
    """

    name = "dont-dump-integers"
    prefix = "JMIN"
    code = 101


def check(node: CallExpr, errors: list[Error]) -> None:
    match node:
        case CallExpr(
            callee=RefExpr(fullname=func),
            args=[arg, *_] as args,
        ) if is_valid_json_call(node):
            match arg:
                case IntExpr(value=value):
                    expr = str(value)
                    replace = f'"{value}"'

                case RefExpr(node=Var(type=ty)) if str(ty) == "builtins.int":
                    expr = (
                        arg.name
                        if hasattr(arg, "name")
                        else arg.fullname or ""
                    )

                    replace = f"str({expr})"

                case _:
                    return

            if func == "json.dump":
                replace = f"f.write({replace})"

            old = format_json_func(func, len(args), arg=expr)

            errors.append(
                ErrorInfo(
                    node.line,
                    node.column,
                    f"Replace `{old}` with `{replace}`",
                )
            )
