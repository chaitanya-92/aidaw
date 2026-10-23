import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
const scriptStart = html.indexOf("<script>");
const scriptEnd = html.indexOf("</script>", scriptStart + 8);
const script = scriptStart >= 0 && scriptEnd >= 0 ? html.slice(scriptStart + 8, scriptEnd) : "";

test("studio page has a document shell and main controls", () => {
  assert.match(html, /<!doctype html>/i);
  for (const id of ["file", "play", "stop", "generate", "exportBtn", "loadProject"]) {
    assert.ok(html.includes('id="' + id + '"'), "missing control: " + id);
  }
});

test("inline JavaScript parses", () => {
  assert.ok(script, "inline script should exist");
  assert.doesNotThrow(() => new Function(script));
});

test("vocal upload, local generation and WAV export are wired", () => {
  assert.ok(script.includes("async function loadFile(f)"));
  assert.ok(script.includes("function gen()"));
  assert.ok(script.includes("async function exportMix()"));
  assert.ok(script.includes("function wav(buffer)"));
});

test("vocal effects and project JSON restore controls exist", () => {
  assert.ok(script.includes("source.connect(conv)"), "reverb send should be connected");
  assert.ok(script.includes("source.connect(d)"), "delay send should be connected");
  assert.ok(script.includes("p.schemaVersion!==1"), "project version should be validated");
});

test("prototype labels procedural generation honestly", () => {
  assert.match(html, /not a generative music model/i);
  assert.match(html, /not a generative music model/i);
});
