

import speech_recognition as sr
import time

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Bool

# This code help with speech recognition https://www.geeksforgeeks.org/build-a-virtual-assistant-using-python/?ref=lbp


class VoiceRecognition(Node):

    def __init__(self):
        super().__init__('voice_recognition')
        self.publisher_ = self.create_publisher(String, 'voice_commands', 10)

        self.subscription = self.create_subscription(
            Bool,
            'activation',
            self.activation_callback,
            10)

        self.listen = True
        self.start_listening()

    # def timer_callback(self):
        #msg = String()
        #msg.data = 'Hello World: %d' % self.i
        # self.publisher_.publish(msg)
        #self.get_logger().info('Publishing: "%s"' % msg.data)
        #self.i += 1

    def activation_callback(self, msg):
        self.listen = msg.data
        if self.listen == True:
            #self.get_logger().info('starting up again')
            self.start_listening()
        #else:
            #self.get_logger().info('stopping')

    def publish_message(self):
        msg = String()
        msg.data = message.lower()
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.publisher_.publish(msg)

    def take_command(self):
        r = sr.Recognizer()
        m = sr.Microphone()

        with m as source:
            value = None
            self.get_logger().info('We are listening here')
            # seconds of non-speaking audio before
            # a phrase is considered complete
            r.pause_threshold = 0.7
            #r.adjust_for_ambient_noise(source) 
            audio = r.listen(source,timeout=6,phrase_time_limit=6) #timeout=8,phrase_time_limit=8
            # Now we will be using the try and catch
            # method so that if sound is recognized
            # it is good else we will have exception
            # handling
            if self.listen == True: #this will probably always be True
                try:
                 # recognize speech using Google Speech Recognition
                    self.get_logger().info('Sending to Google')
                    value = r.recognize_google(audio, language='en')
                    self.get_logger().info("You said {}".format(value))

                except sr.UnknownValueError:
                    self.get_logger().info("Oops! Didn't catch that")
                except sr.RequestError as e:
                    self.get_logger().info(
                        "Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

                return value

    def start_listening(self):

        global message
        while(self.listen == True):

            message = self.take_command()
            if message != None:
                self.publish_message()
                self.listen = False #we turn ourselves off after publishing and another node will turn us back on, this way we don't ever listen for something we end up just saying using TTS. We have to do this because the .listen() function block the thread.


def main(args=None):
    rclpy.init(args=args)

    global voice_recog
    voice_recog = VoiceRecognition()

    try:
        rclpy.spin(voice_recog)

    except KeyboardInterrupt:
        pass
    finally:
        voice_recog.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
