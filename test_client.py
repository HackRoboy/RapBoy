from RoboyClient import RoboyClient

server = "192.168.0.105"
username = "roboy"
password = "Roboy2016"

def print_stream(stream):

    for line in stream.readlines():
        print(line, end="")

if __name__ == "__main__":

    cli = RoboyClient(server, username, password)
    cli.send_file("final.wav", "rapboy/final.wav")
    (stdin, stdout, stderr) = cli.run_command("ls")
    #(stdin, stdout, stderr) = cli.run_command("mkdir test")
    #print_stream(stdin)
    #(stdin, stdout, stderr) = cli.run_command("mpv ./rapboy/final.wav")
    print_stream(stdout)
    print_stream(stderr)
    cli.close()

