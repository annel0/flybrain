#!/usr/bin/env bash
# Run an experiment on the GPU host, keeping a full log and pulling results back.
#
#   ./run_experiment.sh <name> <python module and args...>
#
# Everything the run prints is kept verbatim in logs/, including failures.
set -uo pipefail

NAME="${1:?usage: run_experiment.sh <name> <command...>}"
shift
HOST="${FLYBRAIN_HOST:-homedev-lan}"
REMOTE="${FLYBRAIN_DIR:-~/Projects/flybrain}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="logs/${STAMP}-${NAME}.log"

mkdir -p logs out
rsync -az --exclude 'out/' --exclude 'logs/' src bench docs "${HOST}:${REMOTE}/" || exit 1

{
  echo "# experiment: ${NAME}"
  echo "# started:    ${STAMP}"
  echo "# host:       ${HOST}"
  echo "# command:    $*"
  echo "# code:       $(git rev-parse --short HEAD 2>/dev/null || echo 'uncommitted')"
  echo
} | tee "${LOG}"

ssh -o BatchMode=yes -o ServerAliveInterval=20 "${HOST}" \
    "bash -lc 'cd ${REMOTE} && .venv/bin/python $*'" 2>&1 \
  | grep -vE '^(W[0-9]{4}|In file included|/usr/include|\s+[0-9]+ \|)' \
  | tee -a "${LOG}"
STATUS=${PIPESTATUS[0]}

echo -e "\n# exit status: ${STATUS}\n# finished:    $(date -u +%Y%m%dT%H%M%SZ)" | tee -a "${LOG}"
rsync -az "${HOST}:${REMOTE}/out/" out/ 2>/dev/null
echo "log: ${LOG}"
exit ${STATUS}
