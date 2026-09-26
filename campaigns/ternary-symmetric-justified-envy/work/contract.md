# Prepared contract

Source input is a simple undirected graph `{"vertices": n, "edges": [[u,v],...]}`, with each edge ordered `u<v`. A positive output `{"triples":[[u,v,w],...]}` partitions all vertices into triples and each triple induces a triangle. Otherwise output `{"status":"NO-SOLUTION"}`.

Target input is `{"values":matrix}` with a symmetric matrix of pair values in `{0,1,2}` and zero diagonal. A positive output partitions all agents into triples. An agent `i` in its present triple justifiably envies replacing `j` in another triple if its sum of values for the two staying agents strictly exceeds its current pair-value sum and both staying agents strictly value `i` above `j`. A valid output has no such move; `NO-SOLUTION` is valid exactly if no valid partition exists. The diagonal is a zero placeholder, as only pair values are used.

`algorithm.py` reads source JSON from stdin and emits legal target JSON. `algorithm.py --extract` reads `{"source":source,"target_solution":output}` and emits a valid source output. Both commands are deterministic, polynomial time, independent subprocesses. Errors exit nonzero; diagnostics go to stderr. Recovery must handle every valid target output.
