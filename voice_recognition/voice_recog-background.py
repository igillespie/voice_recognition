import speech_recognition as sr
import time
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


        
class VoiceRecognition(Node):

    def __init__(self):
        super().__init__('voice_recognition')
        self.publisher_ = self.create_publisher(String, 'voice_commands', 10)
        #timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        #self.i = 0
        self.start_listening()
        
           
    #def timer_callback(self):
        #msg = String()
        #msg.data = 'Hello World: %d' % self.i
        #self.publisher_.publish(msg)
        #self.get_logger().info('Publishing: "%s"' % msg.data)
        #self.i += 1
        
    def publish_message(self):
        msg = String()
        msg.data = message
        self.get_logger().info('Plugging there to publish: "%s"' % msg.data)
        stop_listening(wait_for_stop=False)
        self.publisher_.publish(msg)
        time.sleep(1.0)
        self.start_listening()
        
        
    def start_listening(self):
        self.m = sr.Microphone()
        self.r = sr.Recognizer()
        with self.m as source:
           self.r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.get_logger().info('We are listening')
        global stop_listening
        stop_listening = self.r.listen_in_background(self.m, callback_google)

        
def callback_sphinx(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    voice_recog.get_logger().info('Sending to Sphinx')
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        global message
        message = recognizer.recognize_sphinx(audio)
        #voice_recog.get_logger().info("Sphinx thinks you said " + message)
        voice_recog.publish_message()
    except sr.UnknownValueError:
        voice_recog.get_logger().info("Sphinx could not understand audio")

    except sr.RequestError as e:
        voice_recog.get_logger().info("Could not request results from Sphinx service; {0}".format(e))
    
def callback_google(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    voice_recog.get_logger().info('Sending to Google')
    
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        global message
        message = recognizer.recognize_google(audio)
        #voice_recog.get_logger().info("Google Speech Recognition thinks you said " + message)
        voice_recog.publish_message()
    except sr.UnknownValueError:
        voice_recog.get_logger().info("Google Speech Recognition could not understand audio")

    except sr.RequestError as e:
        voice_recog.get_logger().info("Could not request results from Google Speech Recognition service; {0}".format(e))
   
        
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
