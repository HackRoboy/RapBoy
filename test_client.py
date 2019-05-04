from RoboyClient import RoboyClient

server = "192.168.0.105"
username = "roboy"
password = "roboy2016"

def print_stream(stream):

    for line in stream.readlines():
        print(line)

if __name__ == "__main__":

    cli = RoboyClient(server, username, password)
    cli.send_file("RoboyClient.py", "RoboyClient.py")
    (stdin, stdout, stderr) = cli.run_command("ls")
    #(stdin, stdout, stderr) = cli.run_command("mkdir test")
    #print_stream(stdin)
    print_stream(stdout)
    print_stream(stderr)
    cli.close()

