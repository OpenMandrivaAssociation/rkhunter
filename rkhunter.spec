Summary:	Rootkit scans for rootkits, backdoors and local exploits
Name:		rkhunter
Version:	1.4.6
Release:	2
License:	GPLv2+
Group:		System/Configuration/Other
URL:		http://rkhunter.sourceforge.net/
Source0:	http://downloads.sourceforge.net/rkhunter/%{name}-%{version}.tar.gz
Source1:	http://downloads.sourceforge.net/rkhunter/%{name}-%{version}.tar.gz.asc
Source2:	rkhunter.cron
Source3:	rkhunter.logrotate
# https://issues.openmandriva.org/show_bug.cgi?id=2654
Patch0:  %{name}-%{version}-omv.patch
BuildArch:	noarch

Requires:	binutils
Requires:	e2fsprogs
Requires:	webfetch
Suggests:	unhide

%description
Rootkit scanner is scanning tool to ensure you you're clean of known nasty 
tools. This tool scans for rootkits, backdoors and local exploits by running 
tests like:
 - MD5/SHA1 hash compare
 - Look for default files used by rootkits
 - Wrong file permissions for binaries
 - Look for suspected strings in LKM and KLD modules
 - Look for hidden files
 - Optional scan within plaintext and binary files

%prep

%setup -q
%autopatch -p1
chmod -R a+r .

%build

%install
mkdir -p %{buildroot}%{_sysconfdir} %{buildroot}%{_sbindir} \
 %{buildroot}%{_var}/lib/rkhunter/{db/i18n,scripts,tmp} \
 %{buildroot}%{_mandir}/man8
install files/rkhunter %{buildroot}%{_sbindir}/
install -m 644 files/%{name}.conf %{buildroot}%{_sysconfdir}

cat<<EOF>>%{buildroot}%{_sysconfdir}/rkhunter.conf
INSTALLDIR=%{_var}
SCRIPTDIR=%{_var}/lib/rkhunter/scripts
PKGMGR=RPM
# to avoid some false positives...
ALLOWDEVFILE=/dev/shm/pulse-shm-*
ALLOWDEVFILE=/dev/shm/mono.*
ALLOWHIDDENDIR="/etc/.java"
ALLOWHIDDENDIR=/dev/.udev
ALLOWHIDDENDIR=/dev/.udevdb
ALLOWHIDDENDIR=/dev/.udev.tdb
ALLOWHIDDENDIR=/dev/.static
ALLOWHIDDENDIR=/dev/.initramfs
ALLOWHIDDENDIR=/dev/.SRC-unix
ALLOWHIDDENDIR=/dev/.mdadm
ALLOWHIDDENDIR=/dev/.systemd
ALLOWHIDDENDIR=/dev/.mount
ALLOWHIDDENFILE=/usr/share/man/man1/..1%{_extension}
ALLOWHIDDENFILE=/usr/share/man/man1/.nvidia-current-settings.1%{_extension}
ALLOWHIDDENFILE=/usr/share/man/man1/.nvidia-current-smi.1%{_extension}
ALLOWHIDDENFILE=/usr/share/man/man1/.nvidia-current-xconfig.1%{_extension}
ALLOWHIDDENFILE=/usr/share/man/man1/.nvidia96xx-settings.1%{_extension}
ALLOWHIDDENFILE=/usr/share/man/man1/.nvidia96xx-xconfig.1%{_extension}
ALLOWHIDDENFILE=/usr/share/man/man5/.k5login.5%{_extension}
ALLOWHIDDENFILE=/usr/share/man/man5/.k5identity.5%{_extension}
#SCRIPTWHITELIST=/usr/bin/GET
SCRIPTWHITELIST=/usr/bin/groups
SCRIPTWHITELIST=/usr/bin/ldd
SCRIPTWHITELIST=/usr/bin/whatis
#SCRIPTWHITELIST=/sbin/ifup
#SCRIPTWHITELIST=/sbin/ifdown
ALLOWDEVFILE=/dev/shm/pulse-shm-*
ALLOWDEVFILE=/dev/md/md-device-map
# tomboy creates this one
ALLOWDEVFILE="/dev/shm/mono.*"
# created by libv4l
ALLOWDEVFILE="/dev/shm/libv4l-*"
# created by spice video
ALLOWDEVFILE="/dev/shm/spice.*"
EOF

install -m 644 files/*.dat %{buildroot}%{_var}/lib/rkhunter/db
install -m 644 files/i18n/* %{buildroot}%{_var}/lib/rkhunter/db/i18n
install -m 754 files/*.{pl,sh} %{buildroot}%{_var}/lib/rkhunter/scripts
install -m 644 files/rkhunter.8 %{buildroot}%{_mandir}/man8

mkdir -p %{buildroot}%{_sysconfdir}/cron.daily
install -m 0755 %{SOURCE2} \
 %{buildroot}%{_sysconfdir}/cron.daily/rkhunter

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE3} \
 %{buildroot}%{_sysconfdir}/logrotate.d/rkhunter

%post
if [ $1 = 1 ]; then
    # create rkhunter.dat
    %{_sbindir}/rkhunter --propupd
    # gather user / group info
    echo "\r"|%{_sbindir}/rkhunter --enable group_changes,passwd_changes
    # Suppress warning on fresh install because of missing copies of passwd 
    # and groups file above
    /bin/true
fi

%files
%doc files/CHANGELOG files/README
%config(noreplace) %{_sysconfdir}/rkhunter.conf
%{_sysconfdir}/cron.daily/rkhunter
%{_sysconfdir}/logrotate.d/rkhunter
%{_sbindir}/*
%{_var}/lib/rkhunter
%{_mandir}/man8/*


