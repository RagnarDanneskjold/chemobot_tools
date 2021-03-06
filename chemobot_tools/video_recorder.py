import cv2
import time
import threading

from _logger import create_logger

SLEEP_TIME = 0.1


class VideoRecorderInUseError(Exception):

    def __init__(self):
        Exception.__init__(self, "Video actively being recorded already")


class VideoCapture(threading.Thread):
    """
    This class query frames as fast a possible for other programs to use
    """
    def __init__(self, device, frame_size=(640, 480)):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interrupted = threading.Lock()
        self.lock = threading.Lock()

        self.logger = create_logger(self.__class__.__name__)

        self.device = device
        self.frame_size = frame_size

        self.open()
        self.start()
        self.wait_until_ready()

    def open(self):
        self.logger.debug('Opening device {} at size {}'.format(self.device, self.frame_size))
        self.video_capture = cv2.VideoCapture(self.device)
        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.frame_size[0])
        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.frame_size[1])

    def close(self):
        self.logger.debug('Closing device and all windows')
        if hasattr(self, "video_capture"):
            self.video_capture.release()

    def __del__(self):
        self.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def stop(self):
        self.interrupted.release()

    def run(self):
        self.interrupted.acquire()
        while self.interrupted.locked():
            ret, frame = self.video_capture.read()
            if ret:
                self.lock.acquire()
                self.frame = frame
                self.lock.release()
        self.close()

    def wait_until_ready(self):
        while not hasattr(self, 'frame'):
            time.sleep(SLEEP_TIME)

    def get_last_frame(self):
        self.lock.acquire()
        frame = self.frame.copy()
        self.lock.release()
        return frame


class VideoRecorder(threading.Thread):

    def __init__(self, device, frame_size=(640, 480)):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interrupted = threading.Lock()
        self.recording = False

        self.logger = create_logger(self.__class__.__name__)

        self.device = device
        self.frame_size = frame_size
        self.video_capture = VideoCapture(self.device, self.frame_size)

        self.init()
        self.start()

    def close(self):
        self.logger.debug('Closing device and all windows')
        self.video_capture.stop()
        self.video_capture.join()
        if hasattr(self, "video_writer"):
            self.video_writer.release()
        cv2.destroyAllWindows()

    def __del__(self):
        self.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def stop(self):
        self.interrupted.release()

    def init(self):
        # starting the window and putting something in it so it is ready to work at descent speed, the first frame is slow to display
        cv2.namedWindow("video")
        frame = self.video_capture.get_last_frame()
        cv2.imshow("video", frame)
        cv2.waitKey(1)

    def run(self):
        self.interrupted.acquire()
        while self.interrupted.locked():
            if self.recording:
                self._record()
                self.recording = False
            else:
                time.sleep(SLEEP_TIME)
        self.close()

    def wait_until_idle(self):
        while self.recording:
            time.sleep(SLEEP_TIME)

    def _record(self):
        start_time = time.time()
        while True:
            start_loop = time.time()

            frame = self.video_capture.get_last_frame()
            self.video_writer.write(frame)

            cv2.imshow("video", frame)
            cv2.waitKey(1)  # needed for the display to work

            # wait the appropriate time to stick with the fps
            dt = time.time() - start_loop
            wait_time = max(self.time_between_frame - dt, 0)
            time.sleep(wait_time)

            elapsed = time.time() - start_time
            if elapsed > self.duration_in_sec:
                self.video_writer.release()
                break

    def record_to_file(self, video_filename, duration_in_sec=60, fps=20):

        if self.recording:
            raise VideoRecorderInUseError

        # creating the writer
        video_format = cv2.cv.CV_FOURCC('D', 'I', 'V', 'X')
        self.video_writer = cv2.VideoWriter(video_filename, video_format, fps, self.frame_size)

        # setting param
        self.duration_in_sec = duration_in_sec
        self.time_between_frame = 1. / fps

        # ready to record
        self.recording = True
