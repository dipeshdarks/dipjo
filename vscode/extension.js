const vscode = require("vscode");

function activate(context) {
  console.log("Dipjo extension is now active!");

  const diagnosticCollection = vscode.languages.createDiagnosticCollection("dipjo");
  context.subscriptions.push(diagnosticCollection);

  if (vscode.window.activeTextEditor) {
    updateDiagnostics(vscode.window.activeTextEditor.document, diagnosticCollection);
  }

  context.subscriptions.push(
    vscode.window.onDidChangeActiveTextEditor((editor) => {
      if (editor) {
        updateDiagnostics(editor.document, diagnosticCollection);
      }
    })
  );

  context.subscriptions.push(
    vscode.workspace.onDidChangeTextDocument((event) => {
      updateDiagnostics(event.document, diagnosticCollection);
    })
  );
}

function updateDiagnostics(document, diagnosticCollection) {
  if (document.languageId !== "dipjo") return;

  const diagnostics = [];
  const text = document.getText();
  const lines = text.split("\n");

  lines.forEach((line, index) => {
    if (line.trim().endsWith("..") && !line.trim().startsWith("note")) {
      const range = new vscode.Range(
        new vscode.Position(index, line.length - 2),
        new vscode.Position(index, line.length)
      );
      diagnostics.push(
        new vscode.Diagnostic(
          range,
          "Double period detected. Did you mean single period?",
          vscode.DiagnosticSeverity.Warning
        )
      );
    }
  });

  diagnosticCollection.set(document.uri, diagnostics);
}

function deactivate() {}

module.exports = { activate, deactivate };
