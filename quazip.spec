%define major 1
%define libname %mklibname %{name}1-qt5 %{major}
%define devname %mklibname -d %{name}1-qt5

Summary:	Qt/C++ wrapper for the minizip library
Name:		quazip
Version:	1.1
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://github.com/stachenov/quazip
Source0:	https://github.com/stachenov/quazip/archive/v%{version}.tar.gz
# (tpg) fix build with zlib-ng
Patch0:		quazip-1.1-no-ZEXPORT.patch
Patch1:		quazip-1.1-zlib-ng.patch
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	pkgconfig(libzip)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	qt5-devel
BuildRequires:	cmake(ECM)

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

%prep
%autosetup -p1
%cmake_qt5 -G Ninja

%build
%ninja_build -C build

doxygen Doxyfile
for file in doc/html/*; do
    touch -r Doxyfile $file
done

%install
%ninja_install -C build

# No need for static libs...
rm -f %{buildroot}%{_libdir}/*.a

# Compatibility with releases < 1.1
ln -s libquazip1-qt5.so %{buildroot}%{_libdir}/libquazip5.so
ln -s quazip1-qt5.pc %{buildroot}%{_libdir}/pkgconfig/quazip.pc
