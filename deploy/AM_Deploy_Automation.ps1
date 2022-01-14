#Minimun PowerShell Version: 5.0, Tested in 5.1

#Check Required Cmdlets
if (Get-Command Get-SSHSession){}
else {
    "Posh-SSH Module이 설치되지 않았습니다. 모듈을 설치합니다.." | Out-Host
        if (([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).isInRole([Security.Principal.WindowsBuiltinRole]::Administrator) -match $false)
        {
            "PowerShell이 관리자 권한으로 실행되지 않았습니다. 관리자 권한으로 재실행하여 주십시오." | Out-Host
            Exit
        }    
        Install-Module Posh-SSH
        "Posh-SSH Module의 설치가 완료되었습니다. 스크립트를 재실행하여 주십시오."
        Exit
     }

if (Get-Command Set-PowerCLIConfiguration){}
else{
    "PowerCLI가 설치되지 않았습니다. VMware PowerCLI를 설치합니다." | Out-Host
    Install-Module VMware.PowerCLI
    "VMware PowerCLI가 설치되었습니다. 스크립트를 재실행하여 주십시오" | Out-Host
    Exit
    }


$OpenVPN_Logo = @"
                                               .:=++++++++++++++++++++++++++=:
                                            :=++++++++++++++++++++++++++++++++++=:
                                         :=++++++++++++++++++++++++++++++++++++++++=.
                                       =++++++++++++++++++++++++++++++++++++++++++++++:
                                     =++++++++++++++++++++++++++++++++++++++++++++++++++=
                                   =++++++++++++++++++++++++++++++++++++++++++++++++++++++:
                                 .++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.
                                :+++++++++++++++++++++++++==::::::==+++++++++++++++++++++++++:
                               =+++++++++++++++++++++=:.              .:=+++++++++++++++++++++=
                              =++++++++++++++++++++.                      :++++++++++++++++++++=
                             =+++++++++++++++++++.                          .+++++++++++++++++++:
                            .++++++++++++++++++:         .=*##%%##*=.         :++++++++++++++++++.
                            ++++++++++++++++++         +%%%%%%%%%%%%%%+        .++++++++++++++++++
                           .+++++++++++++++++.       +%%%%%%%%%%%%%%%%%%+       .+++++++++++++++++.
                           =++++++++++++++++:       #%%%%%%%%%%%%%%%%%%%%*       =++++++++++++++++=
                           +++++++++++++++++       =%%%%%%%%%%%%%%%%%%%%%%=       +++++++++++++++++
                           +++++++++++++++++       %%%%%%%%%%%%%%%%%%%%%%%#       +++++++++++++++++
                           +++++++++++++++++       %%%%%%%%%%%%%%%%%%%%%%%#       +++++++++++++++++
                           +++++++++++++++++       +%%%%%%%%%%%%%%%%%%%%%%=       +++++++++++++++++
                           =++++++++++++++++:       #%%%%%%%%%%%%%%%%%%%%#       =++++++++++++++++=
                           .+++++++++++++++++        +%%%%%%%%%%%%%%%%%%+       .+++++++++++++++++.
                            ++++++++++++++++++         +%%%%%%%%%%%%%%+        .++++++++++++++++++
                            .++++++++++++++++++.         .=%%%%%%%#=.         :++++++++++++++++++.
                             =++++++++++++++++++=         .%%%%%%%%         .+++++++++++++++++++:
                              ++++++++++++++++++++=.      *%%%%%%%%.      .++++++++++++++++++++=
                               =++++++++++++++++++++*     %%%%%%%%%+     *++++++++++++++++++++=
                                =+++++++++++++++++++     :%%%%%%%%%%      +++++++++++++++++++:
                                 .+++++++++++++++++      *%%%%%%%%%%.      +++++++++++++++++.
                                   =+++++++++++++=       %%%%%%%%%%%+       =+++++++++++++=
                                     =++++++++++:       =%%%%%%%%%%%%        =++++++++++=
                                      .=+++++++:        #%%%%%%%%%%%%.        :+++++++=
                                         :++++.         %%%%%%%%%%%%%=         .++++:
                                            :          =%%%%%%%%%%%%%#          .:
                                                       #%%%%%%%%%%%%%%
                                                       =+**##%%%%##**+.

"@
#Script Begin
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore | Out-Null
$OVF_Name = "/OpenWRT-AM.ovf"
$OVF_Location = $PSScriptRoot + $OVF_Name
$OpenVPN_Logo | Out-Host
"OpenWRT - OpenVPN Server Automated Management 배포 자동화 스크립트" | Out-Host
"OpenWRT 19.07 / OpenVPN 2.7.2" | Out-Host
"" | Out-Host
"사용 전 README 파일을 반드시 읽으십시오" | Out-Host
"사용자 입력값에는 오타가 있어서는 안 됩니다. 만약 잘못된 입력값을 넣었다면 PowerShell을 종료 후 재실행하십시오" | Out-Host
"" | Out-Host
$Server_Key = $PSScriptRoot + "/key/server.key"
$Server_DH = $PSScriptRoot + "/key/dh2048.pem"
$Server_Cert = $PSScriptRoot + "/key/server.crt"
$Server_CA = $PSScriptRoot + "/key/ca.crt"
$Client_Cert = $PSScriptRoot + "/key/client.crt"
$Client_Key = $PSScriptRoot + "/key/client.key"

$ESXI_Server_Address = Read-Host -Prompt "VM을 배포할 ESXi 호스트의 주소를 입력하십시오"
$ESXi_Server_Username = Read-Host -Prompt "ESXi 호스트의 사용자 이름을 입력하십시오"
$ESXi_Server_Password = Read-Host -Prompt "ESXi 호스트의 사용자 비밀번호를 입력하십시오"
"" | Out-Host
$SSH_Port = Read-Host -Prompt "OVF 이미지의 SSH 포트 번호를 입력하십시오"
$SSH_PW = Read-Host -Prompt "OVF 이미지의 root 비밀번호를 입력하십시오"
"" | Out-Host
$SSH_ID = "root"
$Default_LAN_Address = "192.168.100.1"

$secureString = New-Object System.Security.SecureString
$SSH_PW.ToCharArray() | %{ $secureString.AppendChar($_)}
$cred = new-object -typename System.Management.Automation.PSCredential -argumentlist $SSH_ID, $secureString

$ESXI_Session = Connect-VIServer -Server $ESXI_Server_Address -User $ESXi_Server_Username -Password $ESXi_Server_Password
$VMHost = Get-VMHost 


"호스트의 PortGroup 리스트를 출력합니다.." | Out-Host
Get-VirtualPortGroup -VMHost $VMHost | Out-Host
$PortGroup_WAN_Name = Read-Host -Prompt "WAN 포트그룹의 이름을 입력하세요"
$PortGroup_LAN_Name = Read-Host -Prompt "LAN 포트그룹(관리용)의 이름을 입력하세요"


$PortGroup_WAN = Get-VirtualPortGroup -Name $PortGroup_WAN_Name
$PortGroup_LAN = Get-VirtualPortGroup -Name $PortGroup_LAN_Name

$OvfConfig = @{"NetworkMapping.LAN"=$PortGroup_LAN_Name; "NetworkMapping.WAN"=$PortGroup_WAN_Name }
"" | Out-Host

$IP_Num = Read-Host -Prompt "LAN IP 대역을 입력하세요 (ex. 192.168.x.0)"
$Subnet_Mask = Read-Host -Prompt "LAN Subnet Mask를 입력하세요"
"" | Out-Host
$Name_Head = Read-Host -Prompt "VM 이름에 사용될 접두사를 입력하세요.(Ex. GN.S1.L2)"
$Start_IP_Number = Read-Host -Prompt "시작 IP 번호를 입력하세요"
$End_IP_Number = Read-Host -Prompt "종료 IP 번호를 입력하세요"


for ($i = [int]$Start_IP_Number; $i -le [int]$End_IP_Number; $i++){
    #For VM_Name, add leading zeros to IP
    $lz_IP_Num = '{0:d3}' -f [int]$IP_Num
    $lz_i = '{0:d3}' -f $i


    $VM_Name = $Name_Head + "-" +  [string]$lz_IP_Num + '.' + [string]$lz_i
    Import-VApp -Source $OVF_Location -Name $VM_Name -OvfConfiguration $OvfConfig -VMHost $VMHost | Out-Null
    $VM = Get-VM -Server $ESXI_Session -Name $VM_Name 

    Start-VM -Server $ESXI_Session -VM $VM
    $VM_Name + " 배포중.." | Out-Host
    Start-Sleep -s 30
    $LAN_Address = "192.168."+$IP_Num+"."+$i
    $Finish = 0
    while ($Finish -eq 0)
    {
        try{
            Get-SSHTrustedHost | Remove-SSHTrustedHost
            $session = New-SSHSession -ComputerName $Default_LAN_Address -Port $SSH_Port -Credential $cred -AcceptKey:$true -ConnectionTimeout 5 -ErrorAction Stop
            $SFTP_Session = New-SFTPSession -ComputerName $Default_LAN_Address -Port $SSH_Port -Credential $cred -AcceptKey:$true -ConnectionTimeout 5 -ErrorAction Stop
            $Finish = 1
        }
        catch {
            Get-SSHSession
            Get-SFTPSession
            $VM_Name + " SSH 접속 실패! 5초 후 재시도합니다.." | Out-Host
            Start-Sleep -s 5
        }
      }
                  Get-SSHSession
            Get-SFTPSession
      $BR_input = Read-Host -Prompt "브릿지로 접속할 아이피를 입력하세요."
      $Command_String = "echo > /etc/config/openvpn"
      Invoke-SSHCommand -SSHSession $session -Command "echo > /etc/config/openvpn # clear the openvpn uci config" | Out-host
            Invoke-SSHCommand -SSHSession $session -Command "uci commit openvpn" | Out-host
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client=openvpn" | Out-host

      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.enabled=1" | Out-host
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.dev=tun" | Out-host
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.proto=udp" | Out-host
           Start-Sleep 1
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.ca=/etc/openvpn/keys/ca.crt" | Out-host
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.cert=/etc/openvpn/keys/client.crt" | Out-host
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.key=/etc/openvpn/keys/client.key" | Out-host
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.port=1194" | Out-host
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.client=1" | Out-host
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.comp_lzo=yes" | Out-host
           Start-Sleep 1
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.cipher=AES-256-CBC" | Out-host
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.ifconfig='10.0.0.2 10.0.0.1'" | Out-host
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.log=/var/log/cliopenvpn.log" | Out-host
      Invoke-SSHCommand -SSHSession $session -Command "uci set openvpn.client.remote=$BR_input" | Out-host
      Invoke-SSHCommand -SSHSession $session -Command "uci commit openvpn" | Out-host
           Start-Sleep 1
      
      Set-SFTPFile -SFTPSession $SFTP_Session -LocalFile $Server_Key -RemotePath "/etc/openvpn/keys/"  -Overwrite
      Set-SFTPFile -SFTPSession $SFTP_Session -LocalFile $Server_Cert -RemotePath "/etc/openvpn/keys/" -Overwrite
      Set-SFTPFile -SFTPSession $SFTP_Session -LocalFile $Server_CA -RemotePath "/etc/openvpn/keys/" -Overwrite
      Set-SFTPFile -SFTPSession $SFTP_Session -LocalFile $Server_DH -RemotePath "/etc/openvpn/keys/" -Overwrite
      Set-SFTPFile -SFTPSession $SFTP_Session -LocalFile $Client_Cert -RemotePath "/etc/openvpn/keys/" -Overwrite
      Set-SFTPFile -SFTPSession $SFTP_Session -LocalFile $Client_Key -RemotePath "/etc/openvpn/keys/" -Overwrite
      
      $Command_String = "echo $VM_Name > /etc/uuid"
      Invoke-SSHCommand -SSHSession $session -Command $Command_String | Out-Null

      Invoke-SSHCommand -SSHSession $session -Command "uci set network.lan.ipaddr=$LAN_Address" | Out-Null
      Invoke-SSHCommand -SSHSession $session -Command "uci set network.lan.netmask=$Subnet_Mask" | Out-Null
      Invoke-SSHCommand -SSHSession $session -Command "uci commit network" | Out-Null
	  Invoke-SSHCommand -SSHSession $session -Command "uci set system.@system[0].hostname=$VM_Name" | Out-Null
	  Invoke-SSHCommand -SSHSession $session -Command "uci commit system" | Out-Null
      Start-Sleep 1
      Invoke-SSHCommand -SSHSession $session -Command "reboot" | Out-Null
      Get-SSHSession | Remove-SSHSession
      Get-SFTPSession | Remove-SFTPSession
}