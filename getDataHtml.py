import subprocess
import sys
import os


sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

basic = {
    "Current_Date": 'Get-Date -Format "dddd MM/dd/yyyy"',
    "Current_Time": 'Get-Date -Format "HH:mm K"',
    "System_Name": "(Get-CimInstance -ClassName Win32_ComputerSystem).Name",
    "System_Manufacturer": "(Get-CimInstance -ClassName Win32_ComputerSystem).Manufacturer",
    "System_Model": "(Get-CimInstance -ClassName Win32_ComputerSystem).Model",
}

osInfo = {
    "Operating_System_Name": "(Get-ComputerInfo | Select OSName).OsName",
    "Operating_System_Version": "(Get-ComputerInfo | Select OSVersion).OSVersion",
    "Operating_System_Display_Version": '(Get-ComputerInfo -Property "*version").OSDisplayVersion',
    "Operating_System_Last_Boot": "(Get-ComputerInfo | Select OSLastBootupTime).OSLastBootupTime",
}

usersInfo = {
    "Users_List": 'foreach ($i in (Get-LocalUser)){Write-Host $i."Name" "| Enabled:" $i."Enabled"}',
    "Active_Users": "query user /server:$SERVER",
}

networkInfo = {
    "Network_Adapter_List": 'Get-NetAdapter | ForEach-Object{Write-Host "Adapter: $($_.Name)`nInterface Index: $($_.InterfaceIndex)`nStatus: $($_.Status)`nMac Address: $($_.MacAddress)`nLink Speed: $($_.Speed)`nIPv4 Address: $((Get-NetIPConfiguration -InterfaceIndex $_.InterfaceIndex).IPv4Address.IPAddress)`nIPv4 Default Gateway: $((Get-NetIPConfiguration -InterfaceIndex $_.InterfaceIndex).IPv4Defaultgateway.NextHop)`nDNS Server: $((Get-NetIPConfiguration -InterfaceIndex $_.InterfaceIndex).DNSServer.ServerAddresses)`n-----------------------------`n"} -ErrorAction Ignore',
}

cpuInfo = {
    "Cpu_Name": "(Get-CimInstance -ClassName Win32_Processor).Name",
    "Cpu_Usage": '(Get-Counter "\Processor(_Total)\% Processor Time").CounterSamples.CookedValue.ToString("#,0.000") + "%"',
}

ramInfo = {
    "Total_RAM": "(Get-CimInstance -ClassName Win32_ComputerSystem).totalphysicalmemory / (1024 * 1024 * 1024)",
    "Used_RAM": "[math]::Round((Get-CimInstance -ClassName Win32_ComputerSystem).totalphysicalmemory / (1024 * 1024 * 1024) - (Get-CimInstance -ClassName Win32_OperatingSystem).FreePhysicalMemory / (1024 * 1024),2)",
    "Free_RAM": "(Get-CimInstance -ClassName Win32_OperatingSystem).FreePhysicalMemory / (1024 * 1024)",
}

hypervInfo = {
    "HyperV_VMs": "Get-VM",
    "HyperV_Switches": "Get-VMSwitch",
}

dockerInfo = {
    "Docker_Containers": 'docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"',
    "Docker_Images": 'docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"',
}

checkServicesAndProcessesHost = {
    "Host_Service:ssh": "Get-Service 'SshdBroker'",
    "Host_Service:jenkins": "Get-Service 'Jenkins'",
    "Host_Service:dynu": "Get-Service 'Dynu.service'",
    "Host_Processes_Open_Window": "Get-Process | Where-Object {$_.mainWindowTitle} | Format-Table Id, Name, mainWindowtitle -AutoSize",
}

ubuntuDetails = {
    "Ubuntu_Version": "ssh jesus@192.168.0.109 grep '^VERSION' /etc/os-release",
    "Ubuntu_Uptime": "ssh jesus@192.168.0.109 uptime -p",
    "Ubuntu_Upgradables": "ssh jesus@192.168.0.109 \"apt list --upgradable 2>&1 | grep -v 'does not have a stable' \"",
    "Ubuntu_Network": "ssh jesus@192.168.0.109 ifconfig",
    "Ubuntu_Homebridge_Status": "ssh jesus@192.168.0.109 \"systemctl status homebridge | awk 'NR<=8'\" | Select-Object -Skip 1",
    "PiVPN_Clients": "ssh jesus@192.168.0.109 pivpn -c",
}

kubDetails = {
    "kubVersion": "kubectl version",
    "kubNodes": "kubectl get nodes",
    "kubDeployments": "kubectl get deployments",
    "kubServices": "kubectl get services",
    "kubPods": "kubectl get pods",
    "kubAllPods": "kubectl get pods --all-namespaces",
}

minikubeDetails = {
    "minikubeVersion": "minikube version",
    "minikubeStatus": "minikube status",
    "minikubeService": "minikube service list",
}


def report():
    print("<html><body style='font-family: Trebuchet MS;'>")
    print("<div><h1>Kaesto Report</h1></div><br>")
    print("<div><p>")
    for key in basic.keys():
        print("<h4>" + key + ":</h4>")
        print(
            subprocess.run(
                ["powershell", "-Command", basic[key]], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            + "<br>"
        )
    print("</p></div><br><br>")

    print("<div><p>----------------------------------------------<br>")
    print("<h3>Operating System Info</h3>")
    print("----------------------------------------------<br>")
    for key in osInfo.keys():
        print("<h4>" + key + ":</h4>")
        print(
            subprocess.run(
                ["powershell", "-Command", osInfo[key]], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            + "<br>"
        )
    print("</p></div><br><br>")

    print("<div><p>----------------------------------------------<br>")
    print("<h3>Users Info</h3>")
    print("----------------------------------------------<br>")
    for key in usersInfo.keys():
        print("<h4>" + key + ":</h4>")
        print(
            "<pre style='font-family:consolas;'>"
            + subprocess.run(
                ["powershell", "-Command", usersInfo[key]], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            + "</pre><br>"
        )
    print("</p></div><br><br>")

    print("<div><p>----------------------------------------------<br>")
    print("<h3>CPU Info</h3>")
    print("----------------------------------------------<br>")
    for key in cpuInfo.keys():
        print("<h4>" + key + ":</h4>")
        print(
            subprocess.run(
                ["powershell", "-Command", cpuInfo[key]], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            + "<br>"
        )
    print("</p></div><br><br>")

    print("<div><p>----------------------------------------------<br>")
    print("<h3>RAM Inf</h3>")
    print("----------------------------------------------<br>")
    for key in ramInfo.keys():
        print("<h4>" + key + ":</h4>")
        print(
            subprocess.run(
                ["powershell", "-Command", ramInfo[key]], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            + "<br>"
        )
    print("</p></div><br><br>")

    print("<div><p>----------------------------------------------<br>")
    print("<h3>Host Network Info</h3>")
    print("----------------------------------------------<br>")
    for key in networkInfo.keys():
        print("<h4>" + key + ":</h4>")
        print(
            "<pre style='font-family:consolas;'>"
            + subprocess.run(
                ["powershell", "-Command", networkInfo[key]], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            + "</pre><br>"
        )
    print("</p></div><br><br>")

    print("<div><p>----------------------------------------------<br>")
    print("<h3>HyperV Info</h3>")
    print("----------------------------------------------<br>")
    for key in hypervInfo.keys():
        print("<h4>" + key + ":</h4>")
        print(
            "<pre style='font-family:consolas;'>"
            + subprocess.run(
                ["powershell", "-Command", hypervInfo[key]], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            + "</pre><br>"
        )
    print("</p></div><br><br>")

    print("<div><p>----------------------------------------------<br>")
    print("<h3>Host Services and Processes Info</h3>")
    print("----------------------------------------------<br>")
    for key in checkServicesAndProcessesHost.keys():
        print("<h4>" + key + ":</h4>")
        print(
            "<pre style='font-family:consolas;'>"
            + subprocess.run(
                ["powershell", "-Command", checkServicesAndProcessesHost[key]],
                stdout=subprocess.PIPE,
            ).stdout.decode("utf-8")
            + "</pre><br>"
        )
    print("</p></div><br><br>")

    print("<div><p>----------------------------------------------<br>")
    print("<h3>Docker Info</h3>")
    print("----------------------------------------------<br>")
    for key in dockerInfo.keys():
        print("<h4>" + key + ":</h4>")
        print(
            "<pre style='font-family:consolas;'>"
            + subprocess.run(
                ["powershell", "-Command", dockerInfo[key]], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            + "</pre><br>"
        )
    print("</p></div><br><br>")

    print("<div><p>----------------------------------------------<br>")
    print("<h3>Ubuntu Server Info</h3>")
    print("----------------------------------------------<br>")
    for key in ubuntuDetails.keys():
        print("<h4>" + key + ":</h4>")
        print(
            "<pre style='font-family:consolas;'>"
            + subprocess.run(
                ["powershell", "-Command", ubuntuDetails[key]], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            + "</pre><br>"
        )
    print("</p></div><br><br>")

    print("<div><p>----------------------------------------------<br>")
    print("<h3>Kubernetes Info</h3>")
    print("----------------------------------------------<br>")
    for key in kubDetails.keys():
        print("<h4>" + key + ":</h4>")
        print(
            "<pre style='font-family:consolas;'>"
            + subprocess.run(
                ["powershell", "-Command", kubDetails[key]], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            + "</pre><br>"
        )
    print("</p></div><br><br>")

    print("<div><p>----------------------------------------------<br>")
    print("<h3>Minikube Info</h3>")
    print("----------------------------------------------<br>")
    for key in minikubeDetails.keys():
        print("<h4>" + key + ":</h4>")
        print(
            "<pre style='font-family:consolas;'>"
            + subprocess.run(
                ["powershell", "-Command", minikubeDetails[key]], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            + "</pre><br>"
        )
    print("</p></div><br><br>")

    print("</body></html>")


report()
