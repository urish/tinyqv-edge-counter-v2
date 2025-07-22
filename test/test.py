# SPDX-FileCopyrightText: © 2025 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

from tqv import TinyQV

REG_RESET = 0x00
REG_INC = 0x01
REG_VALUE = 0x02
REG_CFG = 0x03
REG_PINS = 0x04

EDGE_NONE = 0
EDGE_RISING = 1
EDGE_FALLING = 2

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 100 ns (10 MHz)
    clock = Clock(dut.clk, 100, units="ns")
    cocotb.start_soon(clock.start())

    # Interact with your design's registers through this TinyQV class.
    # This will allow the same test to be run when your design is integrated
    # with TinyQV - the implementation of this class will be replaces with a
    # different version that uses Risc-V instructions instead of the SPI 
    # interface to read and write the registers.
    tqv = TinyQV(dut)

    # Reset, always start the test by resetting TinyQV
    await tqv.reset()

    dut._log.info("Test counter manipulation")
    await tqv.write_reg(REG_RESET, 0)
    await tqv.write_reg(REG_INC, 0)
    await tqv.write_reg(REG_INC, 0)
    await tqv.write_reg(REG_INC, 0)
    assert await tqv.read_reg(REG_VALUE) == 3

    dut._log.info("Test 7-segment output")
    assert dut.uo_out.value == 0b01001111  # 3 encoded for seven segment display

    dut._log.info("Test rising edge detection")
    await tqv.write_reg(REG_CFG, EDGE_RISING)
    await tqv.write_reg(REG_RESET, 0)
    dut.ui_in.value = 0x01
    # Wait for two clock cycles to see the output values, because ui_in is synchronized over two clocks,
    # and a further clock is required for the output to propagate.
    await ClockCycles(dut.clk, 3)
    # Wait for extra clock cycles to make sure we don't double count the edge
    await ClockCycles(dut.clk, 10)
    value = await tqv.read_reg(REG_VALUE)
    assert value == 1

    # Generate a falling edge
    dut.ui_in.value = 0x00
    await ClockCycles(dut.clk, 3)
    await ClockCycles(dut.clk, 10)
    value = await tqv.read_reg(REG_VALUE)
    assert value == 1

    # Generate a rising edge
    dut.ui_in.value = 0x01
    await ClockCycles(dut.clk, 3)
    await ClockCycles(dut.clk, 10)
    value = await tqv.read_reg(REG_VALUE)
    assert value == 2

    dut._log.info("Test falling edge detection configuration")
    await tqv.write_reg(REG_CFG, EDGE_FALLING)
    await tqv.write_reg(REG_RESET, 0)
    value = await tqv.read_reg(REG_VALUE)
    assert value == 0

    # Generate a falling edge
    dut.ui_in.value = 0x00
    await ClockCycles(dut.clk, 3)
    await ClockCycles(dut.clk, 10)
    value = await tqv.read_reg(REG_VALUE)
    assert value == 1

    # Generate a rising edge
    dut.ui_in.value = 0x01
    await ClockCycles(dut.clk, 3)
    await ClockCycles(dut.clk, 10)
    value = await tqv.read_reg(REG_VALUE)
    assert value == 1

    # Generate another falling edge
    dut.ui_in.value = 0x00
    await ClockCycles(dut.clk, 3)
    await ClockCycles(dut.clk, 10)
    value = await tqv.read_reg(REG_VALUE)
    assert value == 2

    # Test 7-segment output
    assert dut.uo_out.value == 0b01011011  # 2 encoded for seven segment display
