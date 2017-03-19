# Chauffeur

The self-driving Mate delivery robot.

## Build

```shell
catkin_make
```

## Run

The "config file" for the robot is in `src/chauffeur/chauffeur.launch`. Edit it
to your liking and launch it with `roslaunch chauffeur chauffeur.launch`.

## Environment Setup

You will have a bunch of USB serial devices attached to your robot. You'll want
them to have static names, regardless of which order the kernel decides to
initialize them in. See
http://hintshop.ludvig.co.nz/show/persistent-names-usb-serial-devices/ for
a tutorial for how to create udev rules to do this.

