Summary: Rootkit scans for rootkits, backdoors and local exploits
Name: rkhunter
Version: 1.3.2
Release: %mkrel 2
Source0: http://downloads.sourceforge.net/rkhunter/%{name}-%{version}.tar.gz
License: GPLv2+
URL: http://www.rootkit.nl/projects/rootkit_hunter.html
Group: System/Configuration/Other
Requires: webfetch
Requires: e2fsprogs
Requires: binutils
#Requires: ccp
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch

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

To benefit from all the features, you have to run "rkhunter --propupd" to 
generate the rkhunter.dat file.

%prep
%setup -q 
chmod -R a+r .

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%_sysconfdir %{buildroot}%_sbindir \
 %{buildroot}%_var/lib/%name/db/i18n  %{buildroot}%_var/lib/%name/scripts \
 %{buildroot}%_var/lib/%name/tmp \
 %{buildroot}%_mandir/man8
install files/%name %{buildroot}%_sbindir/
install -m 644 files/%name.conf %{buildroot}%_sysconfdir
cat<<EOF>>%{buildroot}%_sysconfdir/%name.conf
INSTALLDIR=%_var
SCRIPTDIR=%_var/lib/%{name}/scripts
PKGMGR=RPM
# to avoid some false positives...
ALLOWDEVFILE=/dev/shm/pulse-shm-*
ALLOWHIDDENFILE=/usr/share/man/man1/..1.lzma
ALLOWHIDDENFILE=/usr/share/man/man1/.nvidia-current-settings.1.lzma
ALLOWHIDDENFILE=/usr/share/man/man1/.nvidia-current-smi.1.lzma
ALLOWHIDDENFILE=/usr/share/man/man1/.nvidia-current-xconfig.1.lzma
ALLOWHIDDENFILE=/usr/share/man/man1/.nvidia96xx-settings.1.lzma
ALLOWHIDDENFILE=/usr/share/man/man1/.nvidia96xx-xconfig.1.lzma
ALLOWHIDDENFILE=/usr/share/man/man5/.k5login.5.lzma
SCRIPTWHITELIST=/usr/bin/GET
SCRIPTWHITELIST=/usr/bin/groups
SCRIPTWHITELIST=/usr/bin/ldd
SCRIPTWHITELIST=/usr/bin/whatis
SCRIPTWHITELIST=/sbin/ifup
SCRIPTWHITELIST=/sbin/ifdown
EOF

install -m 644 files/*.dat %{buildroot}%_var/lib/%name/db
install -m 644 files/i18n/* %{buildroot}%_var/lib/%name/db/i18n
install -m 754 files/*.{pl,sh} %{buildroot}%_var/lib/%name/scripts
install -m 644 files/%name.8 %{buildroot}%_mandir/man8

%clean
rm -rf %{buildroot}

%post
#unfortunately, multiple ALLOW* and SCRIPT* keys forbids use of ccp
#until it supports the feature...
##fix previous broken < 1.2.8 installs.
#ccp --delete --ifexists --set NoOrphans \
# --ignoreopt TMPDIR --ignoreopt DBDIR \
# --oldfile %_sysconfdir/%name.conf \
# --newfile %_sysconfdir/%name.conf.rpmnew

%files
%defattr(-,root,root)
%doc files/CHANGELOG files/README files/WISHLIST
%config(noreplace) %_sysconfdir/%name.conf
%_sbindir/*
%_var/lib/%{name}
%_mandir/man8/*
