/**
 * Maakt van een codeblok met taal `mermaid` een diagram.
 *
 * In de markdown schrijf je gewoon:
 *
 *     ```mermaid
 *     erDiagram
 *         PRODUCT ||--|{ DEELPRODUCT : "bestaat uit"
 *     ```
 *
 * Deze plugin zet het blok om in `<pre class="mermaid">`. In de browser tekent
 * Mermaid het diagram (zie `src/components/Footer.astro`). Zonder JavaScript
 * blijft de tekst van het diagram leesbaar.
 */
import type { Root } from "mdast";
import { visit } from "unist-util-visit";

const escape = (s: string) =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

export function remarkMermaid() {
  return (tree: Root) => {
    visit(tree, "code", (node, index, parent) => {
      if (node.lang !== "mermaid" || !parent || index === undefined) return;
      parent.children[index] = {
        type: "html",
        value: `<pre class="mermaid">${escape(node.value)}</pre>`,
      };
    });
  };
}
