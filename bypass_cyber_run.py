import asyncio
import sys
import os


try:
    import bypass_cyber
except ImportError:
    print("[-] Error: .so ဖိုင်ကို ရှာမတွေ့ပါ။ ဖိုင်နာမည်ကို မှန်အောင် စစ်ဆေးပါ။")
    sys.exit(1)

async def main():
    
    if hasattr(bypass_cyber, 'start_tool'):
        await bypass_cyber.start_tool()
    else:
        print("[-] Error: 'start_tool' ဆိုတဲ့ function ကို မတွေ့ပါ။")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Program stopped by user.")
