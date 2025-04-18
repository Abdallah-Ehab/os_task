
class MemoryAllocator:
    def __init__(self, size):
        self.size = size
        self.memory = [{"start": 0, "end": size - 1, "process": None}]  # Initial free block

    def request_memory(self, process, size, strategy):
        free_blocks = [block for block in self.memory if block["process"] is None]
        if strategy == "W":  # Worst fit
            free_blocks.sort(key=lambda x: x["end"] - x["start"], reverse=True)
        else:
            print("Unsupported strategy")
            return

        for block in free_blocks:
            block_size = block["end"] - block["start"] + 1
            if block_size >= size:
                # Allocate memory
                new_block = {"start": block["start"], "end": block["start"] + size - 1, "process": process}
                block["start"] += size
                if block["start"] > block["end"]:  # Remove block if fully allocated
                    self.memory.remove(block)
                self.memory.append(new_block)
                self.memory.sort(key=lambda x: x["start"])
                print(f"Memory allocated to process {process}")
                return

        print("Not enough memory available")

    def release_memory(self, process):
        for block in self.memory:
            if block["process"] == process:
                block["process"] = None
                print(f"Memory released for process {process}")
                return
        print(f"No memory allocated to process {process}")

    def compact_memory(self):
        allocated = [block for block in self.memory if block["process"] is not None]
        free_size = sum(block["end"] - block["start"] + 1 for block in self.memory if block["process"] is None)

        self.memory = []
        current_address = 0
        for block in allocated:
            size = block["end"] - block["start"] + 1
            self.memory.append({"start": current_address, "end": current_address + size - 1, "process": block["process"]})
            current_address += size

        if free_size > 0:
            self.memory.append({"start": current_address, "end": current_address + free_size - 1, "process": None})

        print("Memory compacted")

    def report_status(self):
        for block in self.memory:
            if block["process"] is None:
                print(f"Addresses [{block['start']}:{block['end']}] Unused")
            else:
                print(f"Addresses [{block['start']}:{block['end']}] Process {block['process']}")

    def run(self):
        while True:
            command = input("allocator> ").strip()
            if command.startswith("RQ"):
                _, process, size, strategy = command.split()
                self.request_memory(process, int(size), strategy)
            elif command.startswith("RL"):
                _, process = command.split()
                self.release_memory(process)
            elif command == "C":
                self.compact_memory()
            elif command == "STAT":
                self.report_status()
            elif command == "X":
                print("Exiting...")
                break
            else:
                print("Invalid command")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: allocator <memory_size>")
        sys.exit(1)

    try:
        memory_size = int(sys.argv[1])
        allocator = MemoryAllocator(memory_size)
        allocator.run()
    except ValueError:
        print("Invalid memory size")
        sys.exit(1)