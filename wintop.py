import psutil
import curses
import time

def display_system_info(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Don't wait for input when calling getch()

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # CPU usage
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Memory usage
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Process header
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)     # High CPU process

    while True:
        stdscr.clear()

        # Get the size of the terminal window
        height, width = stdscr.getmaxyx()

        # CPU Info
        cpu_usage = psutil.cpu_percent(percpu=True)
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(0, 0, "CPU Usage: ")
        stdscr.attroff(curses.color_pair(1))
        for i, usage in enumerate(cpu_usage):
            if i + 1 < height:  # Check if there is enough space
                stdscr.addstr(1 + i, 0, f"Core {i}: {usage}%")

        # Memory Info
        memory = psutil.virtual_memory()
        if 10 < height:  # Check if there is enough space
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(10, 0, f"Memory: {memory.percent}% ({memory.used // (1024 ** 2)} MB used)")
            stdscr.attroff(curses.color_pair(2))

        # Process Info
        processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']))
        processes = sorted(processes, key=lambda p: p.info['cpu_percent'], reverse=True)[:10]

        if 15 < height:  # Check if there is enough space
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(15, 0, "Top Processes:")
            stdscr.attroff(curses.color_pair(3))
            for i, proc in enumerate(processes):
                if 16 + i < height:  # Check if there is enough space
                    color = 4 if proc.info['cpu_percent'] > 50 else 0  # Red for high CPU usage
                    if color:
                        stdscr.attron(curses.color_pair(color))
                    stdscr.addstr(16 + i, 0, f"{proc.info['pid']} - {proc.info['name']} - CPU: {proc.info['cpu_percent']}% - Mem: {proc.info['memory_percent']}%")
                    if color:
                        stdscr.attroff(curses.color_pair(color))

        # Refresh the screen
        stdscr.refresh()

        # Delay for a short time to avoid high CPU usage
        time.sleep(1)

def main():
    curses.wrapper(display_system_info)

if __name__ == "__main__":
    main()
