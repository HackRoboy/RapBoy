from RoboyClient import RoboyClient

server = "192.168.0.105"
username = "roboy"
password = "Roboy2016"

dance_command = """docker exec hungry_fermi bash -c 'source ~/melodic_ws/devel/setup.bash; 
                export ROS_IP=192.168.0.105; 
                rostopic pub /roboy/control/matrix/leds/mode/simple std_msgs/Int32 "data: 1";
                rosservice call /roboy/cognition/face/emotion "emotion: \'img:https://i.imgur.com/wblSb5Y.png\'"; 
                '"""

ACTIVATE_FLAG = True
#ACTIVATE_FLAG = False

def print_stream(stream):

    for line in stream.readlines():
        print(line, end="")

def make_roboy_dance(bytes_sent, bytes_total):

    print(bytes_sent / bytes_total * 100, "/100",)
    if bytes_sent == bytes_total and ACTIVATE_FLAG:
        cli = RoboyClient(server, username, password)
        (stdin, stdout, stderr) = cli.run_command(dance_command)
        #(stdin, stdout, stderr) = cli.run_command("mpv " + remote_audio_path)
        print_stream(stdout)
        print_stream(stderr)
        cli.close()

if __name__ == "__main__":

    cli = RoboyClient(server, username, password)
    remote_audio_path = "rapboy/final.wav"
    cli.send_file("final.wav", remote_audio_path, callback=make_roboy_dance)
    (stdin, stdout, stderr) = cli.run_command(dance_command)
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

