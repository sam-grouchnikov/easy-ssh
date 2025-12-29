import paramiko
import time


class SSHManager:
    def __init__(self, host, user, password=None, port=22):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.client = None
        self.channel = None
    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            print(f"Connecting to {self.host}...")
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                timeout=10
            )

            # --- START THE SHELL ---
            self.channel = self.client.invoke_shell()

            # Wait a moment for the initial login banner/prompt to load
            time.sleep(1)
            if self.channel.recv_ready():
                self.channel.recv(9999).decode('utf-8')  # Clear the initial banner

            return True, "Success"
        except Exception as e:
            return False, str(e)

    def is_active(self):
        """Passive check to see if the transport and channel are alive."""
        if self.client and self.client.get_transport():
            return self.client.get_transport().is_active()
        return False

    def stream_command(self, command):
        """Yields cleaned data by stripping echo and the trailing prompt without Regex."""
        # 1. Clear the buffer of any old data
        while self.channel.recv_ready():
            self.channel.recv(4096)

        # 2. Send command
        self.channel.send(command + "\n")

        command_echo_found = False

        while True:
            if self.channel.recv_ready():
                chunk = self.channel.recv(4096).decode('utf-8', errors='replace')

                # --- STEP 1: STRIP ECHO ---
                if not command_echo_found:
                    lines = chunk.splitlines(keepends=True)
                    if lines:
                        # Check if the first line contains our command
                        if command.strip() in lines[0]:
                            # Join everything EXCEPT the first line back together
                            chunk = "".join(lines[1:])
                            command_echo_found = True

                # --- STEP 2: STRIP PROMPT ---
                temp_chunk = chunk.rstrip()
                if temp_chunk.endswith(("$", "#", ">")):
                    # Find the last newline to isolate the prompt line
                    last_newline_idx = chunk.rfind('\n')

                    if last_newline_idx != -1:
                        # Extract the content before the last line and check if that last line looks like a prompt
                        possible_prompt = chunk[last_newline_idx:].strip()
                        if possible_prompt.endswith(("$", "#", ">")):
                            yield chunk[:last_newline_idx + 1]
                            break
                    else:
                        # If there is no newline, the whole chunk might just be the prompt
                        if temp_chunk in ("$", "#", ">") or "@" in temp_chunk:
                            break

                yield chunk

            if self.channel.exit_status_ready():
                # Final check for remaining data
                time.sleep(0.1)
                if not self.channel.recv_ready():
                    break

            time.sleep(0.01)

    def send_interrupt(self):
        """Sends Ctrl+C (\x03) to the shell channel."""
        if self.channel and not self.channel.closed:
            # \x03 is the ASCII character for Ctrl+C
            self.channel.send('\x03')
            print("Sent Ctrl+C to remote server.")



    def close(self):
        if self.channel:
            self.channel.close()
        if self.client:
            self.client.close()

