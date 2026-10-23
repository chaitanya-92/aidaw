import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const html = await readFile(new URL("../index.html", import.meta.url), "utf8");
const scriptStart = html.indexOf("<script>");
const scriptEnd = html.indexOf("</script>", scriptStart + 8);
const script = scriptStart >= 0 && scriptEnd >= 0 ? html.slice(scriptStart + 8, scriptEnd) : "";

test("studio page has a document shell and main controls", () => {
  assert.match(html, /<!doctype html>/i);
  for (const id of ["file", "play", "stop", "generate", "exportBtn", "loadProject", "referenceFile", "analyzeReference", "autoMix", "mixTarget", "generateReferenceBeat", "aiBeatPrompt", "aiBeatPlayer"]) {
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

test("reference analysis and assisted mix export are wired", () => {
  assert.ok(script.includes("function analyzeAudio(b)"), "reference analyzer should exist");
  assert.ok(script.includes("function renderAnalysis(a)"), "analysis report should exist");
  assert.ok(script.includes("async function createAssistedMix()"), "offline mix renderer should exist");
  assert.ok(script.includes("new OfflineAudioContext"), "mix should render offline");
  assert.ok(script.includes("aida-assisted-mix-"), "mix should download a new WAV");
  assert.ok(script.includes("referenceBuffer"), "reference audio should be stored separately from vocal audio");
});

test("ACE-Step reference generation bridge is connected", () => {
  assert.ok(script.includes("AI_BRIDGE='http://127.0.0.1:8002'"));
  assert.ok(script.includes("fetch(AI_BRIDGE+'/api/generate'"));
  assert.ok(script.includes("fetch(AI_BRIDGE+'/api/jobs/'"));
  assert.ok(script.includes("reference_audio"));
  assert.ok(html.includes("ACE-Step"));
});
test("prototype labels procedural generation honestly", () => {
  assert.match(html, /synthesized backing idea locally/i);
  assert.match(html, /no generative music model/i);
});
