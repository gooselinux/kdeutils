Name: kdeutils
Epoch: 6
Version: 4.3.4
Release: 6%{?dist}
Summary: KDE Utilities
Group: Applications/System
License: GPLv2 and LGPLv2 and MIT and BSD
URL: http://www.kde.org
Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
# part of oxygen-icon-theme
Source1: ark-icons.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# hiolor icons
Patch1: kdeutils-4.3.4-ark-icons.patch

# 4.3 upstream patches
Patch100: kdeutils-4.3.5.patch
Patch101: kdeutils-4.3.4-js.patch

# 4.4 upstream patches

BuildRequires: desktop-file-utils
BuildRequires: kdelibs-experimental-devel >= %{version}
BuildRequires: kdepimlibs-devel >= %{version}
BuildRequires: plasma-devel >= %{version}
BuildRequires: gmp-devel
BuildRequires: libarchive-devel
BuildRequires: libzip-devel
BuildRequires: python-devel python
BuildRequires: qca2-devel
BuildRequires: qimageblitz-devel
BuildRequires: xz-devel

Obsoletes: kdeutils-extras < 6:4.0.0
Obsoletes: kdeutils-devel < 6:4.0.0
Obsoletes: kdeutils < 6:4.3.0-2

Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description
Utilities for the K Desktop Environment.
Includes:
  * ark: tar/gzip archive manager
  * kcalc: scientific calculator
  * kcharselect: character selector
  * kdelirc: Linux Infrared Remote Control frontend 
  * kdessh: ssh front end
  * kdf: view disk usage
  * kfloppy: floppy formatting tool
  * kgpg: gpg gui
  * ktimer: task scheduler
  * kwalletmanager: kde wallet management tool
  * okteta: binary/hex editor
  * superkaramba
  * sweeper: clean unwanted traces the user leaves on the system

%package libs
Summary: Runtime libraries for %{name}
Group:   System Environment/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: kdelibs4%{?_isa} >= %{version}

%description libs
%{summary}.

%prep
%setup -q -a 1

%patch1 -p1 -b .icons
%patch100 -p1 -b .kde435
%patch101 -p1 -b .js

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# nothing should build against these
rm -f %{buildroot}%{_kde4_libdir}/libokteta{core,gui}.so
rm -f %{buildroot}%{_kde4_libdir}/libkdelirc_shared.so
rm -f %{buildroot}%{_kde4_libdir}/libkerfuffle.so
rm -f %{buildroot}%{_kde4_libdir}/libkmilo.so
rm -f %{buildroot}%{_kde4_libdir}/libsuperkaramba.so

# drop printer-applet
rm -rf %{buildroot}%{_kde4_bindir}/printer-applet \
       %{buildroot}%{_kde4_datadir}/autostart/printer-applet.desktop \
       %{buildroot}%{_kde4_appsdir}/printer-applet/

%check
for f in %{buildroot}%{_kde4_datadir}/applications/kde4/*.desktop ; do
# make an exception for irkick service-style .desktop, while we consult
# upstream
  if [ "`basename $f .desktop`" != "irkick" ]; then
  desktop-file-validate $f
  fi
done


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:

%posttrans
update-desktop-database -q &> /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null ||:
  update-desktop-database -q &> /dev/null ||:
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_kde4_bindir}/ark
%{_kde4_bindir}/irkick
%{_kde4_bindir}/kcalc
%{_kde4_bindir}/kcharselect
%{_kde4_bindir}/kdessh
%{_kde4_bindir}/kdf
%{_kde4_bindir}/kfloppy
%{_kde4_bindir}/kgpg
%{_kde4_bindir}/ktimer
%{_kde4_bindir}/kwalletmanager
%{_kde4_bindir}/kwikdisk
%{_kde4_bindir}/okteta
%{_kde4_bindir}/superkaramba
%{_kde4_bindir}/sweeper
%{_kde4_appsdir}/ark/
%{_kde4_appsdir}/irkick/
%{_kde4_appsdir}/kcalc/
%{_kde4_appsdir}/kcharselect/
%{_kde4_appsdir}/kconf_update/*
%{_kde4_appsdir}/kdf/
%{_kde4_appsdir}/kgpg/
%{_kde4_appsdir}/kwalletmanager/
%{_kde4_appsdir}/okteta/
%{_kde4_appsdir}/oktetapart/
%{_kde4_appsdir}/profiles/
%{_kde4_appsdir}/remotes/
%{_kde4_appsdir}/superkaramba/
%{_kde4_appsdir}/sweeper/
%{_kde4_datadir}/kde4/services/*
%{_kde4_datadir}/kde4/servicetypes/*
%{_kde4_datadir}/applications/kde4/*.desktop
%{_kde4_docdir}/HTML/en/*
%{_kde4_iconsdir}/hicolor/*/apps/*
%{_kde4_iconsdir}/oxygen/*/*/*
%{_datadir}/dbus-1/interfaces/*
%{_kde4_datadir}/config.kcfg/*
%{_kde4_datadir}/autostart/irkick.desktop
%{_kde4_datadir}/autostart/kgpg.desktop
%{_kde4_configdir}/*
%{_kde4_libdir}/libkdeinit*.so
%{_kde4_libdir}/kde4/*.so
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%{_kde4_libdir}/lib*.so.*


%changelog
* Thu Jun 24 2010 Than Ngo <than@redhat.com> 6:4.3.4-6
- Resolves: bz#587895, ark does not seem to have icon on menu
- Resolves: bz#595784, disable JS / Java / plugins in khtml file preview

* Tue Mar 30 2010 Than Ngo <than@redhat.com> - 6:4.3.4-5
- rebuilt against qt-4.6.2

* Wed Feb 24 2010 Than Ngo <than@redhat.com> - 6:4.3.4-4
- fix license

* Fri Jan 22 2010 Than Ngo <than@redhat.com> - 6:4.3.4-3
- backport 4.3.5 fixes

* Fri Dec 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.4-2
- BR: xz-devel

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.3.4-1
- 4.3.4

* Fri Nov 13 2009 Than Ngo <than@redhat.com> - 4.3.3-2
- rhel cleanup, Fix conditional for RHEL

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Mon Oct 05 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Sun Aug 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 6:4.3.0-3
- include epoch's in -libs-related Requires

* Sat Aug 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 6:4.3.0-2
- -libs subpkg reborn: Multilib conflicts for index.cache.bz2 (#515087)
- %%check: desktop-file-validate

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 6:4.3.0-1
- 4.3.0

* Wed Jul 22 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Mon Jul 13 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Fri Jun 26 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3rc1

* Wed Jun 03 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.90-1
- KDE-4.3 beta2 (4.2.90)
- Add support for PackageKit service packs (#504136)

* Wed May 20 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.85-3
- remove F9 kjots hack

* Wed May 20 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.85-2
- reenable printer-applet

* Thu May 14 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Thu Apr 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-4
- revert -printer-applet dep changes (and drop for f11+)

* Wed Apr 15 2009 Than Ngo <than@redhat.com> - 4.2.2-3
- drop the BR on PyKDE4, system-config-printer-libs
  it's just needed for runtime
- fix kdeutils-printer-applet dependency
- apply upstream patch to fix several issues in ark

* Wed Apr 01 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.2-2
- optimize scriptlets

* Tue Mar 31 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Sat Mar 14 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.1-3.2
- also drag in the printer-applet on F9

* Sat Mar 14 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.1-3.1
- also build printer-applet on F9, but don't drag it in by default

* Fri Mar 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.1-3
- *really* make a -printer-applet subpkg

* Fri Mar 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.1-2
- -printer-applet subpkg
- cleanup unused -libs/-devel crud

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Wed Jan 14 2009 Rex Dieter <rdieter@fedoraproject.org> 4.1.96-2
- (Build)Req: system-config-printer-libs

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Fri Dec 12 2008 Than Ngo <than@redhat.com> 4.1.85-1
- 4.2beta2

* Mon Dec 08 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.80-5
- BR: PyKDE4-devel >= %%version (vs previously unversioned BR)

* Mon Dec 01 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.80-4
- rebuild for Python 2.6

* Mon Dec 01 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.80-3
- BR plasma-devel instead of kdebase-workspace-devel

* Thu Nov 20 2008 Than Ngo <than@redhat.com> 4.1.80-2
- merged

* Thu Nov 20 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 6:4.1.80-1
- 4.1.80
- BR cmake >= 2.6.2
- make install/fast

* Wed Nov 12 2008 Than Ngo <than@redhat.com> 4.1.3-1
- 4.1.3

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-3
- make VERBOSE=1
- respin against new(er) kde-filesystem

* Sun Sep 28 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- (re)add unpackaged HTML/en/kcontrol/ files

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Tue Jul 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.0-1.1
- omit printer_applet from F-9 build

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Mon Jul 21 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.99-1.1
- reinclude kjots on F9 (moved to kdepim in 4.1, we don't ship kdepim 4 in F9)

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Thu Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Thu Jul 03 2008 Rex Dieter <rdieter@fedorproject.org> 4.0.84-2.1
- disable printer applet (for now, to avoid kdebindings/PyKDE4 deps madness)

* Thu Jul 03 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-2
- %%description: -kedit, -kjots, +kwalletmanager, +superkaramba, +sweeper

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Sat Jun 21 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.83-2
- add explicit dep on rhpl to work around missing dep in
  system-config-printer (#452575)

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- 4.0.82

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta1

* Wed May 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-1
- update to 4.0.72
- Obsoletes/Provides: okteta, update file list and description for okteta
- remove .so symlinks which should not be in a non-devel package

* Fri Apr 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-4
- add BR libarchive-devel

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-3
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-2
- rebuild for NDEBUG and _kde4_libexecdir

* Fri Mar 28 2008 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Tue Feb 05 2008 Than Ngo <than@redhat.com> 4.0.1-2
- backport to fix the wrong signal name of a KSelectAction

* Thu Jan 31 2008 Rex Dieter <rdieter@fedoraproject.org> 6:4.0.1-1
- kde-4.0.1

* Wed Jan 08 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 6:4.0.0-2
- drop Requires: %%name-libs (doesn't exist anymore)

* Tue Jan 08 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 6:4.0.0-1
- kde-4.0.0

* Fri Dec 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.97.0-3
- libs subpkg
- Obsoletes: -extras
- omit parallel-install symlink hack

* Wed Dec 12 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 6:3.97.0-2
- rebuild for changed _kde4_includedir

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.97.0-1
- kde-3.97.0

* Sat Dec 01 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.96.2-2
- kcalc_32bit patch

* Sat Dec 01 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 6:3.96.2-1
- kde-3.96.2

* Sat Nov 24 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.1-1
- kde-3.96.1
- added epoch in changelog (also backwards)

* Mon Nov 19 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.0-6
- BR: kde-filesystem >= 4

* Mon Nov 19 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.0-5
- BR: libXcomposite-devel
- BR: libXdamage-devel
- BR: libxkbfile-devel
- BR: libXv-devel
- BR: libXxf86misc-devel
- BR: libXScrnSaver-devel

* Fri Nov 16 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.0-4
- require /sbin/ldconfig xdg-utils on %%post and %%postun
- some small spec cleanups
- +BR: kde-filesystem
- +BR: kde4-macros(api)

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.0-3
- BR: libzip-devel
- added %%defattr to package devel

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.0-2
- re-added missing epoch (from kdeutils3)

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.0-1
- Initial version for Fedora
