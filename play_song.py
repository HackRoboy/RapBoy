from RoboyClient import RoboyClient

def print_stream(stream):

    for line in stream.readlines():
        print(line, end="")

cli = RoboyClient()

(stdin, stdout, stderr) = cli.run_command("ls ~/rapboy")
print_stream(stdout)
while(True):
    print("Which song to play?")
    song = input()
    cli.run_command("mpv ~/rapboy/" + str(song))

