from rover import Rover
import datetime
import os

# Create a logs folder if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Function to write logs to a file
def log_command(command, status):
    with open("logs/move_log.txt", "a", encoding="utf-8") as file:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{time}] Command: {command} | {status}\n")

# Create a rover instance
rover = Rover()

# Welcome message
print("🚀 Mars Rover Command Console")
print("Available commands: MOVE, LEFT, RIGHT, STATUS, EXIT")

# Start command loop
while True:
    command = input(">> ").strip().upper()

    if command == "MOVE":
        status = rover.move()  # 👈 now gets the return value
        print(status)
        log_command("MOVE", status)

    elif command == "LEFT":
        status = rover.turn_left()  # 👈 gets the return value
        print(status)
        log_command("LEFT", status)

    elif command == "RIGHT":
        status = rover.turn_right()  # 👈 gets the return value
        print(status)
        log_command("RIGHT", status)

    elif command == "STATUS":
        status = rover.status()
        print(status)
        rover.display_map()
        log_command("STATUS", status)

    elif command == "EXIT":
        print("🛑 Exiting mission control. Goodbye!")
        break

    else:
        print("❌ Unknown command. Please enter MOVE, LEFT, RIGHT, STATUS, or EXIT.")
