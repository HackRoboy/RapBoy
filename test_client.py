from RoboyClient import RoboyClient

server = "192.168.0.105"
username = "roboy"
password = "Roboy2016"

def print_stream(stream):

    for line in stream.readlines():
        print(line, end="")

if __name__ == "__main__":

    cli = RoboyClient(server, username, password)
    remote_audio_path = "rapboy/final.wav"
    if cli.send_file("final.wav", remote_audio_path):
        (stdin, stdout, stderr) = cli.run_command("""docker exec hungry_fermi bash -c 'source ~/melodic_ws/devel/setup.bash; 
                   export ROS_IP=192.168.0.105; rostopic pub /roboy/control/matrix/leds/mode/simple std_msgs/Int32 "data: 1"'""")
        print_stream(stdin)
        (stdin, stdout, stderr) = cli.run_command("mpv " + remote_audio_path)
        print_stream(stdout)
        print_stream(stderr)
    cli.close()

    # cli.remove_remote("rapboy/final.wav")
    # cli.send_file("final.wav", "rapboy/final.wav")
    # (stdin, stdout, stderr) = cli.run_command("ls rapboy")
    #(stdin, stdout, stderr) = cli.run_command("""docker exec hungry_fermi bash -c 'source ~/melodic_ws/devel/setup.bash; 
     #   export ROS_IP=192.168.0.105; rostopic pub /roboy/control/matrix/leds/mode/simple std_msgs/Int32 "data: 1"'""")

    #(stdin, stdout, stderr) = cli.run_command("mkdir test")
    #print_stream(stdin)
    #(stdin, stdout, stderr) = cli.run_command("mpv ./rapboy/final.wav")
    # print_stream(stdout)
    # print_stream(stderr)
    # cli.close()

