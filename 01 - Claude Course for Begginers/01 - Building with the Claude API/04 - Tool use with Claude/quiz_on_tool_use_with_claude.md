### How can you tell if Claude wants to make another tool call in a conversation?
- Look at the stop_reason field for "tool_use"

### When Claude uses a tool, what type of message structure does it return?
-  Multi-block messages with text and tool use blocks

### What is the main purpose of a JSON schema when working with Claude tools?
-  To tell Claude what arguments your function expects and how to use it

### What problem does the batch tool solve?
-  It reduces the number of back-and-forth communications when multiple tools are needed

### What is the correct sequence of steps in the tool use workflow?
-  Initial Request → Tool Request → Data Retrieval → Final Response

### Claude can only access information from its training data by default. What allows Claude to get current, real-time information?
-  Using tools to access external information

### What makes Claude's built-in text editor and web search tools different from custom tools?
-  Claude provides the schema, but you may still need to implement some functionality