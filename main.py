import time as t

start = t.time()

N_ITEMS = None

# Data preparation
items = []
with open("data/knapsack.lst") as datafile:
    first_line = True
    for line in datafile:
        if not first_line:  # Discard first line
            new_line = line.split("\t")
            new_line = [new_line[0], float(new_line[1]), float(new_line[2])]
            ratio = new_line[2] / new_line[1]  # Compute value/size ratio
            new_line.append(ratio.__round__(3))
            items.append(tuple(new_line))
        else:
            first_line = False

# Use less items for testing
if N_ITEMS is not None:
    items = items[0:N_ITEMS]

# Sort data by value/size ratio in ascending order. This will cause all items with low value/size ratio to be
# evaluated first and the algorithm will discard them immediately. This lowers the runtime from 0.4 s to 0.02 s
items.sort(key=lambda tup: tup[3])


# Function to compute the space required and value of an item placement
def compute_space_and_value(placement):
    global items, MAX_SIZE
    required_space = 0
    current_value = 0
    # For each item in the bag, add its value and size
    for i in range(len(placement)):
        if placement[i] == "1":
            required_space += items[i][1]
            current_value += items[i][2]
    return required_space, current_value


# Function to compute the upper bound of the placement
def compute_bound(placement, occupied_space, total_value):
    global items, MAX_SIZE
    available_items = items
    available_items = available_items[placement.find("X"):]  # Remove used items from available items
    # available_items.sort(key=lambda tup: tup[3])  # Sort available items, ascending
    current_value = total_value
    available_space = MAX_SIZE - occupied_space

    while available_space > 0 and len(available_items) > 0:
        curr_item = available_items.pop()  # Pop available item with largest value/size ratio
        if curr_item[1] < available_space:  # If item fits in knapsack
            available_space -= curr_item[1]  # Take available space
            current_value += curr_item[2]  # Add value to total
        else:
            # Add item value multiplied by teh fraction of available space over item space ("cutting" the item)
            current_value += curr_item[2] * (available_space / curr_item[1])
            available_space = 0
    return current_value


MAX_SIZE = 342  # Size of the knapsack
item_placement = "X" * len(items)  # 0: out, 1: in, X: undecided
best_placement = ""
best_value = 0
stack = [item_placement]
while len(stack) > 0:
    current_placement = stack.pop()
    space, value = compute_space_and_value(current_placement)
    if space > MAX_SIZE:  # Discard if items don't fit
        continue
    bound = compute_bound(current_placement, space, value)
    if bound < best_value:  # Discard if bound is lower than best value
        continue
    if "X" in current_placement:  # If not finished, append next problem
        next_x = current_placement.find("X")
        stack.append(f"{current_placement[:next_x]}1{current_placement[next_x + 1:]}")
        stack.append(f"{current_placement[:next_x]}0{current_placement[next_x + 1:]}")
    elif value > best_value:  # If it's the best placement, save it
        best_value = value
        best_placement = current_placement

best_space, best_value = compute_space_and_value(best_placement)
print(f"Best placement: {best_placement}",
      f"Items:          {best_placement.count('1')}",
      f"Combined size:  {best_space.__round__(1)}",
      f"Combined value: {best_value.__round__(1)}",
      sep="\n")

end = t.time()

print(f"{(end - start).__round__(5)}s")

# Output (best placement in different order due to items being sorted before running the branch & bound):
# Best placement: 0000000000000000000000000000000000000000000000000000000000000000000000000000000101111111111111111111
# Items:          20
# Combined size:  341.8
# Combined value: 3000.8
# 0.01762s
