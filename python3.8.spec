# Some tips thanks to:
# Beyond Linux From Scratch http://www.linuxfromscratch.org/blfs/view/svn/general/python3.html
# Arch Linux https://www.archlinux.org/packages/extra/x86_64/python/

	
# This prevents ALL subpackages built from this spec to require
# /usr/bin/python3*. Granularity per subpackage is impossible.
# It's intended for the libs package not to drag in the interpreter, see
# https://bugzilla.redhat.com/show_bug.cgi?id=1547131
# All others require %%{pkgname} anyway.
%global __requires_exclude ^/usr/bin/python3

	
# We'll not provide this, on purpose
%global __requires_exclude ^libpython3.8\\.so.*$
%global __requires_exclude ^/usr/local/bin/python$


# Disable automatic bytecompilation. The python3 binary is not yet be
# available in /usr/bin when Python is built. Also, the bytecompilation fails
# on files that test invalid syntax.
%undefine py_auto_byte_compile

# When a main_python build is attempted despite the %%__default_python3_pkgversion value
# We undefine magic macros so the python3-... package does not provide wrong python3X-...
%undefine __pythonname_provides

# Main interpreter loop optimization
%bcond_without computed_gotos

# Get proper option names from bconds
%if %{with computed_gotos}
%global computed_gotos_flag yes
%else
%global computed_gotos_flag no
%endif

Name: python3.8
Summary: Version 3.8 of the Python interpreter
URL: https://www.python.org/


Version: 3.8.3
Release: 5%{?dist}
License: Python

# =======================
# Build-time requirements
# =======================

# (keep this list alphabetized)

BuildRequires: autoconf
BuildRequires: bluez-libs-devel
BuildRequires: bzip2
BuildRequires: bzip2-devel
BuildRequires: desktop-file-utils
BuildRequires: expat-devel

BuildRequires: findutils
BuildRequires: gcc-c++

BuildRequires: gdbm-devel

BuildRequires: glibc-all-langpacks
BuildRequires: glibc-devel
BuildRequires: gmp-devel
BuildRequires: gnupg2
BuildRequires: libappstream-glib
BuildRequires: libffi-devel
BuildRequires: libnsl2-devel
BuildRequires: libtirpc-devel
BuildRequires: libGL-devel
BuildRequires: libuuid-devel
BuildRequires: libX11-devel
BuildRequires: ncurses-devel

BuildRequires: openssl-devel
#BuildRequires: python3-rpm-macros
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: redhat-rpm-config >= 127
BuildRequires: sqlite-devel
BuildRequires: gdb

BuildRequires: tar
BuildRequires: tcl-devel
BuildRequires: tix-devel
BuildRequires: tk-devel

BuildRequires: valgrind-devel


BuildRequires: xz-devel
BuildRequires: zlib-devel

BuildRequires: /usr/bin/dtrace

# workaround http://bugs.python.org/issue19804 (test_uuid requires ifconfig)
BuildRequires: /usr/sbin/ifconfig

Conflicts:     python3 = 3.8.3

# =======================
# Source code and patches
# =======================

Source0: https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tar.xz
Source1: python3.8.conf

# A simple script to check timestamps of bytecode files
# Run in check section with Python that is currently being built
# Originally written by bkabrda
Source8: check-pyc-timestamps.py

# Desktop menu entry for idle3
Source10: idle38.desktop

# AppData file for idle3
Source11: idle38.appdata.xml

# 00001 #
# Fixup distutils/unixccompiler.py to remove standard library path from rpath:
# Was Patch0 in ivazquez' python3000 specfile:
Patch1:         00001-rpath.patch

# 00102 #
# Change the various install paths to use /usr/lib64/ instead or /usr/lib
# Only used when "%%{_lib}" == "lib64"
# Not yet sent upstream.
Patch102: 00102-lib64.patch

# 00111 #
# Patch the Makefile.pre.in so that the generated Makefile doesn't try to build
# a libpythonMAJOR.MINOR.a
# See https://bugzilla.redhat.com/show_bug.cgi?id=556092
# Downstream only: not appropriate for upstream
Patch111: 00111-no-static-lib.patch

# 00189 #
# Instead of bundled wheels, use our RPM packaged wheels from
# /usr/share/python-wheels
# Downstream only: upstream bundles
# We might eventually pursuit upstream support, but it's low prio
Patch189: 00189-use-rpm-wheels.patch

# 00251
# Set values of prefix and exec_prefix in distutils install command
# to /usr/local if executable is /usr/bin/python* and RPM build
# is not detected to make pip and distutils install into separate location
# Fedora Change: https://fedoraproject.org/wiki/Changes/Making_sudo_pip_safe
# Downstream only: Awaiting resources to work on upstream PEP
Patch251: 00251-change-user-install-location.patch

# 00274 #
# Upstream uses Debian-style architecture naming. Change to match Fedora.
Patch274: 00274-fix-arch-names.patch

# 00328 #
# Restore pyc to TIMESTAMP invalidation mode as default in rpmbubild
# See https://src.fedoraproject.org/rpms/redhat-rpm-config/pull-request/57#comment-27426
# Downstream only: only used when building RPM packages
# Ideally, we should talk to upstream and explain why we don't want this
Patch328: 00328-pyc-timestamp-invalidation-mode.patch

# 00350 #
# bpo-40784: Fix sqlite3 deterministic test (GH-20448)
# https://bugs.python.org/issue40784
# https://github.com/python/cpython/commit/00a240bf7f95bbd220f1cfbf9eb58484a5f9681a
Patch350: 00350-sqlite-fix-deterministic-test.patch



# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================


%description
Python 3.8 is an accessible, high-level, dynamically typed, interpreted
programming language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

Summary: Python 3.8 interpreter
Requires: %{name}-libs = %{version}-%{release}

#----------------------------------------------------
%package libs
Summary:        Python runtime libraries
Conflicts: 	python3-libs = 3.8.3

%description libs
This package contains runtime libraries for use by Python:
- the majority of the Python standard library
- a dynamically linked library for use by applications that embed Python as
  a scripting language, and by the main "%{exename}" executable


%package devel
Summary: Libraries and header files needed for Python development
Requires: %{name} = %{version}-%{release}
Conflicts: python3-devel = 3.8.3

%description devel
This package contains the header files and configuration needed to compile
Python extension modules (typically written in C or C++), to embed Python
into other programs, and to make binary distributions for Python libraries.

It also contains the necessary macros to build RPM packages with Python modules
and 2to3 tool, an automatic source converter from Python 2.X.


# ======================================================
# The prep phase of the build:
# ======================================================

%prep
%setup -n Python-3.8.3
# Remove all exe files to ensure we are not shipping prebuilt binaries
# note that those are only used to create Microsoft Windows installers
# and that functionality is broken on Linux anyway
find -name '*.exe' -print -delete

# Remove bundled libraries to ensure that we're using the system copy.
rm -r Modules/expat

#
# Apply patches:
#
%patch1 -p1

%if "%{_lib}" == "lib64"
%patch102 -p1
%endif
%patch111 -p1

#rpmwheels
#patch189 -p1

%patch251 -p1
%patch274 -p1
%patch328 -p1
%patch350 -p1


# ======================================================
# Configuring and building the code:
# ======================================================

%build

# redundant prefix, but we need avoid wrong paths

CXX="/usr/bin/g++"
%configure \
  --prefix=/usr \
  --enable-shared \
  --with-threads \
  --enable-ipv6 \
  --enable-shared \
  --with-computed-gotos=%{computed_gotos_flag} \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
  --with-system-ffi \
  --enable-loadable-sqlite-extensions \
  --with-dtrace \
  --with-lto \
  --with-ssl-default-suites=openssl \
  --with-valgrind \
  --with-system-libmpdec \
  --with-ensurepip=yes
  %{nil}


%install

  # Hack to avoid building again
  sed -i 's/^all:.*$/all: build_all/' Makefile

  make DESTDIR=%{buildroot} EXTRA_CFLAGS="$CFLAGS" install

  rm -f %{buildroot}/usr/share/man/man1/python3.1
  rm -f %{buildroot}/usr/lib64/libpython3.so
  rm -f %{buildroot}/usr/lib64/pkgconfig/python3.pc
  rm -rfv %{buildroot}/usr/lib64/python3.8/test
  rm -f %{buildroot}/usr/lib64/pkgconfig/python3-embed.pc

  rm -f %{buildroot}/usr/bin/python3-config
  rm -f %{buildroot}/usr/bin/idle3
  rm -f %{buildroot}/usr/bin/pydoc3
  rm -f %{buildroot}/usr/bin/2to3
  rm -f %{buildroot}/usr/bin/pyvenv
  rm -f %{buildroot}/usr/bin/python3
  rm -f %{buildroot}/usr/bin/pip3
  
# add idle3 to menu
install -D -m 0644 Lib/idlelib/Icons/idle_16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/idle38.png
install -D -m 0644 Lib/idlelib/Icons/idle_32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/idle38.png
install -D -m 0644 Lib/idlelib/Icons/idle_48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/idle38.png
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{S:10}
  
# Install and validate appdata file
mkdir -p %{buildroot}%{_metainfodir}
cp -a %{S:11} %{buildroot}%{_metainfodir}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/idle38.appdata.xml
  
	
# Remove shebang lines from .py files that aren't executable, and
# remove executability from .py files that don't have a shebang line:
find %{buildroot} -name \*.py \
  \( \( \! -perm /u+x,g+x,o+x -exec sed -e '/^#!/Q 0' -e 'Q 1' {} \; \
  -print -exec sed -i '1d' {} \; \) -o \( \
  -perm /u+x,g+x,o+x ! -exec grep -m 1 -q '^#!' {} \; \
  -exec chmod a-x {} \; \) \)
  
  # Get rid of DOS batch files:
find %{buildroot} -name \*.bat -exec rm {} \;
 
# Get rid of backup files:
find %{buildroot}/ -name "*~" -exec rm -f {} \;
find . -name "*~" -exec rm -f {} \;

# Fixup permissions for shared libraries from non-standard 555 to standard 755:
find %{buildroot} -perm 555 -exec chmod 755 {} \;

# Install profile and ld.so.config files
install -Dm644 %{S:1} "%{buildroot}/etc/ld.so.conf.d/python3.8.conf"

  
# mangling shebang fixes  

sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/trace.py
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/tabnanny.py
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/idlelib/pyshell.py

sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/idlelib/pyshell.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/quopri.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/profile.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/lib2to3/pgen2/token.py 

sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/lib2to3/tests/pytree_idempotency.py
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/uu.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/webbrowser.py 

sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/smtpd.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/turtledemo/lindenmayer.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/turtledemo/forest.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/turtledemo/bytedesign.py 

sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/turtledemo/yinyang.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/turtledemo/planet_and_moon.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/turtledemo/fractalcurves.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/turtledemo/tree.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/turtledemo/peace.py 

sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/turtledemo/minimal_hanoi.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/turtledemo/penrose.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/turtledemo/clock.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/cProfile.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/smtplib.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/tarfile.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/timeit.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/pdb.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/platform.py 
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/base64.py
sed -i 's|/usr/bin/env python3|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/turtledemo/paint.py  

sed -i 's|/usr/bin/env python|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/encodings/rot_13.py 
sed -i 's|/usr/bin/env python|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/lib2to3/tests/data/different_encoding.py 
sed -i 's|/usr/bin/env python|/usr/bin/python3.8|g' %{buildroot}/usr/lib64/python3.8/lib2to3/tests/data/false_encoding.py 

sed -i 's|/bin/sh|/usr/bin/sh|g' %{buildroot}/usr/lib64/python3.8/config-3.8-x86_64-linux-gnu/install-sh 
sed -i 's|/bin/sh|/usr/bin/sh|g' %{buildroot}/usr/lib64/python3.8/config-3.8-x86_64-linux-gnu/makesetup 
sed -i 's|/bin/sh|/usr/bin/sh|g' %{buildroot}/usr/lib64/python3.8/ctypes/macholib/fetch_macholib 
sed -i 's|/bin/sh|/usr/bin/sh|g' %{buildroot}/usr/bin/python3.8-config
  
	
%files 
/usr/bin/python3.8-config 
/usr/bin/2to3-3.8
/usr/bin/idle3.8
/usr/bin/pydoc3.8
/usr/bin/python3.8
/usr/bin/easy_install-3.8
/usr/bin/pip3.8
/usr/share/man/man1/python3.8.1.gz
%{_metainfodir}/idle38.appdata.xml
%{_datadir}/icons/hicolor/*/apps/idle38.png
%{_datadir}/applications/idle38.desktop

# PIP
/usr/lib/python3.8/site-packages/easy_install.py
/usr/lib/python3.8/site-packages/pip/
/usr/lib/python3.8/site-packages/pip-19.2.3.dist-info/INSTALLER
/usr/lib/python3.8/site-packages/pip-19.2.3.dist-info/LICENSE.txt
/usr/lib/python3.8/site-packages/pip-19.2.3.dist-info/METADATA
/usr/lib/python3.8/site-packages/pip-19.2.3.dist-info/RECORD
/usr/lib/python3.8/site-packages/pip-19.2.3.dist-info/WHEEL
/usr/lib/python3.8/site-packages/pip-19.2.3.dist-info/entry_points.txt
/usr/lib/python3.8/site-packages/pip-19.2.3.dist-info/top_level.txt
/usr/lib/python3.8/site-packages/__pycache__/easy_install.cpython-38.pyc

# Setup tools
/usr/lib/python3.8/site-packages/setuptools/
/usr/lib/python3.8/site-packages/setuptools-41.2.0.dist-info/
/usr/lib/python3.8/site-packages/pkg_resources/

%files libs
/usr/lib64/libpython3.8.so
/usr/lib64/libpython3.8.so.1.0
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
/usr/lib64/python3.8/

%files devel 
/usr/include/python3.8/
#/usr/lib64/libpython3.so
# /usr/lib64/pkgconfig/python3.pc
#/usr/lib64/pkgconfig/python3-embed.pc
/usr/lib64/pkgconfig/python-3.8.pc
/usr/lib64/pkgconfig/python-3.8-embed.pc


# ======================================================
# Finally, the changelog:
# ======================================================

%changelog

* Mon Sep 21 2020 David Va <davidva AT tuta DOT io> - 3.8.3-5
- Rebuilt

* Thu Jun 04 2020 David Va <davidva AT tuta DOT io> - 3.8.3-4
- Cleaned and ready for the action

* Fri May 29 2020 Petr Viktorin <pviktori@redhat.com> - 3.8.3-3
- Rebuild without bootstrap

* Fri May 29 2020 Victor Stinner <vstinner@python.org> - 3.8.3-2
- Fix sqlite3 deterministic test

* Fri May 15 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8.3-1
- Rebased to 3.8.3 final

* Thu Apr 30 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8.3~rc1-1
- Rebased to 3.8.3rc1

* Fri Feb 28 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8.2-2
- Enable https://fedoraproject.org/wiki/Changes/PythonNoSemanticInterpositionSpeedup on power and arm

* Wed Feb 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8.2-1
- Rebased to 3.8.2 final

* Mon Feb 24 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8.2~rc2-2
- Update the ensurepip module to work with setuptools >= 45

* Mon Feb 24 2020 Marcel Plch <mplch@redhat.com> - 3.8.2~rc2-1
- Rebased to 3.8.2rc2

* Wed Feb 12 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8.2~rc1-1
- Rebased to 3.8.2rc1

* Thu Jan 30 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
- ctypes: Disable checks for union types being passed by value (#1794572)
- Temporarily disable https://fedoraproject.org/wiki/Changes/PythonNoSemanticInterpositionSpeedup
  on ppc64le and armv7hl (#1795575)

* Thu Dec 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.1-1
- Update to Python 3.8.1

* Tue Dec 10 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.1~rc1-1
- Rebased to Python 3.8.1rc1

* Tue Dec 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0-3
- Build Python with -fno-semantic-interposition for better performance
- https://fedoraproject.org/wiki/Changes/PythonNoSemanticInterpositionSpeedup

* Thu Nov 28 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0-2
- Recommend python3-tkinter when tk is installed

* Mon Oct 14 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0-1
- Update to Python 3.8.0 final

* Tue Oct 01 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~rc1-1
- Rebased to Python 3.8.0rc1

* Fri Aug 30 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~b4-1
- Rebased to Python 3.8.0b4

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~b3-4
- Enable Profile-guided optimization for all arches, not just x86 (#1741015)

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~b3-3
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~b3-2
- Bootstrap for Python 3.8

* Tue Aug 13 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~b3-1
- Update to 3.8.0b3# with test
