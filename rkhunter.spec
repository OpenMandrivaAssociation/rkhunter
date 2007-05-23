Summary: Rootkit scans for rootkits, backdoors and local exploits
Name: rkhunter
Version: 1.2.9
Release: %mkrel 1
Source0: http://downloads.rootkit.nl/%{name}-%{version}.tar.bz2
License: GPL
URL: http://www.rootkit.nl/projects/rootkit_hunter.html
Group: System/Configuration/Other
Requires: webfetch e2fsprogs binutils ccp
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
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%_sysconfdir $RPM_BUILD_ROOT%_sbindir \
 $RPM_BUILD_ROOT%_var/lib/%name/db  $RPM_BUILD_ROOT%_var/lib/%name/scripts \
 $RPM_BUILD_ROOT%_var/lib/%name/tmp \
 $RPM_BUILD_ROOT%_mandir/man8
install files/%name $RPM_BUILD_ROOT%_sbindir/
install -m 644 files/%name.conf $RPM_BUILD_ROOT%_sysconfdir
echo "INSTALLDIR=%_var" >> $RPM_BUILD_ROOT%_sysconfdir/%name.conf
install -m 644 files/*.dat $RPM_BUILD_ROOT%_var/lib/%name/db
install -m 754 files/*.{pl,sh} $RPM_BUILD_ROOT%_var/lib/%name/scripts
install -m 644 files/development/%name.8 $RPM_BUILD_ROOT%_mandir/man8

%clean
rm -rf $RPM_BUILD_ROOT

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
