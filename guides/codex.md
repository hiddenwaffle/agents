# Codex

Codex may be useful for a second opinion or browser work. Judge it by results on the actual task.

- The `codex` CLI may be installed. Using a hosted model sends task context to its provider and can start an agent that runs commands. Obtain approval before handing work to it unless that work is already authorized. Pass along my project boundaries, tool limits, and other applicable constraints.
- Use the model I request. When choosing or comparing models, check [current official model documentation](https://learn.chatgpt.com/docs/models). Availability and defaults depend on the client, account, and configuration. Do not treat an old ranking or benchmark on a different task as evidence for this one.
- For authorized browser work, check which tools the actual session provides. [Browser and Developer mode](https://learn.chatgpt.com/docs/browser) capabilities depend on the client and configuration; model capability alone does not provide a browser tool.
- Check the browser coverage a test actually exercises. [Playwright's WebKit](https://playwright.dev/docs/browsers#webkit) is not the Safari application, so do not report a WebKit run as a Safari test.
- The main instructions' browser, process, and outward-facing permission rules still apply, regardless of the client loading them.
