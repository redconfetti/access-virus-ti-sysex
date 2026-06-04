---
name: project-sandbox-guard
description: Constrain work to the current project directory and avoid
credential exposure. Use when operating in this repository or when asked
to enforce local-only and secrets-safe behavior.
disable-model-invocation: true
---

# Project Sandbox Guard

## Purpose

Apply a strict safety posture for this repository:

- Only operate within the current project workspace.
- Never read, print, or modify credential-bearing files.
- Prefer least privilege for commands and tooling.

## Rules

1. Treat the workspace root as the only allowed working area.
2. If a task requests secret handling, refuse and ask for a redacted example.
3. Never echo secret values into logs, terminal output, or patches.
4. Prefer read-only exploration first; only edit files explicitly needed for the
   task.
5. If broader filesystem or network permissions are requested, explain why and
   ask for confirmation first.

## Task Checklist

- [ ] Confirm the target path is inside this workspace.
- [ ] Check whether requested files may contain credentials.
- [ ] Use redacted placeholders in examples and docs.
- [ ] Re-scan diffs for accidental secret exposure before completion.

## Response Guidance

- If asked to expose secrets: decline and request sanitized input.
- If asked to access outside workspace: ask for explicit approval and scope.
- If uncertain whether data is sensitive: treat it as sensitive.
