# Agent instructions

Personal instructions maintained in one place, with a modular version for local agents and a generated, self-contained version to paste into claude.ai.

## Files

| File | Purpose | Update directly? |
| --- | --- | --- |
| [AGENTS.md](AGENTS.md) | Main instructions and pointers to task-specific guidance | Yes |
| [Grimoire skill](skills/grimoire/SKILL.md) | Markdown formatting rules shared by local and chat versions | Yes |
| [Codex guide](guides/codex.md) | Guidance used by the local version when relevant | Yes |
| `generate_claude_ai.py` | Selects chat sections and embeds the Grimoire rules | When generation or section selection needs to change |
| [chat_AGENTS.md](chat_AGENTS.md) | Generated instructions for the claude.ai Account textbox | No; regenerate it |

`AGENTS.md` is the shared source for Claude Code, Codex, and GitHub Copilot. Its on-demand paths use `~/.agents/`, where `~` means the current user's home directory. The repository can live anywhere on each machine. Each client has its own installation steps; a machine needs only the clients it actually uses.

## Generate chat instructions

Requires Python 3. No third-party packages are needed.

From this directory:

```bash
python3 generate_claude_ai.py
```

This reads `AGENTS.md` and `skills/grimoire/SKILL.md`, then writes `chat_AGENTS.md`. Copy the entire generated file into the instructions textbox under Account in claude.ai settings.

To check whether the export matches the sources without writing anything:

```bash
python3 generate_claude_ai.py --check
```

The check exits with status `0` when current, or `1` when missing, stale, or invalid. A normal generation run replaces the previous export, so make changes in the source files.

Default paths are relative to the script's directory, regardless of the working directory. You can also run it from elsewhere:

```bash
python3 /absolute/path/to/agents/generate_claude_ai.py
```

## Update the rules

1. Edit `AGENTS.md` for general preferences or local-agent rules, `skills/grimoire/SKILL.md` for Grimoire rules, or `guides/codex.md` for Codex guidance.
2. If you add, remove, or rename a level-two heading (`##`) in `AGENTS.md`, update `SECTION_POLICY` in `generate_claude_ai.py`. Set its value to `True` to include that section in chat, or `False` to omit it.
3. When refactoring these instructions or their export, update the date in the top heading of `AGENTS.md` to the current date (`YYYY-MM-DD`). Update any existing header dates in other affected source files too. The generator copies the date into `chat_AGENTS.md`; do not edit the generated date separately.
4. Run the generator and review `chat_AGENTS.md`, including that its header date matches `AGENTS.md`.
5. Paste the new export into claude.ai. Installed symlinks already point to the edited sources, so ordinary content updates need no copying or relinking. Start a fresh local-agent session and perform the checks below.

The generator stops before writing if it encounters unclassified, missing, or duplicate main-file sections. It also rejects malformed document structure, including unclosed code fences and missing skill frontmatter. A renamed section therefore requires a deliberate inclusion decision.

### Maintenance checklist

These instructions cover routine maintenance of the layouts documented below without another documentation search. Run only the setup steps for clients actually installed or requested. Source changes propagate through existing links; each client still needs the loading and behaviour checks below. Consult the linked upstream documentation if a client changes its configuration format or the documented checks fail.

| Change | Local agents | Chat export |
| --- | --- | --- |
| Edit rules inside an existing `AGENTS.md` section | Edit the source once; keep existing links | Regenerate; included sections change, omitted sections do not |
| Add, rename, or remove a main-file section | Edit the source and update matching `SECTION_POLICY` entries | Regenerate after deliberately choosing inclusion |
| Edit Grimoire rules | Edit `skills/grimoire/SKILL.md`; all installed skill-directory links see it | Regenerate and paste the updated export |
| Add, edit, or remove resources inside an existing skill directory | Directory links expose the changed contents; update references in `SKILL.md` | Grimoire's Markdown body is embedded, but separate resources are not |
| Edit `guides/codex.md` | Existing guide link sees the edit | No effect; this guide is excluded |
| Add another skill or guide | Follow the lifecycle steps below | No automatic inclusion; decide explicitly whether to extend the generator |
| Rename or move a source file or skill directory | Replace affected links and update all instruction references | Update generator input paths if affected, then regenerate |
| Edit the generator | Local instruction links are unaffected | Generate, review the diff, and check freshness |

From this repository, finish an update with:

```bash
python3 generate_claude_ai.py
python3 generate_claude_ai.py --check
git diff --check
git diff
```

Review the source and generated changes together. Refresh any separately maintained copies using the procedure below, then perform the client-specific checks. Report which clients were actually exercised and which remain untested. Copilot being documented does not establish that it is installed or verified.

The generator reads exactly two input files: the main instructions and the Grimoire `SKILL.md`. It does not scan `skills/` or `guides/`, follow Markdown links, or embed scripts and other skill resources. If Grimoire gains references to separate files, keep the chat export self-contained by adding the necessary text to its generation logic. A new skill intended for chat requires an explicit generator change; editing `SECTION_POLICY` alone only selects sections from the main file.

## What the chat export includes

The export keeps conversation preferences, fictional-story rules, file and document preferences, em dash rules, verification by behaviour, and inline-math emphasis rules. It appends the Grimoire skill body, removing its YAML metadata and nesting its headings under the main document.

It omits the local loading instructions, filesystem boundaries, host introspection, subagent rules, browser and process rules, the entire Transparency and confirmation section, and the Codex guide. The exact selection lives in `SECTION_POLICY`.

The embedded Grimoire text takes context in chat, but the export can be pasted as one block without installing a separate skill.

## Local installation with symlinks

The following commands are for a macOS or Linux shell. Installation depends on the agent application, regardless of which model it uses. Put this repository in a permanent location, open a shell at its root, and set the source directory:

```bash
agent_source="$(pwd -P)"
```

Run the shared supporting-file setup, followed by only the client sections you need. No source-file edits are needed for a different username, checkout location, or combination of these clients. `$HOME` in the shell examples resolves on the destination machine. Absolute symlink targets are local installation details and must be recreated there, not committed or copied between machines.

| Client | Main instruction destination | Skill discovery destination |
| --- | --- | --- |
| Claude Code CLI | `~/.claude/CLAUDE.md` | `~/.claude/skills/grimoire` |
| Codex | `~/.codex/AGENTS.md` | `~/.agents/skills/grimoire` |
| GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` | `~/.agents/skills/grimoire` |

All three read the guide on demand at `~/.agents/guides/codex.md`. This guide is a text file and does not require Codex to be installed. `~/.agents/guides/` is this repository's convention, not an automatic guide discovery feature of the clients. The main file tells the agent to read it when needed; it does not use `@` imports.

### Prepare existing destinations

Before each `ln -s` command, inspect the destination. Leave an existing link alone if it already points to the intended source. For a link that needs replacing, use `unlink` on the link itself, without a trailing slash. For a regular file or directory, move it to a unique backup name first. This example uses the shared guide path; substitute the destination being prepared:

```bash
destination="$HOME/.agents/guides/codex.md"
ls -ld "$destination"
```

If it is a symlink, inspect its target:

```bash
readlink "$destination"
```

To remove a symlink you intend to replace:

```bash
unlink "$destination"
```

For an existing regular file or directory, choose an unused backup name and move it instead:

```bash
mv -i "$destination" "$destination.before_symlinks"
```

Do not overwrite an earlier backup. For skill directories, choose a backup location outside all skill discovery directories so the backup does not load as another skill. Run the installation commands only when their destinations are absent, including dangling symlinks and directories.

### Shared supporting files

Every local installation uses the same supporting paths under `~/.agents/`. This directory belongs to the shared setup and does not require any particular client. A machine using only Copilot will have these links and its `.copilot` instruction link; it needs no `.claude` or `.codex` directory.

After preparing the destinations, run this once:

```bash
mkdir -p "$HOME/.agents/guides" "$HOME/.agents/skills"
ln -s "$agent_source/guides/codex.md" "$HOME/.agents/guides/codex.md"
ln -s "$agent_source/skills/grimoire" "$HOME/.agents/skills/grimoire"
```

### Claude Code CLI

Install the shared supporting files above, then link the main instructions and the skill into Claude's discovery directory:

```bash
mkdir -p "$HOME/.claude/skills"
ln -s "$agent_source/AGENTS.md" "$HOME/.claude/CLAUDE.md"
ln -s "$agent_source/skills/grimoire" "$HOME/.claude/skills/grimoire"
```

The maintained source can be named `AGENTS.md` while the global file Claude opens is named `CLAUDE.md`. Claude Code supports symlinked skill folders. After source edits, start a fresh session and check `/context` for the global memory file and `/skills` for `grimoire`. Run a Markdown task using `/grimoire`, then try one without explicitly naming the skill to check automatic loading. See the [memory documentation](https://code.claude.com/docs/en/memory) and [skills documentation](https://code.claude.com/docs/en/skills).

### Codex

Install the shared supporting files above, then link the main instructions:

```bash
mkdir -p "$HOME/.codex"
ln -s "$agent_source/AGENTS.md" "$HOME/.codex/AGENTS.md"
```

Codex reads global instructions from `~/.codex/AGENTS.md` and supports symlinked personal skills under `~/.agents/skills/`. If `CODEX_HOME` is set, use that directory for the main instruction link. A nonempty `AGENTS.override.md` there takes precedence over `AGENTS.md`; review an existing override before expecting the shared file to load. See the [instruction documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [skill documentation](https://learn.chatgpt.com/docs/build-skills).

After editing sources, start a fresh Codex session, ask it to list the instruction sources it loaded, and confirm the global file is included. Ask it to use `$grimoire` for a Markdown task, then try a task without naming the skill to check automatic selection. Codex detects skill changes automatically; restart if a change does not appear.

### GitHub Copilot CLI

Install the shared supporting files above, then link the personal instructions:

```bash
mkdir -p "$HOME/.copilot"
ln -s "$agent_source/AGENTS.md" "$HOME/.copilot/copilot-instructions.md"
```

The shared step already installed the skill at `~/.agents/skills/grimoire`; keep that one link even if Codex also uses it. Copilot CLI documents `~/.copilot/copilot-instructions.md` for personal instructions and `~/.agents/skills/` as a personal skill location. If `COPILOT_HOME` is set, use it for the instruction destination instead of `~/.copilot`. See GitHub's [instruction documentation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions) and [skill documentation](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills).

After updating sources, start a fresh Copilot session and use `/instructions` to confirm the personal instruction file is enabled. For skill changes, use `/skills reload` and `/skills info grimoire`. Try a Markdown task with `/grimoire`, then without explicitly naming it. This repository's symlink setup has not been tested in Copilot. If its installed version does not discover the linked skill, place a copy of the skill directory at that destination and refresh the copy after source edits.

### GitHub Copilot in editors and on GitHub

The CLI setup above does not configure every Copilot interface. For repository instructions in an editor or on GitHub, adapt the shared rules into that repository's `.github/copilot-instructions.md`. Copy `skills/grimoire/` to `.github/skills/grimoire/` and `guides/codex.md` to `.github/agent_guides/codex.md`. In the copied main instructions, replace the two on-demand paths with `.github/skills/grimoire/SKILL.md` and `.github/agent_guides/codex.md`, explicitly resolved from that repository's root. Remove the home-directory expansion sentence from that copy. The named-file exceptions continue to refer to those same instructions. These are repository paths, so they work for remote checkouts as well as local ones.

Use real, versioned files for GitHub-hosted agents; home-directory symlinks cannot provide files to a remote checkout. Refresh these copies when the shared sources change. Some clients also read repository `AGENTS.md`; check GitHub's [support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support) before choosing a format, and [skill instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) for supported skill locations. Test loading and a representative task in the actual interface you use.

### Migrate an earlier installation

If an earlier installation put supporting files under `~/.claude/`, create the shared `~/.agents/` links above before starting a session with the updated main instructions. Keep any already-correct `~/.agents/skills/grimoire` link. Main instruction links that already point to this checkout need no replacement.

The old `~/.claude/guides/codex.md` link is no longer used by this repository's instructions. Remove it only after inspecting it and confirming it is the old link to this repository, not a separate file. Keep `~/.claude/skills/grimoire` when Claude Code is used, since that is still its skill discovery path. Do not remove configuration directories, backups, or other clients' files as part of this migration.

### Move or replace the source directory

1. Put the full repository in its new permanent location.
2. Open a shell at the new repository root and set `agent_source="$(pwd -P)"` again.
3. Inspect each installed link, unlink it without a trailing slash, and recreate it using the applicable commands above. Include the shared guide and skill links.
4. Keep the shared `~/.agents/` destinations. Moving the checkout or changing usernames requires no edits to `AGENTS.md` or the chat export.
5. Start fresh agent sessions and verify loading and behaviour again.

The generator's defaults continue to work after moving the repository as long as its directory structure stays together. It generates the chat export only; installing links and pasting account instructions remain separate steps.

## Add or remove skills and guides

### Add a skill

1. Create `skills/<name>/SKILL.md` in this repository. Use a lowercase skill name, a YAML frontmatter block containing `name` and `description`, and a Markdown body explaining the workflow. Put supporting resources in the same skill directory and reference them from the body.
2. Decide which clients should use it. Keep shared skill instructions compatible with those clients; describe client-specific tools conditionally.
3. Set `agent_source` as above and choose `skill_name` below. Prepare each destination using the existing-destination procedure, then run only the applicable link commands.
4. If loading the skill is mandatory for particular tasks, add a trigger and `~/.agents/skills/<name>/SKILL.md` path under `On-demand instructions` in `AGENTS.md`. The named-file exceptions cover those instruction reads and their installed aliases. Do not insert a username, checkout path, or another client's configuration path. Ask before reading any additional out-of-project resources not covered by those exceptions.
5. Decide whether chat needs the new content. The current generator embeds only Grimoire; extend it deliberately if another skill belongs in chat.
6. Check discovery, explicit invocation, and automatic selection in each intended client using the new skill's name.

Set the name to the source directory being installed:

```bash
skill_name="example"
```

For every local installation, create the shared link once:

```bash
mkdir -p "$HOME/.agents/skills"
ln -s "$agent_source/skills/$skill_name" "$HOME/.agents/skills/$skill_name"
```

For Claude Code, also add its discovery link. Codex and Copilot CLI use the shared link directly:

```bash
mkdir -p "$HOME/.claude/skills"
ln -s "$agent_source/skills/$skill_name" "$HOME/.claude/skills/$skill_name"
```

### Add a guide

Create `guides/<name>.md` and add its task trigger and `~/.agents/guides/<name>.md` path to `AGENTS.md`. The named-file exceptions then cover it. Link it into the shared guide directory:

```bash
guide_name="example"
mkdir -p "$HOME/.agents/guides"
ln -s "$agent_source/guides/$guide_name.md" "$HOME/.agents/guides/$guide_name.md"
```

Prepare an existing destination before linking. All clients sharing the main file can follow that pointer. Guides do not become discoverable skills or enter the chat export automatically.

### Rename or remove a skill or guide

Update or remove its pointers in `AGENTS.md`, including filesystem exceptions and subagent references. Inspect the corresponding installed destinations and unlink only the links that target this repository. Move separately installed copies to backup locations outside skill discovery directories. Update or remove the source, recreate links if it was renamed, and check that each client discovers the intended result in a fresh session.

For a renamed skill, update its frontmatter `name`, invocation examples, and references too. Grimoire is a required generator input: renaming its directory requires updating the default `--grimoire` path in `generate_claude_ai.py` and the installation examples. Removing it requires changing the generator's rendering logic before regeneration can succeed.

## Refresh copied installations

Symlinked installations need no recopying after content edits. A copied skill, guide, or instruction file must be refreshed explicitly. This applies to Copilot's copy fallback and to files adapted for editors or GitHub-hosted agents.

For an unmodified skill copy, inspect the destination, move the existing copy to a unique backup outside all skill discovery directories, and copy the complete source directory to the now-absent destination:

```bash
skill_name="grimoire"
skill_destination="/absolute/path/to/installed/skills/$skill_name"
cp -R "$agent_source/skills/$skill_name" "$skill_destination"
```

Ensure the parent directory exists. Do not copy onto a symlink or into an existing skill directory; replacing the whole copy also removes resources deleted from the source. If converting a symlink to a copy, unlink only that symlink first. Recheck skill discovery and behaviour afterward.

For the personal installations above, copy updated instruction files and guides to their same destinations without rewriting the shared paths. For repository adaptations, merge source changes while preserving the repository-relative paths described above. Review the resulting diff and use that repository's normal commit and publication workflow before expecting a remote agent to see the update. After regenerating `chat_AGENTS.md`, replace the text in claude.ai's Account instructions and test a fresh chat.

## Verify after installation

Use the client-specific checks above. Test global loading from another project so this repository's own `AGENTS.md` cannot hide a missing global installation. Confirm both that the expected files load and that the agent follows their rules. For Grimoire, check relative links, simple headings, and inline math outside bold or italic spans.

`readlink` and reading through a link verify the filesystem setup. They do not verify an agent's runtime loading or rule-following.

After pasting the chat export, try a fresh claude.ai chat with a representative Markdown task. Successful generation verifies the export; observing the agent follow the rules verifies their use.

## Generator options

```bash
python3 generate_claude_ai.py --help
```

| Option | Default | Purpose |
| --- | --- | --- |
| `--source PATH` | `AGENTS.md` beside the script | Read another main instruction file |
| `--grimoire PATH` | `skills/grimoire/SKILL.md` beside the script | Read another Grimoire skill file |
| `--output PATH` | `chat_AGENTS.md` beside the script | Write or check another export |
| `--check` | Off | Check freshness without writing |

Explicit relative paths are resolved from the working directory. The output cannot be a symlink or resolve to either source path.
