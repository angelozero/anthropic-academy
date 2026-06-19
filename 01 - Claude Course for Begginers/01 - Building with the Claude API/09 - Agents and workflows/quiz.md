### You're building an agent with tools. Which approach will give Claude the most flexibility to handle unexpected requests?
-  Provide abstract tools like "read_file", "write_file", and "run_command"

### You want Claude to write a report, then check if it's good enough, and improve it if needed. What pattern are you using?
- Evaluator-Optimizer pattern

### Your app generates different types of social media content. Programming topics need educational scripts, while sports topics need entertainment-focused content. What pattern should you use?
- Route requests to specialized processing pipelines

### Claude keeps ignoring some of your rules when you give it a long prompt with many requirements. What workflow approach would help?
-  Chain the task into focused sequential steps

### You need Claude to recommend the best material for a part by considering metal, plastic, ceramic, and wood options. Each material has different criteria. What's the best approach?
- Send separate requests for each material type in parallel

### You need to choose between a workflow and an agent for your app. Reliability and predictable results are most important to you. Which should you pick?
- Use a workflow since it's more reliable and testable

### You're building an app where users upload photos of damaged car parts and always get repair cost estimates. You know exactly what steps are needed each time. What should you use?
- A workflow with predetermined steps