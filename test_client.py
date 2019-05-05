from RoboyClient import RoboyClient
import time
remote_audio_path = "rapboy/final.wav"


#source ~/workspace/cognition_ws/devel/setup.bash;
#rosservice call /roboy/cognition/face/emotion "emotion: \'img:https://i.imgur.com/wblSb5Y.png\'";


dance_command = """
                docker exec hungry_fermi bash -c 'source ~/melodic_ws/devel/setup.bash; 
                export ROS_IP=192.168.0.105;
                rostopic pub /roboy/control/matrix/leds/mode/simple std_msgs/Int32 "data: 1";  
                '"""

ACTIVATE_FLAG = True
#ACTIVATE_FLAG = False

def print_stream(stream):

    for line in stream.readlines():
        print(line, end="")

def make_roboy_dance(bytes_sent, bytes_total):

    #print(bytes_sent / bytes_total * 100, "/100",)
    if bytes_sent == bytes_total:
        print("File transfer finished.")
        if ACTIVATE_FLAG:
            cli = RoboyClient()
            (stdin, stdout, stderr) = cli.run_command(dance_command)
            (stdin, stdout, stderr) = cli.run_command("mpv " + remote_audio_path)
            print_stream(stdout)
            print_stream(stderr)
            cli.close()
"""
def move_command(angle):

    return "rostopic pub /sphere_head_axis0/sphere_head_axis0/targettd_msgs/Float32 \"data: {}\" ".format(angle)


def move_head(times=2):

    for _ in range(times):
        cli = RoboyClient()
        cli.run_command(move_command(0.5))
        time.sleep(1)
        cli.close()
        print("sent")
        cli = RoboyClient()
        cli.run_command(move_command(-0.5))
        cli.close()
"""
if __name__ == "__main__":

    cli = RoboyClient()
    cli.send_file("final.wav", remote_audio_path, callback=make_roboy_dance)
    cli.close()