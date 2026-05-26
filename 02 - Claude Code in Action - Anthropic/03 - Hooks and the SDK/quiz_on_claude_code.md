### What is the fundamental limitation of language models that necessitates the use of a tool system in coding assistants?
- They can only process text input/output and cannot directly interact with external systems

### What permission configuration is required when integrating MCP servers with Claude Code in GitHub Actions?
- Each MCP server tool must be individually listed in the permissions

### What is the primary difference between Plan Mode and Thinking Mode in Claude Code?
- Plan Mode handles breadth (multi-step tasks) while Thinking Mode handles depth (complex logic)

### Which of the following correctly describes the three types of Claude.md files and their usage?
- Project level (shared with team, committed), Local level (personal, not committed), Machine level (global for all projects)

### How do you create a custom command in Claude Code that accepts runtime parameters?
-  Include $ARGUMENTS placeholder in the markdown command file

### Which type of hook can prevent a tool call from happening if certain conditions are met?
- PreToolUse hook

### A developer wants to prevent Claude from reading sensitive .env files. Which type of hook should they set up, and what tool names would they likely match?
- PreToolUse hook, matching Read and Grep

### What is the primary purpose of hooks in Claude Code?
- To run commands before or after Claude executes a tool.