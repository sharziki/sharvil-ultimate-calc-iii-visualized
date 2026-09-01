// stdin: JSON array of {tex, display}. stdout: JSON array of rendered HTML strings.
const katex = require("katex");
let raw = "";
process.stdin.on("data", d => raw += d);
process.stdin.on("end", () => {
  const items = JSON.parse(raw);
  const out = items.map(it =>
    katex.renderToString(it.tex, {
      displayMode: !!it.display,
      throwOnError: true,
      strict: "ignore",
    })
  );
  process.stdout.write(JSON.stringify(out));
});
