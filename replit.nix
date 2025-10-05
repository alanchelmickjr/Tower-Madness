{ pkgs }: {
  deps = [
    pkgs.python39
    pkgs.python39Packages.pygame
    pkgs.python39Packages.pip
    pkgs.SDL2
    pkgs.SDL2_mixer
    pkgs.SDL2_image
    pkgs.SDL2_ttf
    pkgs.xvfb-run
  ];
  env = {
    PYGAME_HIDE_SUPPORT_PROMPT = "1";
    SDL_VIDEODRIVER = "x11";
    DISPLAY = ":0";
  };
}