%define major 1
%define libname %mklibname %{name}5 %{major}
%define devname %mklibname -d %{name}5
%define debug_package %nil

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

%description -n %{libname}
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package that
can be used to access ZIP archives. It uses Trolltech's Qt toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice API,
and - yes! - that means that you can also use QTextStream, QDataStream or
whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both reading
from and writing to ZIP archives.

%files -n %{libname}
%{_libdir}/libquazip5.so.%{major}*

#------------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains libraries, header files and documentation
for developing applications that use %{libname}.

%files -n %{devname}
%doc COPYING* NEWS.txt
%doc doc/html
%{_includedir}/%{name}5
%{_libdir}/pkgconfig/quazip.pc
%{_libdir}/libquazip5.so
%{_libdir}/cmake/QuaZip5/*.cmake

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
