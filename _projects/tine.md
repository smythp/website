---
weight: 100
layout: project
name: Tine
current: true
link: https://github.com/smythp/tine
link_text: View on GitHub
role: Creator
image: tine.png
description: Drive a GNOME Wayland desktop with AI agents. Uses the AT-SPI accessibility tree where apps expose it, computer vision where they don't.
---

<p>
  Tine is a command-line bridge between an AI coding agent (Claude Code, Codex, etc.) and a running Linux desktop. It reads the screen, walks the accessibility tree, and injects keyboard and mouse events at the kernel level — no Wayland portal dialogs, no per-action consent prompts, no X11 fallback hacks.
</p>

<p>
  Anthropic's computer-use feature works on Windows and macOS. If you use Linux — and especially Wayland, which is more locked-down than X11 and breaks most of the existing Linux automation stack — you're mostly out of luck. Tine is an attempt at a usable Wayland alternative.
</p>
