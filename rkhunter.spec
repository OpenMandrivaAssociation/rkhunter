Summary:	Rootkit scans for rootkits, backdoors and local exploits
Name:		rkhunter
Version:	1.4.0
Release:	3
License:	GPLv2+
Group:		System/Configuration/Other
URL:		http://rkhunter.sourceforge.net/
Source0:	http://downloads.sourceforge.net/rkhunter/%{name}-%{version}.tar.gz
Source1:	http://downloads.sourceforge.net/rkhunter/%{name}-%{version}.tar.gz.asc
Source2:	rkhunter.cron
Source3:	rkhunter.logrotate
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
SCRIPTWHITELIST=/usr/bin/GET
SCRIPTWHITELIST=/usr/bin/groups
SCRIPTWHITELIST=/usr/bin/ldd
SCRIPTWHITELIST=/usr/bin/whatis
SCRIPTWHITELIST=/sbin/ifup
SCRIPTWHITELIST=/sbin/ifdown
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

%{__mkdir_p} %{buildroot}%{_sysconfdir}/cron.daily
%{__install} -m 0755 %{SOURCE2} \
 %{buildroot}%{_sysconfdir}/cron.daily/rkhunter

%{__mkdir_p} %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -m 0644 %{SOURCE3} \
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


%changelog
* Tue May 01 2012 Oden Eriksson <oeriksson@mandriva.com> 1.4.0-1mdv2012.0
+ Revision: 794720
- 1.4.0

* Tue Jan 31 2012 Oden Eriksson <oeriksson@mandriva.com> 1.3.8-3
+ Revision: 770016
- heh, 2011 needs the 2.1 release
- it needs the enter key in %%post, so fix that...
- sync slightly with fedora (rkhunter-1.3.8-13.fc17.src.rpm)
- use %%{_extension} instead of hardcoding it (duh!)
- added more annoying false positives (fedora)

* Sun Feb 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.8-2
+ Revision: 638851
- added backporting magic

* Sat Nov 20 2010 Jani Välimaa <wally@mandriva.org> 1.3.8-1mdv2011.0
+ Revision: 599218
- new version 1.3.8

* Mon Aug 02 2010 Jani Välimaa <wally@mandriva.org> 1.3.6-2mdv2011.0
+ Revision: 565129
- suggest unhide (see mdv #60455)

* Fri Jan 01 2010 Emmanuel Andry <eandry@mandriva.org> 1.3.6-1mdv2010.1
+ Revision: 484719
- New version 1.3.6

* Mon Jun 01 2009 Guillaume Bedot <littletux@mandriva.org> 1.3.4-3mdv2010.0
+ Revision: 381936
- Fix mdv bug #51310

* Fri Feb 13 2009 Guillaume Bedot <littletux@mandriva.org> 1.3.4-2mdv2009.1
+ Revision: 340059
- whitelist update

* Sun Feb 08 2009 Frederik Himpe <fhimpe@mandriva.org> 1.3.4-1mdv2009.1
+ Revision: 338555
- update to new version 1.3.4

* Tue Oct 28 2008 Guillaume Bedot <littletux@mandriva.org> 1.3.2-7mdv2009.1
+ Revision: 297803
- fix description, typos in post
- avoid first warning about user / group
- logrotate
- do not overwrite previous log

* Tue Oct 21 2008 Guillaume Bedot <littletux@mandriva.org> 1.3.2-5mdv2009.1
+ Revision: 296265
- First try to fix bug #40266

* Fri Aug 01 2008 Thierry Vignaud <tv@mandriva.org> 1.3.2-5mdv2009.0
+ Revision: 260240
- rebuild

* Mon Jul 28 2008 Thierry Vignaud <tv@mandriva.org> 1.3.2-4mdv2009.0
+ Revision: 251267
- rebuild

* Tue Mar 04 2008 Guillaume Bedot <littletux@mandriva.org> 1.3.2-1mdv2008.1
+ Revision: 178884
- 1.3.2

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Nov 22 2007 Guillaume Bedot <littletux@mandriva.org> 1.3.0-2mdv2008.1
+ Revision: 111089
- added missing i18n files and SCRIPTDIR option

* Tue Nov 20 2007 Adam Williamson <awilliamson@mandriva.org> 1.3.0-1mdv2008.1
+ Revision: 110811
- fix manpage location in tarball
- new release 1.3.0
- small spec clean

* Wed May 23 2007 Guillaume Bedot <littletux@mandriva.org> 1.2.9-1mdv2008.0
+ Revision: 30072
- More adequate config update thanks to ccp.
- 1.2.9 (thankks to lenny) + try to definitely fix #28571 and alike.


* Thu Mar 16 2006 Guillaume Bedot <littletux@zarb.org> 1.2.8-1mdk
- 1.2.8
- avoid duplicated files
- added man page

* Sat Aug 06 2005 Gaetan Lehmann <glehmann@n4.mandriva.com> 1.2.7-1mdk
- complete URL
- use mkrel
- fix config file (reported on expert mailing list)

* Wed May 25 2005 Lenny Cartier <lenny@mandriva.com> 1.2.7-1mdk
- 1.2.7

* Wed May 11 2005 Lenny Cartier <lenny@mandriva.com> 1.2.6-1mdk
- 1.2.6

* Fri Feb 11 2005 Mandrakelinux Team <http://www.mandrakeexpert.com> 1.2.0-1mdk
- New release 1.2.0

* Tue Feb 08 2005 Mandrakelinux Team <http://www.mandrakeexpert.com> 1.1.9-1mdk
- New release 1.1.9

* Mon Aug 23 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.1.6-2mdk
- fixed update script path (Mario R. Pizzolanti)

* Wed Aug 18 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.1.6-1mdk
- added missing requires
- New release 1.1.6

* Wed Jun 23 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.1.1-1mdk
- New release 1.1.1

* Fri May 28 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.0.9-1mdk
- initial package

