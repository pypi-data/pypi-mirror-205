# Utils for GH Cli
import dataclasses
import json
import os
import subprocess
from typing import Union, List, Tuple

from pbsrollout.internal.utils import clean_stderr, print_error_body


def does_gh_cli_exist() -> bool:
    try:
        ret = subprocess.run(["gh", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
        return ret.stdout is not None and 'github.com' in ret.stdout
    except Exception:
        return False


# support filtering by one or multiple hashs
# return a list of (author, pr title, hash)
# only return open PR! Add `-s all` to return all PR
def get_pr_titles_and_author_from_commit_hash(hash: Union[str, List[str]]) -> List[Tuple[str, str, str]]:
    def get_name(e):
        name = e['name']
        return name if name != '' else e['login']

    if isinstance(hash, str):
        cmd = f"gh pr list -S {hash} --repo publica-project/platform --json author,title"
    else:
        cmd = 'gh pr list --repo=publica-project/platform --json=author,commits,title --search="sort:updated-desc" --limit=20'

    ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5, shell=True)
    ret.stderr = clean_stderr(ret.stderr)
    if ret.returncode != 0 or ret.stderr != "":
        print_error_body(f"ERROR:\n\ncmd:\n{cmd}\nstdout:\n{ret.stdout}\nstderr:\n{ret.stderr}")
        return []

    ret_json = json.loads(ret.stdout)
    if len(ret_json) == 0:
        return []
    if isinstance(hash, str):
        return [(get_name(ret_json[0]['author']), ret_json[0]['title'], hash)]
    else:
        out = []
        # filter to find commit hash
        for e in ret_json:
            commits = e['commits']
            hash_found = False
            for c in commits:
                if hash_found:
                    break
                commit_hash: str = c['oid']
                for h in hash:
                    if commit_hash.startswith(h):
                        out.append((get_name(e['author']), e['title'], h))
                        hash_found = True
                        break
        return out
