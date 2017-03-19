# mpu9250_arduino

An Arduino sketch to read out an MPU9250 9DoF sensor and an accompanying ROS driver.

## Hardware Setup

I'm using an Arduino Uno running at 16MHz/3.3V.

## Calibration

The calibration routine in the sketch is commented out. Uncomment it and do the
calibration a few times by doing a figure of eight to exercise the extreme
values on all axes. Then average out the `magbias` values and update the
statically-defined ones in the sketch. For real-world operation, comment out
the calibration routine.

## Code Style

```shell
clang-format -i MPU9250BasicAHRS/* -style='{BasedOnStyle: llvm, ColumnLimit: 0}'
```
