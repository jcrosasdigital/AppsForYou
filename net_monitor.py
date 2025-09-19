import os
import sys
import time
import datetime
import psutil

try:
    import msvcrt
except ImportError:
    sys.exit("Error: This script currently only supports Windows for live input.")

def get_connections():
    connections = []
    for conn in psutil.net_connections(kind='tcp'):
        if conn.status == 'ESTABLISHED':
            process_name = 'N/A'
            pid = conn.pid
            if pid:
                try:
                    p = psutil.Process(pid)
                    process_name = p.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
            connections.append({
                "process": process_name,
                "pid": pid,
                "local": f"{conn.laddr.ip}:{conn.laddr.port}",
                "remote": remote_addr,
            })
    return sorted(connections, key=lambda x: (x['process'].lower(), x['pid'] if x['pid'] is not None else -1))

def display_ui(connections, user_input, message=""):
    os.system('cls')
    print(f"--- Live TCP Connections by Jc Rosas ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")
    print("Run as Admin to kill processes. Type and press Enter. Updates every 10s.")
    print("")
    print(f"{ '#':<4} {'Process':<30} {'PID':<10} {'Local Address':<25} {'Remote Address':<25}")
    print("="*95)
    
    if not connections:
        print("No established connections found.")
    else:
        for i, conn in enumerate(connections):
            print(f"{i+1:<4} {conn['process']:<30} {str(conn['pid']):<10} {conn['local']:<25} {conn['remote']:<25}")
    
    print("-" * 95)
    if message:
        print(f"Status: {message}")
        print("-" * 95)

    sys.stdout.write(f"Enter # to kill, (r)efresh, (q)uit: {user_input}")
    sys.stdout.flush()

def terminate_process(pid):
    if pid is None:
        return "Cannot terminate: process has no PID."
    try:
        p = psutil.Process(pid)
        p_name = p.name()
        p.terminate()
        return f"Termination signal sent to {p_name} (PID: {pid})."
    except psutil.NoSuchProcess:
        return f"Error: Process with PID {pid} not found."
    except psutil.AccessDenied:
        return f"Error: Access denied for PID {pid}. Try running as Admin."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def process_command(command, connections):
    action = command.lower().strip()
    if action == 'q':
        return 'quit'
    if action == 'r':
        return "Refreshing..."
    if action.isdigit():
        try:
            choice = int(action) - 1
            if 0 <= choice < len(connections):
                pid_to_kill = connections[choice]['pid']
                return terminate_process(pid_to_kill)
            else:
                return "Invalid number."
        except ValueError:
            return "Invalid input."
    return "Invalid command."

def main():
    last_refresh = 0
    user_input = ""
    connections = []
    status_message = ""

    while True:
        if time.time() - last_refresh > 10:
            last_refresh = time.time()
            connections = get_connections()
            display_ui(connections, user_input, status_message)
            status_message = ""

        if msvcrt.kbhit():
            char = msvcrt.getch()

            if char == b'\r':
                result = process_command(user_input, connections)
                if result == 'quit':
                    break
                status_message = result
                user_input = ""
                last_refresh = 0
                continue 
            elif char == b'\x08':
                user_input = user_input[:-1]
            else:
                try:
                    user_input += char.decode('utf-8')
                except UnicodeDecodeError:
                    pass
            
            display_ui(connections, user_input, status_message)

        time.sleep(0.01)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting NetMonitor.")
