from smbus2 import SMBus, i2c_msg
import time
import json
import colorama
import sys

colorama.init(autoreset=True)

class EEPROM_24LC256:
    def __init__(self):
        self.addr = 0x54
        self.size = 32768
        self.page_size = 64
        self.n_of_pages = self.size//self.page_size
        self.i2c = SMBus(2)

    def wait(self):
        curr_time = time.monotonic()
        success = False
        while(time.monotonic() - curr_time < 1):
            try:
                self.i2c.i2c_rdwr(i2c_msg.write(self.addr, [0, 0]))
                success = True
                break
            except Exception as e: 
                pass
        if not success: 
            raise RuntimeError("Error! EEPROM wait timeout")
        
    def read_bytes(self, start_addr, n_bytes, print_ctr = False):
        if (start_addr+n_bytes) > self.size: raise ValueError("Error! Too many bytes")
        if start_addr%self.page_size != 0: raise ValueError("Error! Incorrect write address")
        pages_to_read = ((n_bytes-1)//self.page_size) + 1
        collected_bytes = b''
        for p in range(pages_to_read):
            read = i2c_msg.read(self.addr, self.page_size)
            addr_to_read = start_addr+p*self.page_size
            write = i2c_msg.write(self.addr, [(addr_to_read>>8)&0xFF, addr_to_read&0xFF])
            self.i2c.i2c_rdwr(write, read)
            collected_bytes += bytes(read)
            if print_ctr and (p%16==0):
                ctr = str(len(collected_bytes))
                sys.stdout.write(ctr+'\x1b[' + str(len(ctr)) + 'D')
        return collected_bytes[:n_bytes]
    
        
    def write_bytes(self, start_addr, data, print_ctr = False):
        n_bytes = len(data)
        if (start_addr+n_bytes) > self.size: raise ValueError("Error! Too many bytes")
        if start_addr%self.page_size != 0: raise ValueError("Error! Incorrect write address")
        start_page = start_addr//self.page_size
        n_pages = ((n_bytes-1)//self.page_size) + 1
        bytes_written = 0
        for p in range(n_pages):
            self.wait()
            page = data[p*self.page_size:]
            if len(page) > self.page_size: page = page[:self.page_size]
            addr_to_wr = (start_page + p)*self.page_size
            #print('Writing to %u:\n%s'%(addr_to_wr, page.hex()))
            write = i2c_msg.write(self.addr, [(addr_to_wr>>8)&0xFF, addr_to_wr&0xFF, *list(page)])
            self.i2c.i2c_rdwr(write)
            bytes_written += len(write)
            if print_ctr and (p%16==0):
                ctr = str(bytes_written)
                sys.stdout.write(ctr+'\x1b[' + str(len(ctr)) + 'D')
        self.wait()
        
class EEPROM:
    print_red = lambda self, txt: print(colorama.Style.BRIGHT+colorama.Fore.RED+txt)
    print_cyan = lambda self, txt: print(colorama.Style.BRIGHT+colorama.Fore.CYAN+txt)
    print_magenta = lambda self, txt: print(colorama.Fore.MAGENTA+txt)
    print_green = lambda self, txt: print(colorama.Style.BRIGHT+colorama.Fore.GREEN+txt)
    print_black = lambda self, txt: print(colorama.Fore.BLACK+colorama.Back.WHITE+txt)
    print_yellow = lambda self, txt: print(colorama.Fore.YELLOW+txt)
    
    def __init__(self):
        self.print_cyan('Starting EEPROM utility')
        self.chip = EEPROM_24LC256()
        self.size = self.chip.size
        
    def read_json(self, do_print = False):
        full_contents = bytearray()
        for page in range(self.chip.n_of_pages):
            addr = page*self.chip.page_size
            contents = self.chip.read_bytes(addr, self.chip.page_size)
            try: eol = contents.index(0)
            except: eol = None
            if eol is None: 
                full_contents += contents
                continue
            else:
                full_contents += contents[:eol]
                break
        
        if eol is None: 
            self.print_yellow('End of line not found in EEPROM')
            if len(set(full_contents)) == 1: self.print_yellow('EEPROM is EMPTY!')
            raise RuntimeError("Read text from eeprom failed")
        print('EEPROM is not empty, expecting json...', end = '')
        try:
            s = json.loads(full_contents.decode('ASCII'))
        except Exception as e:
            self.print_red('FAILURE')
            print(repr(e))
            raise RuntimeError("JSON decode failed") from None
        self.print_green('SUCCESS')
        self.print_yellow(json.dumps(s, indent=4, sort_keys=True))
        return s
            
    def read_hex(self):
        contents = self.read(0, self.size, do_print = True)
        print(self.hexdump(contents, length=24))
    
    def hexdump(self, data, length=32):
        def format_line(data, offset):
            hex_part = ''.join(f'{byte:02X}' for byte in data)
            ascii_part = ''.join(chr(byte) if 32 <= byte < 127 else '.' for byte in data)
            return f'{offset:04X}  {hex_part}  {ascii_part}'
    
        lines = []
        last_chunk = None
        skip_mode = False
    
        for i in range(0, len(data), length):
            chunk = data[i:i+length]
    
            if len(set(chunk)) == 1:
                if chunk == last_chunk:
                    if not skip_mode:
                        lines.append('....' + ' '*(len(format_line(chunk, i))-4))
                        skip_mode = True
                    continue
                else:
                    skip_mode = False
            
            lines.append(format_line(chunk, i))
            last_chunk = chunk
            
        if skip_mode and last_chunk is not None:
            lines.append(format_line(last_chunk, len(data) - length))
    
        return '\n' + '\n'.join(lines) + '\n'
        
    def test(self):
        print('Detecting EEPROM (addr 0x%02X)... '%self.chip.addr, end = '')
        try: 
            self.chip.wait()
            self.print_green('SUCCESS')
        except Exception as e:
            self.print_red('FAILURE')
            raise RuntimeError(f"EEPROM not detected:\n{repr(e)}")
    
    def read(self, addr, n_bytes, do_print = False):
        print('Reading EEPROM contents... ', end = '')
        try:
            contents = self.chip.read_bytes(addr, n_bytes, print_ctr=do_print)
            self.print_green('SUCCESS')
        except:
            self.print_red('FAILURE')
            raise RuntimeError("EEPROM read failed")
            
        return contents
            
    def write(self, addr, data, do_print = False):
        print('Writing to addr 0x%04X...'%addr, end ='')
        if isinstance(data, str):
            if data[-1] != '\0': data += '\0'
            data = data.encode('ascii')
        try:
            self.chip.write_bytes(addr, data, print_ctr = do_print)
            print('')
        except:
            self.print_red('FAILURE')
            raise RuntimeError("EEPROM write failed")
            
        print('Verifying...')
        contents = self.read(addr, len(data), do_print = do_print)
    
        if contents == data: 
            self.print_green('WRITE SUCCESS')
        else: 
            self.print_red('FAILURE')
            raise RuntimeError("EEPROM verify failed")
            
    def erase(self):
        print("Erasing EEPROM...")
        try:
            self.write(0, b'\xFF'*self.size, do_print = True)
            self.print_green('ERASE SUCCESS')
        except:
            self.print_red('WRITE FAILURE')
            raise RuntimeError("EEPROM write failed")
        
if __name__ == "__main__":
    try:
        eeprom = EEPROM()
        eeprom.test()
    except Exception as e:
        print(f"Something wrong...\n{repr(e)}")
    print("OK, run one of utilities")
    