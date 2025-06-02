// ** PLEASE ONLY CHANGE THIS FILE WHERE INDICATED **
// In particular, do not change the names of the input parameters.

int             N = ...;
int m[1..N][1..N] = ...;


// Define here your decision variables and
// any other auxiliary program variables you need.
// You can run an execute block if needed.

// Define decision variables
dvar boolean x[1..N][1..N]; // x[i][j] = 1 means i has priority over j

// Auxiliary variables for cycle prevention (Topological sort values)
dvar int+ order[1..N]; // Order values for members

// Write here the objective function.

maximize 
    // Objective: maximize the total collected bid value from chosen priorities
    sum(i in 1..N, j in 1..N: i != j) x[i][j] * m[i][j];

subject to {

    // Prevent loops: use a topological ordering constraint
    // If i has priority over j, then order[i] < order[j]
    // This ensures that the directed graph is acyclic
    forall(i in 1..N, j in 1..N: i != j)
        order[i] + 1 <= order[j] + (1 - x[i][j]) * N;

    // Optional: ensure no self-prioritization
    forall(i in 1..N)
        x[i][i] == 0;
}

// You can run an execute block if needed.

execute {
  writeln("Selected priority relations (i -> j):");
  for (var i = 1; i <= N; i++) {
    for (var j = 1; j <= N; j++) {
      if (i != j && x[i][j] == 1) {
        writeln(i, " -> ", j);
      }
    }
  }

  writeln("\n=== SOLUTION STATS ===");
  writeln("N = ", N);
  writeln("Objective = ", cplex.getObjValue());
  writeln("MIP Gap = ", cplex.getMIPRelativeGap());
}



