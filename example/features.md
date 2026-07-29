Listed directory vscode-extension
Listed directory src
Viewed extension.ts:1-51

To extend **Arun-Code** for inline editor completions (in VS Code / Antigravity) and agentic shell script execution, you can build on top of your existing local server ([server.py](file:///c:/Users/Arun/projects/arun-code/arun_code/server.py)) and tool engine ([agent.py](file:///c:/Users/Arun/projects/arun-code/arun_code/agent.py)).

---

## 1. Inline Code Completions (VS Code & Antigravity)

VS Code extensions provide the `vscode.languages.registerInlineCompletionItemProvider` API to show ghost text completions at the user's cursor in real time.

### Step 1: Update the Extension Provider
In your extension (e.g. [extension.ts](file:///c:/Users/Arun/projects/arun-code/vscode-extension/src/extension.ts)), register an inline completion provider:

```typescript
import * as vscode from "vscode";

export function activate(context: vscode.ExtensionContext) {
  const provider: vscode.InlineCompletionItemProvider = {
    async provideInlineCompletionItems(document, position, context, token) {
      // 1. Get surrounding text (prefix before cursor, suffix after cursor)
      const prefix = document.getText(new vscode.Range(new vscode.Position(0, 0), position));
      const suffix = document.getText(new vscode.Range(position, new vscode.Position(document.lineCount, 0)));

      // 2. Send request to your local Arun-Code server
      const prompt = `Fill in the missing code at <CURSOR>:\n\n${prefix}<CURSOR>${suffix}`;
      
      try {
        const response = await fetch("http://localhost:8000/v1/chat/completions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            messages: [{ role: "user", content: prompt }],
          }),
        });

        const data = await response.json();
        const completionText = data.choices?.[0]?.message?.content ?? "";

        // 3. Return the suggestion to render as ghost text in the editor
        return [
          new vscode.InlineCompletionItem(
            completionText,
            new vscode.Range(position, position)
          ),
        ];
      } catch (error) {
        return [];
      }
    },
  };

  // Register for all programming languages
  context.subscriptions.push(
    vscode.languages.registerInlineCompletionItemProvider({ pattern: "**" }, provider)
  );
}
```

---

## 2. Agentic Task Execution (Running Bash / Shell Scripts)

Your backend already has a basic tool execution engine in [agent.py](file:///c:/Users/Arun/projects/arun-code/arun_code/agent.py) with `run_shell` and `read_file`. You can extend this into an interactive **Agent Loop**.

### Architecture Overview

```mermaid
graph TD
    A[VS Code Extension / User Request] -->|1. Prompt: 'Run test suite'| B[Local FastAPI Server]
    B -->|2. Request completion + available tools| C[NVIDIA NIM Model]
    C -->|3. Tool Call: run_shell\('pytest'\)| B
    B -->|4. Execute tool via agent.py| D[Local System / Terminal]
    D -->|5. Output: 5 passed| B
    B -->|6. Send output back to model| C
    C -->|7. Final response| A
```

---

### Step 1: Implement an Agent Loop in [agent.py](file:///c:/Users/Arun/projects/arun-code/arun_code/agent.py)

Add an agent loop function that lets the model run shell commands or scripts until the user's task is completed:

```python
from arun_code.agent import execute_tool
from arun_code.models import ChatMessage
from arun_code.nim_client import send_completion

def run_agent_task(prompt: str, config, max_steps: int = 5) -> str:
    """Run an autonomous task using available local tools (e.g. run_shell)."""
    
    system_prompt = (
        "You are an AI developer assistant. You can run shell commands using the format:\n"
        "TOOL: run_shell\nCOMMAND: <command>\n\n"
        "When the task is complete, answer normally without any tool calls."
    )
    
    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=prompt),
    ]

    for step in range(max_steps):
        response = send_completion(messages, config)
        if response.error:
            return f"Agent Error: {response.error}"

        content = response.content

        # Check if the model wants to execute a shell tool
        if "TOOL: run_shell" in content and "COMMAND:" in content:
            command = content.split("COMMAND:")[1].strip().split("\n")[0]
            print(f"[Agent Step {step+1}] Running shell command: {command}")

            # Execute command using local tool
            tool_result = execute_tool("run_shell", command=command)
            
            # Feed tool execution output back to the conversation
            messages.append(ChatMessage(role="assistant", content=content))
            messages.append(ChatMessage(
                role="user", 
                content=f"Tool execution result:\n{tool_result.output}"
            ))
        else:
            # Model finished task
            return content

    return "Agent reached maximum execution steps."
```

---

### Step 2: Triggering Execution Tasks in VS Code / Antigravity

In your VS Code extension, you can trigger tasks via VS Code's integrated terminal API:

```typescript
// Execute a shell script or task directly in VS Code's integrated terminal
function runShellTask(command: string) {
  const terminal = vscode.window.createTerminal("Arun-Code Task");
  terminal.show();
  terminal.sendText(command);
}
```

Or execute tasks via VS Code Task API (`vscode.tasks.executeTask`):
```typescript
const task = new vscode.Task(
  { type: "shell" },
  vscode.TaskScope.Workspace,
  "Run Build Script",
  "Arun-Code",
  new vscode.ShellExecution("./scripts/build.sh")
);

await vscode.tasks.executeTask(task);
```

---

### Summary of What to Add Next

1. **Inline Suggestions**: Add `registerInlineCompletionItemProvider` to `vscode-extension/src/extension.ts`.
2. **Tool Execution API**: Add a `/v1/agent/execute` endpoint to [server.py](file:///c:/Users/Arun/projects/arun-code/arun_code/server.py) to process agentic tasks that require shell commands.