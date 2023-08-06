from mypy.nodes import CallExpr, RefExpr


def format_json_func(func: str, arg_count: int, arg: str = "x") -> str:
    extra = format_json_trailing_args(func, arg_count)

    return f"{func}({arg}{extra})"


def format_json_trailing_args(func: str, arg_count: int) -> str:
    if func == "json.dumps":
        min_args = 1
        extra = ""

    else:
        min_args = 2
        extra = ", f"

    if arg_count > min_args:
        extra += ", ..."

    return extra


def is_valid_json_call(node: CallExpr) -> bool:
    match node:
        case CallExpr(
            callee=RefExpr(fullname="json.dump" | "json.dumps" as func),
            args=args,
        ):
            min_args = 1 if func == "json.dumps" else 2

            return len(args) >= min_args

    return False
