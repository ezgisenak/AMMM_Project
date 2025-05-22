import os
import random

def generate_instance(N, max_bid=10, file_path="instance.dat"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(f"N = {N};\n\n")
        f.write("m = [\n")
        for i in range(N):
            row = []
            for j in range(N):
                if i == j:
                    row.append(0)
                else:
                    row.append(random.randint(0, max_bid))
            row_str = "  [" + " ".join(str(x) for x in row) + "]"
            if i < N - 1:
                row_str += ","
            f.write(row_str + "\n")
        f.write("];\n")
    print(f"Instance with N={N} written to {file_path}")

# Example usage
N = 45
generate_instance(N, max_bid=10, file_path=f"output/instance{N}_1.dat")
generate_instance(N, max_bid=10, file_path=f"output/instance{N}_2.dat")
generate_instance(N, max_bid=10, file_path=f"output/instance{N}_3.dat")
generate_instance(N, max_bid=10, file_path=f"output/instance{N}_4.dat")
generate_instance(N, max_bid=10, file_path=f"output/instance{N}_5.dat")
