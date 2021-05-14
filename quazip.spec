%define major 1
%define libname %mklibname %{name}1-qt5 %{major}
%define devname %mklibname -d %{name}1-qt5

%define lib6name %mklibname %{name}1-qt6 %{major}
%define dev6name %mklibname -d %{name}1-qt6

Summary:	Qt/C++ wrapper for the minizip library
Name:		quazip
Version:	1.1
Release:	3
License:	LGPLv2+
Group:		System/Libraries
Url:		https://github.com/stachenov/quazip
Source0:	https://github.com/stachenov/quazip/archive/v%{version}.tar.gz
# (tpg) fix build with zlib-ng
Patch0:		quazip-1.1-no-ZEXPORT.patch
Patch1:		quazip-1.1-zlib-ng.patch
Patch2:		quazip-1.1-fix-cmake-files.patch
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	pkgconfig(libzip)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt6)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	%mklibname -d Qt6Test
BuildRequires:	%mklibname -d Qt6Core
BuildRequires:	%mklibname -d Qt6Network
BuildRequires:	%mklibname -d Qt6Core5Compat

%description
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package that
can be used to access ZIP archives. It uses Trolltech's Qt toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice API,
and - yes! - that means that you can also use QTextStream, QDataStream or
whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both reading
from and writing to ZIP archives.

#------------------------------------------------------------------------------

%package -n %{libname}
Summary:	Qt/C++ wrapper for the minizip library
%rename quazip
%rename %{mklibname %{name}5 %{major}}

%description -n %{libname}
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package that
can be used to access ZIP archives. It uses Trolltech's Qt toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice API,
and - yes! - that means that you can also use QTextStream, QDataStream or
whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both reading
from and writing to ZIP archives.

%files -n %{libname}
%{_libdir}/libquazip1-qt5.so.%{major}*

#------------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
%rename %{mklibname -d %{name}5}

%description -n %{devname}
This package contains libraries, header files and documentation
for developing applications that use %{libname}.

%files -n %{devname}
%doc COPYING* NEWS.txt
%doc doc/html
%{_includedir}/QuaZip-Qt5-%{version}
%{_libdir}/pkgconfig/quazip.pc
%{_libdir}/pkgconfig/quazip1-qt5.pc
%{_libdir}/libquazip1-qt5.so
%{_libdir}/libquazip5.so
%{_libdir}/cmake/QuaZip-Qt5-%{version}/*.cmake

#------------------------------------------------------------------------------

%package -n %{lib6name}
Summary:	Qt/C++ wrapper for the minizip library for Qt 6.x

%description -n %{lib6name}
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package that
can be used to access ZIP archives. It uses Trolltech's Qt toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice API,
and - yes! - that means that you can also use QTextStream, QDataStream or
whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both reading
from and writing to ZIP archives.

%files -n %{lib6name}
%{_libdir}/libquazip1-qt6.so.%{major}*

#------------------------------------------------------------------------------

%package -n %{dev6name}
Summary:	Development files for %{name} for Qt 6.x
Group:		Development/Other
Requires:	%{lib6name} = %{version}-%{release}

%description -n %{dev6name}
This package contains libraries, header files and documentation
for developing applications that use %{libname}.

%files -n %{dev6name}
%doc COPYING* NEWS.txt
%doc doc/html
%{_includedir}/QuaZip-Qt6-%{version}
%{_libdir}/pkgconfig/quazip1-qt6.pc
%{_libdir}/libquazip1-qt6.so
%{_libdir}/cmake/QuaZip-Qt6-%{version}/*.cmake

#------------------------------------------------------------------------------

%prep
%autosetup -p1
%cmake_qt5 -G Ninja -DQUAZIP_QT_MAJOR_VERSION=5
cd ..
export CMAKE_BUILD_DIR=build-qt6
%cmake -G Ninja -DQUAZIP_QT_MAJOR_VERSION=6

%build
%ninja_build -C build-qt6
%ninja_build -C build

doxygen Doxyfile
for file in doc/html/*; do
    touch -r Doxyfile $file
done

%install
%ninja_install -C build-qt6
%ninja_install -C build

# No need for static libs...
rm -f %{buildroot}%{_libdir}/*.a

# Compatibility with releases < 1.1
ln -s libquazip1-qt5.so %{buildroot}%{_libdir}/libquazip5.so
ln -s quazip1-qt5.pc %{buildroot}%{_libdir}/pkgconfig/quazip.pc
