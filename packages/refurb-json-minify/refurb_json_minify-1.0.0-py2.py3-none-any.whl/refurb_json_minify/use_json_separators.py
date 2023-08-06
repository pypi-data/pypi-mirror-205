from dataclasses import dataclass

from mypy.nodes import CallExpr, NameExpr, RefExpr

from refurb.error import Error
from refurb_json_minify.common import (
    format_json_trailing_args,
    is_valid_json_call,
)


@dataclass
class ErrorInfo(Error):
    """
    By default when calling `json.dumps()` Python will emit spaces around
    colons and commas. By removing these spaces you can compress your JSON
    output slightly, allowing you will store less JSON in your database or
    filesystem, send less bytes to clients using your API, and much more.

    This does not effect reading of the JSON: Any JSON-compliant library
    should be able to parse the minified data without any issues.

    Bad:

    ```
    x = json.dumps({"nums": [1, 2, 3, 4, 5]})

    print(x)  # {"nums": [1, 2, 3, 4, 5]}
    ```

    Good:

    ```
    x = json.dumps({"nums": [1, 2, 3, 4, 5]}, separators=(",", ":"))

    print(x)  # {"nums":[1,2,3,4,5]}
    ```
    """

    name = "use-json-separators"
    prefix = "JMIN"
    code = 100


def check(node: CallExpr, errors: list[Error]) -> None:
    match node:
        case CallExpr(
            callee=RefExpr(fullname=func),
            args=args,
            arg_names=arg_names,
        ) if is_valid_json_call(node):
            for i, name in enumerate(arg_names):
                if name == "separators":
                    return

                if name == "indent":
                    match args[i]:
                        case NameExpr(fullname="builtins.None"):
                            pass

                        case _:
                            return

            extra = format_json_trailing_args(func, len(args))

            separators = ', separators=(",", ":")'

            errors.append(
                ErrorInfo(
                    node.line,
                    node.column,
                    f"Replace `{func}(x{extra})` with `{func}(x{extra}{separators})`",  # noqa: E501
                )
            )
