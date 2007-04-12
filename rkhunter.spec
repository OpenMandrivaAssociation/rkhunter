Summary: Rootkit scans for rootkits, backdoors and local exploits
Name: rkhunter
Version: 1.2.8
Release: %mkrel 1
Source0: http://downloads.rootkit.nl/%{name}-%{version}.tar.bz2
License: GPL
URL: http://www.rootkit.nl/projects/rootkit_hunter.html
Group: System/Configuration/Other
Requires: webfetch e2fsprogs binutils
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
%setup -q -n %name
chmod -R a+r .

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%_sysconfdir $RPM_BUILD_ROOT%_sbindir \
 $RPM_BUILD_ROOT%_var/lib/%name/db  $RPM_BUILD_ROOT%_var/lib/%name/scripts \
 $RPM_BUILD_ROOT%_var/lib/%name/tmp \
 $RPM_BUILD_ROOT%_mandir/man8
install files/rkhunter $RPM_BUILD_ROOT%_sbindir/
install -m 644 files/rkhunter.conf $RPM_BUILD_ROOT%_sysconfdir
echo "INSTALLDIR=%_var" >> $RPM_BUILD_ROOT%_sysconfdir/rkhunter.conf
install -m 644 files/*.dat $RPM_BUILD_ROOT%_var/lib/%name/db
install -m 754 files/*.{pl,sh} $RPM_BUILD_ROOT%_var/lib/%name/scripts
install -m 644 files/development/rkhunter.8 $RPM_BUILD_ROOT%_mandir/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc files/CHANGELOG files/README files/WISHLIST
%config(noreplace) %_sysconfdir/rkhunter.conf
%_sbindir/*
%_var/lib/%{name}
%_mandir/man8/*

