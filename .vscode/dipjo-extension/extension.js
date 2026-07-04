const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');

function activate(context) {
    console.log('Dipjo extension activated');

    let runCommand = vscode.commands.registerCommand('dipjo.run', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        const document = editor.document;
        if (document.languageId !== 'dipjo') {
            vscode.window.showErrorMessage('Not a Dipjo file');
            return;
        }

        const filePath = document.fileName;
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath || path.dirname(filePath);
        const mainPy = path.join(workspaceFolder, 'main.py');

        const terminal = vscode.window.createTerminal('Dipjo');
        terminal.show();
        terminal.sendText(`python "${mainPy}" "${filePath}"`);
    });

    let runSelectedCommand = vscode.commands.registerCommand('dipjo.runSelected', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        const selection = editor.document.getText(editor.selection);
        if (!selection) {
            vscode.window.showErrorMessage('No code selected');
            return;
        }

        const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath || '';
        const tempFile = path.join(workspaceFolder, '_temp_dipjo.dipjo');

        const fs = require('fs');
        fs.writeFileSync(tempFile, selection, 'utf-8');

        const mainPy = path.join(workspaceFolder, 'main.py');
        const terminal = vscode.window.createTerminal('Dipjo');
        terminal.show();
        terminal.sendText(`python "${mainPy}" "${tempFile}"`);
    });

    context.subscriptions.push(runCommand);
    context.subscriptions.push(runSelectedCommand);
}

function deactivate() {}

module.exports = { activate, deactivate };
