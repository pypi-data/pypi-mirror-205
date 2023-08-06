# refurb-json-minify

A small plugin for [Refurb](https://github.com/dosisod/refurb) aimed at minifying JSON outputs.

## Why is this important?

JSON is a widely used format for data exchange, whether that be APIs talking over the
internet, metadata being stored in a database, or config files stored on a user's
filesystem. Although CPU and harddrive space is getting cheaper and cheaper, it isn't
free, and being mindful of resources can lead to faster and more efficient programs.

## Supported Checks

### `JMIN100`: Use `separators`

The [`json.dump`](https://docs.python.org/3/library/json.html#json.dump) and
[`json.dumps`](https://docs.python.org/3/library/json.html#json.dumps) functions
allow for an optional `separators` field which specifies what characters to use
for colons (`:`) and commas (`,`) in the JSON output. Normally there is whitespace
after these characters, but you can change this to use a more compact format.

Here is a simple example comparing the output of `json.dumps()` with and without
`separators` specified:

```python
import json

data = {
  "hello": "world",
  "numbers": [1, 2, 3, 4],
}

a = json.dumps(data)
b = json.dumps(data, separators=(",", ":"))

print(f"{len(a)=}", f"{len(b)=}")
```

When we run this, we get:

```
len(a)=43 len(b)=37
```

By reducing the whitespace in our JSON output we where able to shave off 6 bytes, or about
16% in this example.

### `JMIN101`: Don't `json.dump()` integers

Don't call `json.dump()` on integers, use `str()` instead since they share the
same representation.
