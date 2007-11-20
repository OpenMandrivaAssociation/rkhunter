Summary: Rootkit scans for rootkits, backdoors and local exploits
Name: rkhunter
Version: 1.3.0
Release: %mkrel 1
Source0: http://downloads.rootkit.nl/%{name}-%{version}.tar.gz
License: GPLv2+
URL: http://www.rootkit.nl/projects/rootkit_hunter.html
Group: System/Configuration/Other
Requires: webfetch
Requires: e2fsprogs
Requires: binutils
Requires: ccp
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch

%description
Rootkit scanner is scanning tool to ensure you for about 99.9%% you're
clean of nasty tools. This tool scans for rootkits, backdoors and local
exploits by running tests like:
	- MD5 hash compare
	- Look for default files used by rootkits
	- Wrong file permissions for binaries
	- Look for suspected strings in LKM and KLD modules
	- Look for hidden files
	- Optional scan within plaintext and binary files

%prep
%setup -q 
chmod -R a+r .

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%_sysconfdir %{buildroot}%_sbindir \
 %{buildroot}%_var/lib/%name/db  %{buildroot}%_var/lib/%name/scripts \
 %{buildroot}%_var/lib/%name/tmp \
 %{buildroot}%_mandir/man8
install files/%name %{buildroot}%_sbindir/
install -m 644 files/%name.conf %{buildroot}%_sysconfdir
echo "INSTALLDIR=%_var" >> %{buildroot}%_sysconfdir/%name.conf
install -m 644 files/*.dat %{buildroot}%_var/lib/%name/db
install -m 754 files/*.{pl,sh} %{buildroot}%_var/lib/%name/scripts
install -m 644 files/%name.8 %{buildroot}%_mandir/man8

%clean
rm -rf %{buildroot}

%post
#fix previous broken < 1.2.8 installs.
ccp --delete --ifexists --set NoOrphans \
 --ignoreopt TMPDIR --ignoreopt DBDIR \
 --oldfile %_sysconfdir/%name.conf \
 --newfile %_sysconfdir/%name.conf.rpmnew

%files
%defattr(-,root,root)
%doc files/CHANGELOG files/README files/WISHLIST
%config(noreplace) %_sysconfdir/%name.conf
%_sbindir/*
%_var/lib/%{name}
%_mandir/man8/*
