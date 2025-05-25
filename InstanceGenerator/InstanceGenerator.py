import os
import random

class InstanceGenerator(object):
    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        # Use N and maxBid from config, with defaults if not present
        N = getattr(self.config, 'N', 10)
        max_bid = getattr(self.config, 'maxBid', 10)

        if not os.path.isdir(instancesDirectory):
            os.makedirs(instancesDirectory, exist_ok=True)

        for i in range(numInstances):
            instancePath = os.path.join(instancesDirectory, f'{fileNamePrefix}{N}_{i}.{fileNameExtension}')
            with open(instancePath, 'w') as f:
                f.write(f'N={N};\n')
                f.write('m=[\n')
                for row in range(N):
                    row_data = []
                    for col in range(N):
                        if row == col:
                            row_data.append(0)
                        else:
                            row_data.append(random.randint(0, max_bid))
                    row_str = "  [" + " ".join(str(x) for x in row_data) + "]"
                    if row < N - 1:
                        row_str += ","
                    f.write(row_str + "\n")
                f.write('];\n')
            print(f"Instance written to {instancePath}")
