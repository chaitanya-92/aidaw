import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
const script = html.match(/<script>([\\s\\S]*?)<\\/script>/i)?.[1];

test("studio page has a document shell and accessible main controls", () => {
  assert.match(html, /<!doctype html>/i);
  assert.match(html, /id="file"/);
  assert.match(html, /id="play"/);
  assert.match(html, /id="stop"/);
  assert.match(html, /id="generate"/);
  assert.match(html, /id="exportBtn"/);
});

test("inline JavaScript parses", () => {
  assert.ok(script, "inline script should exist");
  assert.doesNotThrow(() => new Function(script));
});

test("vocal upload, local generation and WAV export are wired", () => {
  assert.match(script, /async function loadFile\(f\)/);
  assert.match(script, /function gen\(\)/);
  assert.match(script, /async function exportMix\(\)/);
  assert.match(script, /function wav\(buffer\)/);
});

test("vocal effects and project JSON restore controls exist", () => {
  assert.match(html, /id="reverb"/);
  assert.match(html, /id="delay"/);
  assert.match(html, /id="loadProject"/);
  assert.match(script, /source\.connect\(conv\)/);
  assert.match(script, /source\.connect\(d\)/);
  assert.match(script, /p\.schemaVersion!==1/);
});

test("prototype labels procedural generation honestly", () => {
  assert.match(html, /not an AI-generated recording/i);
  assert.match(html, /not a generative music model/i);
});
