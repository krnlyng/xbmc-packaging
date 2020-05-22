Name: kodi
Version: 18.7
Release: Leia
Summary: Media center

License: GPLv2
# Main binary and all supporting files are GPLv2+/GPLv3+
# Some supporting libraries use the LGPL / BSD / MIT license
URL: http://www.kodi.tv/
Source0: %{name}-%{version}.tar.xz

%global _with_libbluray 0
%global _with_cwiid 0
%global _with_libssh 0
%global _with_libcec 0
%global _with_external_ffmpeg 0
%global _with_wayland 1

%ifarch x86_64 i686
%global _with_crystalhd 1
%endif

# Upstream does not support ppc64
ExcludeArch: ppc64

# NOTE: EXTRA DEPS:

# java:
# sb2 -t target -R tar xzvf jdk-8u212-linux-arm32-vfp-hflt.tar.gz -C /opt
# create symlinks:
# /usr/bin/java -> /opt/.../bin/java
# /usr/bin/javac -> /opt/.../bin/javac
# TODO: proper solution?

# ps2pdf:
# get rid of ps2pdf intermediate dependency:
# sb2 -t target -R cp /bin/cp /usr/bin/ps2pdf
# TODO: proper solution is to build ghostscript

# copy input-event-codes.h from your host
# TODO: proper solution is to update kernel-headers

BuildRequires: SDL2-devel
BuildRequires: bluez5-libs-devel
BuildRequires: boost-devel
BuildRequires: bzip2-devel
BuildRequires: cmake
%if 0%{?_with_cwiid}
BuildRequires: cwiid-devel
%endif
BuildRequires: dbus-devel
BuildRequires: desktop-file-utils
BuildRequires: e2fsprogs-devel
BuildRequires: expat-devel
%if 0%{?_with_external_ffmpeg}
BuildRequires: ffmpeg-devel
%endif
BuildRequires: flac-devel
BuildRequires: flex
BuildRequires: fontconfig-devel
BuildRequires: fontpackages-devel
BuildRequires: freetype-devel
BuildRequires: fribidi-devel
BuildRequires: gettext-devel
BuildRequires: glib2-devel
BuildRequires: gperf
%if 0%{?_with_libbluray}
BuildRequires: libbluray-devel
%endif
BuildRequires: libcap-devel
BuildRequires: libcdio-devel
%if 0%{?_with_libcec}
BuildRequires: libcec-devel >= 3.0.0
%endif
%if 0%{?_with_crystalhd}
BuildRequires: libcrystalhd-devel
%endif
BuildRequires: libcurl-devel
BuildRequires: libjpeg-devel
BuildRequires: libogg-devel
# for AirPlay support
BuildRequires: libpng-devel
%if 0%{?_with_libssh}
BuildRequires: libssh-devel
%endif
BuildRequires: libtiff-devel
BuildRequires: libtool
BuildRequires: libuuid-devel
%ifnarch %{arm}
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
%endif
BuildRequires: libvorbis-devel
%if 0%{?_with_wayland}
BuildRequires: wayland-devel
BuildRequires: wayland-protocols-devel
%endif
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: lzo-devel
BuildRequires: mesa-llvmpipe-libEGL-devel
BuildRequires: mesa-llvmpipe-libGLESv2-devel
BuildRequires: nasm
BuildRequires: pcre-devel
BuildRequires: pixman-devel
BuildRequires: pulseaudio-devel
BuildRequires: python-devel
BuildRequires: sqlite-devel
BuildRequires: swig
BuildRequires: systemd-devel
BuildRequires: taglib-devel >= 1.8
BuildRequires: tinyxml-devel
BuildRequires: zlib-devel

# SFOS
BuildRequires: libaudioresource-devel

#Requires: google-roboto-fonts
# need explicit requires for these packages
# as they are dynamically loaded via XBMC's arcane
# pseudo-DLL loading scheme (sigh)
%if 0%{?_with_libbluray}
Requires: libbluray%{?_isa}
%endif
%if 0%{?_with_libcec}
Requires: libcec%{?_isa} >= 3.0.0
%endif
%if 0%{?_with_crystalhd}
Requires: libcrystalhd%{?_isa}
%endif
#Requires: libmad%{?_isa}
#Requires: librtmp%{?_isa}

# needed when doing a minimal install, see
# https://bugzilla.rpmfusion.org/show_bug.cgi?id=1844
#Requires: glx-utils
#Requires: xorg-x11-utils

# This is just symlinked to, but needed both at build-time
# and for installation
#Requires: python-pillow%{?_isa}


%description
Kodi is a free cross-platform media-player jukebox and entertainment hub.
Kodi can play a spectrum of of multimedia formats, and featuring playlist,
audio visualizations, slideshow, and weather forecast functions, together
third-party plugins.


%package devel
Summary: Development files needed to compile C programs against kodi
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: xbmc-devel < 14.0
Provides: xbmc-devel = %{version}

%description devel
Kodi is a free cross-platform media-player jukebox and entertainment hub.
If you want to develop programs which use Kodi's libraries, you need to
install this package.


#%package eventclients
#Summary: Media center event client remotes
#Obsoletes: xbmc-eventclients < 14.0
#Provides: xbmc-eventclients = %{version}
#
#%description eventclients
#This package contains support for using Kodi with the PS3 Remote, the Wii
#Remote, a J2ME based remote and the command line xbmc-send utility.
#
#%package eventclients-devel
#Summary: Media center event client remotes development files
#Requires:	%{name}-eventclients%{?_isa} = %{version}-%{release}
#Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
#Obsoletes: xbmc-eventclients-devel < 14.0
#Provides:  xbmc-eventclients-devel = %{version}
#
#%description eventclients-devel
#This package contains the development header files for the eventclients
#library.


%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%cmake -DCORE_PLATFORM_NAME=wayland -DWAYLAND_RENDER_SYSTEM=gles -DENABLE_INTERNAL_RapidJSON=On -DENABLE_INTERNAL_FMT=On -DENABLE_INTERNAL_FSTRCMP=On -DENABLE_INTERNAL_FLATBUFFERS=On
make %{?_smp_mflags} VERBOSE=1


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
#make -C tools/EventClients DESTDIR=$RPM_BUILD_ROOT install
# remove the doc files from unversioned /usr/share/doc/xbmc, they should be in versioned docdir
rm -r $RPM_BUILD_ROOT/%{_datadir}/doc/

mv ${RPM_BUILD_ROOT}%{_datadir}/applications/kodi.desktop ${RPM_BUILD_ROOT}%{_datadir}/applications/kodi-wayland.desktop

desktop-file-install \
 --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
 $RPM_BUILD_ROOT%{_datadir}/applications/kodi-wayland.desktop

# Normally we are expected to build these manually. But since we are using
# the system Python interpreter, we also want to use the system libraries
install -d $RPM_BUILD_ROOT%{_libdir}/kodi/addons/script.module.pil/lib
ln -s %{python_sitearch}/PIL $RPM_BUILD_ROOT%{_libdir}/kodi/addons/script.module.pil/lib/PIL
#install -d $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pysqlite/lib
#ln -s %{python_sitearch}/pysqlite2 $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pysqlite/lib/pysqlite2

# Use external Roboto font files instead of bundled ones
#ln -sf %{_fontbasedir}/google-roboto/Roboto-Regular.ttf ${RPM_BUILD_ROOT}%{_datadir}/kodi/addons/skin.confluence/fonts/
#ln -sf %{_fontbasedir}/google-roboto/Roboto-Bold.ttf ${RPM_BUILD_ROOT}%{_datadir}/kodi/addons/skin.confluence/fonts/

# Move man-pages into system dir
#mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
#cp -r docs/manpages/* ${RPM_BUILD_ROOT}%{_mandir}/man1/


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
if [ ! -L %{_libdir}/xbmc ] ; then
    rmdir %{_libdir}/xbmc %{_datadir}/xbmc
    ln -s kodi ${RPM_BUILD_ROOT}%{_libdir}/xbmc
    ln -s kodi ${RPM_BUILD_ROOT}%{_datadir}/xbmc
fi


%posttrans devel
if [ ! -L %{_includedir}/xbmc ] ; then
    rmdir %{_includedir}/xbmc
    ln -s kodi ${RPM_BUILD_ROOT}%{_includedir}/xbmc
fi


%files
#%license copying.txt LICENSE.GPL
#%doc CONTRIBUTING.md README.md docs
%{_bindir}/kodi
%{_bindir}/kodi-standalone
#%{_bindir}/xbmc
#%{_bindir}/xbmc-standalone
%{_libdir}/kodi
%ghost %{_libdir}/xbmc
%{_datadir}/kodi
%ghost %{_datadir}/xbmc
%{_datadir}/xsessions/kodi.desktop
#%{_datadir}/xsessions/xbmc.desktop
%{_datadir}/applications/kodi-wayland.desktop
%{_datadir}/icons/hicolor/*/*/*.png
#%{_mandir}/man1/kodi.1.gz
#%{_mandir}/man1/kodi.bin.1.gz
#%{_mandir}/man1/kodi-standalone.1.gz
%{_bindir}/TexturePacker
%{_libdir}/firewalld/services/kodi-eventserver.xml
%{_libdir}/firewalld/services/kodi-http.xml
%{_libdir}/firewalld/services/kodi-jsonrpc.xml


%files devel
%{_includedir}/kodi
%ghost %{_includedir}/xbmc
#%files eventclients
#%license copying.txt LICENSE.GPL
#%python_sitelib/kodi
#%dir %{_datadir}/pixmaps/kodi
#%{_datadir}/pixmaps/kodi/*.png
#%{_bindir}/kodi-j2meremote
#%{_bindir}/kodi-ps3d
#%{_bindir}/kodi-ps3remote
#%{_bindir}/kodi-send
#%{_bindir}/kodi-wiiremote
#%{_mandir}/man1/kodi-j2meremote.1.gz


#%files eventclients-devel
#%{_includedir}/kodi/xbmcclient.h

