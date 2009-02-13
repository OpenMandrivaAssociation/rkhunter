Name:			rkhunter
Version:		1.3.4
Release:		%mkrel 2

Summary:	Rootkit scans for rootkits, backdoors and local exploits
License:	GPLv2+
Group:		System/Configuration/Other
URL:		http://www.rootkit.nl/projects/rootkit_hunter.html
Source0:	http://downloads.sourceforge.net/rkhunter/%{name}-%{version}.tar.gz
Source1:	rkhunter.cron
Source2:	rkhunter.logrotate
BuildRoot:	%{_tmppath}/%{name}-%{version}

BuildArch:	noarch
Requires:	webfetch
Requires:	e2fsprogs
Requires:	binutils
#Requires:	ccp

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
chmod -R a+r .

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir} %{buildroot}%{_sbindir} \
 %{buildroot}%{_var}/lib/rkhunter/{db/i18n,scripts,tmp} \
 %{buildroot}%{_mandir}/man8
install files/rkhunter %{buildroot}%{_sbindir}/
install -m 644 files/%{name}.conf %{buildroot}%{_sysconfdir}
cat<<EOF>>%{buildroot}%{_sysconfdir}/rkhunter.conf
INSTALLDIR=%{_var}
SCRIPTDIR=%{_var}/lib/rkhunter/scripts
# PKGMGR=RPM
# to avoid some false positives...
ALLOWDEVFILE=/dev/shm/pulse-shm-*
ALLOWDEVFILE=/dev/shm/mono.*
ALLOWHIDDENDIR=/dev/.udev
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

install -m 644 files/*.dat %{buildroot}%{_var}/lib/rkhunter/db
install -m 644 files/i18n/* %{buildroot}%{_var}/lib/rkhunter/db/i18n
install -m 754 files/*.{pl,sh} %{buildroot}%{_var}/lib/rkhunter/scripts
install -m 644 files/rkhunter.8 %{buildroot}%{_mandir}/man8

%{__mkdir_p} %{buildroot}%{_sysconfdir}/cron.daily
%{__install} -m 0755 %{_sourcedir}/rkhunter.cron \
 %{buildroot}%{_sysconfdir}/cron.daily/rkhunter

%{__mkdir_p} %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -m 0644 %{_sourcedir}/rkhunter.logrotate \
 %{buildroot}%{_sysconfdir}/logrotate.d/rkhunter

%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
    # create rkhunter.dat
    %{_sbindir}/rkhunter --propupd
    # gather user / group info
    %{_sbindir}/rkhunter --enable group_changes,passwd_changes
fi

#unfortunately, multiple ALLOW* and SCRIPT* keys forbids use of ccp
#until it supports the feature...
##fix previous broken < 1.2.8 installs.
#ccp --delete --ifexists --set NoOrphans \
# --ignoreopt TMPDIR --ignoreopt DBDIR \
# --oldfile %{_sysconfdir}/rkhunter.conf \
# --newfile %{_sysconfdir}/rkhunter.conf.rpmnew

%files
%defattr(-,root,root)
%doc files/CHANGELOG files/README files/WISHLIST
%config(noreplace) %{_sysconfdir}/rkhunter.conf
%{_sysconfdir}/cron.daily/rkhunter
%{_sysconfdir}/logrotate.d/rkhunter
%{_sbindir}/*
%{_var}/lib/rkhunter
%{_mandir}/man8/*
