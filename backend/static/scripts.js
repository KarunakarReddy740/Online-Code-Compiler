// Initialize CodeMirror instance
let editor = CodeMirror(document.getElementById("editor"), {
  value: "# Write your code here...\nprint('Hello from Python!')",
  mode: "python",
  theme: "dracula",
  lineNumbers: true,
  matchBrackets: true,
  autoCloseBrackets: true,
  indentUnit: 4,
  tabSize: 4
});

// Switch syntax mode when language changes
const langSelect = document.getElementById("language");
langSelect.addEventListener("change", () => {
  const lang = langSelect.value;
  editor.setOption("mode", lang === "Python" ? "python" : "javascript");
  if (lang === "JavaScript" && editor.getValue().startsWith("# Write your code here")) {
    editor.setValue(`// Write your code here...\nconsole.log('Hello from Node.js!');`);
  }
});

// Run code
document.getElementById("run-btn").addEventListener("click", async () => {
  const code = editor.getValue();
  const language = langSelect.value;

  const output = document.getElementById("output");
  output.textContent = "⏳ Running...";

  try {
    const res = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, language })
    });
    const data = await res.json();
    output.textContent = data.output || "(no output)";
  } catch (e) {
    output.textContent = "❌ Failed to reach server: " + e;
  }
});
