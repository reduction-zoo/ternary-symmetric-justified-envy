"""Fix triangle-partition source cases before construction."""

import json
import random
from pathlib import Path


def graph(n,edges):
    return {"vertices":n,"edges":sorted(edges)}


def clique(n):
    return [[i,j] for i in range(n) for j in range(i+1,n)]


EDGE_CASES = [
    (graph(0,[]),True),
    (graph(1,[]),False),
    (graph(2,[[0,1]]),False),
    (graph(3,clique(3)),True),
    (graph(3,[[0,1],[1,2]]),False),
    (graph(3,[]),False),
    (graph(6,clique(3)+[[3,4],[3,5],[4,5]]),True),
    (graph(6,clique(6)),True),
    (graph(6,clique(5)),False),
    (graph(6,clique(3)+[[3,4],[4,5]]),False),
    (graph(9,clique(9)),True),
    (graph(9,clique(3)+[[3,4],[3,5],[4,5],[6,7],[6,8],[7,8]]),True),
    (graph(4,clique(4)),False),
    (graph(6,[[0,1],[0,2],[1,2],[2,3],[3,4],[3,5],[4,5]]),True),
]


def random_source(seed):
    rng = random.Random(seed)
    n = rng.choice((3,6,9))
    edges = []
    if seed % 2 == 0:
        for start in range(0,n,3):
            edges += [[start,start+1],[start,start+2],[start+1,start+2]]
        edges += [[u,v] for u in range(n) for v in range(u+1,n)
                  if u//3 != v//3 and rng.randrange(3) == 0]
    else:
        edges = [[u,v] for u in range(n) for v in range(u+1,n) if rng.randrange(5) == 0]
    return graph(n,edges)


def build_cases():
    from check import solve_source
    cases,seen = [],set()

    def add(source,kind,seed=None,expected=None):
        key = json.dumps(source,sort_keys=True,separators=(",",":"))
        if key in seen:
            return False
        answer = solve_source(source)
        if expected is not None and ("triples" in answer) != expected:
            raise AssertionError(f"Hand label disagrees with oracle: {source}")
        seen.add(key)
        case = {"source":source,"kind":kind,"expected":answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for source,expected in EDGE_CASES:
        add(source,"edge",expected=expected)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed),"random",seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases,indent=2)+"\n")
    print(f"Wrote {len(cases)} cases to {path}")
