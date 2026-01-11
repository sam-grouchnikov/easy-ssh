import paramiko
import time

from PyQt6.QtCore import pyqtSignal, QThread


class SSHManager:
    def __init__(self, host, user, port, password=None):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.client = None
        self.channel = None

    def connect(self):
        print("Connecting...")
        print("Host: " + self.host)
        print("User: " + self.user)
        print("Password: " + self.password)
        print("Port: " + str(self.port))
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.host, port=self.port,
                username=self.user, password=self.password, timeout=10
            )
            self.channel = self.client.invoke_shell()
            time.sleep(1)
            if self.channel.recv_ready():
                self.channel.recv(9999)
            return True, "Successfully connected"
        except Exception as e:
            return False, str(e)

    def is_active(self):
        if self.client and self.client.get_transport():
            return self.client.get_transport().is_active()
        return False

    def stream_command(self, command):
        """Yields cleaned data by stripping echo and the trailing prompt."""
        if not self.channel: return

        # 1. Clear buffer
        while self.channel.recv_ready():
            self.channel.recv(4096)

        self.channel.send(command + "\n")
        echo_stripped = False

        while True:
            if self.channel.recv_ready():
                chunk = self.channel.recv(4096).decode('utf-8', errors='replace')

                # Strip Echo (First line)
                if not echo_stripped:
                    lines = chunk.splitlines(keepends=True)
                    if lines and command.strip() in lines[0]:
                        chunk = "".join(lines[1:])
                    echo_stripped = True

                # Strip Prompt and Break
                temp_chunk = chunk.rstrip()
                if temp_chunk.endswith(("$", "#", ">")):
                    last_nl = chunk.rfind('\n')
                    if command.startswith("cd"):
                        if chunk == "":
                            yield "Changed directory successfully"
                        else:
                            yield
                    if last_nl != -1:
                        # Yield everything up to the prompt line, then stop
                        yield chunk[:last_nl].rstrip()
                        break
                    else:
                        # The whole chunk is likely just the prompt
                        break

                yield chunk

            if self.channel.exit_status_ready():
                break
            time.sleep(0.01)


    def get_pwd_silently(self):
        """Fetches directory using a separate exec session to stay truly silent."""
        if not self.client:  # The paramiko.SSHClient object
            return ""

        try:
            # exec_command creates a brand new, temporary channel
            # that doesn't share stdout with your main interactive shell.
            stdin, stdout, stderr = self.client.exec_command("pwd")

            # Read the output and strip newlines
            path = stdout.read().decode('utf-8').strip()

            if path.startswith('/'):
                return path
            return ""
        except Exception as e:
            print(f"Silent PWD Error: {e}")
            return ""

    def send_interrupt(self):
        if self.channel and not self.channel.closed:
            self.channel.send('\x03')

    def close(self):
        if self.channel: self.channel.close()
        if self.client: self.client.close()


class SSHStreamWorker(QThread):
    # Signal to send new text to the UI
    output_received = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, manager, command):
        super().__init__()
        self.manager = manager
        self.command = command
        self._is_running = True

    def run(self):
        for chunk in self.manager.stream_command(self.command):
            if not self._is_running:
                break
            if chunk:
                self.output_received.emit(chunk)

        self.finished.emit()

    def stop(self):
        self._is_running = False