<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## What it does

Edge counter peripheral for TinyQV that counts the number of edges on the `edge_detect` (ui_in[0]) pin.

The lower 4 bits of the counter are displayed on the 7-segment display. The DP is lit when the counter is greater than 0x0F.

## Register map

| Address | Name  | Access | Description                                                         |
|---------|-------|--------|---------------------------------------------------------------------|
| 0x00    | RESET | W      | Resets the counter to 0                                             |
| 0x01    | INC   | W      | Increments the counter by 1                                         |
| 0x02    | VALUE | R/W    | Reads the current value of the counter                              |
| 0x03    | CFG   | R/W    | Edge detection configuration: 0 = disabled, 1 = rising, 2 = falling |

## How to test

1. Set the edge detection configuration in the CFG register.
2. Pulse an edge on the `edge_detect` (ui_in[0]) pin.
3. The counter will increment by 1 for each edge detected.
4. The counter value is displayed on the 7-segment display.

## External hardware

None
