[Claude Certified Architect Ep 07: Agent Error Handling & tool_choice Explained](https://www.youtube.com/watch?v=eZj6FtTVV58&list=PLviC8AFqAj5A9MHkRIn2fU5Ac2lEdJxNf&index=9)

# Each error category carries enough metadata for the coordinator to decide:
#   transient   -> retry after delay (infra hiccup, safe to re-attempt)
#   permission  -> escalate; retrying won't help
#   validation  -> model should correct its params before retrying
#   internal    -> unexpected; surface to coordinator / human

```python
try:
    execute_tool_logic()
except BackendException as e:
    metadata = {
        'errorCategory': 'transient',
        'isRetryable': True,
        'description': str(e)
    }
    return ToolResult(
        is_error=True,
        content=[TextContent(text=json.dumps(metadata))]
    )
```