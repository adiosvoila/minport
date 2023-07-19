Code Portfolio
https://github.com/adiosvoila/minport

VM which is based on open source Router OS-OPENWRT auto-deploy on Vmware ESXI

.
•	Deploy setup file is made of Vmware PowerCLI-Windows Powershell.  

•	(File : Deploy/AM_Deploy_Automation.ps1) – Reffered to as Deploy.PS

•	For Openvpn setup, setup file provide encrypt key which is already made by easyRSA

•	(File : Deploy/key/* all files, ca.crt, client.crt, client.key, dh2048.pem ••••••)

•	Line 66~80, OVF VMfile, file routing.

•	Line 82~88 ESXi Server input ID / PW /, OVF image SSH Port / SSH PW (line 89 basic ID “ root “)

•	Line 101 Show ESXi host PortGroup list

•	Line 102~103 OVF image define WAN/LAN 

•	Line 112~117 OVF image LAN set up

•	Line 120 For until deploy done

•	Line 153~174  openvpn setup, Key file, Protocol, Port, IP setup

•	Line 176~181 openvpn key overwrite

•	Line 183 gives UUID 

•	Line 184~191 Lan setup and Line 192 reboot to to communicate with MGS API server via init.d/

OPENWRT Image

	/etc/rc.d/S99update_node

	Line 10~14 UUID check

	Line 18~46 Create Openvpn Client Profile

	Line 48~50 Openvpn Clinet Profile Get

	Line 52~59 upload with curl / node date communication

	/usr/enable_idpw_server.conf -> Demand Openvpn Sign in info, line 18

	/usr/disable_idpw_server.conf -> No necessary id/pw to sign in

	/usr/enable_idpw_update_node -> Server profile change, demand Sign in info, line 27

	/usr/disable_idpw_update_node -> No necessary id/pw to sign in



MGS API Server

	Based on flask / centos / nginx

	/MGSAPI/app/__init__.py

	Define each funtions, user / node / auth / lease(rent)

	/MGSAPI/app/main/ 

	Each functions are separated, controller, model, service

	/MSGAPI/app/main/controller/

	Auth_controller wait Admin sign in

	Lease_controller control via SSH, set up lease date.

	Node_controller control Openwrt image servers, deliever openvpn client profile, order reboot, name change on windows 
manager program(reffered to as Win API), each openvpn server wether demand auth or not, change mac addres.

	User_controller is actual user controller add user, delete user, chage user password.

	Model folder below lease,node,user delivery info to sqlite

	Service folder below auth,lease,node,user communicate with Win API



Win API GUI program

	C# based, communicate with MGS API Server

	ApiClient.cs define most of function.

	Line 20 Communicate route

	Line 29~43 for sign in

	Line 46~63 get list of VM. 

	Line 65~80 

	Line 86~93 get cert(openvpn keyfile)

	Line 95~114 download openvpn client profile

	Line 119~136 funtion of change mac address

	Line 138~164 add user who is allowed to connect vpn client, socks5, openvpn

	Line 167~186 delete user

	Line 189~193 define communication

	LoginWindow.xaml GUI design for first sign in

	MainWindow.xaml GUI design for main interface.






