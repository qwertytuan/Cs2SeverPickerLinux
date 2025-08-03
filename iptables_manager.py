import subprocess


# IPtables logic for firewalls
def block_ips_for_servers(server_list):
    """
    Blocks all unique IP addresses from a list of server info lists
    using a single pkexec prompt.

    Args:
        server_list (list): A list of lists, where each inner list contains
                            server info and the IP list is at index 2.
    """
    # Use a set to collect all unique IP addresses from all servers.
    # Each 'server' is a list, and the IPs are in server[2].
    all_unique_ips = set()
    for server_info in server_list:
        # Check if the list is long enough and the third element is a list
        if len(server_info) > 2 and isinstance(server_info[2], list):
            for ip in server_info[2]:
                all_unique_ips.add(ip)

    if not all_unique_ips:
        print("No IP addresses found to block.")
        return

    # Convert the set to a list for command generation
    ip_list = list(all_unique_ips)

    # Create a single command string with all iptables commands
    commands = [f"iptables -A INPUT -s {ip} -j DROP" for ip in ip_list]
    full_command = "; ".join(commands)

    # Wrap the commands in pkexec to run them with root privileges
    try:
        print(f"Preparing to block {len(ip_list)} unique IP addresses.")
        print(f"Executing command: pkexec /bin/bash -c '{full_command}'")
        subprocess.run(
            ['pkexec', '/bin/bash', '-c', full_command],
            check=True,
            capture_output=True,
            text=True
        )
        print("Successfully blocked the following IP addresses:")
        for ip in sorted(ip_list): # Sorted for cleaner output
            print(f"- {ip}")
    except subprocess.CalledProcessError as e:
        print("Failed to execute iptables commands.")
        print(f"Stderr: {e.stderr}")
    except FileNotFoundError:
        print("Error: 'pkexec' not found. Please ensure PolicyKit is installed.")

def unblock_ips_for_servers(server_list):
    """
    Unblocks all unique IP addresses from a list of server info lists
    using a single pkexec prompt.

    Args:
        server_list (list): A list of lists with IPs at index 2.
    """
    # Collect all unique IPs, same as in the block function
    all_unique_ips = set()
    for server_info in server_list:
        if len(server_info) > 2 and isinstance(server_info[2], list):
            for ip in server_info[2]:
                all_unique_ips.add(ip)

    if not all_unique_ips:
        print("No IP addresses found to unblock.")
        return

    ip_list = list(all_unique_ips)

    # Create a command string to delete the blocking rules
    commands = [f"iptables -D INPUT -s {ip} -j DROP" for ip in ip_list]
    full_command = "; ".join(commands)

    # Wrap the commands in pkexec
    try:
        print(f"Preparing to unblock {len(ip_list)} unique IP addresses.")
        print(f"Executing command: pkexec /bin/bash -c '{full_command}'")
        subprocess.run(
            ['pkexec', '/bin/bash', '-c', full_command],
            check=True,
            capture_output=True,
            text=True
        )
        print("Successfully unblocked the following IP addresses:")
        for ip in sorted(ip_list):
            print(f"- {ip}")
    except subprocess.CalledProcessError as e:
        print("Could not unblock all IPs. This may be because a rule did not exist.")
        print(f"Stderr: {e.stderr}")
    except FileNotFoundError:
        print("Error: 'pkexec' not found. Please ensure PolicyKit is installed.")

# --- Example Usage ---
if __name__ == '__main__':
    # The server data array you provided
    server_data = [
        ['ams', 'Amsterdam (Netherlands)', ['155.133.248.36', '155.133.248.37', '155.133.248.40', '155.133.248.41']],
        ['atl', 'Atlanta (Georgia)', ['162.254.199.166', '162.254.199.170', '162.254.199.173', '162.254.199.178', '162.254.199.179', '162.254.199.180']],
        ['dfw', 'Dallas (Texas)', ['162.254.194.37', '162.254.194.38', '162.254.194.39', '162.254.194.53', '162.254.194.54', '162.254.194.55']],
        ['dxb', 'Dubai (United Arab Emirates)', ['185.25.183.163', '185.25.183.179']],
        ['eze', 'Buenos Aires (Argentina)', ['155.133.255.98', '155.133.255.99', '155.133.255.162', '155.133.255.163']]
    ]

    # Block all IPs from the server data
    print("--- Blocking all server IPs ---")
    block_ips_for_servers(server_data)

    input("\nPress Enter to unblock all IPs...")

    # Unblock all IPs
    print("\n--- Unblocking all server IPs ---")
    unblock_ips_for_servers(server_data)
