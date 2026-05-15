### You want to send a request to Claude's API. What's the minimum information you must include?
- API key, model name, messages, and max tokens

### You ask Claude "What is pizza?" and it answers. Then you ask "What toppings are popular?" but Claude doesn't understand what you're referring to. What's the problem?
-  Claude doesn't remember previous messages

### When Claude processes your text, what's the first thing it does?
- Breaks it into smaller chunks called tokens

### Users complain your chat app feels slow because they wait 20 seconds staring at a loading spinner, then all the generated text appears at once. What can fix this?
- Enabling response streaming

### You're building a web app that talks to Claude. Where should you store your API key?
- On your server that users can't access

### You're building a math tutor bot. You want Claude to give hints instead of direct answers. What should you use?
- A system prompt explaining the tutor role

### You want Claude to give very predictable, consistent answers for a factual Q&A app. What temperature setting should you use?
- Low temperature (near 0.0)

### You're building an app that needs clean JSON from Claude with no extra text or formatting. How do you get just the raw JSON?
-  Combine prefilled messages and stop sequences