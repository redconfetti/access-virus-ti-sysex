#!/usr/bin/env node
/** Extract markdownlint-compatible heading slugs from a markdown file. */

import fs from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const here = dirname(fileURLToPath(import.meta.url));
const mlRoot = join(here, "..", "node_modules", "markdownlint");

const { parse } = await import(join(mlRoot, "lib/micromark-parse.mjs"));
const { filterByPredicate, filterByTypes } = await import(
  join(mlRoot, "helpers/micromark-helpers.cjs")
);

const childrenExclude = new Set(["image", "reference", "resource"]);
const tokensInclude = new Set([
  "characterEscapeValue",
  "codeTextData",
  "data",
  "mathTextData",
]);
const explicitAnchorRe = /\{(#[a-z\d]+(?:[-_][a-z\d]+)*)\}/giu;

function convertHeadingToHTMLFragment(headingText) {
  const inlineText = filterByPredicate(
    headingText.children,
    (token) => tokensInclude.has(token.type),
    (token) => (childrenExclude.has(token.type) ? [] : token.children)
  )
    .map((token) => token.text)
    .join("");
  return (
    "#" +
    encodeURIComponent(
      inlineText
        .toLowerCase()
        .replace(/[^\p{Letter}\p{Mark}\p{Number}\p{Connector_Punctuation}\- ]/gu, "")
        .replace(/ /gu, "-")
    )
  );
}

function headingLevel(headingText, content) {
  const line = content.split("\n")[headingText.startLine - 1] || "";
  const match = line.match(/^(#{1,6})\s/);
  return match ? match[1].length : 2;
}

function displayText(raw) {
  return raw.replace(/\s*\{#[^}]+\}\s*/gu, "").trim();
}

function explicitSlug(raw) {
  const match = explicitAnchorRe.exec(raw);
  explicitAnchorRe.lastIndex = 0;
  return match ? match[1].slice(1) : null;
}

function assignSlug(fragment, counts) {
  const seen = counts.get(fragment) || 0;
  const base = decodeURIComponent(fragment.slice(1));
  const slug = seen === 0 ? base : `${base}-${seen}`;
  counts.set(fragment, seen + 1);
  return slug;
}

const maxLevel = Number.parseInt(process.argv[3] || "4", 10);
const file = process.argv[2];
const content =
  file === "-" ? fs.readFileSync(0, "utf8") : fs.readFileSync(file, "utf8");
const tokens = parse(content);
const headingTexts = filterByTypes(tokens, ["atxHeadingText", "setextHeadingText"]);
const counts = new Map();
const results = [];

for (const headingText of headingTexts) {
  const level = headingLevel(headingText, content);
  if (level < 2 || level > maxLevel) {
    continue;
  }
  const raw = headingText.text.trim();
  const named = explicitSlug(raw);
  const slug = named || assignSlug(convertHeadingToHTMLFragment(headingText), counts);
  results.push({
    level,
    text: displayText(raw),
    slug,
  });
}

process.stdout.write(JSON.stringify(results));
