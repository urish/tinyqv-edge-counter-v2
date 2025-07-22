# Copyright (c) 2024 Caio Alonso da Costa
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

def get_bit(value, bit_index):
  temp = value & (1 << bit_index)
  return temp

def set_bit(value, bit_index):
  temp = value | (1 << bit_index)
  return temp

def clear_bit(value, bit_index):
  temp = value & ~(1 << bit_index)
  return temp

def xor_bit(value, bit_index):
  temp = value ^ (1 << bit_index)
  return temp

def pull_cs_high(value):
  temp = set_bit(value, 4)
  return temp

def pull_cs_low(value):
  temp = clear_bit(value, 4)
  return temp

def spi_clk_high(value):
  temp = set_bit(value, 5)
  return temp

def spi_clk_low(value):
  temp = clear_bit(value, 5)
  return temp

def spi_clk_invert(value):
  temp = xor_bit(value, 5)
  return temp

def spi_mosi_high(value):
  temp = set_bit(value, 6)
  return temp

def spi_mosi_low(value):
  temp = clear_bit(value, 6)
  return temp

def spi_miso_read(port):
  return (get_bit (port.value, 3) >> 3)

async def spi_write_cpha0 (clk, port, address, data):

  temp = port.value;
  result = pull_cs_high(temp)
  port.value = result
  await ClockCycles(clk, 10)

  # Pull CS low + Write command bit - bit 7 - MSBIT in first byte
  temp = port.value;
  result = pull_cs_low(temp)
  result2 = spi_mosi_high(result)
  port.value = result2
  await ClockCycles(clk, 10)
  temp = port.value;
  result = spi_clk_invert(temp)
  port.value = result
  await ClockCycles(clk, 10)

  iterator = 0
  while iterator < 3:
    # Don't care - bit 6, bit 5 and bit 4
    temp = port.value;
    result = spi_clk_invert(temp)
    result2 = spi_mosi_low(result)
    port.value = result2
    await ClockCycles(clk, 10)
    temp = port.value;
    result = spi_clk_invert(temp)
    port.value = result
    await ClockCycles(clk, 10)
    iterator += 1

  iterator = 3
  while iterator >= 0:
    # Address[iterator] - bit 3, bit 2, bit 1 and bit 0
    temp = port.value;
    result = spi_clk_invert(temp)
    address_bit = get_bit(address, iterator)
    if (address_bit == 0):
      result2 = spi_mosi_low(result)
    else:
      result2 = spi_mosi_high(result)
    port.value = result2
    await ClockCycles(clk, 10)
    temp = port.value;
    result = spi_clk_invert(temp)
    port.value = result
    await ClockCycles(clk, 10)
    iterator -= 1

  iterator = 7
  while iterator >= 0:
    # Data[iterator]
    temp = port.value;
    result = spi_clk_invert(temp)
    data_bit = get_bit(data, iterator)
    if (data_bit == 0):
      result2 = spi_mosi_low(result)
    else:
      result2 = spi_mosi_high(result)
    port.value = result2
    await ClockCycles(clk, 10)
    temp = port.value;
    result = spi_clk_invert(temp)
    port.value = result
    await ClockCycles(clk, 10)
    iterator -= 1

  temp = port.value;
  result = spi_clk_invert(temp)
  port.value = result
  await ClockCycles(clk, 10)

  temp = port.value;
  result = pull_cs_high(temp)
  port.value = result
  await ClockCycles(clk, 10)  


async def spi_read_cpha0 (clk, port_in, port_out, address, data):
  
  temp = port_in.value;
  result = pull_cs_high(temp)
  port_in.value = result
  await ClockCycles(clk, 10)

  # Pull CS low + Read command bit - bit 7 - MSBIT in first byte
  temp = port_in.value;
  result = pull_cs_low(temp)
  result2 = spi_mosi_low(result)
  port_in.value = result2
  await ClockCycles(clk, 10)
  temp = port_in.value;
  result = spi_clk_invert(temp)
  port_in.value = result
  await ClockCycles(clk, 10)

  iterator = 0
  while iterator < 3:
    # Don't care - bit 6, bit 5 and bit 4
    temp = port_in.value;
    result = spi_clk_invert(temp)
    result2 = spi_mosi_low(result)
    port_in.value = result2
    await ClockCycles(clk, 10)
    temp = port_in.value;
    result = spi_clk_invert(temp)
    port_in.value = result
    await ClockCycles(clk, 10)
    iterator += 1

  iterator = 3
  while iterator >= 0:
    # Address[iterator] - bit 3, bit 2, bit 1 and bit 0
    temp = port_in.value;
    result = spi_clk_invert(temp)
    address_bit = get_bit(address, iterator)
    if (address_bit == 0):
      result2 = spi_mosi_low(result)
    else:
      result2 = spi_mosi_high(result)
    port_in.value = result2
    await ClockCycles(clk, 10)
    temp = port_in.value;
    result = spi_clk_invert(temp)
    port_in.value = result
    await ClockCycles(clk, 10)
    iterator -= 1

  miso_byte = 0
  miso_bit = 0

  iterator = 7
  while iterator >= 0:
    # Data[iterator]
    temp = port_in.value;
    result = spi_clk_invert(temp)
    data_bit = get_bit(data, iterator)
    if (data_bit == 0):
      result2 = spi_mosi_low(result)
    else:
      result2 = spi_mosi_high(result)
    port_in.value = result2
    await ClockCycles(clk, 10)
    miso_bit = spi_miso_read(port_out)
    miso_byte = miso_byte | (miso_bit << iterator)
    temp = port_in.value;
    result = spi_clk_invert(temp)
    port_in.value = result
    await ClockCycles(clk, 10)
    iterator -= 1

  temp = port_in.value;
  result = spi_clk_invert(temp)
  port_in.value = result
  await ClockCycles(clk, 10)

  temp = port_in.value;
  result = pull_cs_high(temp)
  port_in.value = result
  await ClockCycles(clk, 10)

  return miso_byte
