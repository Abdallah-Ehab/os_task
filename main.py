class MemoryAllocator:
    def __init__(self, size):
        self.size = size
        self.memory = [{"start": 0, "end": size - 1, "process": None}]

    def request_memory(self, process, size, strategy):
        free_blocks = [b for b in self.memory if b["process"] is None]
        if strategy.upper() == "W":
            free_blocks.sort(key=lambda x: x["end"] - x["start"], reverse=True)
        else:
            print("Only worst-fit (W) strategy is supported.")
            return

        for block in free_blocks:
            block_size = block["end"] - block["start"] + 1
            if block_size >= size:
                new_block = {"start": block["start"], "end": block["start"] + size - 1, "process": process}
                block["start"] += size
                if block["start"] > block["end"]:
                    self.memory.remove(block)
                self.memory.append(new_block)
                self.memory.sort(key=lambda x: x["start"])
                print(f"Memory allocated to process {process}")
                return

        print("Not enough memory available.")

    def release_memory(self, process):
        for block in self.memory:
            if block["process"] == process:
                block["process"] = None
                print(f"Memory released from process {process}")
                return
        print(f"Process {process} not found.")

    def compact_memory(self):
        used = [b for b in self.memory if b["process"] is not None]
        free_space = sum(b["end"] - b["start"] + 1 for b in self.memory if b["process"] is None)

        self.memory = []
        current = 0
        for b in used:
            size = b["end"] - b["start"] + 1
            self.memory.append({"start": current, "end": current + size - 1, "process": b["process"]})
            current += size

        if free_space > 0:
            self.memory.append({"start": current, "end": current + free_space - 1, "process": None})

        print("Memory compacted.")

    def report_status(self):
        for b in self.memory:
            if b["process"] is None:
                print(f"Addresses [{b['start']}:{b['end']}] Unused")
            else:
                print(f"Addresses [{b['start']}:{b['end']}] Process {b['process']}")

    def run(self):
        while True:
            command = input("allocator> ").strip()
            if not command:
                continue

            parts = command.strip().split()
            cmd = parts[0].upper()

            if cmd == "RQ" and len(parts) == 4:
                _, process, size, strategy = parts
                self.request_memory(process, int(size), strategy)
            elif cmd == "RL" and len(parts) == 2:
                _, process = parts
                self.release_memory(process)
            elif cmd == "C":
                self.compact_memory()
            elif cmd == "STAT":
                self.report_status()
            elif cmd == "X":
                print("Exiting program.")
                break
            else:
                print("Invalid command.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Please run the program like this: python allocator.py <memory_size>")
        sys.exit()

    memory_size = int(sys.argv[1])
    allocator = MemoryAllocator(memory_size)
    allocator.run()
