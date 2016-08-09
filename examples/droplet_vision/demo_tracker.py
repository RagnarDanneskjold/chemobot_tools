import time

import filetools

from chemobot_tools.droplet_tracking.droplet_tracker import process_video
from chemobot_tools.droplet_tracking.pool_workers import PoolDropletTracker, create_default_tracker_config_from_folder


if __name__ == '__main__':

    # sequential
    start_time = time.time()

    dish_info_in = {
        "dish_circle": [320, 235, 180],
        "arena_circle": [320, 235, 150]
    }

    droplet_info = process_video('videos/06/video.avi', dish_info_in=dish_info_in, debug=True, deep_debug=True)

    elapsed = time.time() - start_time
    print 'It took {} seconds to analyse one video'.format(elapsed)

    # parallel
    # start_time = time.time()
    #
    # droptracker = PoolDropletTracker()
    #
    # folder_list = filetools.list_folders('videos')
    # folder_list.sort()
    # for folder in folder_list:
    #     droptracker.add_task(create_default_tracker_config_from_folder(folder))  # need an abspath
    #
    # droptracker.wait_until_idle()
    #
    # elapsed = time.time() - start_time
    # print 'It took {} seconds to analyse {} videos in parallel'.format(elapsed, len(folder_list))
