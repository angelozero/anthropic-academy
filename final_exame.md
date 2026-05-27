### Your agent handles single-concern requests with 94% accuracy (e.g., "I need a refund for order #1234"). However, when customers include multiple concerns in one message (e.g., "I need a refund for order #1234 and also want to update my shipping address for order #5678"), tool selection accuracy drops to 58%. The agent typically addresses only one concern or mixes up parameters between requests. What's the most effective approach to improve reliability for multi-concern requests?

- The correct answer is A:
Adding few-shot examples demonstrating correct reasoning and tool sequencing for multi-concern requests is the most effective approach because the agent already handles individual concerns well at 94% accuracy—it simply needs pattern guidance for handling multiple concerns in one message. This is a low-cost, proven technique that directly addresses the root cause of the agent failing to decompose and properly route parameters across multiple requests.

Your answer:
Using a separate model call to decompose multi-concern messages adds unnecessary latency, complexity, and cost when the agent already demonstrates strong single-concern understanding. This over-engineers the solution when simpler prompt-level guidance can address the pattern recognition gap.

Study Area:
Customer Support Resolution Agent — review Tool Selection Reliability concepts in the exam study guide.

--- 

### Production logs show the agent sometimes selects get_customer when lookup_order would be more appropriate, particularly for ambiguous requests like "I need help with my recent purchase." You decide to add few-shot examples to your system prompt to improve tool selection. Which approach will most effectively address this issue?
- The correct answer is B:
Targeting few-shot examples at the specific ambiguous scenarios where errors occur, with explicit reasoning about why one tool is preferred over another, directly teaches the model the comparative decision-making process it needs for edge cases. This approach is the most effective because worked examples demonstrating reasoning are better than declarative rules for nuanced tool selection.

Your answer:
Adding explicit usage guidelines to tool descriptions can help, but static declarative rules are less effective than worked examples for teaching nuanced edge-case reasoning. The model benefits more from seeing the actual decision process in context than from reading abstract rules about when to use or avoid each tool.

Study Area:
Customer Support Resolution Agent — review Tool Selection Reliability concepts in the exam study guide.

--- 

### After calling get_customer and lookup_order, the agent has retrieved all available system data but faces uncertainty. Which situation represents the most appropriate trigger for calling escalate_to_human?
- The correct answer is B:
This represents a genuine policy gap where the company's guidelines cover own-site price drops but are silent on competitor price matching, meaning the agent cannot fabricate a policy and must escalate for human judgment on how to interpret or extend existing rules.

Your answer:
While the situation involves contradictory information, the agent has factual tracking data to share with the customer per standard procedure; escalating to avoid presenting evidence out of concern for relationship damage reflects emotional avoidance rather than an operational need for human intervention.

Study Area:


--- 

### Production data shows that in 12% of cases, your agent skips get_customer entirely and calls lookup_order using only the customer's stated name, occasionally leading to misidentified accounts and incorrect refunds. What change would most effectively address this reliability issue?

- The correct answer is D:
Adding a programmatic prerequisite that blocks downstream tools until `get_customer` returns a verified customer ID provides a deterministic guarantee that the required sequence is followed. This is the most effective approach because it removes the possibility of the agent skipping verification, regardless of LLM behavior.

Your answer:
Enhancing the system prompt to mandate customer verification relies on the LLM consistently following instructions, which is inherently probabilistic. Since 12% of cases already show the agent skipping this step, prompt-based guidance alone is insufficient for preventing errors with financial consequences.

Study Area:
Customer Support Resolution Agent — review Multi-step Workflow Enforcement concepts in the exam study guide.

---

### Production logs show that for simple requests like "refund order #1234", your agent succeeds in 3-4 tool calls with 91% resolution rate. However, for complex requests like "I've been charged twice, my discount didn't apply, and I want to cancel", the agent averages 12+ tool calls with only 54% resolution—often investigating concerns sequentially and gathering redundant customer data for each one. What's the most effective change to improve complex request handling?
- The correct answer is A:
Decomposing the request into distinct concerns and investigating them in parallel with shared customer context directly addresses both core issues: it eliminates redundant data fetching by reusing context across concerns and reduces total tool calls by parallelizing investigations before synthesizing a unified resolution.

Your answer:
Adding verification gates between sequential steps would actually worsen the problem by reinforcing the sequential processing pattern and adding overhead, rather than addressing the root cause of redundant data gathering and serial investigation.

Study Area:
Customer Support Resolution Agent — review Multi-step Workflow Orchestration concepts in the exam study guide.

---

### You're implementing the agentic loop for your support agent. After each API call to Claude, you need to determine whether to continue the loop (execute the requested tools and call Claude again) or stop (present the final response to the customer). What determines this decision?
- Check the stop_reason field in Claude's response—continue when it equals "tool_use" and stop when it equals "end_turn".
Correct!
This is correct. The `stop_reason` field is Claude's explicit, structured signal for loop control: `"tool_use"` indicates Claude wants to execute a tool and receive the results back, while `"end_turn"` indicates Claude has completed its response and the loop should terminate.

---

### Production logs reveal a consistent pattern: when customers include "account" in messages (e.g., "I want to check my account for the order I placed yesterday"), the agent calls get_customer first 78% of the time. When customers phrase similar requests without "account" (e.g., "I want to check on the order I placed yesterday"), it calls lookup_order first 93% of the time. The tool descriptions are well-written and unambiguous. What is the most likely root cause of this discrepancy?
- The correct answer is D:
This is the most likely root cause because the systematic, keyword-triggered pattern (78% vs 93%) strongly suggests explicit routing logic in the system prompt that reacts to the word "account" and directs the agent toward customer-related tools. Since the tool descriptions are already well-written and unambiguous, the discrepancy points to prompt-level instructions creating unintended behavioral steering.

Your answer:
Adding negative examples to tool descriptions contradicts the stated premise that the descriptions are already well-written and unambiguous. The issue is not with the tool descriptions themselves but with upstream instructions in the system prompt that override correct tool selection based on keyword triggers.

Study Area:
Customer Support Resolution Agent — review Tool Selection Reliability concepts in the exam study guide.

---

### Production logs show the agent frequently calls get_customer when users ask about orders (e.g., "check my order #12345"), instead of calling lookup_order. Both tools have minimal descriptions ("Retrieves customer information" / "Retrieves order details") and accept similar identifier formats. What's the most effective first step to improve tool selection reliability?
- The correct answer is D:
Expanding tool descriptions to include input formats, example queries, edge cases, and boundaries directly addresses the root cause—minimal descriptions that leave the LLM unable to distinguish between similar tools. This is a low-effort, high-leverage first step that improves the primary mechanism LLMs use for tool selection.

Your answer:
Adding few-shot examples to the system prompt increases token overhead and addresses symptoms rather than the root cause. While examples can help, they are less effective and scalable than fixing the minimal tool descriptions that the LLM relies on for tool selection.

Study Area:
Customer Support Resolution Agent — review Tool Interface Design concepts in the exam study guide.

---

### Production metrics show that when your agent resolves complex cases involving billing disputes or multi-order returns, customer satisfaction scores are 15% lower than for simple cases—even when the resolution is technically correct. Root cause analysis reveals the agent provides accurate resolutions but inconsistently explains the reasoning: sometimes omitting relevant policy details, other times missing timeline information or next steps. The specific context gaps vary by case. You want to improve resolution quality without adding human review overhead. Which approach is most effective?
- The correct answer is A:
A self-critique step (evaluator-optimizer pattern) directly addresses the root cause of inconsistent explanation completeness by having the agent evaluate its own draft against specific criteria—such as policy context, timelines, and next steps—before presenting it. This catches case-specific gaps that vary across different complex scenarios without requiring human review.

Your answer:
While few-shot examples can demonstrate ideal response structure for common case types, they cannot adequately cover the highly variable context gaps that differ from case to case. This approach works better for consistent, predictable patterns rather than the diverse omissions described in the scenario.

Study Area:
Customer Support Resolution Agent — review Self-Evaluation Patterns concepts in the exam study guide.

---

### In testing, you notice the agent frequently calls get_customer when users ask about order status, even though lookup_order would be more appropriate. What should you examine first to address this issue?
- Review tool descriptions to ensure they clearly distinguish each tool's purpose
Correct!
Tool descriptions are the primary input the model uses to decide which tool to call. When an agent consistently selects the wrong tool, the first diagnostic step is to examine whether the tool descriptions clearly distinguish each tool's purpose and specify when each should be used.

---

### Your get_customer tool returns all matches when searching by name. Claude currently picks the customer with the most recent order when multiple results are returned, but production data shows this causes 15% of multi-match cases to proceed with the wrong customer account. How should you address this?
- Instruct Claude to ask for an additional identifier (email, phone, or order number) when get_customer returns multiple matches, before taking any customer-specific action.
Correct!
Asking the user for an additional identifier (such as email, phone, or order number) is the most reliable way to disambiguate multiple matches, since the user has definitive knowledge of their own identity. One extra conversational turn is a small cost to eliminate the 15% error rate caused by incorrect customer selection.

---
### Production logs reveal that the agent misinterprets data from your MCP tools: Unix timestamps from get_customer, ISO 8601 dates from lookup_order, and numeric status codes (1=pending, 2=shipped). Some tools are third-party MCP servers you cannot modify. What's the most maintainable approach to normalize data formats?
- Use a PostToolUse hook to intercept tool results and apply formatting transformations before agent processing
Correct!
Using a PostToolUse hook provides a centralized, deterministic point to intercept and normalize all tool outputs—including those from third-party MCP servers—before the agent processes them. This is the most maintainable approach because it applies transformations uniformly via code rather than relying on LLM interpretation or agent behavior.

---

### Your support agent uses progressive summarization—when context reaches 70% capacity, older turns are summarized while recent ones remain verbatim. Production logs reveal a pattern: customers reference specific amounts ("the 15% discount I mentioned"), but the agent responds with incorrect values. Investigation shows these details were stated 20+ turns ago and got condensed into vague summaries like "discussed promotional pricing." What's the most effective fix?
- The correct answer is C:
Extracting transactional facts (amounts, dates, order numbers) into a persistent "case facts" block addresses the root cause: summarization is inherently lossy for precise details. By preserving critical information in a structured block outside the summarized history, these facts remain reliably available in every prompt regardless of how many turns are summarized.

Your answer:
Revising the summarization prompt to preserve numerical values sounds reasonable but is unreliable in practice—LLMs don't consistently follow such preservation instructions under context pressure, meaning summarization will still be lossy for precise details. You cannot reliably "prompt your way out" of the fundamental information loss that summarization introduces.

Study Area:
Customer Support Resolution Agent — review Conversation Context Management concepts in the exam study guide.

---

### Your agent achieves 55% first-contact resolution, well below the 80% target. Logs show it escalates straightforward cases (standard damage replacements with photo evidence) while attempting to autonomously handle complex situations requiring policy exceptions. What's the most effective way to improve escalation calibration?
- The correct answer is C:
Adding explicit escalation criteria with few-shot examples directly addresses the root cause—unclear decision boundaries between straightforward and complex cases. This is the most proportionate and effective first intervention, as it teaches the agent precisely when to escalate versus resolve autonomously without requiring additional infrastructure.

Your answer:
LLM self-reported confidence scores are notoriously poorly calibrated, and the logs already show the agent is incorrectly confident on complex cases while being overly cautious on simple ones. A numeric self-assessment would likely replicate the same miscalibration rather than fix the underlying decision boundary problem.

Study Area:
Customer Support Resolution Agent — review Escalation Decisions concepts in the exam study guide.

---

### Production metrics show your agent averages 4+ API round-trips per resolution. Analysis reveals Claude frequently requests get_customer and lookup_order in separate sequential turns even when both are needed upfront. What's the most effective way to reduce round-trips?
- The correct answer is A:
Prompting Claude to batch related tool requests in a single turn, and returning all results together before the next API call, leverages Claude's native ability to request multiple tools simultaneously. This is the most effective approach because it directly addresses the sequential calling pattern with minimal architectural changes.

Your answer:
Creating composite tools reduces flexibility and increases maintenance burden by requiring new bundled tools for every common combination, without addressing the root cause—which is that Claude already supports requesting multiple tools per turn and simply needs to be prompted to do so.

Study Area:
Customer Support Resolution Agent — review Parallel Tool Execution concepts in the exam study guide.

### During testing, you observe that the synthesis agent frequently needs to verify specific claims while combining findings. Currently, when verification is needed, the synthesis agent returns control to the coordinator, which invokes the web search agent, then re-invokes synthesis with results. This adds 2-3 round trips per task and increases latency by 40%. Your evaluation shows that 85% of these verifications are simple fact-checks (dates, names, statistics) while 15% require deeper investigation. What's the most effective approach to reduce overhead while maintaining system reliability?
- Give the synthesis agent a scoped verify_fact tool for simple lookups, while complex verifications continue delegating to the web search agent through the coordinator.
Correct!
Providing a scoped fact-verification tool handles the 85% of simple lookups directly, eliminating most round-trips while preserving the coordinator-based delegation path for the 15% of complex verifications. This applies the principle of least privilege, keeping the synthesis agent focused on its primary task while still reducing latency significantly.

---

### The document analysis subagent frequently encounters failures when processing PDF files—some have corrupted sections causing parsing exceptions, others are password-protected, and occasionally the parsing library times out on large files. Currently, any exception immediately terminates the subagent and returns an error to the coordinator, which must decide whether to retry, skip the document, or fail the entire research task. This is causing excessive coordinator involvement in routine error handling. What's the most effective architectural improvement?
- The correct answer is B:
Implementing local recovery for transient failures within the subagent follows the principle of handling errors at the lowest level capable of resolving them. This reduces excessive coordinator involvement while still escalating truly unresolvable issues with full context, including what recovery was attempted and any partial results obtained.

Your answer:
Introducing a dedicated error-handling agent adds unnecessary architectural complexity, an additional coordination layer, and a shared queue dependency. This approach distributes error-handling logic across multiple components rather than resolving failures at the most appropriate level—the subagent itself.

Study Area:
Multi-Agent Research System — review Error Propagation concepts in the exam study guide.

---

### A colleague suggests having the document analysis agent send its output directly to the synthesis agent instead of routing through the coordinator. What is the main advantage of keeping the coordinator as the central hub for all subagent communication?
- The correct answer is A:
This is correct. The coordinator pattern provides centralized visibility into all interactions, consistent error handling across the system, and fine-grained control over what information each subagent receives, which are the primary advantages of hub-and-spoke communication.

Your answer:
This is incorrect. Serialization of data between components is not unique to coordinators—any component can serialize and pass data, so direct communication between subagents would not face a special serialization barrier that only a coordinator can overcome.

Study Area:
Multi-Agent Research System — review Multi-Agent Orchestration concepts in the exam study guide.

---

### During a materials research task, the web search subagent queries three source categories with different outcomes: academic databases returned 15 relevant papers, industry reports returned "0 results found," and patent databases returned "Connection timeout." When designing error propagation to the coordinator, what approach enables the best recovery decisions?
- The correct answer is A:
This is correct because a timeout (access failure) and '0 results' (valid empty result) are semantically distinct outcomes requiring different responses. Distinguishing them enables the coordinator to retry the timed-out patent database while accepting the empty industry report results as a valid and informative finding.

Your answer:
Aggregating outcomes into a single success rate metric like '67% source coverage' destroys the actionable detail needed for recovery decisions, since it obscures whether the missing 33% is due to transient access failures or legitimately empty results. The coordinator cannot make appropriate retry or escalation decisions without understanding the nature of each individual outcome.

Study Area:
Multi-Agent Research System — review Error Propagation concepts in the exam study guide.

---

### The web search subagent times out while researching a complex topic. You need to design how this failure information flows back to the coordinator agent. Which error propagation approach best enables intelligent recovery?
- Return structured error context to the coordinator including the failure type, the attempted query, any partial results, and potential alternative approaches.
Correct!
Returning structured error context—including the failure type, attempted query, partial results, and alternative approaches—gives the coordinator all the information it needs to make intelligent recovery decisions, such as retrying with a modified query or proceeding with partial results. This is the best approach because it preserves maximum context for informed decision-making at the coordination level.

---

### Production monitoring reveals inconsistent synthesis quality. When aggregated results total ~75K tokens, the synthesis agent reliably cites information from the first 15K tokens (web search headlines and snippets) and the final 10K tokens (document analysis conclusions), but frequently omits critical findings that appear in the middle 50K tokens—even when those findings directly address the research question. How should you restructure the aggregated input?
- Place a key findings summary at the beginning of the aggregated input and organize detailed results with explicit section headers for easier navigation.
Correct!
Placing a key findings summary at the beginning leverages the primacy effect, ensuring critical information occupies the most reliably attended position. Adding explicit section headers throughout the aggregated input helps the model navigate and attend to middle-section content, directly mitigating the 'lost in the middle' phenomenon.

---

### The web search and document analysis agents have both completed their tasks and returned findings to the coordinator. What is the appropriate next step for producing an integrated research output?
- The coordinator passes both sets of findings to the synthesis agent for unified integration
Correct!
This is correct because the orchestrator-workers pattern requires the coordinator to maintain centralized control by collecting results from subagents and routing them to the appropriate next component—in this case, the synthesis agent, which is specifically designed to unify and integrate findings into a coherent output.

---

### After running the system on the topic "impact of AI on creative industries," you observe that each subagent completes successfully: the web search agent finds relevant articles, the document analysis agent summarizes papers correctly, and the synthesis agent produces coherent output. However, the final reports cover only visual arts, completely missing music, writing, and film production. When you examine the coordinator's logs, you see it decomposed the topic into three subtasks: "AI in digital art creation," "AI in graphic design," and "AI in photography." What is the most likely root cause?
- The correct answer is D:
The coordinator's logs directly reveal it decomposed the broad topic into only three visual arts subtasks (digital art, graphic design, photography), completely omitting music, writing, and film. Since the subagents all executed their assigned tasks correctly, the narrow decomposition by the coordinator is clearly the root cause of the missing coverage.

Your answer:
While the synthesis agent could theoretically flag coverage gaps, it can only work with the findings it receives. The root problem is upstream—the coordinator never assigned subtasks for music, writing, or film, so there were no findings about those domains to flag as missing.

Study Area:
Multi-Agent Research System — review Multi-Agent Orchestration concepts in the exam study guide.

---

### The document analysis subagent encounters a corrupted PDF file it cannot parse. When designing the system's error handling, what is the most effective way to handle this failure?
- Return the error with context to the coordinator agent, letting it decide how to proceed.
Correct!
Returning the error with context to the coordinator agent is the most effective approach because it enables the coordinator to make an informed decision—such as skipping the file, trying an alternative parsing method, or notifying the user—while maintaining visibility into the failure.

---

### During testing, combined outputs from the web search agent (85K tokens including page content) and the document analysis agent (70K tokens including reasoning chains) total 155K tokens, but the synthesis agent performs optimally with inputs under 50K tokens. What's the most effective solution?
- Modify upstream agents to return structured data (key facts, citations, relevance scores) instead of verbose content and reasoning
Correct!
Modifying upstream agents to return structured data (key facts, citations, relevance scores) addresses the root cause by reducing token volume at the source while preserving essential information. This eliminates verbose page content and reasoning chains that inflate token counts without adding value for the synthesis step.

---

### When designing the system, you gave the document analysis agent access to a general-purpose fetch_url tool so it could load documents from URLs. Production logs reveal this agent now frequently fetches search engine result pages to conduct ad-hoc web searches—behavior that should route through the web search agent. This causes inconsistent results. What's the most effective fix?
- The correct answer is B:
Replacing the general-purpose tool with a document-specific tool that validates URLs point to document formats addresses the root cause by constraining capability at the interface level. This follows the principle of least privilege, making the undesired search behavior impossible rather than merely discouraged.

Your answer:
Removing URL fetching entirely from the document analysis agent and routing all requests through the coordinator eliminates useful capability and adds unnecessary latency for legitimate document loading. This over-corrects the problem when the agent legitimately needs to load documents from URLs.

Study Area:
Multi-Agent Research System — review Tool Distribution concepts in the exam study guide.

--- 

### Production logs reveal a consistent pattern: requests to "analyze the quarterly report I uploaded" are routed to the web search agent 45% of the time instead of the document analysis agent. Examining the tool definitions, you find the web search agent has an analyze_content tool described as "analyzes content and extracts key information," while the document analysis agent has an analyze_document tool described as "analyzes documents and extracts key information." How should you address this misrouting?
- Rename the web search tool to extract_web_results and update its description to "processes and returns information retrieved from web searches and URLs."
Correct!
Renaming the web search tool to `extract_web_results` and updating its description to clearly reference web searches and URLs directly addresses the root cause by eliminating the semantic overlap between the two tools' names and descriptions. This makes each tool's purpose unambiguous, allowing the coordinator to correctly distinguish between document analysis and web search tasks.

---

### When researching a broad topic, you observe that the web search agent and document analysis agent are both investigating the same subtopics, resulting in significant overlap in their findings. Token usage has nearly doubled without proportionally increasing the breadth or depth of research coverage. What's the most effective way to address this?
- The correct answer is C:
Having the coordinator explicitly partition the research space before delegation is the most effective approach because it addresses the root cause—unclear task boundaries—before any work begins. This preserves the benefits of parallel execution while preventing duplicated effort and wasted tokens.

Your answer:
Converting to sequential execution unnecessarily sacrifices the performance benefits of parallelism when the same deduplication goal can be achieved through upfront task partitioning. This approach also increases total execution time without offering meaningful advantages over proactive partitioning of the research space.

Study Area:
Multi-Agent Research System — review Multi-Agent Orchestration concepts in the exam study guide.

---

### The web search subagent returns results for only 3 of 5 requested source categories (competitor websites and industry reports succeeded, but news archives and social media feeds timed out). The document analysis subagent successfully processed all provided documents. The synthesis subagent must now produce a findings summary from this mixed-quality input. What's the most effective error propagation strategy?
- The correct answer is A:
Structuring the synthesis output with coverage annotations embodies graceful degradation with transparency, allowing downstream consumers and end users to understand which findings are well-supported and which topic areas have gaps. This approach preserves the value of completed work while propagating uncertainty information so informed decisions can be made about confidence levels.

Your answer:
Treating partial success as total failure by returning an error wastes all the successfully completed work from both the web search and document analysis subagents. This approach provides no value when partial results with appropriate caveats would still be useful to stakeholders.

Study Area:
Multi-Agent Research System — review Error Propagation concepts in the exam study guide.

---

### The document analysis agent discovers that two credible sources contain directly conflicting statistics on a key metric: one government report states 40% growth while an industry analysis states 12% growth. Both sources appear legitimate and the discrepancy could significantly affect the research conclusions. What's the most effective way for the document analysis agent to handle this?
- The correct answer is D:
This is the most effective approach because it respects separation of concerns: the document analysis agent completes its primary task without blocking, preserves both conflicting data points with explicit source attribution, and appropriately defers the reconciliation decision to the coordinator, which has the broader context needed to resolve the conflict.

Your answer:
Having the document analysis agent apply credibility heuristics to select one figure oversteps its role, as it lacks the broader context needed to make authoritative credibility judgments. This approach also risks losing important information by relegating the discrepancy to a footnote rather than treating it as a significant finding requiring reconciliation.

Study Area:
Multi-Agent Research System — review Multi-Agent Orchestration concepts in the exam study guide.

---

### Your codebase has distinct areas with different coding conventions: React components use functional style with hooks, API handlers use async/await with specific error handling, and database models follow a repository pattern. Test files are spread throughout the codebase alongside the code they test (e.g., Button.test.tsx next to Button.tsx), and you want all tests to follow the same conventions regardless of location. What's the most maintainable way to ensure Claude automatically applies the correct conventions when generating code?
- The correct answer is C:
Using rule files in `.claude/rules/` with YAML frontmatter and glob patterns (e.g., `**/*.test.tsx`, `src/api/**/*.ts`) allows conventions to be automatically and deterministically applied based on file paths, regardless of where those files are located in the directory structure. This is the most maintainable approach because it handles cross-cutting concerns like test files spread throughout the codebase without requiring duplication or manual intervention.

Your answer:
Skills in `.claude/skills/` are designed for task-based workflows and typically require manual invocation or rely on Claude choosing to load them, which contradicts the requirement for automatic, deterministic application of conventions based on file paths. This approach lacks the glob-pattern-based conditional triggering needed to reliably match conventions to specific file types.

Study Area:
Code Generation with Claude Code — review Path-Specific Rule Configuration concepts in the exam study guide.

---

### You're adding error handling wrappers to external API calls across a 120-file codebase. The task has three phases: (1) discovering all API call locations and patterns, (2) designing the error handling approach collaboratively, and (3) implementing wrappers consistently. During Phase 1, Claude generates verbose output listing hundreds of call sites with context. Your context window is filling rapidly before you've finished discovery. What's the most effective approach to complete this while maintaining implementation consistency?

- The correct answer is B:
Using the Explore subagent for Phase 1 is ideal because it isolates the verbose discovery output in a separate context, returning only a concise summary to the main conversation. This preserves the main context window for the collaborative design and consistent implementation phases where retained context is most valuable.

Your answer:
Splitting work across multiple sessions loses the in-session context about nuanced decisions and edge cases encountered during discovery, and CLAUDE.md alone is insufficient to capture all the detailed rationale needed for consistent implementation across 120 files.

Study Area:
Code Generation with Claude Code — review Subagent Delegation Strategy concepts in the exam study guide.

---

### Your team has been using Claude Code for several months. Recently, three developers report that Claude correctly follows your "always include comprehensive error handling" guideline, but a fourth developer who just joined reports Claude isn't following this guideline. All four developers are working in the same repository and have the latest code pulled. What's the most likely cause and appropriate fix?
- The correct answer is A:
This is the most likely cause: if the error handling guideline was added to each original developer's user-level ~/.claude/CLAUDE.md rather than the project's .claude/CLAUDE.md, new team members would not receive it. Moving the instruction to the project-level configuration file ensures all current and future team members automatically receive the guideline.

Your answer:
While conflicting user-level instructions could theoretically cause issues, it is unlikely that a newly joined developer would already have pre-existing conflicting configurations in their user-level CLAUDE.md file. This scenario doesn't explain why the three existing developers all have the guideline working consistently.

Study Area:
Code Generation with Claude Code — review CLAUDE.md Configuration Hierarchy concepts in the exam study guide.

---

### Your team's CLAUDE.md file has grown to over 500 lines, mixing TypeScript conventions, testing guidelines, API patterns, and deployment procedures. Developers find it difficult to locate and update relevant sections. What approach does Claude Code support for organizing project-level instructions into focused, topic-specific modules?
- Create separate markdown files in .claude/rules/, each covering one topic (e.g., testing.md, api-conventions.md)
Correct!
This is correct. Claude Code supports a `.claude/rules/` directory where you can create separate markdown files for topic-specific guidelines (e.g., `testing.md`, `api-conventions.md`), allowing teams to organize large instruction sets into focused, maintainable modules.

---

### You want to create a custom /review slash command that runs your team's standard code review checklist. This command should be available to every developer when they clone or pull the repository. Where should you create this command file?
- The correct answer is D:
Placing custom slash commands in the `.claude/commands/` directory within the project repository is correct because these files are version-controlled and automatically available to every developer who clones or pulls the repo. This is the designated location for project-scoped custom commands in Claude Code.

Your answer:
The `CLAUDE.md` file at the project root is used for project instructions, context, and conventions that guide Claude's behavior, not for defining custom slash commands. Command definitions require their own dedicated files in the appropriate commands directory.

Study Area:
Code Generation with Claude Code — review Custom Slash Commands concepts in the exam study guide.

---

### You've found that including 2-3 full exemplar endpoint implementations as context significantly improves consistency when generating new API endpoints. However, this context is only useful for creating new endpoints—not for bug fixes, code reviews, or other API directory work. What's the most efficient configuration approach?
- Create a skill that references the exemplar endpoints and includes pattern-following instructions, invoked on-demand via slash command.
Correct!
Creating a skill with the exemplar endpoints and pattern-following instructions allows on-demand invocation via a slash command, ensuring the context is loaded only when generating new endpoints and not during unrelated tasks like bug fixes or code reviews.

---

### Your team created an /analyze-codebase skill that performs comprehensive code analysis—dependency scanning, test coverage calculation, and code quality metrics. After running this command, team members report that Claude becomes less responsive in the session and loses track of their original task. What's the most effective way to address this while preserving full analysis capability?
- The correct answer is B:
Using `context: fork` in the skill's frontmatter runs the analysis in an isolated sub-agent context, which prevents the verbose output from polluting the main conversation's context window and causing Claude to lose track of the original task. This preserves full analysis capability while keeping the main session responsive.

Your answer:
Compressing all outputs into a brief summary would sacrifice the full analysis capability that the question requires to be preserved. While it might reduce context pollution, it fundamentally undermines the purpose of comprehensive code analysis by discarding detailed results.

Study Area:
Code Generation with Claude Code — review Custom Slash Commands concepts in the exam study guide.

---

### Your team has created a /migration skill that generates database migration files. The skill accepts a migration name via $ARGUMENTS. In production, you're seeing three issues: (1) developers often invoke the skill without arguments, resulting in poorly-named files, (2) the skill sometimes incorporates database schema details from unrelated earlier conversations, and (3) a developer accidentally triggered destructive test cleanup when the skill had broad tool access. Which configuration approach addresses all three issues?
- The correct answer is D:
This approach correctly uses three distinct skill configuration features to address each issue: `argument-hint` frontmatter shows expected parameters during autocomplete (addressing missing arguments), `context: fork` isolates execution in a subagent context separate from conversation history (preventing context bleeding from earlier conversations), and `allowed-tools` restricts tool access to only file write operations (preventing destructive actions).

Your answer:
This approach relies entirely on prompt-based instructions, which are unreliable for enforcement—telling Claude to "ignore prior context" doesn't actually isolate execution context, and listing forbidden operations doesn't restrict tool access the way `allowed-tools` does, leaving the system vulnerable to all three issues.

Study Area:
Code Generation with Claude Code — review Custom Slash Commands concepts in the exam study guide.

---

### You've created a /commit skill in .claude/skills/commit/SKILL.md that your team uses. One developer wants to customize it for their personal workflow (different commit message format, additional checks) without affecting teammates. What should you recommend?
- Create a personal version in ~/.claude/skills/ with a different name like /my-commit
Correct!
This is correct. Since project skills take precedence over personal skills with the same name, the developer must use a different skill name (like `/my-commit`) in their personal `~/.claude/skills/` directory to ensure their custom version is accessible alongside the team's project skill.

---

### Your CLAUDE.md has grown to over 400 lines containing coding standards, testing conventions, a detailed PR review checklist, deployment workflow instructions, and database migration procedures. You want Claude to always follow the coding standards and testing conventions, but only apply PR review, deployment, and migration guidance when you're actually performing those tasks. What's the most effective restructuring approach?
- The correct answer is D:
This is the most effective approach because CLAUDE.md content is loaded for every conversation, ensuring coding standards and testing conventions are always applied, while Skills are invoked on-demand when Claude detects relevant trigger keywords, making them ideal for task-specific workflows like PR reviews, deployments, and migrations.

Your answer:
Moving all guidance into Skills files means that universal coding standards and testing conventions won't be automatically loaded into every conversation. Since these standards should always be applied, they belong in CLAUDE.md where they are included by default.

Study Area:
Code Generation with Claude Code — review Skills vs CLAUDE.md Scope concepts in the exam study guide.

---

### Your team wants to add a GitHub MCP server to enable PR lookups and CI status checks through Claude Code. Each of the six developers has their own GitHub personal access token. You want consistent tooling across the team without committing credentials to version control. What's the most effective configuration approach?
- The correct answer is B:
Using a project-scoped `.mcp.json` with environment variable expansion (`${GITHUB_TOKEN}`) is the idiomatic approach—it provides a single, version-controlled source of truth for the team's MCP configuration while allowing each developer to supply their own credentials through environment variables. Documenting the required variable in the README ensures easy onboarding without ever committing secrets.

Your answer:
Building a custom wrapper to proxy GitHub API requests and read tokens from a `.env` file is over-engineered, since Claude Code's native environment variable expansion in `.mcp.json` already solves the credential injection problem cleanly. This approach introduces additional maintenance burden and potential points of failure without meaningful benefit.

Study Area:
Code Generation with Claude Code — review MCP Server Integration concepts in the exam study guide.

---

### You need to add Slack as a new notification channel. The existing codebase has clear, consistent patterns for email, SMS, and push channels. However, the Slack API offers fundamentally different integration approaches—incoming webhooks (simple, one-way only), bot tokens (enables delivery confirmation and programmatic control), or Slack Apps (bidirectional events, requires workspace approval). Your ticket says "add Slack support" without specifying which integration method or whether advanced features like delivery tracking will be needed. How should you approach this task?
- The correct answer is D:
This is correct because the Slack integration involves multiple valid approaches with significantly different architectural implications, and the requirements are ambiguous. Using plan mode to explore trade-offs between webhooks, bot tokens, and Slack Apps allows for an informed recommendation and team alignment before committing to an implementation path.

Your answer:
This approach incorrectly assumes that meaningful scaffolding can proceed before choosing the integration method, when in reality the authentication flows, response handling, and error patterns differ significantly between webhooks, bot tokens, and Slack Apps. Deferring the integration method decision would likely result in rework once the approach is selected.

Study Area:
Code Generation with Claude Code — review Plan Mode vs Direct Execution concepts in the exam study guide.

---

### You've been assigned to restructure the team's monolithic application into microservices. This will involve changes across dozens of files and requires decisions about service boundaries and module dependencies. Which approach should you take?
- Enter plan mode to explore the codebase, understand dependencies, and design an implementation approach before making changes.
Correct!
Using plan mode to explore the codebase, understand dependencies, and design an approach before making changes is the correct strategy for a complex architectural restructuring like breaking apart a monolith. This allows safe exploration and informed decision-making about service boundaries before committing to potentially costly changes across dozens of files.

---

### You're creating a custom /explore-alternatives skill that your team uses to brainstorm and evaluate different implementation approaches before committing to one. However, developers report that after running this skill, Claude's subsequent responses are influenced by the exploration discussion—sometimes referencing abandoned approaches or maintaining exploratory context that confuses actual implementation work. What's the most effective way to configure this skill?
- The correct answer is D:
The `context: fork` frontmatter option runs the skill in an isolated sub-agent context, so the exploration discussion does not pollute the main conversation history. This prevents abandoned approaches and exploratory context from influencing subsequent implementation work.

Your answer:
Using the `!` prefix to execute exploration logic as a bash subprocess misunderstands the feature—bash output still flows back into the conversation context, and meaningful brainstorming and evaluation of implementation approaches requires LLM reasoning rather than shell commands.

Study Area:
Code Generation with Claude Code — review Custom Slash Commands concepts in the exam study guide.

---

### You've asked Claude Code to implement a function that transforms API responses into a normalized internal format. After two iterations, the output structure still doesn't match expectations—some fields are nested differently and timestamps aren't formatted correctly. You've been describing the requirements in prose, but Claude seems to interpret them differently each time. What's the most effective approach for the next iteration?
- The correct answer is C:
Providing concrete input-output examples is the most effective approach because it eliminates the ambiguity inherent in prose descriptions by showing Claude exactly what the expected transformation looks like. This directly addresses the root cause—misinterpretation of prose requirements—by giving unambiguous, concrete targets for field nesting and timestamp formatting.

Your answer:
A JSON schema can validate the output structure but doesn't help Claude understand the actual transformation logic needed to produce correct results. This approach addresses verification rather than comprehension, meaning Claude would still need to understand the mapping requirements to generate correct output in the first place.

Study Area:
Code Generation with Claude Code — review Iterative Refinement concepts in the exam study guide.

---

### Your automated code review averages 15 findings per pull request, with developers reporting a 40% false positive rate. The bottleneck is investigation time: developers must click into each finding to read Claude's reasoning before deciding whether to address or dismiss it. Your CLAUDE.md already contains comprehensive rules for acceptable patterns, and stakeholders have rejected any approach that filters findings before developer review. What change would best address the investigation time bottleneck?
- The correct answer is D:
Including reasoning and confidence assessments inline with each finding directly addresses the investigation time bottleneck by allowing developers to quickly evaluate findings without clicking into each one separately. This approach respects the constraint against filtering, since all findings remain visible while making triage significantly faster.

Your answer:
Automatically suppressing findings that match historical false positive signatures is another form of filtering before developer review, which stakeholders have explicitly rejected. Even though it uses data-driven pattern matching, it still removes findings from the developer's view.

Study Area:
Claude Code for Continuous Integration — review False Positive Reduction concepts in the exam study guide.

---

### The code review component works iteratively: Claude analyzes a changed file, then may request related files (imports, base classes, tests) via tool calling to understand context before providing final feedback. Your application defines a tool that lets Claude request file contents; Claude invokes this tool, receives results, and continues its analysis. You're evaluating batch processing to reduce API costs. What is the primary technical constraint when considering batch processing for this workflow?
- The correct answer is D:
This is correct. The batch API's asynchronous fire-and-forget model means there is no mechanism to intercept a tool call mid-request, execute the tool, and return results for Claude to continue its analysis. This fundamentally breaks iterative tool-calling workflows that require multiple rounds of tool invocation and response within a single logical interaction.

Your answer:
Batch processing provides a custom_id field for each request, which serves as a correlation identifier for matching outputs back to their corresponding inputs. This is not a limitation of the batch API.

Study Area:
Claude Code for Continuous Integration — review Batch Processing concepts in the exam study guide.

---

### Your automated review analyzes comments and docstrings. The current prompt instructs Claude to "check that comments are accurate and up-to-date." Findings frequently flag acceptable patterns (TODO markers, straightforward descriptions) while missing comments that describe behavior the code no longer implements. What change addresses the root cause of this inconsistent analysis?
- The correct answer is D:
Specifying explicit criteria—flag comments only when their claimed behavior contradicts actual code behavior—directly addresses the root cause by replacing the vague instruction with a precise definition of what constitutes a problem. This eliminates both false positives on acceptable patterns and false negatives on genuinely misleading comments.

Your answer:
While few-shot examples of misleading comments can help the model recognize similar patterns, this approach won't generalize well to novel types of contradictions because it relies on pattern-matching rather than defining the underlying criterion the model should apply.

Study Area:
Claude Code for Continuous Integration — review Prompt Specificity concepts in the exam study guide.

---

### Your automated code review system shows inconsistent severity ratings—similar issues like null pointer risks receive "critical" severity in some PRs but only "medium" in others. Developer trust is declining because teams can't predict which findings require immediate attention. What's the most effective way to improve severity consistency?
- The correct answer is C:
Including explicit severity criteria with concrete code examples directly addresses the root cause of inconsistency by removing ambiguity about what each severity level means. This is a proven prompt engineering technique that gives the model clear reference points for classification, leading to more reliable and predictable severity assignments.

Your answer:
A static issue-type-to-severity mapping loses important context, since the same issue type (e.g., a null pointer risk) may warrant different severities depending on factors like code path, exposure, or criticality of the affected component. This rigid approach oversimplifies severity assignment and can lead to inaccurate ratings.

Study Area:
Claude Code for Continuous Integration — review Classification Consistency concepts in the exam study guide.

---

### Your team uses Claude Code to generate code suggestions, but you notice a pattern: subtle issues—performance optimizations that break edge cases, cleanups that change behavior unexpectedly—only surface when a different team member reviews the PR. Claude's reasoning during generation shows it considered these cases but concluded its approach was correct. Which approach directly addresses the root cause of this self-review limitation?
- The correct answer is B:
Using a second, independent Claude Code instance without access to the generator's reasoning directly addresses the root cause by eliminating confirmation bias. This fresh perspective mirrors the benefit of human peer review, where a different team member catches issues the original author rationalized away.

Your answer:
Asking Claude to critique its own suggestions within the same context does not address the root cause, because the same confirmation bias that led it to conclude its approach was correct will persist during self-review. The question explicitly states Claude already considered these cases and rationalized its decisions, so additional self-critique in the same context will likely reach the same conclusions.

Study Area:
Claude Code for Continuous Integration — review Multi-Instance Verification concepts in the exam study guide.

---

### After an initial automated review generates 12 findings, a developer pushes new commits to address the issues. When the review runs again, it produces 8 findings—but developers report that 5 duplicate earlier comments on code that was already fixed in the new commits. What's the most effective way to eliminate this redundant feedback while maintaining thorough analysis?
- The correct answer is C:
Including prior review findings in context allows Claude to intelligently distinguish between new issues and those already addressed by recent commits. This approach maintains thorough analysis while leveraging Claude's reasoning ability to avoid redundant feedback on fixed code.

Your answer:
A post-processing filter based on matching file paths and issue descriptions is brittle because LLM-generated comments vary in wording across runs, making exact matching unreliable. It also cannot semantically determine whether an issue has actually been resolved or merely rephrased differently.

Study Area:
Claude Code for Continuous Integration — review CI/CD Integration concepts in the exam study guide.

---

### Analysis of your automated code review shows significant variation in false positive rates across finding categories. Security and correctness findings have an 8% false positive rate, performance findings have 18%, style and naming findings have 52%, and documentation findings have 48%. Developer surveys indicate growing distrust—many have started dismissing findings without review because "half are wrong." The high false positive categories are undermining confidence in the accurate categories. What approach best restores developer trust while improving the system?

- The correct answer is C:
Temporarily disabling the high false positive categories (style, naming, documentation) immediately stops trust erosion by removing the noise that causes developers to dismiss all findings, while preserving the value of high-precision categories like security and correctness. This approach allows time to improve prompts for the problematic categories before re-enabling them, rebuilding trust through demonstrated accuracy.

Your answer:
Applying uniform strictness reduction across all categories would degrade the performance of already-accurate categories (like security and correctness at 8% false positive rate) to compensate for broken ones, sacrificing real value without effectively solving the trust problem in any category.

Study Area:
Claude Code for Continuous Integration — review False Positive Reduction concepts in the exam study guide.

---

### Your CI pipeline includes two Claude-powered code review modes: a pre-merge-commit hook that blocks PR merging until complete, and "deep analysis" that runs overnight, polls for batch completion, then posts detailed suggestions to the PR. You want to reduce API costs using the Message Batches API, which offers 50% cost savings but requires polling and may take up to 24 hours to complete. Which mode should use batch processing?
- Deep analysis only
Correct!
Deep analysis is the ideal candidate for batch processing because it already runs overnight, tolerates latency, and uses a polling model to check for completion before posting results—perfectly matching the Message Batches API's asynchronous, poll-based design while capturing the 50% cost savings.

---

### Your CI/CD system performs three types of Claude-powered analysis: (1) quick style checks on each PR that block merging until complete, (2) comprehensive security audits of the entire codebase run weekly, and (3) test case generation triggered nightly for recently-modified modules. The Message Batches API offers 50% cost savings but can take up to 24 hours to process. You want to optimize API costs while maintaining acceptable developer experience. Which combination correctly matches each task to its API approach?
- The correct answer is C:
This is the correct approach. PR style checks block developers and require immediate responses via synchronous calls, while weekly security audits and nightly test generation are scheduled tasks with flexible timelines that can easily tolerate the up-to-24-hour batch processing window, capturing the 50% cost savings on both.

Your answer:
Using the Message Batches API for all three tasks would create unacceptable delays for PR style checks, which block merging and require immediate feedback for developers. While this maximizes cost savings, the up-to-24-hour processing time makes it unsuitable for latency-sensitive, developer-blocking workflows.

Study Area:
Claude Code for Continuous Integration — review Batch Processing concepts in the exam study guide.

---

### Your pipeline script runs claude "Analyze this pull request for security issues" but the job hangs indefinitely. Logs indicate Claude Code is waiting for interactive input. What's the correct approach to run Claude Code in an automated pipeline?
- The correct answer is C:
The `-p` (or `--print`) flag is the documented way to run Claude Code in non-interactive mode. It processes the given prompt, outputs the result to stdout, and exits without waiting for user input, making it ideal for CI/CD pipelines.

Your answer:
The `--batch` flag is not a documented or supported option for Claude Code. Using this non-existent flag would likely result in an error or be ignored, failing to resolve the interactive input issue.

Study Area:
Claude Code for Continuous Integration — review CI/CD Integration concepts in the exam study guide.

---

### Your automated reviews identify valid issues but developers report the feedback isn't actionable. Findings say things like "complex ticket allocation logic" or "potential null pointer" without specifying what to change. When you add detailed instructions like "always include specific fix suggestions," the model still produces inconsistent output—sometimes detailed, sometimes vague. What prompting technique would most reliably produce consistently actionable feedback?
- Add 3-4 few-shot examples showing the exact format you want: issue identified, code location, specific fix suggestion
Correct!
Few-shot examples are the most effective technique for achieving consistent output format when instructions alone produce variable results. Providing 3-4 examples showing the exact desired format (issue, location, specific fix) gives the model a concrete pattern to follow, which is more reliable than abstract instructions.

---

### Your team wants to reduce API costs for automated analysis. Currently, real-time Claude calls power two workflows: (1) a blocking pre-merge check that must complete before developers can merge, and (2) a technical debt report generated overnight for review the next morning. Your manager proposes switching both to the Message Batches API for its 50% cost savings. How should you evaluate this proposal?
- Use batch processing for the technical debt reports only; keep real-time calls for pre-merge checks.
Correct!
This is the correct approach because the Message Batches API's up to 24-hour processing time with no guaranteed latency SLA makes it ideal for overnight technical debt reports but unsuitable for blocking pre-merge checks where developers are waiting. This matches each workflow to the appropriate API based on its latency requiremen

---

### A pull request modifies 14 files across the stock tracking module. Your single-pass review analyzing all files together produces inconsistent results: detailed feedback for some files but superficial comments for others, obvious bugs missed, and contradictory feedback—flagging a pattern as problematic in one file while approving identical code elsewhere in the same PR. How should you restructure the review?
- Split into focused passes: analyze each file individually for local issues, then run a separate integration-focused pass examining cross-file data flow.
Splitting the review into focused per-file passes directly addresses the root cause of attention dilution, ensuring consistent depth and catching local issues reliably. A separate integration-focused pass then handles cross-file concerns like data flow dependencies, covering both dimensions of review quality.

---

### Your CI pipeline runs the Claude Code CLI (with --print mode) using CLAUDE.md to provide project context for code reviews, and developers generally find the reviews insightful. However, they report that integrating findings into your workflow is difficult—Claude produces narrative paragraphs that must be manually copied into PR comments. Your team wants to automatically post each finding as a separate inline PR comment at the relevant code location, which requires structured data with file path, line number, severity, and suggested fix. What's the most effective approach?
- Use CLI flags --output-format json and --json-schema to enforce structured findings, then parse output to post inline comments via the GitHub API.
Using `--output-format json` with `--json-schema` enforces structured output at the CLI level, guaranteeing well-formed JSON with the required fields (file path, line number, severity, suggested fix) that can be reliably parsed and posted as inline PR comments via the GitHub API. This is the most effective approach because it leverages native CLI capabilities designed specifically for structured output enforcement.

---

### Your automated review generates test case suggestions for each PR. When reviewing a PR that adds course completion tracking, Claude suggests 10 test cases but developer feedback indicates 6 duplicate scenarios already covered in the existing test suite. What change would most effectively reduce duplicate suggestions?
- Include the existing test file in the context so Claude can identify what scenarios are already covered
Correct!
Including the existing test file in the context directly addresses the root cause of duplication: Claude can only avoid suggesting already-covered scenarios if it knows what tests already exist. This gives Claude the information needed to reason about which suggestions would be genuinely new and valuable.