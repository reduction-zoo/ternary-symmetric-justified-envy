import Challenge
open TernarySymmetricJustifiedEnvy
example : sourceWitness ⟨3,[(0,1),(1,2),(0,2)]⟩ [[0,1,2]] = true := by native_decide
example : sourceWitness ⟨3,[(0,1),(1,2)]⟩ [[0,1,2]] = false := by native_decide
example : targetWitness [[0,0,0],[0,0,0],[0,0,0]] [[0,1,2]] = true := by native_decide
