Name:		qmailmrtg
Summary:	Mrtg for qmail-toaster
Version:	4.2
Release:	0%{?dist}
License:	GPL
Group:		Networking/Other
URL:		http://www.inter7.com/index.php?page=qmailmrtg7
Source0:	http://www.inter7.com/qmailmrtg7/qmailmrtg7-%{version}.tar.gz
Source1:	qmailmrtg.cfg
Source2:	qmailmrtg.index.php
Source3:	qmailmrtg.module
Requires:	control-panel
Requires:	vixie-cron
Requires:	crontabs
Requires:	httpd >= 2.2.2
Requires:	php >= 5.1.6
Requires:	mrtg
Obsoletes:	qmailmrtg-toaster
BuildRoot:      %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}

%define apacheuser     apache
%define apachegroup    apache
%define crontab        /etc/crontab
%define debug_package %{nil}
%define basedir        %{_datadir}/toaster
%define mrtgdir        %{basedir}/mrtg

#-------------------------------------------------------------------
%description
#-------------------------------------------------------------------
Qmail MRTG Stat collector 

#-------------------------------------------------------------------
%prep
#-------------------------------------------------------------------

%setup -q -n %{name}7-%{version}

#-------------------------------------------------------------------
%build
#-------------------------------------------------------------------

gcc %{optflags} checkq.c -o checkq
./checkq
gcc %{optflags} -s -O qmailmrtg7.c -o qmailmrtg

#-------------------------------------------------------------------
%install
#-------------------------------------------------------------------
rm -rf %{buildroot}
install -d                                  %{buildroot}%{_sysconfdir}/cron.d
install -Dp qmailmrtg                       %{buildroot}%{_bindir}
install -Dp %{_sourcedir}/qmailmrtg.cfg     %{buildroot}%{mrtgdir}
install -Dp %{_sourcedir}/qmailmrtg.module  %{buildroot}%{basedir}/include
install -Dp %{_sourcedir}/qmailmrtg.index.php \
            %{buildroot}%{basedir}/htdocs/mrtg/index.php

#-------------------------------------------------------------------
%clean
#-------------------------------------------------------------------
rm -rf %{buildroot}

#-------------------------------------------------------------------
%post
#-------------------------------------------------------------------
# Setup mrtg
# shubes 11/16/2013 - I've no idea why this is repeated 4 times
export LANG=C
%{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg 2>&1 > /dev/null
%{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg 2>&1 > /dev/null
%{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg 2>&1 > /dev/null
%{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg 2>&1 > /dev/null

#-------------------------------------------------------------------
# Install cron-job
# shubes 11/16/2013 - this should be its own crontab file
#-------------------------------------------------------------------
# Remove old cron-job
grep -v '* * * * root %{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg' %{crontab} > %{crontab}.old
mv -f %{crontab}.old %{crontab}

if ! grep '* * * * root env LANG=C %{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg' %{crontab} > /dev/null; then
  echo "" >> %{crontab}
  echo "0-59/5 * * * * root env LANG=C %{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg 2>&1 > /dev/null" >> %{crontab}
fi

#-------------------------------------------------------------------
%postun
#-------------------------------------------------------------------
# Remove cron-job
if [ "$1" = "0" ]; then
  grep -v '* * * * root env LANG=C %{_bindir}/mrtg %{mrtgdir}/qmailmrtg.cfg' %{crontab} > %{crontab}.new
  mv -f %{crontab}.new %{crontab}
fi

#-------------------------------------------------------------------
%files
#-------------------------------------------------------------------
%defattr(-,root,root)
%attr(0755,root,root) %config(noreplace) %{mrtgdir}/qmailmrtg.cfg
%attr(0755,root,root) %{_bindir}/qmailmrtg
%defattr(-,%{apacheuser},%{apachegroup})
%attr(0755,%{apacheuser},%{apachegroup}) %dir  %{basedir}/htdocs/mrtg
%attr(0644,%{apacheuser},%{apachegroup}) %{basedir}/htdocs/mrtg/index.php
%attr(0644,%{apacheuser},%{apachegroup}) %{basedir}/include/*

#-------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------
* Sat Nov 16 2013 Eric Shubert <eric@datamatters.us> 3.4-0.qt
- Migrated to github
- Removed -toaster designation
- Added CentOS 6 support
- Removed unsupported cruft
* Sun Apr 10 2011 Martin Waschbüsch <martin@waschbuesch.de> 3.4-1.3.7
- Converted PHP tags to full format <? to <?php
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 3.4-1.3.6
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Wed Jun 10 2009 Jake Vickers <jake@qmailtoaster.com> 3.4-1.3.6
- Added Mandriva 2009 support
* Thu Apr 23 2009 Jake Vickers <jake@qmailtoaster.com> 3.4-1.3.5
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
- Changed some commenting in spec file to English for consistency
* Fri Feb 13 2009 Jake Vickers <jake@qmailtoaster.com> 3.4-1.3.4
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 3.4-1.3.4
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.3.3
- Add CentOS i386 support
- Add CentOS x86_64 support
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 4.2-1.3.2
- Added Fedora Core 6 support
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.3.1
- Add SuSE 10.1 support
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.11
- Add Fedora Core 5 support
* Sat Apr 29 2006 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.10
- Fix qmailmrtg.cfg
* Fri Apr 28 2006 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.9
- Set path variable for distros - Wade Albright <wade@bidnask.com>
- Additional graphs by Guillermo Villasana <gvillasana@exerwebsolutions.com>
* Sat Nov 12 2005 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.8
- Add SuSE 10.0 and Mandriva 2006.0 support
* Sat Oct 15 2005 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.7
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.6
- Add CentOS 4 x86_64 support
* Mon Jul 18 2005 Erik A. Espinoza <espinoza@forcenetworks.com> 4.2-1.2.5
- Upgraded to qmailmrtg 4.2
- Added support for virus scanning
* Fri Jul 01 2005 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.4
- Add Fedora Core 4 support
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 3.4-1.2.3
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
- Changed Mandrake 9.1,9.2,10.0,10.1 and 10.2 to apache-2x so all spec files has the same requirements.
- Add requirement for mandrake mrtg to Mandrake 9.1,9.2,10.0,10.1 and 10.2
* Sun Feb 27 2005 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.2
- Add Fedora Core 3 support
- Add CentOS 4 support
* Thu Jun 03 2004 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.2.1
- Update spec file
- Add Fedora Core 2 support
* Wed Feb 11 2004 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.0.11
- Define crontab
* Mon Jan 12 2004 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.0.10
- Trustix fix - fcrontab dep by Christian Dietrich
* Mon Dec 29 2003 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.0.9
- Add Fedora Core 1 support
* Tue Nov 25 2003 Nick Hemmesch <nick@ndhsoft.com> 3.4-1.0.8
- Add Trustix 2.0 support
- Fix images to images-toaster
* Fri May 24 2003 Miguel Beccari <miguel.beccari@clikka.com> 03.7-1.0.7
- Fixed mrtg dependency: Red Hat 9 has got its mrtg package
* Thu May 15 2003 Miguel Beccari <miguel.beccari@clikka.com> 03.7-1.0.6
- Red Hat Linux 9.0 support (nick@ndhsoft.com)
- Gnu/Linux Mandrake 9.2 support
- Clean-ups on SPEC: compilation banner, better gcc detects
- Detect gcc-3.2.3
* Mon Mar 31 2003 Miguel Beccari <miguel.beccari@clikka.com> 3.7-1.0.5
- Conectiva Linux 7.0 support
- Better managing of apache user (related to distro)
* Sun Feb 15 2003 Nick Hemmesch <nick@ndhsoft.com> 3.7-1.0.3
- Support for Red Hat 8.0
* Sat Feb 01 2003 Miguel Beccari <miguel.beccari@clikka.com> 3.7-1.0.2
- Redo Macros to prepare supporting larger RPM OS.
  We could be able to compile (and use) packages under every RPM based
  distribution: we just need to write right requirements.
* Sat Jan 25 2003 Miguel Beccari <miguel.beccari@clikka.com> 3.7-1.0.1
- Added MDK 9.1 support
- Try to use gcc-3.2.1
- Added very little patch to compile with newest GLIBC
- Support dor new RPM-4.0.4
* Sun Oct 06 2002 Miguel Beccari <miguel.beccari@clikka.com> 3.7-0.9.2
- Clean-ups
* Sun Sep 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 3.7-0.9.1
- RPM macros to detect Mandrake, RedHat, Trustix are OK again. They are
  very basic but they should work.
* Fri Sep 27 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.8.3.7-1
- Rebuilded under 0.8 tree.
- Important comments translated from Italian to English.
- Written rpm rebuilds instruction at the top of the file (in english).
* Sun Sep 22 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.3.7-2
- Added imap4, imap4-ssl, pop3-ssl statistics.
- Testes crontab jobs: now it REALLY works 100%!!!
* Sun Sep 01 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.3.7-1
- New version: it works now
* Thu Aug 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.2.3-2
- Deleted Mandrake Release Autodetection (creates problems)
- Fixed RedHat compatibility
* Fri Aug 16 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.2.3-1
- First RPM release. It comes with toaster templates, toaster layout,
  toaster dependencies: seems to work.

