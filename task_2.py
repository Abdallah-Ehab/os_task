def sort(arr):
    return sorted(arr)

def FCFS(requests, head):
    seek_time = 0
    print(f"Order: {head}", end=" ")
    for r in requests:
        seek_time += abs(r - head)
        head = r
        print(f"-> {r}", end=" ")
    print(f"\nTotal Seek Time = {seek_time}")

def SCAN(requests, head, max_cylinder):
    seek_time = 0
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    left = sort(left)
    right = sort(right)

    print(f"Order: {head}", end=" ")

    # Move right
    for r in right:
        seek_time += abs(r - head)
        head = r
        print(f"-> {r}", end=" ")

    # Move to end if not already
    if head != max_cylinder - 1:
        seek_time += abs((max_cylinder - 1) - head)
        head = max_cylinder - 1
        print(f"-> {head}", end=" ")

    # Move left
    for r in reversed(left):
        seek_time += abs(r - head)
        head = r
        print(f"-> {r}", end=" ")

    print(f"\nTotal Seek Time = {seek_time}")

def C_SCAN(requests, head, max_cylinder):
    seek_time = 0
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    left = sort(left)
    right = sort(right)

    print(f"Order: {head}", end=" ")

    # Move right
    for r in right:
        seek_time += abs(r - head)
        head = r
        print(f"-> {r}", end=" ")

    # Jump to start
    if head != max_cylinder - 1:
        seek_time += abs((max_cylinder - 1) - head)
        print(f"-> {max_cylinder - 1}", end=" ")
        seek_time += (max_cylinder - 1)
        head = 0
        print(f"-> {head}", end=" ")

    # Continue right from start
    for r in left:
        seek_time += abs(r - head)
        head = r
        print(f"-> {r}", end=" ")

    print(f"\nTotal Seek Time = {seek_time}")

def main():
    while True:
        print("\n=============================")
        print("Disk Scheduling Simulator")
        print("=============================")

        num_cylinders = int(input("Enter number of cylinders: "))
        queue_size = int(input("Enter queue size: "))
        requests = list(map(int, input("Enter the queue (space-separated): ").split()))
        head = int(input("Enter initial head position: "))
        algo = input("Enter algorithm (FCFS / SCAN / C-SCAN): ").strip().upper()

        print("\n--- Disk Scheduling Result ---")
        if algo == "FCFS":
            FCFS(requests, head)
        elif algo == "SCAN":
            SCAN(requests, head, num_cylinders)
        elif algo == "C-SCAN":
            C_SCAN(requests, head, num_cylinders)
        else:
            print("Invalid algorithm type.")

        again = input("\nDo you want to run another simulation? (y/n): ").strip().lower()
        if again != 'y':
            print("Exiting... Goodbye!")
            break

if __name__ == "__main__":
    main()
