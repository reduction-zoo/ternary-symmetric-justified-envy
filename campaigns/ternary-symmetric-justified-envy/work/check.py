"""Finite exact oracles for triangle partitions and justified envy-free triples."""

import argparse
import json
import random
import subprocess
import sys
from itertools import combinations
from pathlib import Path


def legal_source(source):
    if not isinstance(source,dict) or set(source) != {"vertices","edges"}:
        return False
    n,edges = source["vertices"],source["edges"]
    return (type(n) is int and n >= 0 and isinstance(edges,list)
            and all(isinstance(edge,list) and len(edge) == 2
                    and all(type(v) is int and 0 <= v < n for v in edge)
                    and edge[0] < edge[1] for edge in edges)
            and len({tuple(edge) for edge in edges}) == len(edges))


def legal_target(target):
    if not isinstance(target,dict) or set(target) != {"values"}:
        return False
    rows = target["values"]
    if not isinstance(rows,list):
        return False
    n = len(rows)
    return (all(isinstance(row,list) and len(row) == n
                and all(type(value) is int and value in (0,1,2) for value in row)
                for row in rows)
            and all(rows[i][i] == 0 for i in range(n))
            and all(rows[i][j] == rows[j][i] for i in range(n) for j in range(i+1,n)))


def partitions(vertices):
    if not vertices:
        yield []
        return
    first,*rest = vertices
    for second,third in combinations(rest,2):
        remaining = [v for v in rest if v not in (second,third)]
        for suffix in partitions(remaining):
            yield [[first,second,third]]+suffix


def proper_partition(n,triples):
    return (isinstance(triples,list) and len(triples)*3 == n
            and all(isinstance(group,list) and len(group) == 3
                    and all(type(v) is int and 0 <= v < n for v in group) for group in triples)
            and sorted(v for group in triples for v in group) == list(range(n)))


def direct_triangle(source,triples):
    if not proper_partition(source["vertices"],triples):
        return False
    edges = {tuple(edge) for edge in source["edges"]}
    return all(all(tuple(sorted(pair)) in edges for pair in combinations(group,2))
               for group in triples)


def direct_envy(target,triples):
    values = target["values"]
    if not proper_partition(len(values),triples):
        return False
    own = {v:group for group in triples for v in group}
    for incoming in range(len(values)):
        current = sum(values[incoming][v] for v in own[incoming] if v != incoming)
        for group in triples:
            if incoming in group:
                continue
            for outgoing in group:
                staying = [v for v in group if v != outgoing]
                if (sum(values[incoming][v] for v in staying) > current
                        and all(values[v][incoming] > values[v][outgoing] for v in staying)):
                    return False
    return True


def source_solutions(source,limit=3):
    if not legal_source(source):
        raise ValueError("Illegal triangle-partition graph")
    outputs = []
    if source["vertices"] % 3 == 0:
        for triples in partitions(list(range(source["vertices"]))):
            if direct_triangle(source,triples):
                outputs.append({"triples":triples})
                if len(outputs) == limit:
                    break
    return outputs or [{"status":"NO-SOLUTION"}]


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal ternary symmetric valuations")
    outputs = []
    if len(target["values"]) % 3 == 0:
        for triples in partitions(list(range(len(target["values"])))):
            if direct_envy(target,triples):
                outputs.append({"triples":triples})
                if len(outputs) == limit:
                    break
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_source(source):
    return source_solutions(source,1)[0]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_source(source,output):
    if not legal_source(source) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_source(source) == output
    return set(output) == {"triples"} and direct_triangle(source,output["triples"])


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return set(output) == {"triples"} and direct_envy(target,output["triples"])


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases
    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for source,expected in EDGE_CASES:
        assert ("triples" in solve_source(source)) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        answer = solve_source(source)
        assert ("triples" in answer) == ("triples" in case["expected"])
        assert valid_source(source,answer) and valid_source(source,case["expected"])
    test_hand_cases()
    seen = set()
    for seed in range(100):
        rng = random.Random(seed)
        n = rng.choice((0,3,6,9))
        values = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1,n):
                values[i][j] = values[j][i] = rng.randrange(3)
        target = {"values":values}
        key = json.dumps(target)
        if key in seen:
            continue
        seen.add(key)
        answer = solve_target(target)
        assert valid_target(target,answer)
        if n:
            assert not valid_target(target,{"triples":[[0,0,0]]})
    print(f"Self-test passed: {len(cases)} source graphs and {len(seen)} target valuation instances")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal target: {target}")
        for output in target_solutions(target):
            assert valid_target(target,output)
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
