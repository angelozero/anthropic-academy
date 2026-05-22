### What is a tool function in the context of Claude's tool use system?
- A plain function that gets executed when Claude needs additional information or needs to perform an action

### You're improving a prompt that isn't working well. What should you do after applying a prompt engineering technique?
- Use prompt evaluations to see if it actually improved

### You're making a math tutoring app. You want Claude to give hints instead of direct answers. What should you use?
- A system prompt explaining Claude should act like a tutor

### You want Claude to write very creative, unpredictable stories. What temperature setting should you use?
- 1.0 (very high)

### You want an AI to write a product description. Which opening is most clear and direct?
- "Write a product description for running shoes."

### You want to measure how well your AI prompt actually works in practice. Which approach should you focus on?
- Prompt evaluation with automated testing

### You're building a web app that talks to Claude. Where should you store your API key?
- On your server, hidden from users

### What is a model grader in prompt evaluation?
- Another AI model used to assess the quality of outputs

### You're asking an AI to analyze both customer reviews and sales data. How should you organize this information in your prompt?
- Use XML tags like <reviews> and <sales_data> to separate them

### You want to send a message to Claude through the API. Which four things do you absolutely need to include?
- API key, model name, messages, and max tokens

### What is the primary purpose of tool use in Claude?
- To allow Claude to access real-time information and external systems beyond its training data

### You're running a prompt evaluation. After getting responses from Claude, what's the next step in the typical workflow?
- Feed the responses through a grader for scoring

### You ask Claude "What is pizza?" and it answers. Then you ask "What toppings are popular?" but Claude doesn't know you're still talking about pizza. What's the problem?
- You need to send the whole conversation history with each request

### What is the primary difference between an MCP Server and an MCP Client in terms of their roles?
- MCP Servers contain tools, prompts, and resources while MCP Clients act as the communication bridge to access those tools

### Which of the following best describes Computer Use in the context of Claude?
- A capability that lets Claude interact directly with desktop environments like a human would

### What does "transport agnostic" mean in the context of MCP communication?
- MCP clients and servers can communicate using different methods like HTTP or standard input/output

### What is the primary purpose of a batch tool in Claude's tool system?
- To accept multiple tool calls and execute them simultaneously

### Claude responds to your request with both explanatory text and a tool use block. What type of message structure is this?
- Claude responds to your request with both explanatory text and a tool use block. What type of message structure is this?

### You're building an app where users need to verify information Claude provides from documents. What feature should you enable?
- Citations

### When should you choose workflows over agents for handling user tasks?
- When you can picture the exact flow or steps Claude should go through to solve a problem

### Which of the following best describes why environment inspection is crucial for AI agents?
- It allows agents to observe and understand the results of their actions

### What is the Model Context Protocol (MCP)?
- A communication layer that provides Claude with context and tools without requiring tedious integration code

### You keep sending the same long document to Claude with different questions. How can you make this faster and cheaper?
- Use prompt caching with cache breakpoints