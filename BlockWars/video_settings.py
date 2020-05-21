SIZE, VOLUME, FULLSCREEN, GRAPHICS, FPS_GLOBAL = None, None, None, None, None


def video_settings_init(size, volume, fullscreen, graphics, FPS):
    global SIZE, VOLUME, FULLSCREEN, GRAPHICS, FPS_GLOBAL
    SIZE, VOLUME, FULLSCREEN, GRAPHICS, FPS_GLOBAL = size, volume, fullscreen, graphics, FPS


def get_video_settings():
    return SIZE, VOLUME, FULLSCREEN, GRAPHICS, FPS_GLOBAL
