### What is the Files API used for?
-  Uploading files ahead of time and referencing them later instead of encoding them directly in messages

### You're making many requests with the same large system prompt. What feature would make your requests faster and cheaper?
-  Prompt caching

### What is the primary purpose of citations in Claude?
- To create a clear trail from Claude's response back to specific parts of source documents

### When Claude uses extended thinking, what two parts do you get in the response?
- Reasoning process and final answer

### You want Claude to analyze a PDF document. What's the main difference from sending an image?
- Change the type to "document" and media_type to "application/pdf"

### What is a key limitation of Claude's Code Execution tool?
-  It has no network access and runs in an isolated Docker container

### You want to cache your system prompt. What's the minimum requirement for caching to work?
- The content must be at least 1024 tokens long