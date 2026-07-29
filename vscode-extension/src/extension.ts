import * as vscode from "vscode";

const SERVER_URL = "http://localhost:8000/v1/chat/completions";

export function activate(context: vscode.ExtensionContext) {
  const command = vscode.commands.registerCommand("arun-code.chat", async () => {
    const prompt = await vscode.window.showInputBox({
      prompt: "Enter your coding prompt",
      placeHolder: "e.g. Write a Python function to sort a list",
    });

    if (!prompt) {
      return;
    }

    const outputChannel = vscode.window.createOutputChannel("Arun-Code");
    outputChannel.show(true);
    outputChannel.appendLine(`> ${prompt}`);
    outputChannel.appendLine("");

    try {
      const response = await fetch(SERVER_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [{ role: "user", content: prompt }],
        }),
      });

      const data = (await response.json()) as any;

      if (data.error) {
        outputChannel.appendLine(`Error: ${data.error.message}`);
        return;
      }

      const content = data.choices?.[0]?.message?.content ?? "No response received.";
      outputChannel.appendLine(content);
    } catch (err: any) {
      outputChannel.appendLine(
        `Unable to reach the Arun-Code server at ${SERVER_URL}. ` +
          "Make sure it is running (uv run python -m arun_code.server)."
      );
    }
  });

  context.subscriptions.push(command);
}

export function deactivate() {}
