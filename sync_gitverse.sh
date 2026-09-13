#!/usr/bin/env bash
# Publish the GitVerse mirror, where Russian is the primary README.
#
# Both hosts render README.md, so the mirror cannot simply be a copy: it needs
# the two language files swapped. Rather than maintain a divergent branch by
# hand, this rebuilds the `gitverse` branch from master on every run, applies
# the swap as a single commit on top, and force-pushes it. master stays the one
# source of truth and the mirror is always exactly master plus a rename.
set -euo pipefail

REMOTE="${GITVERSE_REMOTE:-gitverse}"
BRANCH="${GITVERSE_BRANCH:-gitverse}"
SRC="${GITVERSE_SOURCE:-master}"

git rev-parse --verify "${SRC}" >/dev/null
if [ -n "$(git status --porcelain)" ]; then
  echo "working tree is dirty; commit or stash first" >&2
  exit 1
fi

here="$(git rev-parse --abbrev-ref HEAD)"
trap 'git checkout -q "${here}"' EXIT

git checkout -q -B "${BRANCH}" "${SRC}"
git mv README.md README.en.md
git mv README.ru.md README.md
git -c user.name="$(git log -1 --format=%an "${SRC}")" \
    -c user.email="$(git log -1 --format=%ae "${SRC}")" \
    commit -q -m "Swap the READMEs for the GitVerse mirror

Both hosts render README.md, so the mirror carries the Russian text there and
the English one as README.en.md. This commit is rebuilt from ${SRC} by
sync_gitverse.sh on every publish; do not commit onto this branch by hand."

git push --force "${REMOTE}" "${BRANCH}:${BRANCH}"
echo "pushed ${BRANCH} -> ${REMOTE}"
