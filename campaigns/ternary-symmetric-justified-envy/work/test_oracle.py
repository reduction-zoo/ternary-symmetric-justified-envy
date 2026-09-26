from check import solve_source,valid_source,solve_target,valid_target


def test_hand_cases():
    triangle = {"vertices":3,"edges":[[0,1],[0,2],[1,2]]}
    assert valid_source(triangle,{"triples":[[0,1,2]]})
    path = {"vertices":3,"edges":[[0,1],[1,2]]}
    assert solve_source(path) == {"status":"NO-SOLUTION"}
    neutral = {"values":[[0,0,0],[0,0,0],[0,0,0]]}
    assert valid_target(neutral,{"triples":[[0,1,2]]})
    assert not valid_target(neutral,{"triples":[[0,0,2]]})
    assert solve_target({"values":[[0,0],[0,0]]}) == {"status":"NO-SOLUTION"}
    values = [[0]*6 for _ in range(6)]
    for v in (4,5):
        values[0][v] = values[v][0] = 2
    assert not valid_target({"values":values},{"triples":[[0,1,2],[3,4,5]]})


if __name__ == "__main__":
    test_hand_cases()
