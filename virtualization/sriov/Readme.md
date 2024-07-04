# SR-IOV
## vfs@.service
### Description
 This is a generator service to allow you to create 8 virtual functions (VFs) for a NIC on boot. That number is hardcoded at the moment. VFs are hardware accelerated virtual copies of a device. The typical use case is to pass a VF through to a VM, enabling the VM to skip a lot of the abstraction overhead.
### Usage
1. Install by moving `vfs@.service` to `/etc/systemd/system/vfs@.service`
2. Reload unit files by running `systemctl daemon-reload`
3. Create VFs now and on boot with `systemctl enable --now vfs@eth0`

