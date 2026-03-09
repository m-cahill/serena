#!/usr/bin/env bash
# Prevent pushing to remotes that are not the Serena repository.
# Install: cp scripts/dev/prevent_upstream_push.sh .git/hooks/pre-push && chmod +x .git/hooks/pre-push
#
# This hook receives: $1 = remote name, $2 = URL of remote
# We validate that the push target URL points to m-cahill/serena.

remote_name="$1"
remote_url="$2"

if [[ -z "$remote_url" ]]; then
  echo "ERROR: Could not determine push target URL"
  exit 1
fi

if [[ "$remote_url" != *"m-cahill/serena"* ]]; then
  echo "ERROR: Push target ($remote_name) does not point to m-cahill/serena"
  echo "  URL: $remote_url"
  if [[ "$remote_url" == *"AUTOMATIC1111"* ]] || [[ "$remote_url" == *"stable-diffusion-webui"* ]]; then
    echo "  Hint: You may be pushing to upstream. Serena development must stay in m-cahill/serena."
  fi
  exit 1
fi

exit 0
