import ctypes
import sys
from pymem import Pymem, exception as pymem_exc

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

if not is_admin():
    # Relaunch script with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

def safe_pointer_chain(pm_ins: Pymem, base: int, offsets: list[int]):
    """
    Safely resolve a pointer chain.
    Prints each step and returns None if any read fails.
    """
    try:
        addr = pm_ins.read_ulonglong(base)
        print(f"[Base] 0x{base:016X} -> 0x{addr:016X}")
    except Exception as e:
        print(f"[Base] Failed to read 0x{base:016X}: {e}")
        return None

    for i, off in enumerate(offsets[:-1]):
        try:
            addr = pm_ins.read_ulonglong(addr + off)
            print(f"[Step {i}] +0x{off:X} -> 0x{addr:016X}")
        except Exception as e:
            print(f"[Step {i}] Failed at offset 0x{off:X}: {e}")
            return None

    final_addr = addr + offsets[-1]
    print(f"[Final Address] 0x{final_addr:016X}")
    return final_addr

def main():
    try:
        pm = Pymem('Minecraft.Windows.exe')
        print("Process opened successfully.")
    except Exception as e:
        print("Failed to open 'Minecraft.Windows.exe':", e)
        input("Press Enter to exit...")
        return

    # Module base + your offset
    base_addr = pm.base_address + 0x0905C8A0
    offsets = [0x0, 0xE8, 0xC0, 0x0, 0x200, 0x10, 0x10]

    final = safe_pointer_chain(pm, base_addr, offsets)
    if final is None:
        print("Pointer chain could not be fully resolved.")
        input("Press Enter to exit...")
        return

    try:
        value = pm.read_float(final)
        print(f"[Value] Float at 0x{final:016X} = {value}")
    except Exception as e:
        print(f"Failed to read float at 0x{final:016X}: {e}")

    input("Done — press Enter to exit...")

if __name__ == "__main__":
    main()
