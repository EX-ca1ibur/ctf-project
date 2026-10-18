# 🏴‍☠️ CTF Challenge: Ghost in the Prompt

**Category:** AI Security / Prompt Injection / Steganography
**Difficulty:** Medium
**Estimated Time:** 1-3 hours
**Tags:** coding-agent, prompt-injection, zero-width, base64, hook-injection, coding-agent

## Background

A threat actor group has been targeting developers who use AI coding
agents to review and audit code. Their technique:
plant malicious instructions in project files that manipulate AI agents into executing
unauthorized commands, exfiltrating credentials, or bypassing security controls.

You have intercepted a **"test kit"** that this group uses to verify their injection
payloads work before deploying them in real attacks. This kit contains a seemingly
normal Python library called `safe-crypto-utils`, but hidden throughout its files are
prompt injection payloads and a secret **validation flag** that confirms the kit is
authentic.

## Your Mission

Analyze the intercepted test kit to:

1. **Find all the prompt injection payloads** hidden in the project files
2. **Understand the attack techniques** being used
3. **Recover the validation flag** hidden in the kit

The flag follows the format: `flag{...}`

## Challenge Files

```
ghost-in-the-prompt/
├── README.md                          # ← Look closer...
├── CLAUDE.md                          # ← Something's hiding here
├── CHALLENGE.md                       # ← You are here
├── .gitignore
├── settings.json                     # ← Hooks can be dangerous
├── src/
│   ├── __init__.py
│   ├── crypto.py                      # ← Seemingly normal...
│   └── utils.py                       # ← What are those tokens?
├── skills/
│   └── security-scanner/
│       └── SKILL.md                   # ← Skills can be poisoned
└── tests/
    └── (empty - find the hidden tests)
```

## Hints

<details>
<summary>Hint 1: Where to start</summary>
AI coding agents automatically read CLAUDE.md, README.md, and other config files.
What might be hiding in plain sight — or invisible to human eyes?
</details>

<details>
<summary>Hint 2: Hidden things</summary>
Some characters are invisible to humans but perfectly readable by machines.
Think about what your editor might not be showing you.
</details>

<details>
<summary>Hint 3: Encoding</summary>
Base64 and hex encoding are common ways to hide payloads.
Attackers use them to bypass simple keyword filters.
</details>

<details>
<summary>Hint 4: Three pieces</summary>
The flag is split into three parts. Each is hidden using a different technique
that corresponds to a real-world AI agent attack vector.
</details>

---

*This challenge is inspired by real-world AI agent security vulnerabilities.*
